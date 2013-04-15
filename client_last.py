#!/usr/bin/python

#client pour le serveur last_seen

import shutil
from easylast import *
from easysummary import *
from getopt import *
import sys

def usage():

    print("Usage :")
    print( "CMD")
    print( "\t --add add an information in the file")
    print( "\t --upd update the information given in parameter")
    print( "\t --del delete the information given in the parameter")
    print( "\t --inc increment the information given in the parameter")
    print( "\t --save save the data in a backup  file")
    print( "\t --restore restore the backup file")
    print(" \t --as add a summary to the INFO given")
    print(" \t --fs find a summary from the INFO or search from the keywords")
    
    print("TYPE")
    print("specify the file to look for")
    print("\t --DL information about the last download")
    print("\t --VU information about the last seen")
    
    print("INFO")

    print("\t -t the title of the show or manga")
    print("\t -n SwxEyz|XxYZ|XYZ (on ajoute une série ou un manga ex: -n S03E04 ou 3x04) ")
    print("\t -s indicate the summary to add or to look for")
    print("\t -p print the infos ")
    print("\t -h print this help" )

    print("\n\n Exemple")
    print("client_last --add --DL -t game.of.thrones -n s03e03")

args = sys.argv[1:]
try:
    optlist,value = getopt(args, 't:n:hps',['DL','VU','as','fs','add','upd','inc','del','save','restore'])  
except GetoptError as err:
    print(err)
    usage()
    sys.exit(2)

if "--VU" in args:
    bd = "VU"
else:
    bd = "DL"

bool_num = False
bool_name = False
bool_sum = False
bool_type = False

for i,o in enumerate(optlist):
    if o[0] == "-h":
        usage()
        exit(0)

    if o[0] == "--restore":
        shutil.copyfile(path_file_info+"."+bd+".bak",path_file_info+"."+bd)
        exit(0)
    if o[0] == "--save":
        shutil.copyfile(path_file_info+"."+bd,path_file_info+"."+bd+".bak")        
        exit(0)
  
    if o[0] == "-p":
        print(bd)
        print("--"*5)
        info_shows = infos_last("SHOW",".",bd)
        names = [(i["name"],i) for i in info_shows]
        names.sort()
        show_sort = [i for (_,i) in names]

        for s in show_sort:
            print(format_name(s["name"],".")+" ===> "+format_SXXEXX(s["num"]))
            
        print("--"*5)
        info_manga = infos_last("MANGA",".",bd)
        names = [(i["name"],i) for i in info_manga]
        names.sort()
        manga_sort = [i for (_,i) in names]

        for m in manga_sort:
            print(format_name(m["name"],".")+" ===> "+str(m["num"]["chap"]))

        exit(0)
  
    if o[0] == "-n":
        hash_num = parse_regex(re.search(regex_infos,optlist[i][1],re.IGNORECASE))
        if "chap" in hash_num.keys():
            type_info = "MANGA"
        else:
            type_info = "SHOW"
     
        bool_num = True

    if o[0] == "-s":       
        summary = optlist[i][1]
        bool_sum = True
       
    if o[0] == "-t":
        name = optlist[i][1]
        bool_name = True

for i,o in enumerate(optlist):
    if o[0] == "--inc":
        if bool_name == True:
            incr_last(name,bd)
        exit(0)

    if o[0] == "--del":
        if bool_name == True:
            suppr_info(name,bd)
        exit(0)

    if o[0] == "--add":
        if bool_num == True and bool_name == True:
            if is_manga({"type":type_info}):
                add_manga(name,hash_num,bd)
            else:
                add_show(name,hash_num,bd)

        if bool_sum == True:
             doc = {"type":type_info,"name":name,"summary":summary,"num":hash_num}
             add_summary(doc)
        exit(0)

    if o[0] == "--upd":
        if bool_num == True and bool_name == True:
            upd_last(name,hash_num,bd)

        if bool_sum == True:
             doc = {"type":type_info,"name":name,"summary":summary,"num":hash_num}
             add_summary(doc)
             exit(0)

    if o[0] == "--as":
        if bool_num == True and bool_name == True and  bool_sum == True:
            doc = {"type":type_info,"name":name,"summary":summary,"num":hash_num}
            add_summary(doc)
    
    if o[0] == "--fs":
        doc = {}
        if bool_type == True:
            doc["type"]=type_info
        if bool_num == True:
            doc["num"]=hash_num
        if bool_sum == True:
            doc["summary"] = {'$regex': summary,'$options' :'i'}
        if bool_name == True:
            doc["name"] = {'$regex': name,'$options' :'i'}
    
        res = find_summary(doc)
        for doc in res:
            print(doc)
    
