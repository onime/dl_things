#!/usr/bin/python

#Télécharge les torrents a partir d'eztv.it

from lxml import etree
from urllib.request import urlretrieve
import os
import re
import socket
from urllib.request import urlopen
import notify2
from easylast import *

path_dir = "/home/yosholo/.config/utils/torrent_file/"
if not os.path.exists(path_dir):
    os.makedirs(path_dir)

list_shows = infos_last_dl("SHOW"," ")

file_rss = "http://eztv.it/showlist/"
base_url = "http://eztv.it"

parserHTML =  etree.HTMLParser( recover=True,encoding='utf-8')
tree_rss = etree.parse(file_rss,parserHTML)
items = tree_rss.xpath("//a[@class='thread_link']")

for i in items:
    for s in list_shows:
        if re.search(s[0],i.text,re.IGNORECASE):
            
            name_dir_show = format_name(s[0],' ')

            #page de la liste des épisodes de la série
            link_ep_show = i.attrib["href"]
            
            tree_ep_show = etree.parse(str(base_url+link_ep_show),parserHTML)
            names_episodes = tree_ep_show.xpath("//a[@class='epinfo']")
            links_torrents = tree_ep_show.xpath("//a[@class='download_2']")
            
            #on parcour la liste des épisodes
            count = 0

            for n in names_episodes:

                m = re.search(re_nseason_nep,n.text,re.IGNORECASE) 
                if m != None:
                    (num_season_cur,num_episode_cur) = parse_regex(m)

                    if int(num_episode_cur) > s[3] and re.search("720p",n.text,re.IGNORECASE) == None:
                        
                        name_file = name_dir_show+".S"+num_season_cur+"E"+num_episode_cur+".torrent"
                        path_torrent = path_dir+name_file

                        urlretrieve(links_torrents[count].attrib["href"],path_torrent)
                        notify2.init("Torrent Téléchargé")
                        notif = notify2.Notification(name_file)
                        notif.show()
                        
                    elif int(num_episode_cur) <= s[3]:
                        break;
           
                count+=1
          
