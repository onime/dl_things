#!/usr/bin/python

#Télécharge les derniers sous-titres des derniers episodes téléchargé
from urllib.parse import *
import re
from easylast import *
from urllib.request import *
import glob
import os

list_shows = infos_last("SHOW"," ","DL")
path_shows = "/media/Data/Shows/"

#Trouve les derniers sous-titre téléchargé
dirs_show = glob.glob(path_shows+"*")
last_sub = []

for dir_show in dirs_show:
    if os.path.isdir(dir_show):
        for show in list_shows:
            if re.search(show["name"].replace(" ","."),dir_show,re.IGNORECASE):
                list_srt = sorted([x.lower() for x in glob.glob(dir_show+"/Saison."+str(show["num"]["season"])+"/*.srt")])
                if list_srt:
                    print(list_srt[-1])

                    match = re.match(".*S[0-9]+E([0-9]+)\.",list_srt[-1],re.IGNORECASE)
                    if match == None:
                        match = re.match(".*[0-9]+x([0-9]+).*",list_srt[-1],re.IGNORECASE)

                    str_ep_sub = match.group(1)

                    print(str_ep_sub)
                    last_sub.append([show["name"],show["num"]["season"],int(str_ep_sub)+1,dir_show])
                else:
                    last_sub.append([show["name"],show["num"]["season"],0,dir_show])
                    
print(last_sub)

base_addicted = "http://www.addic7ed.com/"
tree_addicted = parse_url(base_addicted+"shows.php")
list_link_shows = tree_addicted.xpath("//td[@class='version']")

for show in last_sub:

    for ligne_show in list_link_shows:
        link_show = ligne_show.getchildren()[0].getchildren()[1].attrib["href"]
        name_show = ligne_show.getchildren()[0].getchildren()[1].text
       
        if re.search(show[0],name_show,re.IGNORECASE):
            last_num_season = show[1]
            last_num_episode = show[2]

            tree_show = parse_url(base_addicted+link_show)
            list_episode = tree_show.xpath("//tr[@class='epeven completed']")
            
            cur_num_episode = 1
            list_download_sub = {}

            for episode in list_episode:
                infos = episode.getchildren()
           
                cur_num_season = str(infos[0].text)
                num_episode_line = str(infos[1].text)
                lang = str(infos[3].text)
                is_complete = str(infos[5].text)
                version = str(infos[4].text)
                link_srt = infos[9].getchildren()[0].attrib["href"]
                
                if  (re.search("^Complete",is_complete,re.IGNORECASE) and re.search("^LOL|EVOLVE|ASAP|WEB-DL|IMMERSE|PROPER",version) and
                     re.search("French",lang,re.IGNORECASE) and int(num_episode_line) >= int(last_num_episode)):
                    print(link_srt)
                    if str(num_episode_line) not in list_download_sub.keys():

                        list_download_sub[int(num_episode_line)] = link_srt
                     
            for k in list_download_sub.keys():
                
                path_dl_sub = show[-1]+"/Saison."+str(last_num_season)+"/"
                if not os.path.exists(path_dl_sub):
                    os.makedirs(path_dl_sub)
                
                #On utilise le referer parce que addic7ed n'accepte les téléchargements que des connections qui viennent
                # d'addic7ed

                req = Request(base_addicted+list_download_sub[k])
                req.add_header('referer', base_addicted+link_show)
                r = urlopen(req)
                content_srt = r.read().decode("iso-8859-1")
                
                path_dl_sub +=format_name(name_show," ")+"."+format_SXXEXX({"season":last_num_season,"episode":k})+".srt"
                file_srt = open(path_dl_sub,"w",encoding = "iso-8859-1")
                file_srt.write(content_srt)
                file_srt.close()
                print(path_dl_sub)                              

