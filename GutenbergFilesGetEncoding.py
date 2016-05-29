#Different language files use different character encoding.
#This program is intended to collect the encoding method from the original text files

import os
import sqlite3

#Reading cleaned files
inputdir = 'G:\Gutenberg6'
fullfiledir = 'G:\Gutenberg4'

#sqlite database
conn = sqlite3.connect('Gutenberg5.sqlite3')
conn.text_factory = str
cur = conn.cursor()

#conn.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        #.format(tn='FilesListClean', cn='encoding', ct='TEXT'))

#conn.commit()

word = ''
ncount = 0
nwordcount = 0
nencodingflag = 0
tencoding = ''

for content in os.listdir(inputdir):
  infile = os.path.join(fullfiledir, content)
  print 'content: ', content
  for line in open(infile):
      linelower = line.lower().strip().split()
      linelower = line.split()
      linesplit = line.strip().split()

      nwordcount = len(linelower)

      ncount = 0
      while (ncount < nwordcount):
          #print 'linelower:', ncount, nwordcount, linelower[ncount]
          if (linelower[ncount].strip() == 'encoding:'):
              ncount += 1
              while (ncount < nwordcount):
                  tencoding = tencoding + ' ' + linesplit[ncount]
                  ncount += 1
              print 'tencoding', tencoding
              conn.execute("UPDATE FilesListClean SET encoding = ? where filename = ?", (tencoding, content))
              ncount = 0
              tencoding = ''
              nencodingflag = 1
              break
          else:
              ncount += 1

      if nencodingflag == 1:
          nencodingflag = 0
          ncount = 0
          break

conn.commit()
conn.close()
