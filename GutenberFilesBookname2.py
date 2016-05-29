#Different language files use different character language.
#This program is intended to collect the language from the original text files

import os
import sqlite3

#Reading cleaned files
inputdir = 'G:\Gutenberg6'
fullfiledir = 'G:\Gutenberg4'

#sqlite database
conn = sqlite3.connect('Gutenberg5.sqlite3')
conn.text_factory = str
cur = conn.cursor()

conn.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn='FilesListClean', cn='bookname2', ct='TEXT'))

conn.commit()

word = ''
ncount = 0
nwordcount = 0
ttitle = ''
ntitleflag = 0

for content in os.listdir(inputdir):
  infile = os.path.join(fullfiledir, content)
  print 'content: ', content
  for line in open(infile):
      linelower = line.lower().strip().split()
      linesplit = line.strip().split()

      nwordcount = len(linelower)
      #print 'nwordcount', nwordcount

      ncount = 0
      while (ncount < nwordcount):
          #print 'linelower:', ncount, nwordcount, linelower[ncount]
          if (linelower[ncount].strip() == 'title:'):
              ncount += 1
              while (ncount < nwordcount):
                  ttitle = ttitle + ' ' + linesplit[ncount]
                  ncount += 1
              print 'ttitle', ttitle
              conn.execute("UPDATE FilesListClean SET bookname2 = ? where filename = ?", (ttitle, content))
              ncount = 0
              ttitle = ''
              ntitleflag = 1
              break
          else:
              ncount += 1

      if ntitleflag == 1:
          ntitleflag = 0
          ncount = 0
          break

conn.commit()
conn.close()
