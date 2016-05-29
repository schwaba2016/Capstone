#This program is intended to try to prepopulate some of the files with genre
#based on key words in the text file.

import os
import sqlite3

#Reading cleaned files
inputdir = 'G:\Gutenberg6'
fullfiledir = 'G:\Gutenberg4'

#sqlite database
conn = sqlite3.connect('Gutenberg5.sqlite3')
conn.text_factory = str
cur = conn.cursor()

tgenre = ''
nnonfiction = 0
nfiction = 0

for content in os.listdir(inputdir):
    print 'content: ', content
    infile = os.path.join(fullfiledir, content)
    for line in open(infile):
        linelower = line.lower()
        if linelower.find('biogr') != -1:
            nnonfiction += 1
        if linelower.find('new testament') != -1:
            nnonfiction += 1
        if linelower.find('old testament') != -1:
            nnonfiction += 1
        if linelower.find('scriptures') != -1:
            nnonfiction += 1
        if linelower.find('dictionary') != -1:
            nnonfiction += 1
        if (linelower.find('poetry') != -1 or
            linelower.find('poem') != -1):
            nfiction += 1
        if linelower.find('history ') != -1:
            nnonfiction += 1
        if linelower.find(' novel') != -1:
            nfiction += 1
        if linelower.find('classics ') != -1:
            nfiction += 1

    if (nnonfiction > nfiction):
        tgenre = 'nonfiction'
    elif (nfiction > nnonfiction):
        tgenre = 'fiction'

    if tgenre != None:
        print 'genre: ', tgenre
        cur.execute('UPDATE FilesListClean SET genre = ? WHERE filename = ?', (tgenre, content))

    tgenre = None
    nnonfiction = 0
    nfiction = 0

conn.commit()
conn.close()
