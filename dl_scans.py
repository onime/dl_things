#!/usr/bin/python

#Télécharge les scans de mangastream

from lxml import etree
from urllib.request import urlretrieve
from easylast import infos_last_dl
import socket
import re
import os
import sys
import notify2

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

#On définit le bon path avec la bonne extension
        path_file = path_dirs+"/"+name_page+os.path.splitext(link_img)[1]
        
#On la télécharge 
        urlretrieve(link_img,path_file)
        sys.stdout.write(name_page+" ")
        sys.stdout.flush()
    print("")


list_scan = infos_last_dl("MANGA"," ")
file_rss = "http://feeds.feedburner.com/mstream"
basename = "http://mangastream.com/"
parserXML = etree.XMLParser(ns_clean=True, recover=True,encoding='utf-8')
parserHTML = etree.HTMLParser()

#parse le fichier xml
tree = etree.parse(file_rss,parserXML)
items = tree.xpath('//item')

for i in items:
    childs = i.getchildren()  
    title = childs[0].text

#Parmi les mangas présent on ne prend que ceux présent dans la liste
    for name_scan in list_scan:
        search_scan = re.search("("+name_scan[0]+").*([0-9]{3})",title,re.IGNORECASE)
        if search_scan and int(search_scan.group(2)) > name_scan[1]:
            
            real_name_scan = search_scan.group(1).replace(" ",".")
            num_scan_dl = search_scan.group(2)            
            link_scan = childs[1].text
                
            path_dirs = "/media/Data/test_scan/"+real_name_scan+"/"+num_scan_dl
            path_dirs = path_dirs.replace(" ",".")
                
            if not os.path.exists(path_dirs):
                os.makedirs(path_dirs)

#On récupère les pages du scans                        
            list_link_scan = get_links_scan(link_scan)

            sys.stdout.write(" Downlading "+real_name_scan+" "+num_scan_dl+" "+str(len(list_link_scan))+" pages ")
#On télécharge les images des liens qu'on a récup
            dl_images_of_a_scan(list_link_scan,path_dirs)
            
            notify2.init("Scans Téléchargé")
            notif = notify2.Notification(real_name_scan+" "+num_scan_dl+" "+str(len(list_link_scan))+" pages")
            notif.show()
            
