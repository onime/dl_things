#!/usr/bin/python

#Télécharge les torrents a partir d'eztv.it

from lxml import etree
import os
import re
import socket
from urllib.request import urlopen


port = 2345
host = "192.168.0.101"

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((host,port))

sock.sendall(b"last_seen -w\n")
chunk = sock.recv(1024)
print(chunk.decode("utf-8"))

sock.close()

exit(0)

list_shows = ["American Dad","How i Met your Mother","Two and a half men","Big Bang Theory"]
file_rss = "http://eztv.it/showlist/"
parserHTML =  etree.HTMLParser( recover=True,encoding='utf-8')
tree_rss = etree.parse(file_rss,parserHTML)
base_url = "http://eztv.it"
items = tree_rss.xpath("//a[@class='thread_link']")
#print(etree.tostring(tree_rss,pretty_print=True))


for i in items:
    for s in list_shows:
        if re.search(s,i.text,re.IGNORECASE):
            link = i.attrib["href"]
            print(s+ " " +link)

            tree_show = etree.parse(str(base_url+link),parserHTML)
            name_episode = tree_show.xpath("//a[@class='epinfo']")
            link_torrent = tree_show.xpath("//a[@class='download_1']")
#            for n in name_episode:
            print(name_episode[0].text+ " "+link_torrent[0].attrib["href"])
            exit(0)