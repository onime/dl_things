#!/usr/bin/python

#Télécharge les torrents a partir d'eztv.it

from lxml import etree
from urllib.request import urlretrieve
import os
import re
import socket
from urllib.request import urlopen
import notify2


def get_list_shows():
    port = 2345
    host = "192.168.0.101"
    
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((host,port))
    
    sock.sendall(b"last_seen -d -w\n")
    xml = sock.recv(4096).decode('utf-8')
    
    while re.search('\n',xml) == None:
        xml +=sock.recv(4096).decode('utf-8')

    sock.close()
       
    xml = xml.replace('\n','')
    root_xml = etree.fromstring(xml)
    infos = root_xml.xpath("//info")
    list_show = []

    for i in infos:
        i.attrib["name"] = i.attrib["name"].replace("."," ")
        if i.attrib["type"] == "SHOW":
            list_show.append([i.attrib["name"],i.attrib["num_season"],i.attrib["num_episode"]])

    return list_show
   
path = "/home/yosholo/.config/utils/torrent_file"
if not os.path.exists(path):
    os.makedirs(path)

list_shows = get_list_shows()

file_rss = "http://eztv.it/showlist/"
base_url = "http://eztv.it"

parserHTML =  etree.HTMLParser( recover=True,encoding='utf-8')
tree_rss = etree.parse(file_rss,parserHTML)
items = tree_rss.xpath("//a[@class='thread_link']")

for i in items:
    for s in list_shows:
        if re.search(s[0],i.text,re.IGNORECASE):
            
            #page de la liste des épisodes de la série
            link_show = i.attrib["href"]
            
            tree_show = etree.parse(str(base_url+link_show),parserHTML)
            name_episode = tree_show.xpath("//a[@class='epinfo']")
            link_torrent = tree_show.xpath("//a[@class='download_2']")
            
            #on parcour la liste des épisodes
            count = 0
            for n in name_episode:
                if re.search("(S[0-9]*"+s[1] + "E[0-9]*"+s[2]+")|("+s[1]+"x[0-9]*"+s[2]+")",n.text,re.IGNORECASE):
                    if re.search("720p",n.text,re.IGNORECASE) == None:
                        #On s'arrete quand on a trouvé un nom d'épisode avec le nom
                        #de la dernière saison et épisode qui est téléchargé et qui ne contient pas 720p
                        break
                if re.search("720p",n.text,re.IGNORECASE) == None:
                    
                    #Si on s'est pas arreté on peut le télécharger et afficher une notif
                    name = s[0]+"."+s[1]+"x"+s[2]+".torrent"
                    path += name
                    
                    urlretrieve(link_torrent[count].attrib["href"],path)

                    notify2.init("Torrent Téléchargé")
                    notif = notify2.Notification(name)
                    notif.show()

                count+=1
          
