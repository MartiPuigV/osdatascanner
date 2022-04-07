#!/usr/bin/env python3

import unittest
from pathlib import Path
from itertools import zip_longest

from os2datascanner.engine2.model.ews import \
    EWSMailHandle, EWSAccountSource, OFFICE_365_ENDPOINT
from os2datascanner.engine2.model.file import FilesystemHandle, FilesystemSource
from os2datascanner.engine2.model.core import SourceManager, Source
from os2datascanner.engine2.model.http import WebSource, WebHandle
from os2datascanner.engine2.model.smb import SMBHandle, SMBSource
from os2datascanner.engine2.model.smbc import SMBCHandle, SMBCSource
from os2datascanner.engine2.model.derived.mail import MailPartHandle, MailSource

here_path = Path(__file__).resolve().parent
test_data_path = here_path / "data"

"""Test presentation and other properties of handles

- derived sources.

A file example.odt with text and inline image will, when explored, produce two
handles pointing to a html- and png-file.
The presentation properties (presentation, sort_key, presentation_name, type_label)
will be the same, but handle.name will differ, namely example.html and
example_html_<some-string>.png


- `direct` sources

ie. these sources could produce handles to other resources; but here they are used as
"dummy"-sources, where we only check their presentation values

Examples are ews, filesystem, http

"""
derived_sources = {
    "pdf-file": {
        "fpath": f"{test_data_path}/pdf",
        "fname": "embedded-cpr.pdf",
        "handles": [
            {
                # "name": "page.txt",
                "presentation": f"{test_data_path}/pdf",
                "presentation_name": "embedded-cpr.pdf (page 1)",
                "sort_key": f"{test_data_path}/pdf/embedded-cpr.pdf",
                "type": "pdf-page",
            },
            {
                # "name": "page.txt",
                "presentation": f"{test_data_path}/pdf",
                "presentation_name": "embedded-cpr.pdf (page 2)",
                "sort_key": f"{test_data_path}/pdf/embedded-cpr.pdf",
                "type": "pdf-page",
            },
            {
                # "name": "image-000.png",
                "presentation": f"{test_data_path}/pdf",
                "presentation_name": "embedded-cpr.pdf (page 2)",
                "sort_key": f"{test_data_path}/pdf/embedded-cpr.pdf",
                "type": "pdf-page",
            },
            {
                # "name": "image-001.png",
                "presentation": f"{test_data_path}/pdf",
                "presentation_name": "embedded-cpr.pdf (page 2)",
                "sort_key": f"{test_data_path}/pdf/embedded-cpr.pdf",
                "type": "pdf-page",
            },
        ],
    },
    "odt-file": {
        "fpath": f"{test_data_path}/libreoffice",
        "fname": "embedded-cpr.odt",
        "handles": [
            {
                # "name": "embedded-cpr.html",
                "presentation": f"{test_data_path}/libreoffice",
                "presentation_name": "embedded-cpr.odt",
                "sort_key": f"{test_data_path}/libreoffice/embedded-cpr.odt",
                "type": "lo",
            },
            {
                # "name": "embedded-cpr_html_3ebb4365c1c086a0.png",
                "presentation": f"{test_data_path}/libreoffice",
                "presentation_name": "embedded-cpr.odt",
                "sort_key": f"{test_data_path}/libreoffice/embedded-cpr.odt",
                "type": "lo",
            },
        ],
    },
    "zip-odt-file": {
        "fpath": f"{test_data_path}/zip",
        "fname": "embedded-cpr-odt.zip",
        "handles": [
            {
                # "name": "embedded-cpr.html",
                "presentation": f"{test_data_path}/zip",
                "presentation_name": "embedded-cpr-odt.zip (file embedded-cpr.odt)",
                "sort_key": f"{test_data_path}/zip/embedded-cpr-odt.zip",
                "type": "lo",
            },
            {
                # "name": "embedded-cpr_html_3ebb4365c1c086a0.png",
                "presentation": f"{test_data_path}/zip",
                "presentation_name": "embedded-cpr-odt.zip (file embedded-cpr.odt)",
                "sort_key": f"{test_data_path}/zip/embedded-cpr-odt.zip",
                "type": "lo",
            },
        ],
    },
    "zip-pdf-file": {
        "fpath": f"{test_data_path}/zip",
        "fname": "embedded-cpr-pdf.zip",
        "handles": [
            {
                "presentation": f"{test_data_path}/zip",  # noqa: E501
                "presentation_name": "embedded-cpr-pdf.zip (file embedded-cpr.pdf (page 1))",
                "sort_key": f"{test_data_path}/zip/embedded-cpr-pdf.zip",
                "type": "pdf-page",
            },
            {
                "presentation": f"{test_data_path}/zip",  # noqa: E501
                "presentation_name": "embedded-cpr-pdf.zip (file embedded-cpr.pdf (page 2))",
                "sort_key": f"{test_data_path}/zip/embedded-cpr-pdf.zip",
                "type": "pdf-page",
            },
            {
                "presentation": f"{test_data_path}/zip",  # noqa: E501
                "presentation_name": "embedded-cpr-pdf.zip (file embedded-cpr.pdf (page 2))",
                "sort_key": f"{test_data_path}/zip/embedded-cpr-pdf.zip",
                "type": "pdf-page",
            },
            {
                "presentation": f"{test_data_path}/zip",  # noqa: E501
                "presentation_name": "embedded-cpr-pdf.zip (file embedded-cpr.pdf (page 2))",
                "sort_key": f"{test_data_path}/zip/embedded-cpr-pdf.zip",
                "type": "pdf-page",
            },
        ],
    },
    # mail with inline cpr.jpg and attached embedded-cpr.odt with cpr.png
    "eml-file": {
        "fpath": f"{test_data_path}/mail",
        "fname": "mail-with-inline-img-and-attached-odt.eml",
        "handles": [
            {
                # "name": "file",
                "presentation": f"{test_data_path}/mail",
                "presentation_name": "mail-with-inline-img-and-attached-odt.eml",
                "sort_key": f"{test_data_path}/mail/mail-with-inline-img-and-attached-odt.eml",
                "type": "mail",
            },
            {
                # "name": "cpr.jpg",
                "presentation": f"{test_data_path}/mail",
                "presentation_name": "mail-with-inline-img-and-attached-odt.eml (attachment cpr.jpg)",  # noqa: E501
                "sort_key": f"{test_data_path}/mail/mail-with-inline-img-and-attached-odt.eml",
                "type": "mail",
            },
            {
                # "name": "embedded-cpr.html",
                "presentation": f"{test_data_path}/mail",  # noqa: E501
                "presentation_name": "mail-with-inline-img-and-attached-odt.eml (file embedded-cpr.odt)",  # noqa: E501
                "sort_key": f"{test_data_path}/mail/mail-with-inline-img-and-attached-odt.eml",
                "type": "lo",
            },
            {
                # "name": "embedded-cpr_html_3ebb4365c1c086a0.png",
                "presentation": f"{test_data_path}/mail",  # noqa: E501
                "presentation_name": "mail-with-inline-img-and-attached-odt.eml (file embedded-cpr.odt)",  # noqa: E501
                "sort_key": f"{test_data_path}/mail/mail-with-inline-img-and-attached-odt.eml",
                "type": "lo",
            },
        ],
    },
}


direct_sources = {
    "websource": {
        "handle": WebHandle(
            WebSource(url="https://www.example.com"), "/not_a_page.html"
        ),
        "handles": {
            "name": "not_a_page.html",
            "presentation": "https://www.example.com/not_a_page.html",
            "presentation_name": "not_a_page.html",
            "sort_key": "https://www.example.com/not_a_page.html",
            "type": "web",
        },
    },
    "filesystem": {
        "handle": FilesystemHandle(
            FilesystemSource(path="/home/dummy/"), "not_a_file.txt"
        ),
        "handles": {
            "name": "not_a_file.txt",
            "presentation": "/home/dummy",
            "presentation_name": "not_a_file.txt",
            "sort_key": "/home/dummy/not_a_file.txt",
            "type": "file",
        },
    },
    "ews": {
        "handle": EWSMailHandle(
            source=EWSAccountSource(
                domain="example.com",
                server="mail.example.com",
                admin_user="BOFH",
                admin_password="1234",
                user="dummy",
            ),
            path="/some_path",
            mail_subject="subject: you got mail",
            folder_name="/inbox",
            entry_id=5000,
        ),
        "handles": {
            "name": "subject: you got mail",
            "presentation": "In folder /inbox of account dummy@example.com",
            "presentation_name": "subject: you got mail",
            "sort_key": "example.com/dummy/inbox/subject: you got mail",
            "type": "ews",
        },
    },
    "smb": {
        "handle": SMBHandle(SMBSource(unc="\\\\SERVER\\"), "not_a_file.txt"),
        "handles": {
            "name": "not_a_file.txt",
            "presentation": "\\\\SERVER\\not_a_file.txt",
            "presentation_name": "not_a_file.txt",
            "sort_key": "\\\\SERVER\\not_a_file.txt",
            "type": "smb",
        },
    },
    "mail-part": {
        "handle": MailPartHandle(
            MailSource(
                EWSMailHandle(
                            EWSAccountSource(
                                    domain="cloudy.example",
                                    server=OFFICE_365_ENDPOINT,
                                    admin_user="cloudministrator",
                                    admin_password="littlefluffy",
                                    user="claude"),
                            path="SW5ib3hJRA==.TWVzc2dJRA==",
                            mail_subject="Re: Castles in the sky",
                            folder_name="Inbox",
                            entry_id="000001234567")
            ),
            path="1/pictograph.jpeg",
            mime="image/jpeg"),
        "handles": {
            "name": "pictograph.jpeg",
            "presentation": "In folder Inbox of account claude@cloudy.example",  # noqa: E501
            "presentation_name": 'Re: Castles in the sky (attachment pictograph.jpeg)',  # noqa: E501
            "sort_key": "cloudy.example/claude/Inbox/Re: Castles in the sky",
            "type": "mail",
        },
    }
}


def traverse_derived_source(source, sm):
    """Get handles from Source OR if the handle can be reinterpretted as a Source,
    recursively explore it"""
    # print(f"called with source {source.type_label}")

    for handle in source.handles(sm):
        derived = Source.from_handle(handle, sm)

        if derived:
            yield from traverse_derived_source(derived, sm)
        else:
            yield {
                "type": handle.source.type_label,
                "presentation": handle.presentation,
                "name": handle.name,
                "sort_key": handle.sort_key,
                "presentation_name": handle.presentation_name,
            }


class Engine2PresentationTest(unittest.TestCase):
    def test_derived_models(self):
        "test presentations of models that acts as containers"

        for fdesc, expected in derived_sources.items():
            fptr = Path(expected["fpath"]) / expected["fname"]
            handle = FilesystemHandle.make_handle(fptr)

            # store the presentation of each of the handles from the derived source.
            with SourceManager() as sm:
                source = Source.from_handle(handle, sm)
                presentation = list(traverse_derived_source(source, sm))

            # remove name from handle-dicts
            presentation = [
                {k: v for k, v in a.items() if k != "name"} for a in presentation
            ]

            for exp, pre in zip_longest(expected["handles"], presentation, fillvalue={}):
                self.assertDictEqual(
                    exp, pre, f"{fdesc} didn't produce the expected presentations"
                )

    def test_direct_models(self):
        for fdesc, expected in direct_sources.items():
            handle = expected["handle"]
            presentation = {
                "type": handle.source.type_label,
                "presentation": handle.presentation,
                "name": handle.name,
                "sort_key": handle.sort_key,
                "presentation_name": handle.presentation_name,
            }

            self.assertDictEqual(
                expected["handles"],
                presentation,
                f"{fdesc} didn't produce the expected presentations",
            )

    def test_drive_letters(self):
        expected = (
            (SMBHandle(
                    SMBSource("//SERVER/DRIVE"),
                    "Departments/Finance/FY 2022.ods"),
             r"\\SERVER\DRIVE\Departments\Finance\FY 2022.ods"),
            (SMBHandle(
                    SMBSource("//SERVER/DRIVE", driveletter="H:"),
                    "Departments/Finance/FY 2022.ods"),
             r"H:\Departments\Finance\FY 2022.ods"),
            (SMBCHandle(
                    SMBCSource("//SERVER/DRIVE", driveletter="H"),
                    "Departments/Finance/FY 2022.ods"),
             r"H:\Departments\Finance\FY 2022.ods"),
            (SMBHandle(
                    SMBSource(
                            "//SERVER/DRIVE/Departments",
                            driveletter="H:/Departments"),
                    "Finance/FY 2022.ods"),
             r"H:\Departments\Finance\FY 2022.ods"),
            (SMBCHandle(
                    SMBCSource(
                            "//SERVER/DRIVE/Departments/Finance",
                            driveletter="H:\\Departments\\Finance\\"),
                    "FY 2022.ods"),
             r"H:\Departments\Finance\FY 2022.ods"),
        )
        for handle, presentation in expected:
            self.assertEqual(
                    handle.presentation,
                    presentation,
                    "drive letter substitution failed")
