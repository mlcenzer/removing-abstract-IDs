#!/usr/bin/env python3                                                          
import sys
import re

#accept file names from command line
file_name_dirty=sys.argv[1]
file_name_clean=sys.argv[2]

#open files
file_dirty=open(file_name_dirty, "r")
file_clean=open(file_name_clean, "w")

#Empty lists for storing meta-data. Currently does not add people or location data.  
References=[]
#People=[]
Genders=[]
Status=[]
Preference=[]
Poster_Present=[]
#Location=[]

#makes your latex file not terrible
file_clean.write('\\documentclass[12pt]{article}\n')
file_clean.write('\\usepackage{fullpage}\n')
file_clean.write('\\begin{document}\n')


##I started writing this not realizing the line breaks in word did not correspond to actual new lines. That is why I used identifying if statements when I could have gone down more or less line by line; if you want to do it that way go wild!

#unless it's the title line
title=0
posttitle=0

for old_line in file_dirty:
    
    #Deal with the use of characters that need to be escaped in latex
    forbidden=old_line.split('%')
    joiner='\\%'
    new_line=joiner.join(forbidden)
    forbidden=new_line.split('&')
    joiner='\\&'
    line=joiner.join(forbidden)
    #Make title line bold
    if title==1:
            title_line=str('\\textbf{'+ line + '}\n')
            file_clean.write('\\vspace{12pt}\n')
            file_clean.write(title_line)
            file_clean.write('\n\\vspace{12pt}\n')
            title=0 #reset
            posttitle=0 #reset
    else:    
        if line.startswith('Author gender'):
            gender=line[15:] #presenter gender
            Genders.append(gender[:-1])#add to metadata
        elif line.startswith('Author status'):
            status=line[15:]#presenter career stage
            Status.append(status[:-1])#add to metadata
            if posttitle==1:
                title=1 #for poster presentations, title line follows status line
        elif line.startswith('Reference'):
            ref=line[11:] #reference number
            References.append(ref[:-1]) #add to metadata
            ref_line=str('\\textbf{Reference: }'+ref + '\n') #prettify
            file_clean.write('\\clearpage') #new page for a new abstract
            file_clean.write(ref_line) #write reference number into file
        elif line.startswith('Preferred'):
            pref=line[32:] #and so on
            Preference.append(pref[:-1])
            pref_line=str('\\textbf{Preferred format: }'+pref + '\n')
            file_clean.write(pref_line)
            if re.findall(r"Poster", pref):
                Poster_Present.append("Yes") #presenter's who prefer posters were not asked this question
                posttitle=1 #presenter's who prefer posters don't get the next two lines
        elif line.startswith('- If you'):
            poster=line[113:]
            Poster_Present.append(poster[:-1])
            post_line=str('\\textbf{Would accept a poster: }'+poster + '\n')
            file_clean.write(post_line)
        elif line.startswith('- We plan'):
            record=line[211:]
            rec_line=str('\\textbf{Willing to record: }'+record + '\n')
            file_clean.write(rec_line)
            title=1 #title line always follows willing to record line
            #UNLESS they prefer a poster
        else:
            giveaways=re.findall(r'\(\d[,\d]*\)', line) #identifying name and institution lines. These lines always contain an institution identifier in parentheses.
            if giveaways:
                line.strip()
                if line[-2:-1]=='.': #sometimes people use numbers in parentheses in their abstracts. Abstracts end with punctuation. Haven't seen any ! or ?.
                    file_clean.write(new_line)
                    file_clean.write('\n')
            else:
                file_clean.write(line) #writes abstracts
                file_clean.write('\n')

                
file_meta=open('meta_data.tex', "w") #makes metadata file

total_talks=len(References)

#print(len(References))
#print(len(Poster_Present))
#print(len(Genders))
#print(len(Status))

for talk in range(0,total_talks): #make tab-delimited file of metadata
    line=str(References[talk] + '\t' + Preference[talk] + '\t' + Poster_Present[talk] + '\t' + Genders[talk] + '\t' + Status[talk] + '\n')
    file_meta.write(line)


file_clean.write('\\end{document}')

file_dirty.close()
file_clean.close()
file_meta.close()
