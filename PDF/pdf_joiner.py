try:
    from PyPDF2 import PdfFileReader, PdfFileWriter
except ImportError:
    from PyPdf import PdfFileReader, PdfFileWriter
import os
import sys


def pdf_cat(input_files, output_file):
    input_streams = []
    output_stream = open(output_file, 'wb')
    try:
        # First open all the files, then produce the output file, and
        # finally close the input files. This is necessary because
        # the data isn't read from the input files until the write
        # operation. Thanks to
        # https://stackoverflow.com/questions/6773631/problem-with-closing-python-pypdf-writing-getting-a-valueerror-i-o-operation/6773733#6773733
        for input_file in input_files:
            input_streams.append(open(input_file, 'rb'))
        writer = PdfFileWriter()
        for reader in map(PdfFileReader, input_streams):
            for n in range(reader.getNumPages()):
                writer.addPage(reader.getPage(n))
        writer.write(output_stream)
    finally:
        for f in input_streams:
            f.close()

if __name__ == "__main__":
    # get the new directory name
    directory_name = sys.argv[1]

    # get the files from an inputed directory
    input_files = [f"{directory_name}/{file}" for file in os.listdir(directory_name) if ".pdf" in file]

    # get a new file name
    new_file_name = sys.argv[2]

    pdf_cat(input_files, new_file_name)
