#!/usr/bin/python

#Télécharge les derniers sous-titres des derniers episodes téléchargé
from urllib.parse import *
import re
from easylast import *
from urllib.request import *
import glob
import os

#opener = build_opener()
#opener.addheaders = [('User-agent', 'Mozilla/5.0')]

list_shows = infos_last("SHOW"," ","DL")
path_shows = "/media/Data/Shows/"
#récupérer liste des sous-titre qu'on a besoin

dirs_show = glob.glob(path_shows+"*")
last_sub = []

for dir_show in dirs_show:
    if os.path.isdir(dir_show):
        for show in list_shows:
            if re.search(show[0].replace(" ","."),dir_show,re.IGNORECASE):
                list_srt = sorted([x.lower() for x in glob.glob(dir_show+"/Saison."+str(show[1])+"/*.srt")])
                
                str_ep_sub = re.match(".*S[0-9]+E([0-9]+)\.",list_srt[-1],re.IGNORECASE).group(1)
                
                last_sub.append([show[0],show[1],int(str_ep_sub),dir_show])

base_addicted = "http://www.addic7ed.com/"
tree_addicted = etree.parse(base_addicted+"shows.php",parserHTML)

list_link_shows = tree_addicted.xpath("//td[@class='version']")

for show in last_sub:

    for ligne_show in list_link_shows:
        link_show = ligne_show.getchildren()[0].getchildren()[1].attrib["href"]
        name_show = ligne_show.getchildren()[0].getchildren()[1].text


    
        if re.search(show[0],name_show,re.IGNORECASE):
            last_num_season = show[1]
            last_num_episode = show[2]

            tree_show = etree.parse(base_addicted+link_show,parserHTML)
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
                
                 
                if  (re.search("^Complete",is_complete,re.IGNORECASE) and re.search("^LOL|EVOLVE|ASAP|WEB-DL",version) and
                     re.search("French",lang,re.IGNORECASE) and int(num_episode_line) > int(last_num_episode)):
                    
                    if str(num_episode_line) not in list_download_sub.keys():
                        list_download_sub[int(num_episode_line)] = link_srt

            for k in list_download_sub.keys():
                
                path_dl_sub = show[-1]+"/Saison."+str(last_num_season)+"/"
                if not os.path.exists(path_dl_sub):
                    os.makedirs(path_dl_sub)
                
                req = Request(base_addicted+link_srt)
                req.add_header('referer', base_addicted+link_show)
                r = urlopen(req)
                content_srt = r.read().decode("iso-8859-1")
                
                path_dl_sub +=format_name(name_show," ")+".S"+format_number_zero([last_num_season])[0]+"E"+format_number_zero([k])[0]+".srt"
                file_srt = open(path_dl_sub,"w",encoding = "iso-8859-1")
                file_srt.write(content_srt)
                file_srt.close()
                print(path_dl_sub)
                            
          
exit(0)  
#On tvsubtitles
base_tvsub = "http://fr.tvsubtitles.net/"
tree_tvsub = etree.parse(base_tvsub+"tvshows.html",parserHTML)
list_link_shows = tree_tvsub.xpath("//td[@align='left']")

for show_tvsub in list_link_shows:
    name_show_tvsub = show_tvsub.getchildren()[0].getchildren()[0].text
    link_show_tvsub = show_tvsub.getchildren()[0].attrib["href"]

    for show in last_sub:
        if re.search(show[0],name_show_tvsub,re.IGNORECASE):
            
            print(name_show_tvsub + "  "+link_show_tvsub)
        
            tree_show = etree.parse(base_tvsub+link_show_tvsub)
            print("trte")
exit(0)
