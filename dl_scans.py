#!/usr/bin/python

from operator import attrgetter
from lxml import etree
from urllib.request import urlretrieve,urlopen,Request
from easylast import *
import re
import os
import sys
import notify2
import subprocess

def ms_get_links_pages(link_scan):

#On parse une page d'un scan pour récupérer les liens de toutes les pages du scan
    tree_page_princ = parse_url(link_scan)
    list_url = tree_page_princ.xpath("//div[@class='btn-group'][2]/ul[@class='dropdown-menu']/li/a/@href")
    
    return list_url
   
def ms_dl_images(list_url,path_dirs):

    for u in list_url:
        
        #On parse chaque lien pour récupérer l'adresse de l'image
        tree_page_img = parse_url(u)
        link_img = tree_page_img.xpath("//img[@id='manga-page']/@src")[0]

        #On définit le bon path avec la bonne extension
        name_page = link_img.split('/')[-1]

        path_file = path_dirs+"/"+ name_page
        
        #On la télécharge 
        content_img = urlopen(Request(link_img,headers={'User-Agent': 'Mozilla/5.0'})).read().decode("iso-8859-1")
        file_img = open(path_file,"w",encoding = "iso-8859-1")
        file_img.write(content_img)
        file_img.close()
               
def om_dl_page(name,num,page):
    
    base_url = "http://www.onemanga.me/"+name_one_manga[name]+"/"+str(num)+"/"+str(page)
    tree = parse_url(base_url,"html")
    item_img = tree.xpath("//img[@class='manga-page']/@src")
    url_img = item_img[0]

    path_img = "/media/Data/Scans/"+format_name(name,' ')+"/"+str(num)
    
    if not os.path.exists(path_img):
        os.makedirs(path_img)
    try :
        urlretrieve(url_img,path_img+"/"+str(format_number_zero({"page":int(page)})["page"]) + "." + url_img.split(".")[-1])
    except OSError as Err:
        print("Failed to retrieve",url_img,name,num,page) 

def om_dl_scan(name,num):

    #the name given for the directory's name
    base_url = "http://www.onemanga.me/"+name_one_manga[name]+"/"+str(num)
    tree = parse_url(base_url,"html")

    #there is two select one at the top of the image and one at the bottom but i need only one
    items_nb_page = tree.xpath("//li/select[@class='cbo_wpm_pag']")[0]
    nb_pages = len(items_nb_page)
    
    print("Download ",format_name(name," "),num,nb_pages)
    for n in items_nb_page:
        om_dl_page(name,num,int(n.text))

def find_missing_chapters(num_chaps):

    missing_chaps = []
    count=1

    for n in num_chaps:
        if count != n:
            missing_chaps += (list(range(count,n)))
            count = n
        count+=1
    
    return missing_chaps

def dl_missing_scans(last_scan_dl):
                               
    for scan in list_scan:
            
        str_num_chaps = os.listdir("/media/Data/Scans/"+format_name(scan['name']," "))
        num_chaps = [int(n) for n in str_num_chaps if n.isdigit()]
        num_chaps = sorted(num_chaps)

        missing_chaps = find_missing_chapters(num_chaps)
        for chap in  missing_chaps:           
            om_dl_scan(scan['name'],chap)

def get_list_new_chap():
    
    file_rss = "http://feeds.feedburner.com/mstream"
    #parse the xml rss
    tree = parse_url(file_rss,"xml")
    names = tree.xpath('//item/title/text()')
    links = tree.xpath('//item/link/text()')

    list_scan_out = []

    #go through the names and get the links and num of the last scans
    for (i,name) in enumerate(names):
        for info_scan in list_scan:
            if re.search("("+info_scan["name"]+")",name,re.IGNORECASE):
                
                info_chap_curr = {}
                info_chap_curr["num"] = name.split(" ")[-1]
                info_chap_curr["name"] = info_scan["name"]
                info_chap_curr["link"] = links[i]

                #We keep the most recent
                if info_chap_curr["num"].isdigit():
                    if int(info_chap_curr["num"]) > info_scan["num"]["chap"]:
                        list_scan_out.append(info_chap_curr)
                else:
                    if not os.path.exists(path_dirs+format_name(info_scan["name"]," ")+"/"+info_chap_curr["num"]):
                        list_scan_out.append(info_chap_curr)

    #sort the list by the name then by the num 
    return sorted(list_scan_out,key=lambda k: (k["name"],k["num"]))

def print_new_chap(list_chap):

    for chap in list_chap:
        print(format_name(chap["name"]," "),chap["num"],chap["link"])

list_scan = infos_last("MANGA"," ","DL")
name_one_manga={"naruto":"naruto_manga","bleach":"bleach","claymore":"claymore","fairy tail":"fairy-tail","one piece":"one-piece"}

if len(sys.argv) > 1:
    if sys.argv[1] == "--list-new":    
        print_new_chap(get_list_new_chap())
    exit(0)

basename = "http://mangastream.com/"
path_dirs = "/media/Data/Scans/"
    
list_scan_out = get_list_new_chap()

#loop in the latest scan and dl it
for item in list_scan_out:
        
    name_dir_scan = format_name(item["name"],' ')
    path_dirs_scan = path_dirs+name_dir_scan+"/"+item["num"]+"/"

    #get a list of the pages
    list_link_scan = ms_get_links_pages(item["link"])
        
    if len(list_link_scan) > 0:
            
        if not os.path.exists(path_dirs_scan):
            os.makedirs(path_dirs_scan)

        print(" Downlading "+name_dir_scan+" "+item["num"]+" "+str(len(list_link_scan))+" pages ")

        ms_dl_images(list_link_scan,path_dirs_scan)
        
        notify2.init("Scans Téléchargé")
        notif = notify2.Notification(name_dir_scan+" "+item["num"]+" "+str(len(list_link_scan))+" pages")
        notif.show()
        
        if item["num"].isdigit():
            upd_last(name_dir_scan,{"chap":item["num"]},"DL")

dl_missing_scans(list_scan)
