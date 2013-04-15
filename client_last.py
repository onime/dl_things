#!/usr/bin/python

#client pour le serveur last_seen

import shutil
from easylast import *
from easysummary import *
from getopt import *
import sys

#arg dl ou vu 
#    et presque comme le reste sur last seen sauf peut etre pour le num  dépisode S0xEyz ou XxYZ

def usage():

    print("Usage :")
    print("\t -a name (fonctionne avec -n) ")
    print("\t -x name (supprime name dans la bd) ")
    print("\t -u name (fonctionne avec -n) ")
    print("\t -n SwxEyz|XxYZ|XYZ (on ajoute une série ou un manga ex: -n S03E04 ou 3x04) ")
    print("\t -i name (incrémente le name dans la bd)")
    print("\t -s (save the bd in a file) ")
    print("\t -r (restore the file in the bd) ")
    print("\t -p (print the infos) ")

args = sys.argv[1:]
try:
    optlist,value = getopt(args, 'z:x:n:hps',['DL','VU','ar','fr','add','upd','inc','del','save','restore'])  
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
        print(infos_last("SHOW",".",bd))
        print("--"*5)
        print(infos_last("MANGA",".",bd))
        exit(0)
  
    if o[0] == "-n":
        hash_num = parse_regex(re.search(regex_infos,optlist[i][1],re.IGNORECASE))
        if "chap" in hash_num.keys():
            type_info = "SHOW"
        else:
            type_info = "MANGA"         
        bool_num = True

    if o[0] == "-s":       
        summary = optlist[i][1]
        bool_sum = True
       
    if o[0] == "-z":
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
            add_manga(name,hash_num,bd)
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

    if o[0] == "--ar":
        if bool_num == True and bool_name == True and  bool_sum == True:
            doc = {"type":type_info,"name":name,"summary":summary,"num":hash_num}
            add_summary(doc)
    
    if o[0] == "--fr":
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
    
