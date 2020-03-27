import PyPDF2
from tika import parser
from collections import defaultdict
from multiprocessing import Pool


def getsubs(loc, s):
    substr = s[loc:]
    i = -1
    while(substr):
        yield substr
        substr = s[loc:i]
        i -= 1


def repeat(some_tuple):
    i, r, occ = some_tuple
    for sub in getsubs(i, r):
        occ[sub] += 1


def longestRepetitiveSubstring(r, minocc):
    occ = defaultdict(int)
    # tally all occurrences of all substrings

    # do it with multiprocessing
    tuple_list = [(i, r, occ) for i in range(len(r))]

    with Pool(processes=8) as pool:
        pool.map(repeat, tuple_list, chunksize=1)

    # filter out all substrings with fewer than minocc occurrences
    occ_minocc = [k for k, v in occ.items() if v >= minocc]

    if occ_minocc:
        maxkey = max(occ_minocc, key=len)
        return maxkey
    else:
        raise ValueError("no repetitions of any substring of '%s' with %d or more occurrences" % (r, minocc))


# obtain filepath
filepath = input('What is the PDF called? \n')

# get text from filepath
text = ''
pdfFileObject = open(filepath, 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
count = pdfReader.numPages
if count == 0:
    count += 1
for i in range(count):
    page = pdfReader.getPage(i)
    text += page.extractText()

# name the file
name = filepath[:-4]

print('PyPDF2 output snippet: ')
print(text[:100])

# write document with tika
sufficient = input('Try with tika? (yes or no) \n')
if 'yes' in sufficient.lower():
    raw = parser.from_file(filepath)
    text = raw['content']

# find repetitions in content
maxkey = "asdfghjkwertyuiosdfghjxcvbnm"
while len(maxkey) > 10:
    maxkey = longestRepetitiveSubstring(text, 3)
    replace = input(f"Next largest string: {maxkey}\nWould you like to replace it (y/n)?\n")
    if 'y' in replace.lower():
        text.replace(maxkey, '')


# write document with pypdf
print('writing document... \n')
doc = open(name + ".txt", "w")
doc.write(text)
doc.close()
