#!/bin/sh

EZTV="https://eztv.it"
EZTV_TORRENT="eztv_torrents_links"
HTML_TORRENTS="html_torrents_links"
TORRENTSLINKS_TMP="torrentslinks_tmp"
TORRENTSLINKS="torrentslinks"
SEP="|"
BEGIN="#"

read show

ep_list=$(cat showslinks | grep -i "$show" |  cut -d'|' -f2)

# si n'existe pas stop
echo $EZTV/$ep_list
curl "$EZTV/$ep_list" > $EZTV_TORRENT

#search line with torrents link and numero of each episode with version
cat $EZTV_TORRENT | grep -A 3 "<td class=\"forum_thread_post\">" | grep -v "^--" | grep -v "<td class=\"forum_thread_post\">" | sed 's/^\t*//' | grep -v "^</td>$" > $HTML_TORRENTS

#remove html tag for episode
cat $HTML_TORRENTS | sed "s/<a href.*title.*alt.*class=\"epinfo\">/$BEGIN/" | sed "s/<\/a>$/|/" > $TORRENTSLINKS_TMP

#remove html tag for torrents links 
cat $TORRENTSLINKS_TMP | sed -r 's/(class|align|target|title|onclick)="[^"]*"//g' | sed "s/ *><\/a><a href=\"/$SEP/g" | sed 's/.*<td.*href=\"//' | sed 's/"//g' | sed 's/ *>.*$//' | sed ":a;N;$!ba;s/$SEP\n/$SEP/g" |  sed ':a;N;$!ba;s/|\n/|/g' > $TORRENTSLINKS

rm $EZTV_TORRENT $HTML_TORRENTS $TORRENTSLINKS_TMP

#; (semicolon is just a command separator within sed)
#sed (The command that calls the sed program)
#:a (a marker which we use to iterate over and over)
#N (Appends the next line to the pattern space)
#$!ba (repeats the N command for all lines but the last line)
#s/\n/\t/g (replaces all occurences of the newline character with tab)
