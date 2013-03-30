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
        file_dump = open("/home/yosholo/.config/utils/dump_bd_last_seen."+bd,"r")
        lines = file_dump.readlines()
        for line in lines:
            elem = line.split(",")
            if int(elem[1]) == 0:
                add_show(elem[0],elem[2],elem[3],bd)
            else:
                add_manga(elem[0],elem[1],bd)
            file_dump.close()
        exit(0)
    if o[0] == "--save":
        file_dump = open("/home/yosholo/.config/utils/dump_bd_last_seen."+bd,"w")
        infos=infos_last("*","MANGA",bd)
        new_str = []
        for i in infos:
            new_str.append(",".join([str(x) for x in i]))
        infos=infos_last("*","SHOW",bd)
        new_str = []
        for i in infos:
            new_str.append(",".join([str(x) for x in i]))

        s = "\n".join([ str(info) for info in new_str])
        file_dump.write(s)
        file_dump.close()
        exit(0)
  
    if o[0] == "-p":
        print(bd)
        print("--"*5)
        print(infos_last("SHOW",".",bd))
        print("--"*5)
        print(infos_last("MANGA",".",bd))
        exit(0)
  
    if o[0] == "-n":
        hash_num = {}
        num = parse_regex(re.search(regex_infos,optlist[i][1],re.IGNORECASE))
        if len(num) > 1:
            type_info = "SHOW"
            hash_num["season"]=num[0]
            hash_num["episode"]=num[1]
        else:
            type_info = "MANGA"
            hash_num["chap"] = num[0]
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
            incr_last(o[1],bd)
        exit(0)

    if o[0] == "--del":
        if bool_name == True:
            suppr_info(o[1],bd)
        exit(0)

    if o[0] == "--add":
        if bool_num == True and bool_name == True:
            add_manga(o[1],hash_num,bd)
        if bool_sum == True:
             doc = {"type":type_info,"name":name,"summary":summary,"num":hash_num}
             add_summary(doc)
        exit(0)

    if o[0] == "--upd":
        if bool_num == True and bool_name == True:
            upd_last(o[1],hash_num,bd)
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
    
