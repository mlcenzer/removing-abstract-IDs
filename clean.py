#!/usr/bin/env python3                                                          

import sys
import re

file_name_dirty=sys.argv[1]
file_name_clean=sys.argv[2]

file_dirty=open(file_name_dirty, "r")

file_clean=open(file_name_clean, "w")

References=[]
People=[]
Genders=[]
Status=[]
Preference=[]
Poster_Present=[]
Location=[]

file_clean.write('\\documentclass[12pt]{article}')
file_clean.write('\n')
file_clean.write('\\usepackage{fullpage}')
file_clean.write('\n')
file_clean.write('\\begin{document}')
file_clean.write('\n')


title=0

for old_line in file_dirty:
    forbidden=old_line.split('%')
    joiner='\\%'
    new_line=joiner.join(forbidden)
    forbidden=new_line.split('&')
    joiner='\\&'
    line=joiner.join(forbidden)
    if title==1:
            title_line=str('\\textbf{'+ line + '}\n')
            file_clean.write('\\vspace{12pt}\n')
            file_clean.write(title_line)
            file_clean.write('\n\\vspace{12pt}\n')
            title=0
    else:    
        if line.startswith('Author gender'):
            gender=line[15:]
            Genders.append(gender[:-1])
        elif line.startswith('Author status'):
            status=line[15:]
            Status.append(status[:-1])
        elif line.startswith('Reference'):
            ref=line[11:]
            References.append(ref[:-1])
            ref_line=str('\\textbf{Reference: }'+ref + '\n')
            file_clean.write('\\clearpage')
            file_clean.write(ref_line)
        elif line.startswith('Preferred'):
            pref=line[32:]
            Preference.append(pref[:-1])
            pref_line=str('\\textbf{Preferred format: }'+pref + '\n')
            file_clean.write(pref_line)
        elif line.startswith('- If you'):
            poster=line[113:]
            Poster_Present.append(poster[:-1])
            post_line=str('\\textbf{Would accept a poster: }'+poster + '\n')
            file_clean.write(post_line)
        elif line.startswith('- We plan'):
            record=line[211:]
            rec_line=str('\\textbf{Willing to record: }'+record + '\n')
            file_clean.write(rec_line)
            title=1
        
        else:
            giveaways=re.findall(r'\(\d,?\d?\)', line)
            if giveaways:
                line.strip()
                if line[-2:-1]=='.':
                    file_clean.write(new_line)
                    file_clean.write('\n')
            else:
                file_clean.write(line)
                file_clean.write('\n')

                
#print(Preference))
file_meta=open('meta_data.tex', "w")

for talk in range(0,164):
    line=str(References[talk] + '\t' + Preference[talk] + '\t' + Genders[talk] + '\t' + Status[talk] + '\n')
    file_meta.write(line)


file_clean.write('\\end{document}')

file_dirty.close()
file_clean.close()
file_meta.close()
