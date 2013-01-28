#!/usr/bin/python

#Télécharge les scans de mangastream

from lxml import etree
from urllib.request import urlretrieve
import socket
import re
import os
import sys
import notify2

def get_list_scans():
    port = 2345
    host = "192.168.0.101"
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((host,port))
    
    sock.sendall(b"last_seen -d -w\n")
    xml = sock.recv(4096).decode('utf-8')
    
    while re.search('\n',xml) == None:
        xml +=sock.recv(4096).decode('utf-8')

    sock.close()
    print(xml)
    xml = xml.replace('\n','')
    root_xml = etree.fromstring(xml)
    infos = root_xml.xpath("//info")
    list_show = []

    for i in infos:
        print(i.attrib["name"])
        i.attrib["name"] = i.attrib["name"].replace("."," ")
        if i.attrib["type"] == "MANGA":
            print(i.attrib["type"])
            list_show.append([i.attrib["name"],i.attrib["num_chap"]])

    return list_show

def get_links_scan(link_scan):

#On parse une page d'un scan pour récupérer les liens de toutes les pages du scan
    tree_page_princ = etree.parse(link_scan,parserHTML)
    id_controls = tree_page_princ.xpath("//div[@id='controls']")
    
    childs= id_controls[0].getchildren()
    
    list_url = []
#On évite les deux premiers liens et les deux derniers car ce sont les liens prev next une balise div et une strong RAF
    for i in range(2,len(childs)-2):
        list_url.append(basename+childs[i].attrib["href"])
    
    return list_url

def hook_retrieve(count_of_block,block_zise,total_size):
#Pour la barre de progression
    
    if count_of_block > 0:
        nb_bloc_total = int(total_size / block_zise)
        nb_bloc_to_progress = int(nb_bloc_total / 50)
        nb_bloc_to_draw = 1
        nb_cara = 30

        if nb_bloc_to_progress  <= 0:
            nb_bloc_to_draw = int(nb_cara / nb_bloc_total)+1
            nb_bloc_to_progress = 1

        if count_of_block % nb_bloc_to_progress == 0:
            if count_of_block < nb_cara / nb_bloc_to_draw:
                sys.stdout.write("#"*nb_bloc_to_draw)
                sys.stdout.flush()
        if count_of_block == nb_bloc_total:
                print("#"*int(1+(nb_cara / nb_bloc_total)))
    
    

def dl_images_of_a_scan(list_url,path_dirs):

    count = 0
    for u in list_url:
#On parse chaque lien pour récupérer l'adresse de l'image
        tree_page_img = etree.parse(u,parserHTML)
        img = tree_page_img.xpath("//img[@id='p']")

        count+=1
        link_img = img[0].attrib["src"]
        
        name_page = str(count)
        if count < 10:
            name_page = "0"+str(count)

        path_file = path_dirs+"/"+name_page+os.path.splitext(link_img)[1]
        
        sys.stdout.write("\t\t Downlading page "+ os.path.basename(link_img)+" ")
        sys.stdout.flush()

#On la télécharge 
        urlretrieve(link_img,path_file,hook_retrieve)

list = get_list_scans()
print(list)
exit(0)
file_rss = "http://feeds.feedburner.com/mstream"
basename = "http://mangastream.com/"
parserXML = etree.XMLParser(ns_clean=True, recover=True,encoding='utf-8')
parserHTML = etree.HTMLParser()

list_scan = ["Naruto","One Piece","Bleach","Fairy Tail","Claymore"]

#parse le fichier xml
tree = etree.parse(file_rss,parserXML)
items = tree.xpath('//item')

for i in items:
    childs = i.getchildren()  
    title = childs[0].text

#Parmi les mangas présent on ne prend que ceux présent dans la liste
    for name_scan in list_scan:
        search_scan = re.search(name_scan+".*([0-9]{3})",title,re.IGNORECASE)
        if search_scan:
            num_scan = search_scan.group(1)
            link_scan = childs[1].text
            
            path_dirs = name_scan+" "+num_scan
            path_dirs = path_dirs.replace(" ","-")

            if not os.path.exists(path_dirs):
                  print("Creating "+path_dirs)                         
                  os.makedirs(path_dirs)

#On récupère les pages du scans            
            print("\tGetting urls of "+name_scan)
            list_link_scan = get_links_scan(link_scan)
            print("\tPrepare Download "+name_scan+" Number pages : "+str(len(childs)-4))

#On télécharge les images des liens qu'on a récup
            dl_images_of_a_scan(list_link_scan,path_dirs)
            
            notify2.init("Scans Téléchargé")
            notif = notify2.Notification(name_scan)
            notif.show()
            
