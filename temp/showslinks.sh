#!/bin/sh

EZTV="eztv_show.html"
AIRING="airing_show.html"
SHOWSLINKS="showslinks"
SEP="|"

#fetch html show list
curl "https://eztv.it/showlist/" | grep "thread_link" | grep -v "<img" > $EZTV

#parse line we don't need
#cat eztv_show.html | grep -B 1 -i airing | grep -vi airing | grep -v "^--" | sed 1d > $AIRING

#remove html tag
cat $EZTV | sed  "s/<td class=\"forum_thread_post\"><a href=\"/$SEP/" | sed "s/\" class=\"thread_link\">/$SEP/" | sed "s/<\/a><\/td>/$SEP/" | sed 's/^\t*//' | sed 's/\t*$//'  > $SHOWSLINKS

rm $EZTV
#rm $AIRING

#gerer les erreurs de changement de version du site

