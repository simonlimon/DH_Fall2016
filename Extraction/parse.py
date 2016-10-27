import re
import csv
import sys

filename = "result/page_1_edited.txt"

processing_object = False
with open(filename) as text:
    for line in text:
        if re.match("CH. .*].*",line): #name file after header
            sjm_chapter = line.split("]")[0][4:]
            target = open("result/"+line[:-1]+".csv","w")
            writer = csv.writer(target)
            writer.writerow(("Chapter","Site","Length", "Height", "Description"))
            processing_object = True
        elif re.match("\d.*\w{2}. *\d",line): #start of a new entry
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
            writer.writerow((sjm_chapter,site,length,height,description))

target.close()


line = "113. a. Mm. 15-286; cell I 5; 10 ft. below surface. Heart-shaped lamp of micaceous schist, with projecting handle at back and beaded border on rim. Length 6.12 in. This also is from the Mohra Moridu monastery, and of the same date as the preceding. (Pl. 142, a.)"