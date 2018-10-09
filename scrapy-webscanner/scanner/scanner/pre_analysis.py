import time
import magic
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def _type_dict(group, sub, relevant=False, supported=None):
    type_dict = {'super-group': group,
                 'sub-group': sub,
                 'relevant': relevant,
                 'supported': supported}
    return type_dict


def file_type_group(filetype):
    types = {}
    types['ASCII'] = _type_dict('Text', 'Text', True, 'text.py')
    types['ISO-8859'] = _type_dict('Text', 'Text', True, 'text.py')
    types['UTF-'] = _type_dict('Text', 'Text', True, 'text.py')
    types['vCalendar'] = _type_dict('Text', 'Text', True, None)
    types['Event Log'] = _type_dict('Text', 'Text', True, None)
    types['vCard'] = _type_dict('Text', 'Text', True, None)
    types['sendmail m4'] = _type_dict('Text', 'Text', True, None)
    types['Microsoft Word'] = _type_dict('Text', 'Office', True, 'libreoffice.py')
    types['Excel'] = _type_dict('Text', 'Office', True, 'libreoffice.py')
    types['PowerPoint'] = _type_dict('Text', 'Office', True, 'libreoffice.py')
    types['OpenDocument'] = _type_dict('Text', 'Office', True, 'libreoffice.py')
    types['Composite'] = _type_dict('Text', 'Office', True, 'libreoffice.py')
    types['XML'] = _type_dict('Text', 'Structured Text', True, 'xml.py')
    types['HTML'] = _type_dict('Text', 'Structured Text', True, 'html.py')
    types['C#'] = _type_dict('Text', 'Source Code', True, None)
    types['Java'] = _type_dict('Text', 'Source Code', True, None)
    types['Dyalog APL'] = _type_dict('Text', 'Source Code', True, None)
    types['byte-compiled'] = _type_dict('Binary', 'Source Code', False, None)
    types['SysEx'] = _type_dict('Media', 'Sound', False, None)
    types['Audio'] = _type_dict('Media', 'Sound', False, None)
    types['MP4'] = _type_dict('Media', 'Sound', False, None)
    types['MED_Song'] = _type_dict('Media', 'Sound', False, None)
    types['WebM'] = _type_dict('Media', 'Video', False, None)
    types['Matroska'] = _type_dict('Media', 'Video', False, None)
    types['MPEG'] = _type_dict('Media', 'Video', False, None)
    types['QuickTime'] = _type_dict('Media', 'Video', False, None)
    types['Git'] = _type_dict('Data', 'Text', False, None)
    types['Media descriptor 0xf4'] = _type_dict('Data', 'Data', False, None)
    types['TDB database'] = _type_dict('Data', 'Data', False, None)
    types['SQLite'] = _type_dict('Data', 'Data', False, None)
    types['very short file'] = _type_dict('Data', 'Data', False, None)
    types['Qt Traslation'] = _type_dict('Data', 'Data', False, None)
    types['FoxPro'] = _type_dict('Data', 'Data', False, None)
    types['GVariant'] = _type_dict('Data', 'Data', False, None)
    types['Debian'] = _type_dict('Data', 'Data', False, None)
    types['dBase III'] = _type_dict('Data', 'Data', False, None)
    types['PEM certificate'] = _type_dict('Data', 'Data', False, None)
    types['OpenType'] = _type_dict('Data', 'Data', False, None)
    types['RSA'] = _type_dict('Data', 'Data', False, None)
    types['OpenSSH'] = _type_dict('Data', 'Data', False, None)
    types['Applesoft'] = _type_dict('Data', 'Data', False, None)
    types['GStreamer'] = _type_dict('Data', 'Data', False, None)
    types['Snappy'] = _type_dict('Data', 'Data', False, None)
    types['snappy'] = _type_dict('Data', 'Data', False, None)
    types['GStreamer'] = _type_dict('Data', 'Data', False, None)
    types['Minix filesystem'] = _type_dict('Data', 'Data', False, None)
    types['SE Linux policy'] = _type_dict('Data', 'Data', False, None)
    types['binary'] = _type_dict('Data', 'Data', False, None)
    types['Compiled terminfo'] = _type_dict('Data', 'Data', False, None)
    types['GPG'] = _type_dict('Data', 'Data', False, None)
    types['PGP'] = _type_dict('Data', 'Data', False, None)
    types['Mini Dump'] = _type_dict('Data', 'Data', False, None)
    types['Font'] = _type_dict('Data', 'Data', False, None)
    types['GUS patch'] = _type_dict('Data', 'Data', False, None)
    types['TrueType'] = _type_dict('Data', 'Data', False, None)
    types['SoftQuad'] = _type_dict('Data', 'Data', False, None)
    types['PPD'] = _type_dict('Data', 'Data', False, None)
    types['GNU mes'] = _type_dict('Data', 'Data', False, None)
    types['GNOME'] = _type_dict('Data', 'Data', False, None)
    types['ColorSync'] = _type_dict('Data', 'Data', False, None)
    types['Berkeley'] = _type_dict('Data', 'Data', False, None)
    types['ESRI Shapefile'] = _type_dict('Data', 'Data', False, None)
    types['Flash'] = _type_dict('Data', 'Data', False, None)
    types['Microsoft ASF'] = _type_dict('Data', 'Data', False, None)
    types['DWG AutoDesk'] = _type_dict('Data', 'Data', False, None)
    types['CLIPPER'] = _type_dict('Data', 'Data', False, None)
    types['Transport Neutral'] = _type_dict('Data', 'Data', False, None)
    types['shortcut'] = _type_dict('Data', 'Data', False, None)
    types['Windows Registry'] = _type_dict('Data', 'Data', False, None)
    types['init='] = _type_dict('Data', 'Data', False, None)
    types['tcpdump'] = _type_dict('Data', 'Data', False, None)
    types['Solitaire Image'] = _type_dict('Data', 'Data', False, None)
    types['GeoSwath RDF'] = _type_dict('Data', 'Data', False, None)
    types['CDFV2 Encrypted'] = _type_dict('Data', 'Data', False, None)
    types['Translation'] = _type_dict('Data', 'Data', False, None)
    types['X11 cursor'] = _type_dict('Data', 'Data', False, None)
    types['MSX ROM'] = _type_dict('Data', 'Data', False, None)
    types['Quake'] = _type_dict('Data', 'Data', False, None)
    types['empty'] = _type_dict('Data', 'Data', False, None)
    types['data'] = _type_dict('Data', 'Cache Data', False, None)
    types['PDF'] = _type_dict('Media', 'PDF', True, 'pdf.py')
    types['PostScript'] = _type_dict('Media', 'PDF', True, None)
    types['PNG'] = _type_dict('Media', 'Image', True, 'ocr.py')
    types['GIF'] = _type_dict('Media', 'Image', True, 'ocr.py')
    types['JPEG'] = _type_dict('Media', 'Image', True, 'ocr.py')
    types['YUV'] = _type_dict('Media', 'Image', True, None)
    types['Icon'] = _type_dict('Media', 'Image', False, None)
    types['SVG'] = _type_dict('Media', 'Image', False, None)
    types['RIFF'] = _type_dict('Media', 'Image', False, None)
    types['bitmap'] = _type_dict('Media', 'Image', False, None)
    types['ISO Media'] = _type_dict('Container', 'ISO Image', True, None)
    types['ISO Image'] = _type_dict('Container', 'ISO Image', True, None)
    types['ISO 9660'] = _type_dict('Container', 'ISO Image', True, None)
    types['Zip'] = _type_dict('Container', 'Archive', True, 'zip.py')
    types['Microsoft Cabinet'] = _type_dict('Container', 'Archive', True, None)
    types['Tar'] = _type_dict('Container', 'Archive', True, None)
    types['Par archive'] = _type_dict('Container', 'Archive', True, None)
    types['current ar archive'] = _type_dict('Container', 'Archive', True, None)
    types['XZ'] = _type_dict('Container', 'Archive', True, None)
    types['zlib'] = _type_dict('Container', 'Archive', True, None)
    types['VirtualBox'] = _type_dict('Container', 'Virtual Machine', False, None)
    types['ELF'] = _type_dict('Data', 'Executable', False, None)
    types['PE32'] = _type_dict('Data', 'Executable', False, None)
    types['Executable'] = _type_dict('Data', 'Executable', False, None)
    types['amd 29K'] = _type_dict('Data', 'Executable', False, None)

    types['ERROR'] = _type_dict('Error', 'Error', True, None)

    for current_type in types.keys():
        if filetype.lower().find(current_type.lower()) > -1:
            filetype = types[current_type]
            return filetype
    filetype = _type_dict('Unknown', filetype, True, None)
    return filetype


def _to_filesize(filesize):
    sizes = {0: 'Bytes', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    filesize = float(filesize)
    for i in range(0, len(sizes)):
        if (filesize / 1024) > 1:
            filesize = filesize / 1024
        else:
            break
    formatted_size = ('{:.1f}{}'.format(filesize, sizes[i]))
    return formatted_size


class PreDataScanner(object):
    def __init__(self, path):
        self.nodes = {}
        self.stats = {}
        self.t0 = time.time()
        self.read_file_system(path)

    def read_file_system(self, path):
        self.nodes[path] = {'size': 0,
                            'filetype': _type_dict('Directory', 'Directory',
                                                   False, None)}
        self.read_dirtree(path)

        # We have not yet read the files, so at this point the
        # node-dict contains only directories
        self.stats['number_of_dirs'] = len(self.nodes)
        self.stats['time_number_of_dirs'] = time.time() - self.t0
        status_string = 'Read {} directories. Total run-time: {:.2f}s'
        print(status_string.format(self.stats['number_of_dirs'],
                                   self.stats['time_number_of_dirs']))

        self.stats['number_of_files'] = self.read_files()
        status_string = 'Read {} directories. Total run-time: {:.2f}s'
        self.stats['time_number_of_files'] = time.time() - self.t0
        status_string = 'Read {} files. Total run-time: {:.2f}s'
        print(status_string.format(self.stats['number_of_files'],
                                   self.stats['time_number_of_files']))
        self.stats['total_size'] = self.determine_file_information()
        self.stats['time_file_types'] = time.time() - self.t0

    def read_dirtree(self, path):
        all_dirs = path.glob('**')
        next(all_dirs)  # The root of the tree is already created
        for item in all_dirs:
            self.nodes[item] = {'size': 0,
                                'filetype': _type_dict('Directory', 'Directory',
                                                       False, None)}

    def read_files(self):
        new_nodes = {}
        for node in self.nodes.keys():
            items = node.glob('*')
            for item in items:
                if item.is_dir():
                    continue
                if item.is_symlink():
                    continue
                new_nodes[item] = {'size': 0}
        self.nodes.update(new_nodes)
        return len(new_nodes)

    def determine_file_information(self):
        """ Read through all file-nodes. Attach size and
        filetype to all of them.
        :param nodes: A dict with all nodes
        :param root: Pointer to root-node
        :return: Total file size in bytes
        """
        total_size = 0
        processed = 0
        t0 = time.time()
        t = t0
        for node in self.nodes.keys():
            processed += 1
            if processed % 2500 == 0:
                delta_t = time.time() - self.t0
                avg_speed = processed / delta_t
                now = time.time()
                current_speed = 2500 / (now - t)
                t = now
                eta = (len(self.nodes) - processed) / current_speed
                status = ('Progress: {}/{} in {:.0f}s. Avg. Speed: {:.0f}/s. ' +
                          'Current Speed {:.0f}/s ETA: {:.0f}s')
                print(status.format(processed, len(self.nodes), delta_t,
                                    avg_speed, current_speed, eta))
            if node.is_file():
                size = node.stat().st_size
                self.nodes[node]['size'] = size
                total_size += size
                if node.suffix == '.txt':  # No need to check these two
                    filetype = 'ASCII'
                elif node.suffix == '.html':
                    filetype = 'HTML'
                else:
                    try:
                        filetype = magic.from_buffer(open(str(node), 'rb').read(512))
                    except TypeError:
                        filetype = 'ERROR'
                filetype = file_type_group(filetype)
                self.nodes[node]['filetype'] = filetype
            else:
                self.nodes[node]['filetype'] = _type_dict('Directory', 'Directory',
                                                          False, None)
        return total_size

    def check_file_group(self, filetype, size=0):
        for node in self.nodes:
            if (node['filetype'] == filetype) and (node['size'] > size):
                print(node)

    def summarize_file_types(self):
        types = {'super': {},
                 'sub': {},
                 'supported': 0,
                 'relevant': 0}

        for node in self.nodes.keys():
            node_info = self.nodes[node]
            if not node.is_file():
                continue
            supergroup = self.nodes[node]['filetype']['super-group']
            subgroup = self.nodes[node]['filetype']['sub-group']

            if node_info['filetype']['supported'] is not None:
                types['supported'] += 1
            if node_info['filetype']['relevant'] is True:
                types['relevant'] += 1

            if supergroup in types['super']:
                types['super'][supergroup]['count'] += 1
                types['super'][supergroup]['sizedist'].append(node_info['size'])
            else:
                types['super'][supergroup] = {'count': 1,
                                              'sizedist': [node_info['size']]}
            if subgroup in types['sub']:
                types['sub'][subgroup]['count'] += 1
                types['sub'][subgroup]['sizedist'].append(node_info['size'])
            else:
                types['sub'][subgroup] = {'count': 1,
                                          'sizedist': [node_info['size']]}
        return types

    def update_stats(self, print_output=True):
        """ Update the internal stat-collection """
        self.stats['supported_file_count'] = 0
        self.stats['supported_file_size'] = 0
        self.stats['relevant_file_count'] = 0
        self.stats['relevant_file_size'] = 0
        self.stats['relevant_unsupported_count'] = 0
        self.stats['relevant_unsupported_size'] = 0
        for file_info in self.nodes.values():
            if file_info['filetype']['relevant']:
                self.stats['relevant_file_count'] += 1
                self.stats['relevant_file_size'] += file_info['size']
            if file_info['filetype']['supported'] is not None:
                self.stats['supported_file_count'] += 1
                self.stats['supported_file_size'] += file_info['size']
            if (file_info['filetype']['supported'] is None and file_info['filetype']['relevant']):
                self.stats['relevant_unsupported_count'] += 1
                self.stats['relevant_unsupported_size'] += file_info['size']

        if print_output:
            print('--- Stats ---')
            print('Total directories: {}'.format(self.stats['number_of_dirs']))
            print('Total Files: {}'.format(self.stats['number_of_files']))
            print('Total Size: {}'.format(_to_filesize(self.stats['total_size'])))
            print()

            supported = 'Total Supported Files: {} in {}bytes'
            print(supported.format(self.stats['supported_file_count'],
                                   _to_filesize(self.stats['supported_file_size'])))

            relevant = 'Total Relevant files: {} in {}bytes'
            print(relevant.format(self.stats['relevant_file_count'],
                                  _to_filesize(self.stats['relevant_file_size'])))

            rel_unsup = 'Relevant unsupported files: {} in {}bytes'
            size = self.stats['relevant_unsupported_size']
            print(rel_unsup.format(self.stats['relevant_unsupported_count'],
                                   _to_filesize(size)))
            print('-------')
            print()

    def plot(self, pp, types):
        labels = []
        sizes = []
        counts = []
        for filetype, stat in types.items():
            size = _to_filesize(sum(stat['sizedist']))
            status_string = 'Mime-type: {}, number of files: {}, total_size: {}'
            print(status_string.format(filetype, stat['count'], size))

            size_list = np.array(stat['sizedist'])
            size_list = size_list / 1024**2

            plt.hist(size_list, range=(0, max(size_list)), bins=50, log=True)
            plt.title(filetype)
            plt.xlabel('Size / MB')
            plt.savefig(pp, format='pdf')
            plt.close()

            labels.append(filetype)
            sizes.append(sum(stat['sizedist']))
            counts.append(stat['count'])

        other = 0
        compact_sizes = []
        compact_labels = []
        for i in range(0, len(sizes)):
            if (sizes[i] / self.stats['total_size']) < 0.025:
                other += sizes[i]
            else:
                compact_sizes.append(sizes[i])
                compact_labels.append(labels[i])
        compact_labels.append('Other')
        compact_sizes.append(other)

        explode = [0.4 if (i / self.stats['total_size']) < 0.05 else 0
                   for i in compact_sizes]

        fig1, ax1 = plt.subplots()
        textprops = {'fontsize': 'x-small'}
        wedges, texts, autotext = ax1.pie(compact_sizes, autopct='%1.0f%%',
                                          shadow=False, startangle=90,
                                          explode=explode,
                                          textprops=textprops)
        ax1.axis('equal')
        ax1.legend(wedges, compact_labels, fontsize='x-small')

        plt.savefig(pp, format='pdf')
        plt.close()


if __name__ == '__main__':
    t = time.time()
    p = Path('/mnt/new_var/mailscan/users/')
    # p = Path('/usr/share/')

    pre_scanner = PreDataScanner(p)
    filetypes = pre_scanner.summarize_file_types()
    pre_scanner.update_stats(print_output=True)

    pp = PdfPages('multipage.pdf')
    pre_scanner.plot(pp, filetypes['super'])
    pre_scanner.plot(pp, filetypes['sub'])
    pp.close()

    # pre_scanner.check_file_group('Virtual Machine')
