#!/usr/bin/python

#Télécharge les scans de mangastream

from lxml import etree
from urllib.request import urlretrieve
from easylast import *
import re
import os
import sys
import notify2
import subprocess

def get_links_scan(link_scan):

#On parse une page d'un scan pour récupérer les liens de toutes les pages du scan
    tree_page_princ = parse_url(link_scan)
    id_controls = tree_page_princ.xpath("//div[@id='controls']")
    
    childs= id_controls[0].getchildren()
    
    list_url = []
#On évite les deux premiers liens et les deux derniers car ce sont les liens prev next une balise div et une strong RAF
    for i in range(2,len(childs)-2):
        list_url.append(basename+childs[i].attrib["href"])
    
    return list_url
   
def dl_images_of_a_scan(list_url,path_dirs):

    count = 1
    
    for u in list_url:

#On parse chaque lien pour récupérer l'adresse de l'image
        tree_page_img = parse_url(u)
        img = tree_page_img.xpath("//img[@id='p']")

        link_img = img[0].attrib["src"]
        
        #On définit le bon path avec la bonne extension    
        name_page = str(format_number_zero({"page":int(count)})["page"]) + os.path.splitext(link_img)[1]
        
        path_file = path_dirs+"/"+ name_page
                
        #On la télécharge 
        urlretrieve(link_img,path_file)
        count+=1

def dl_page_one_manga(name,num,page):
    
    base_url = "http://www.onemanga.me/"+name_one_manga[name]+"/"+str(num)+"/"+str(page)
    tree = parse_url(base_url,"html")
    item_img = tree.xpath("//img[@class='manga-page']")
    url_img = item_img[0].attrib["src"]
    path_img = "/media/Data/Scans/"+format_name(name,' ')+"/"+str(num)
    
    if not os.path.exists(path_img):
        os.makedirs(path_img)
    try :
        urlretrieve(url_img,path_img+"/"+str(format_number_zero({"page":int(page)})["page"]))
    except OSError as Err:
        fail_load.append([name,num,page,url_img])

def dl_one_manga(name,num):
    #the name given for the directory's name
    base_url = "http://www.onemanga.me/"+name_one_manga[name]+"/"+str(num)
    tree = parse_url(base_url,"html")

    try:
        items_nb_page = tree.xpath("//li/select[@class='cbo_wpm_pag']")[0]
        print("\t\tDownload",name,num)
        for n in items_nb_page:
            dl_page_one_manga(name,num,int(n.text))
    except:
        print("\t\t",name,num,"no available")

    #there is two select one at the top of the image and one at the bottom but i need only one
    
   
        
name_one_manga={"naruto":"naruto_manga","bleach":"bleach","claymore":"claymore","fairy tail":"Fairy_Tail","one piece":"One_Piece"}
fail_load = []

list_scan = infos_last("MANGA"," ","DL")

if len(sys.argv) > 1:
    if(sys.argv[1] == "--missing"):
        
        for scan in list_scan:
            
            str_num_chaps = os.listdir("/media/Data/Scans/"+format_name(scan['name']," "))
            num_chaps = [int(n) for n in str_num_chaps if n.isdigit()]
            num_chaps = sorted(num_chaps)
            
            count = 1
            print(name_one_manga[scan['name']])

            for n in num_chaps:
                if count != n:
                    print("\tDownload",count,n-1)
                    for i in range(count,n):
                        dl_one_manga(scan['name'],i)
                        
                    count = n
                count+=1

        print(fail_load)
else:

    file_rss = "http://feeds.feedburner.com/mstream"
    basename = "http://mangastream.com/"
    
    path_dirs = "/media/Data/Scans/"
    
    #parse le fichier xml
    tree = parse_url(file_rss,"xml")
    items = tree.xpath('//item')
    hash_scan = {} 

    for i in items:
        childs = i.getchildren()  
        title = childs[0].text

    #Parmi les mangas présent on ne prend que ceux présent dans la liste
    for info_scan in list_scan:
        if re.search("("+info_scan["name"]+")",title,re.IGNORECASE):
            num_scan_dl = parse_regex(re.search(regex_infos,title,re.IGNORECASE))["chap"]
        
            if int(num_scan_dl) > int(info_scan["num"]["chap"]):
                
                name_dir_scan = format_name(info_scan["name"],' ')
                link_scan = childs[1].text
                
                path_dirs_scan = path_dirs+name_dir_scan+"/"+num_scan_dl+"/"

                if name_dir_scan not in hash_scan.keys():
                    hash_scan[name_dir_scan] = []

                hash_scan[name_dir_scan].append(num_scan_dl)
                            
                if not os.path.exists(path_dirs_scan):
                    os.makedirs(path_dirs_scan)

#On récupère les pages du scans                        
                list_link_scan = get_links_scan(link_scan)

                print(" Downlading "+name_dir_scan+" "+num_scan_dl+" "+str(len(list_link_scan))+" pages ")
#On télécharge les images des liens qu'on a récup
                dl_images_of_a_scan(list_link_scan,path_dirs_scan)
                
                notify2.init("Scans Téléchargé")
                notif = notify2.Notification(name_dir_scan+" "+num_scan_dl+" "+str(len(list_link_scan))+" pages")
                notif.show()
                
    for k in hash_scan:
        hash_scan[k] = sorted(hash_scan[k])
        print("maj")
        for num in hash_scan[k]:
            upd_last(k,{"chap":num},"DL")

