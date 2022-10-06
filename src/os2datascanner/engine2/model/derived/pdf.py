import os

from os import listdir, remove
from pathlib import Path
from hashlib import md5
import PyPDF2
import string
import datetime
from tempfile import TemporaryDirectory

from ....utils.system_utilities import run_custom
from ... import settings as engine2_settings
from ..core import Handle, Source, Resource
from ..file import FilesystemResource
from .derived import DerivedSource
from .utilities.extraction import should_skip_images


PAGE_TYPE = "application/x.os2datascanner.pdf-page"
WHITESPACE_PLUS = string.whitespace + "\0"


def _open_pdf_wrapped(obj):
    reader = PyPDF2.PdfFileReader(obj)
    if reader.getIsEncrypted():
        # Some PDFs are "encrypted" with an empty password: give that a shot...
        try:
            if reader.decrypt("") == 0:  # the document has a real password
                reader = None
        except NotImplementedError:  # unsupported encryption algorithm
            reader = None
    return reader


def calculate_md5(filename):
    """Calculates the md5 sum of a file 4kb at a time."""
    md5sum = md5()

    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5sum.update(chunk)

    return md5sum.hexdigest()


def _filter_duplicate_images(directory_str):
    """Removes duplicate images if their md5sum matches."""
    hash_stack = []

    for image in listdir(directory_str + "/image"):
        checksum = calculate_md5(image)

        if checksum not in hash_stack:
            hash_stack.append(checksum)
        else:
            remove(image)


def _extract_and_filter_images(path):
    """Extracts all images for a pdf
    and puts it in a temporary output directory."""
    parent = Path(path).parent.absolute
    outdir = parent + '/image'

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    run_custom(
        ["pdfimages", "-q", "-png", "-j", path, f"{outdir}"],
        timeout=engine2_settings.subprocess["timeout"],
        check=True, isolate_tmp=True)

    _filter_duplicate_images(outdir)

    return outdir


@Source.mime_handler("application/pdf")
class PDFSource(DerivedSource):
    type_label = "pdf"

    def _generate_state(self, sm):
        with self.handle.follow(sm).make_path() as p:
            # Explicitly download the file here for the sake of PDFPageSource,
            # which needs a local filesystem path to pass to pdftohtml
            print(f"Path for PDF: {p} has type: {type(p)}")
            outdir = _extract_and_filter_images(p)
            yield outdir
            yield p

    def handles(self, sm):
        reader = _open_pdf_wrapped(sm.open(self))
        for i in range(1, reader.getNumPages() + 1 if reader else 0):
            yield PDFPageHandle(self, str(i))


class PDFPageResource(Resource):
    def _generate_metadata(self):
        with self.handle.source.handle.follow(self._sm).make_stream() as fp:
            reader = _open_pdf_wrapped(fp)
            info = reader.getDocumentInfo() if reader else None
            # Some PDF authoring tools helpfully stick null bytes into the
            # author field. Make sure we remove these
            author = (
                    info.get("/Author").strip(WHITESPACE_PLUS)
                    if info and info.get("/Author") else None)

        if author:
            yield "pdf-author", str(author)

    def check(self) -> bool:
        page = int(self.handle.relative_path)
        with self.handle.source._make_stream(self._sm) as fp:
            reader = _open_pdf_wrapped(fp)
            return page in range(1, reader.getNumPages() + 1 if reader else 0)

    def compute_type(self):
        return PAGE_TYPE


@Handle.stock_json_handler("pdf-page")
class PDFPageHandle(Handle):
    type_label = "pdf-page"
    resource_type = PDFPageResource

    @property
    def presentation_name(self):
        return f"page {self.relative_path}"

    @property
    def presentation_place(self):
        return str(self.source.handle)

    def __str__(self):
        return f"{self.presentation_name} of {self.presentation_place}"

    @property
    def sort_key(self):
        "Return the file path of the document"
        return self.base_handle.sort_key

    def censor(self):
        return PDFPageHandle(self.source.censor(), self.relative_path)

    def guess_type(self):
        return PAGE_TYPE

    @classmethod
    def make(cls, handle: Handle, page: int):
        return PDFPageHandle(PDFSource(handle), str(page))


@Source.mime_handler(PAGE_TYPE)
class PDFPageSource(DerivedSource):
    type_label = "pdf-page"

    def _generate_state(self, sm):
        # As we produce FilesystemResources, we need to produce a cookie of the
        # same format as FilesystemSource: a filesystem directory in which to
        # interpret relative paths
        page = self.handle.relative_path
        path = sm.open(self.handle.source)
        with TemporaryDirectory() as outputdir:
            # Run pdftotext and pdfimages separately instead of running
            # pdftohtml. Not having to parse HTML is a big performance win by
            # itself, but what's even better is that pdfimages doesn't produce
            # uncountably many texture images for embedded vector graphics
            run_custom(
                    [
                            "pdftotext", "-q", "-nopgbrk", "-eol", "unix",
                            "-f", page, "-l", page, path,
                            "{0}/page.txt".format(outputdir)
                    ],
                    timeout=engine2_settings.subprocess["timeout"],
                    check=True, isolate_tmp=True)

            if not should_skip_images(sm.configuration):
                run_custom(
                    [
                            "pdfimages", "-q", "-png", "-j", "-f", page, "-l", page,
                            path, "{0}/image".format(outputdir)
                    ],
                    timeout=engine2_settings.subprocess["timeout"],
                    check=True, isolate_tmp=True)

            yield outputdir

    def handles(self, sm):
        for p in listdir(sm.open(self)):
            yield PDFObjectHandle(self, p)


class PDFObjectResource(FilesystemResource):
    def _generate_metadata(self):
        # Suppress the superclass implementation of this method -- generated
        # files have no interesting metadata
        yield from ()

    def get_last_modified(self):
        # This is a generated, embedded file, so the last_modified_date should
        # be taken from the parent container.
        last_modified = None
        # Get the top-level handle and follow it.
        parent_handle = self.handle.source.handle.source.handle
        with parent_handle.follow(self._sm).make_stream() as fp:
            reader = _open_pdf_wrapped(fp)
            info = reader.getDocumentInfo()
            # Extract the modification date time and format it properly.
            mod_date = info.get("/ModDate")
            # Check that the mod_date is a string-like object.
            if isinstance(mod_date, PyPDF2.generic.TextStringObject):
                mod_date = mod_date.strip(WHITESPACE_PLUS).replace("'", "")[2:]
                last_modified = datetime.datetime.strptime(mod_date, "%Y%m%d%H%M%S%z")
        return last_modified


@Handle.stock_json_handler("pdf-object")
class PDFObjectHandle(Handle):
    type_label = "pdf-object"
    resource_type = PDFObjectResource

    def censor(self):
        return PDFObjectHandle(self.source.censor(), self.relative_path)

    @property
    def sort_key(self):
        return self.source.handle.sort_key

    @property
    def presentation_name(self):
        mime = self.guess_type()
        page = str(self.source.handle.presentation_name)
        container = self.source.handle.source.handle.presentation_name
        if mime.startswith("text/"):
            return f"text on {page} of {container}"
        elif mime.startswith("image/"):
            return f"image on {page} of {container}"
        else:
            return f"unknown object on {page} of {container}"

    @property
    def presentation_place(self):
        return str(self.source.handle.source.handle.presentation_place)

    @classmethod
    def make(cls, handle: Handle, page: int, name: str):
        return PDFObjectHandle(
                PDFPageSource(PDFPageHandle.make(handle, page)), name)
