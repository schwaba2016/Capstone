# Initial code downloaded from http://www.winwaed.com/blog/2012/04/09/calculating-word-statistics-from-the-gutenberg-corpus/
# Code revised to attempt to remove a broader set of header and footer text patterns.

# Loops over all of the gutenberg text files
# Extracting unique texts, and copies them
# Removes header and footer information - leaving just the text, ready for
# statistical processing
#
# Usage: Be sure to change these paths to point to the relevant directories on your system

import string
import os
import gc
import shutil

inputdir = 'G:/Gutenberg4'
outputdir = "G:/Gutenberg6"

# The logic for keeping a file based on its name is put
# into a name to improve readability

# fname = Name of file without path or file extension
def keep_file(fname):
    # filter out readme, info, notes, etc
    if (fname.lower().find("readme") != -1):
        return False
    if  (fname.find(".zip.info") != -1):
        return False
    if (fname.find("pnote") != -1 ):
        return False
    # Filter out the Human Genome
    if (len(fname)==4):
        try:
            n = int(fname)
            if (n >=2201 and n <=2224):
                print "*** Genome skipped:",n
                return False    # Human Genome
        except ValueError:
            n=0  # dummy line

    # Looks good =&gt; keep this file
    return True

# Recursively walk the entire directory tree finding all .txt files which
# are not in old sub-directories. readme.txt files are also skipped.

# Empty the output directory
for f in os.listdir(outputdir):
    fpath = os.path.join(outputdir, f)
    try:
        if (os.path.isfile(fpath)):
            os.unlink(fpath)
    except Exception, e:
        print e

for (dirname, dirnames, filenames) in os.walk(inputdir):
    if (dirname.find('old') == -1  and
        dirname.find('-h') == -1 ) :
        # some files are duplicates, remove these and only copy a single copy
        # The -8 suffix takes priority (8 bit ISO-8859-1) over the
        # files with no suffix or -1 suffix (simple ASCII)
        # also remove auxiliaries: Names contain pnote or .zip.info
        flist = []
        flist_toremove = []
        for fname in filenames:
            fbase, fext = os.path.splitext(fname)
            if ( fext == '.txt'):
                if (keep_file(fbase)):
                    flist.append(fname)
                    #print 'file to keep: ', fname
                    if (fname.endswith("-8.txt") ):
                        # -8 takes priority =&gt; remove any duplicates
                        flist_toremove.append( fname[: (len(fname)-6)] + ".txt" )
                        flist_toremove.append( fname[: (len(fname)-6)] + "-0.txt" )

        flist_to_proc = [i for i in flist if i not in flist_toremove]

        # flist_to_proc now contains the files to copy
        # loop over them, copying line-by-line
        # Check for header/footer markers - file is skipped if header marker is missing
        for f in flist_to_proc:
            infile = os.path.join(dirname, f)
            outfile = os.path.join(outputdir, f)

            #Algorighm re-designed to be O(3n) due to the various styles of headers and closers in the files.
            #first run through each line of the file is to find how the file is structured.
            #second run is to copy only the book portion removing as much of the header and footer as possible.

            #First run through to find number of lines in file.
            #Short files need to use lower number of maximum rows to pickup headers
            nlinenumber = sum(1 for line in open(infile))
            if nlinenumber > 750:
                nheaderlinenumber = 400
            else:
                nheaderlinenumber = 200
            nlinenumber = 0

            #Second Run Through to help identify header and footer boundaries
            #(Re)Initializing Variables
            bDoNotCopy = False
            nEndHeader = 0
            nEtextIndicator = 0
            nwebsite = 0
            nNeedDonations = 0
            ndesktoptool = 0
            nVolunteers = 0
            nDavidReed = 0
            nForMembership = 0
            nProjectStart = 0
            nProducedBy= 0
            ntrainscribe = 0
            nProofReader = 0
            nInternetArchive = 0
            nEtextPrepared = 0
            nEndofPGutenberg = 0
            nprintedby = 0
            nascii = 0
            nEndofFile = 0
            nNewebooks = 0
            nlinenumber = 0
            nmaxlinenumber = 0
            neoflinenumber = 0

            print 'filename: ', f

            #Third fun through
            for line in open(infile):
                nlinenumber += 1
                if (line.find('Human Genome Project') != -1 and nlinenumber <= nheaderlinenumber):
                    bDoNotCopy = True
                    break
                    #print 'Human Genome Project: ', nlinenumber
                if ((line.find('FRANÇAISE') != -1 or
                     line.lower().find('bibliothèque') != -1 or
                     line.find('personne') != -1 or
                     line.find('históricos') != -1 or
                     line.find('cinco ') != -1 or
                     line.find('vienompia') != -1 or
                     line.find('worden') != -1 or
                     line.find('Доба') != -1 or
                     line.find('ogsaa') != -1 or
                     line.find('joka ') != -1 or
                     line.lower().find('transcripteur') != -1) and
                     nlinenumber <= nheaderlinenumber):
                    bDoNotCopy = True
                    break
                if (line.find('beiden') != -1 and nlinenumber <= nheaderlinenumber):
                    bDoNotCopy = True
                    break
                elif (line.find('*END*') != -1 and nlinenumber <= nheaderlinenumber):
                    nEndHeader += 1
                    nmaxlinenumber = max(nmaxlinenumber, nlinenumber + 1)
                    #print '*END* found at line ', nlinenumber
                elif ((line.lower().find('project gutenberg etext') != -1  or
                      line.lower().find("project gutenberg's etext") != -1) and nlinenumber <= nheaderlinenumber):
                    nEtextIndicator += 1
                    nmaxlinenumber = max(nmaxlinenumber, nlinenumber + 1 )
                    #print 'Project Gutenberg Etext found at line: ', nlinenumber
                elif ((line.find('gutenberg.org') != -1 or
                      line.find('gutenberg.net') != -1 or
                      line.find('ibiblio.org') != -1 or
                      line.find('gallica.bnf.fr') != -1) and nlinenumber <= nheaderlinenumber):
                    nwebsite += 1
                    nmaxlinenumber = max(nmaxlinenumber, nlinenumber + 1)
                elif (line.lower().find('we need your donations') != -1 and nlinenumber <= nheaderlinenumber):
                    nNeedDonations += 1
                    nmaxlinenumber = max(nmaxlinenumber, nlinenumber +1 )
                    #print 'We need your donations. found at line: ', nlinenumber
                elif (line.lower().find('desktop tool') != -1 and nlinenumber <= nheaderlinenumber):
                    ndesktoptool += 1
                    nmaxlinenumber = max(nmaxlinenumber, nlinenumber +1 )
                elif (line.lower().find('volunteers') != -1 and nlinenumber <= nheaderlinenumber):
                    nVolunteers += 1
                    nmaxlinenumber = max(nmaxlinenumber, nlinenumber +1)
                    #print "Volunteers :", nlinenumber
                elif ((line.find('David Reed') != -1 or
                       line.find('Dennis McCarthy') !=-1 or
                       line.find('Michael S. Hart') != -1 or
                       line.find('D.K.R.') != -1) and nlinenumber <= nheaderlinenumber):
                    nDavidReed += 1
                    nmaxlinenumber = max(nmaxlinenumber, nlinenumber +1 )
                    #print 'David Reed found at line: ', nlinenumber
                elif (line.lower().find('for membership') != -1 and nlinenumber <= nheaderlinenumber):
                    nForMembership += 1
                    nmaxlinenumber = max(nmaxlinenumber, nlinenumber +1)
                elif ((line.find('START OF THIS PROJECT GUTENBERG') != -1 or
                       line.find('START OF THE PROJECT GUTENBERG') != -1) and nlinenumber <= nheaderlinenumber):
                    nProjectStart += 1
                    nmaxlinenumber = max(nmaxlinenumber, nlinenumber +1)
                elif (line.lower().find('produced by') != -1 and nlinenumber <= nheaderlinenumber):
                    nProducedBy += 1
                    nmaxlinenumber = max(nmaxlinenumber, nlinenumber +1)
                elif ((line.lower().find('transcribe') != -1 or line.lower().find('handwritten') != -1) and nlinenumber <= nheaderlinenumber):
                     ntrainscribe += 1
                     nmaxlinenumber = max(nmaxlinenumber, nlinenumber +1)
                elif (line.lower().find('proofread') != -1 and nlinenumber <= nheaderlinenumber):
                    nProofReader += 1
                    nmaxlinenumber = max(nmaxlinenumber, nlinenumber +1)
                elif (line.lower().find('internet archive') != -1 and nlinenumber <= nheaderlinenumber):
                    nInternetArchive += 1
                    nmaxlinenumber = max(nmaxlinenumber, nlinenumber +1)
                elif (line.find('Etext was prepared') != -1 and nlinenumber <= nheaderlinenumber ):
                    nEtextPrepared += 1
                    nmaxlinenumber = max(nmaxlinenumber, nlinenumber)
                elif (line.find('End of The Project Gutenberg') != -1 or
                      line.find('End of the Project Gutenberg') != -1 or
                      line.find('END OF THE PROJECT GUTENBERG') != -1 or
                      line.find('END OF PROJECT GUTENBERG') != -1 or
                      line.find('End of Project Gutenberg') != -1):
                    nEndofPGutenberg += 1
                    if neoflinenumber == 0:
                        neoflinenumber = nlinenumber
                    else:
                        neoflinenumber = min(neoflinenumber, nlinenumber -3)
                    #print "End of Project Gutenberg found at line :", nlinenumber
                elif (line.lower().find('printed by') != -1):
                    nprintedby += 1
                    neoflinenumber = min(neoflinenumber, nlinenumber -3)
                elif (line.lower().find('ascii') != -1):
                    nascii += 1
                    neoflinenumber = min(neoflinenumber, nlinenumber -3)
                elif ((line.find('End of') != -1 or
                      line.find('END OF') != -1)
                      and line.lower().find('end of the project gutenberg') == -1):
                    nEndofFile +=1
                    if neoflinenumber == 0:
                        neoflinenumber = nlinenumber
                    else:
                        neoflinenumber = min(neoflinenumber, nlinenumber -3)
                    #print "End of .... found at:", nlinenumber
                elif (line.lower().find('hear about new ebooks') != -1):
                    nNewebooks += 1
                    if neoflinenumber == 0:
                        neoflinenumber = nlinenumber
                    else:
                        neoflinenumber = min(neoflinenumber, nlinenumber -3)
                    #print "new ebooks found at line: ", nlinenumber
            #print 'reviewed: ', infile
            #raw_input('Press <ENTER> to continue')
            #print 'nmaxlinenumber: ', nmaxlinenumber
            #print 'neoflinenumber: ', neoflinenumber

            #Second Run through
            bCopying = False
            nlinenumber = 0
            for line in open(infile):
                nlinenumber += 1
                if (not bDoNotCopy):
                    if nlinenumber == nmaxlinenumber:
                        fout = open(outfile, "w")
                        print "Copying: " + f
                        bCopying = True

                    elif (bCopying):
                        #print 'bCopying is True', nlinenumber, "eof line number:", neoflinenumber
                        if nlinenumber == neoflinenumber:
                            #print 'Eof linenumber: ', nlinenumber
                            fout.close()
                            bCopying = False

                        else:
                            fout.write(line)
