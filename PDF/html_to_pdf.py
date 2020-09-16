import pdfkit
import sys


def convert(filename, export_filename=None):
    if not export_filename:
        export_filename = filename.split('.')[0] + '.pdf'
    pdfkit.from_file(filename, export_filename)


if __name__ == '__main__':
    html_file = sys.argv[1].strip().replace('\\', '')

    convert(html_file)
