import re
import csv
import sys

filename = "result/edited/page_1.txt"

#parser requires each entry to be entirely present and to be divided by line break.
#Edit the text file if this isn't the case for certain objects

processing_object = False
with open(filename) as text:
    sjm_chapter = ""
    current_class = ""
    for line in text:
        if re.match("CH. .*",line): #name file after header
            sjm_chapter = line.split("[][]")[0][4:]
            target = open("result/"+line[:-1]+".csv","w")
            writer = csv.writer(target)
            writer.writerow(("Chapter","Site","Length", "Height", "Description"))
            processing_object = True
        elif re.match("\d.*\w{2}. *\d",line): #start of a new entry
            line = line.replace("\xe2\x80\x94","-")
            line = line.replace("\xe2\x80\x99","'")
            divided_list = re.split("[;.] ",line) #break line
            print divided_list
            site = ""
            ID = ""
            sjm = ""
            length = ""
            height = ""
            description = ""
            for item in divided_list:
                if re.match("[A-Z][a-z]",line) and len(item)==2:
                    site = item
                elif "Length " in item:
                    length = item.replace("Length ", "")
                elif "Height  " in item:
                    length = item.replace("Height ", "")                
                else:
                    description += item + ". "
            
        elif line != "\n":
            description += line
        else:
            try:
                writer.writerow((sjm_chapter,site,length,height,description))
            except:
                continue

target.close()