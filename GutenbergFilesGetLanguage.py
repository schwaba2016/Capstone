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

#conn.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        #.format(tn='FilesListClean', cn='language', ct='TEXT'))

conn.commit()

word = ''
ncount = 0
nwordcount = 0
nlanguageflag = 0

for content in os.listdir(inputdir):
  infile = os.path.join(fullfiledir, content)
  print 'content: ', content
  for line in open(infile):
      linelower = line.lower().strip().split()

      nwordcount = len(linelower)
      #print 'nwordcount', nwordcount

      ncount = 0
      while (ncount < nwordcount):
          #print 'linelower:', ncount, nwordcount, linelower[ncount]
          if (linelower[ncount] == 'language:'):
              print 'language:', linelower[ncount]
              if ((ncount + 1) < nwordcount):
                  tlanguage = linelower[ncount + 1]
              print 'tlanguage', tlanguage
              conn.execute("UPDATE FilesListClean SET language = ? where filename = ?", (tlanguage, content))
              ncount = 0
              nlanguageflag = 1
              break
          else:
              ncount += 1

      if nlanguageflag == 1:
          nlanguageflag = 0
          ncount = 0
          break

conn.commit()
conn.close()
