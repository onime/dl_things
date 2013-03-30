#!/usr/bin/python

#Télécharge les torrents a partir d'eztv.it

from lxml import etree
from urllib.request import urlretrieve
import os
import re
import socket
from urllib.request import urlopen
from urllib.parse import unquote
import notify2
from easylast import *
import subprocess

path_dir = "/home/yosholo/.config/utils/torrent_file/"
if not os.path.exists(path_dir):
    os.makedirs(path_dir)

list_shows = infos_last("SHOW"," ","DL")

file_rss = "http://eztv.it/showlist/"
base_url = "http://eztv.it"
tree_rss = parse_url(file_rss)
    
items = tree_rss.xpath("//a[@class='thread_link']")


for i in items:

    for s in list_shows:
      
        if re.search(s["name"],i.text,re.IGNORECASE):
            
            name_dir_show = format_name(s["name"],' ')

            #page de la liste des épisodes de la série
            link_ep_show = i.attrib["href"]
            
            tree_ep_show = parse_url(str(base_url+link_ep_show))
            names_episodes = tree_ep_show.xpath("//a[@class='epinfo']")
            links_torrents = tree_ep_show.xpath("//a[@class='download_1']")
            
            #on parcour la liste des épisodes
            count = 0
           
            maj = True            
          
            for n in names_episodes:

                m = re.search(regex_infos,n.text,re.IGNORECASE) 
                if m != None:

                    (num_season_cur,num_episode_cur) = parse_regex(m)
                    hash_num_cur = {"season":int(num_season_cur),"episode":int(num_episode_cur)}
                    
                    # if the current show is more recent than the last dl
                    res_cmp = cmp_num(hash_num_cur,s["num"],"SHOW") 
                    if  res_cmp > 1 and (re.search("720p",n.text,re.IGNORECASE)) == None:
                
                        name_file = name_dir_show+".S"+num_season_cur+"E"+num_episode_cur+".torrent"
                        path_torrent = path_dir+name_file
                        
                        print(unquote(links_torrents[count].attrib["href"]))
                        urlretrieve(links_torrents[count].attrib["href"],path_torrent)
                        
                        if maj == True:
                            maj == False
                            upd_last(name_dir_show,{"season":num_seasoncur,"episode":num_episode_cur},"DL")

                        notify2.init("Torrent Téléchargé")
                        notif = notify2.Notification(name_file)
                        notif.show()
                    #if he is not more recent we break and not see the rest    
                    elif res_cmp <= 0:
                        break;
           
                count+=1
          
