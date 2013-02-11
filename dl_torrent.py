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

def try_parse():
    try:
        tree_rss = etree.parse(file_rss,parserHTML)
        return tree_rss
    except:
        return False

path_dir = "/home/yosholo/.config/utils/torrent_file/"
if not os.path.exists(path_dir):
    os.makedirs(path_dir)

list_shows = infos_last("SHOW"," ","DL")

file_rss = "http://eztv.it/showlist/"
base_url = "http://eztv.it"

parserHTML =  etree.HTMLParser( recover=True,encoding='utf-8')

tree_rss = try_parse()

if tree_rss == False:
    exit(0)

print("Parsed")
    
items = tree_rss.xpath("//a[@class='thread_link']")

for i in items:

    for s in list_shows:
      
        if re.search(s[0],i.text,re.IGNORECASE):
            
            name_dir_show = format_name(s[0],' ')

            #page de la liste des épisodes de la série
            link_ep_show = i.attrib["href"]
            
            tree_ep_show = etree.parse(str(base_url+link_ep_show),parserHTML)
            names_episodes = tree_ep_show.xpath("//a[@class='epinfo']")
            links_torrents = tree_ep_show.xpath("//a[@class='download_1']")
            
            #on parcour la liste des épisodes
            count = 0
           
            maj = True            
          
            for n in names_episodes:

                m = re.search(regex_infos,n.text,re.IGNORECASE) 
                if m != None:

                    (num_season_cur,num_episode_cur) = parse_regex(m)
                    
                    if  (int(num_season_cur) > int(s[1]) or
                    (int(num_season_cur) == int(s[1]) and int(num_episode_cur) > int(s[2])) and
                    (re.search("720p",n.text,re.IGNORECASE)) == None):
                        
                        name_file = name_dir_show+".S"+num_season_cur+"E"+num_episode_cur+".torrent"
                        path_torrent = path_dir+name_file
                        
                        print(unquote(links_torrents[count].attrib["href"]))
                        urlretrieve(links_torrents[count].attrib["href"],"here.torrent")
                        
 #                       if maj == True:
  #                          maj == False
   #                         subprocess.getoutput("/usr/local/bin/client_last -u "+name_dir_show+" -n "+num_season_cur+"x"+num_episode_cur)
                        notify2.init("Torrent Téléchargé")
                        notif = notify2.Notification(name_file)
                        notif.show()
                        
                    elif int(num_season_cur) < int(s[1]) or (int(num_season_cur) == int(s[1]) and int(num_episode_cur)) <= int(s[2]):
                        break;
           
                count+=1
          
