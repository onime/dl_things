#!/usr/bin/python

#client pour le serveur last_seen

import shutil
from easylast import *
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
    optlist,value = getopt(args, 'a:x:u:n:i:hprs',['DL','VU'])  
except GetoptError as err:
    print(err)
    usage()
    sys.exit(2)

if "--VU" in args:
    bd = "VU"
else:
    bd = "DL"

if "-a" in args or "-a" in args:
    if "-n" not in args:
        print("Erreur : -a ou -u doit renseigner un numéro de saison ou un chapitre")
        usage()
        sys.exit(2)

for i,o in enumerate(optlist):
    if o[0] == "-h":
        usage()
        exit(0)

    if o[0] == "-r":
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
    if o[0] == "-s":
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
    if o[0] == "-i":
        incr_last(o[1],bd)
        exit(0)
    if o[0] == "-x":
        suppr_info(o[1],bd)
        exit(0)
    if o[0] == "-p":
        print(bd)
        print("--"*5)
        print(infos_last("SHOW",".",bd))
        print("--"*5)
        print(infos_last("MANGA",".",bd))
        exit(0)
    if o[0] == "-a":
        num = parse_regex(re.search(regex_infos,optlist[i+1][1],re.IGNORECASE))
        print(o[1])
        if len(num) > 1: 
            add_show(o[1],num[0],num[1],bd)
        else:
            add_manga(o[1],num[0],bd)
        exit(0)
    if o[0] == "-u":
        num = parse_regex(re.search(regex_infos,optlist[i+1][1],re.IGNORECASE))
        if len(num) > 1: 
            upd_last_show(o[1],num[0],num[1],bd)
        else:
            upd_last_manga(o[1],num[0],bd)
        exit(0)




