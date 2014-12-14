#!/usr/bin/python

#Télécharge les torrents a partir d'eztv.it

from lxml import etree
from urllib.request import urlretrieve
import os
import re
import socket
from urllib.request import urlopen
from urllib.parse import unquote
from urllib import error
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

def infos_episode(tr):
    num_epispde = ""
    torrent_links = []
    count = -1 # on commence à -1 parce que les deux premiers td sont un lien vers la description et 
    # un lien vers l'episode

    for td in tr:
        a = td.find("a[@class='epinfo']")
        if a != None:

            # si y en a plusieurs prendre le plus léger
            # pour une version interactive proposer un choix
            m = re.search(regex_infos,a.text,re.IGNORECASE)
            if m != None:
               num_epispde = parse_regex(m)

            
        a = td.find("a[@class='download_"+str(count)+"']")
        if a != None:
            torrent_links.append(a.attrib["href"])

        count += 1
      
        return(name_ep,torrent_links)

for i in items:
    print(i.text)
    for s in list_shows:
        
        if re.search(s["name"],i.text,re.IGNORECASE):
            
            name_dir_show = format_name(s["name"],' ')

            #page de la liste des épisodes de la série
            link_ep_show = i.attrib["href"]
            
            tree_ep_show = parse_url(str(base_url+link_ep_show))

            xml_info_lines = tree_ep_show.xpath("//table[@align='center']/tr[@class='forum_header_border']")

            #on parcour la liste des épisodes
            count = 0
            
            maj = True            
            print(s["name"])
            
            for xml_tr in xml_info_lines:
                (name_ep,torrent_links) = infos_episode(xml_tr)
        
                m = re.search(regex_infos,name_ep,re.IGNORECASE) 
                if m != None:

                    
                    
                    # if the current show is more recent than the last dl
                    res_cmp = cmp_num(num_epispde_cur,s["num"],"SHOW")
                    if  res_cmp > 0 and (re.search("720p",name_ep,re.IGNORECASE)) == None:
                        
                        name_file = name_dir_show+"."+format_SXXEXX(num_epispde_cur)+".torrent"
                        path_torrent = path_dir+name_file
                        
                        print(unquote(torrent_links[count].attrib["href"]))
                        
                        try:
                            urlretrieve(torrent_links[count].attrib["href"],path_torrent)
                        except error.HTTPError:
                            print("fails")
                            print(unquote(links_torrents_2[count].attrib["href"]))
                            urlretrieve(links_torrents_2[count].attrib["href"],path_torrent)

                        if maj == True:
                            maj == False
                            upd_last(name_dir_show,num_cur,"DL")

                        notify2.init("Torrent Téléchargé")
                        notif = notify2.Notification(name_file)
                        notif.show()
                        #if he is not more recent we break and not see the rest    
                    elif res_cmp <= 0:
                        break;
                        
                count+=1
                
