# This script is intended to glean the bookname from file name from each file
# based the first line that does not have select key words in identified paragraph
# (i.e., list of contiguous lines of text).

#Manual adjustments will be required later.

import os
import sqlite3
import re
import textwrap

#Reading cleaned files
inputdir = 'G:/Gutenberg6'

conn = sqlite3.connect('Gutenberg5.sqlite3')
conn.text_factory = str
cur = conn.cursor()

content_list = []
tline = ''
nlinecount = 0
nmarginpos = 0
ndonotuse = 0
nletter = 0
ncount = 0

for content in os.listdir('G:\Gutenberg6\.'):

    infile = os.path.join(inputdir, content)
    print 'infile: ', infile
    tparagraph = ''
    for line in open(infile):

        if len(line) > 1:
            line = line.strip()

            words = line.split()
            for word in words:
                tline = tline + ' ' + word
            tparagraph = tparagraph + tline
            #print 'tparagraph reading lines:', tparagraph
            tline = ''
            nlinecount += 1
        else: #current line has no more than one character (assuming after)
            if (nlinecount > 0): #at least one line of text processed

                if tparagraph.find('|') != -1:
                    nmarginpos = tparagraph.find('|') + 1
                    tparagraphlower = tparagraph[nmarginpos:]

                tparagraph = textwrap.fill(tparagraph)
                tparagraph = textwrap.dedent(tparagraph)
                tparagraph = tparagraph.strip()

                #trying to not have number as bookname
                if len(tparagraph) <= 4:
                    tnumcheck = re.search('[0-9]+', tparagraph)
                    if (tnumcheck != None):
                        ndonotuse += 1

                tparagraphlower = tparagraph.lower()

                #trying to clean out some files with | in the line
                #want to still read the line

                if (tparagraphlower.find('electronic text') != -1 or
                    tparagraphlower.find('project gutenberg') != -1 or
                    tparagraphlower.find('1. license') != -1 or
                    tparagraphlower.find('@') != -1 or
                    tparagraphlower.find('.png') != -1 or
                    tparagraphlower.find('desktop') != -1 or
                    tparagraphlower.find('content') != -1 or
                    tparagraphlower.find('shakespear') != -1 or
                    tparagraphlower.find('scan') != -1 or
                    tparagraphlower.find('etext') != -1 or
                    tparagraphlower.find('e-text') != -1 or
                    tparagraphlower.find('errata') != -1 or
                    tparagraphlower.find('ebooks:') != -1 or
                    tparagraphlower.find('copyright') != -1 or
                    tparagraphlower.find('typographical') != -1 or
                    tparagraphlower.find('this text ') != -1 or
                    tparagraphlower.find('hyphenat') != -1 or
                    tparagraphlower.find('this ebook contains') != -1 or
                    tparagraphlower.find('versions') != -1 or
                    tparagraphlower.find('solicit contribut') != -1 or
                    tparagraphlower.find('***') != -1 or
                    tparagraphlower.find('* * *') != -1 or
                    tparagraphlower.find('+++') != -1 or
                    tparagraphlower.find('---') != -1 or
                    tparagraphlower.find('____') != -1 or
                    tparagraphlower.find('===') != -1 or
                    tparagraphlower.find('italics =') != -1 or
                    tparagraphlower.find('italics are') != -1 or
                    tparagraphlower.find('diphthong ') != -1 or
                    tparagraphlower.find('underscore') != -1 or
                    tparagraphlower.find('italic text') != -1 or
                    tparagraphlower.find('editor') != -1 or
                    tparagraphlower.find('footnote') != -1 or
                    tparagraphlower.find('transcribe') != -1 or
                    tparagraphlower.find('notes:') != -1 or
                    tparagraphlower.find('note:') != -1 or
                    tparagraphlower.find('proof read') != -1 or
                    tparagraphlower.find('proofread') != -1 or
                    tparagraphlower.find('please note:') != -1 or
                    tparagraphlower.find('to the reader') != -1 or
                    tparagraphlower.find('legal small print') != -1 or
                    tparagraphlower.find('+--') != -1 or
                    tparagraphlower.find('other books by') != -1 or
                    tparagraphlower.find('[illustra') != -1 or
                    tparagraphlower.find('[handwriting') != -1 or
                    tparagraphlower.find('[note') != -1 or
                    tparagraphlower.find('[frontispiece') != -1 or
                    tparagraphlower.find('[see letter') != -1 or
                    tparagraphlower.find('marginal note') != -1 or
                    tparagraphlower.find('[image') != -1 or
                    tparagraphlower.find('[redact') != -1 or
                    tparagraphlower.find('transcriptor') != -1 or
                    tparagraphlower.find('http:') != -1 or
                    tparagraphlower.find('ascii') != -1 or
                    tparagraphlower.find('text file') != -1 or
                    tparagraphlower.find(" printer's ") != -1 or
                    tparagraphlower.find('limited warranty') != -1 or
                    tparagraphlower.find('international donation') != -1 or
                    tparagraphlower.find('electonic work') != -1 or
                    tparagraphlower.find('file was produced') != -1 or
                    tparagraphlower.find('common project with') != -1 or
                    tparagraphlower.find('Carnegie Mellon') != -1 or
                    tparagraphlower.find('rec.arts.books') != -1 or
                    tparagraphlower.find('biographical note') != -1 or
                    tparagraphlower.find('italian and longfellow') != -1 or
                    tparagraphlower.find('produced by') != -1 or
                    tparagraphlower.find('prepared by') != -1):

                    ndonotuse += 1

                if (ndonotuse == 0 and nlinecount > 0):

                    if tparagraphlower.find('title:') != -1:

                        tparagraph = tparagraph[7:]
                        tparagraph = tparagraph.strip()

                    cur.execute('UPDATE FilesListClean SET bookname = ? WHERE filename = ?', (tparagraph, content))
                    print 'Copied bookname:', tparagraph


                    if ncount == 1000:
                        conn.commit()
                        ncount = 0
                    else:
                        ncount += 1

                    tparagraph = ''
                    tparagraphlower = ''
                    ndonotuse = 0
                    nlinecount = 0
                    break

                else:
                    tparagraph = ''
                    ndonotuse = 0
                    nlinecount = 0
            else:
                nlinecount = 0
                tparagraph = ''
                tparagraphlower = ''
                ndonotuse = 0

conn.commit()
conn.close()
