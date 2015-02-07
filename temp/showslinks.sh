#!/bin/sh

IFS='
'
#WWW_EZTV="https://eztv.it/showlist/"
DIR="/home/yosholo/.config/utils"
WWW_EZTV="https://eztv-proxy.net"
EZTV_TORRENT="$DIR/eztv_torrents_links"
EZTV_SHOWLIST="$DIR/eztv_show.html"
LOGHTTP="$DIR/loghttp"
LOGSHOWS="$DIR/log_shows"
SHOWSLINKS="$DIR/showslinks"
SEP="|"

HTML_TORRENTS="$DIR/html_torrents_links"
TORRENTSLINKS_TMP="$DIR/torrentslinks_tmp"
TORRENTSLINKS="$DIR/torrentslinks"
BEGIN="#"

show=$(echo $1 | tr '.' ' ')

# showslinks.sh [--download-shows] shows-name

# Download the eztv showlist
if [ "$1" = "--download-shows" ]
then

    #fetch html show list
    wget -S "$WWW_EZTV/showlist/" -O $EZTV_SHOWLIST -o $LOGHTTP

    code_http=$(cat $LOGHTTP| grep "HTTP/1.1" | cut -d' ' -f4)

    if [ $code_http -ne 200 ]
    then
	echo "$WWW_EZTV : code d'erreur $code_http"
	exit
    fi

    #remove html tag
    cat $EZTV_SHOWLIST | grep "thread_link" | grep -v "<img" | sed  "s/<td class=\"forum_thread_post\"><a href=\"/$SEP/" | sed "s/\" class=\"thread_link\">/$SEP/" | sed "s/<\/a><\/td>/$SEP/" | sed 's/^\t*//' | sed 's/\t*$//'  > $SHOWSLINKS

    rm $EZTV_SHOWLIST
    rm $LOGHTTP

    nb_shows=$(cat $SHOWSLINKS | grep "^|.*|$" | wc -l)


    echo "$nb_shows shows"
    show=$2
fi

if [ "$1" = "--add" ]
then
    show=$2
fi

if [ "$2" = "--add" ]
then
    show=$3
fi

# Search the argument in the showlist
if [ -n "$2" ] || [ -n "$1" ] || [ -n "$3" ]
then

    res=$(cat $SHOWSLINKS | grep -i "$show" |cut -d'|' -f3 | nl -w 1)
    nb_res=$(cat $SHOWSLINKS | grep -i "$show" | wc -l)

    ep_list=$(cat $SHOWSLINKS | grep -i "$show" |  cut -d'|' -f2)
    eztv_name_show=$(cat $SHOWSLINKS | grep -i "$show" |  cut -d'|' -f3 | tr ' ' '.')
    
    
    if [ $nb_res -gt 1 ]
    then
	echo "There is multiple $show in the list choose the one you want:"
	for i in $res
	do
	    echo $i
	done
	echo -n "Number :"
	read kb_number

	if [ $kb_number -gt $nb_res ] || [ $kb_number -lt 1 ]
	then
	    echo "$kb_number : wrong number"
	    exit 2
	else
	    ep_list=$(cat $SHOWSLINKS | grep -i "$show" |  cut -d'|' -f2 | head -$kb_number | tail -1)
	    eztv_name_show=$(cat $SHOWSLINKS | grep -i "$show" |  cut -d'|' -f3 | tr ' ' '.' | head -$kb_number | tail -1)
	fi
	
    fi
    
    if [ -z $ep_list ]
    then
	echo "$show est introuvable"
	exit
    fi

    show_with_dot=$(echo $show | tr ' ' '.')
    last_dl=$(whatsnews --DL -p | grep -i $show_with_dot | cut -d' ' -f3)
    #real_name=$(whatsnews --DL -p | grep -i $show_with_dot | cut -d' ' -f1)

    if [ ! "$last_dl" ]
    then
	if [ "$1" = "--add" ] || [ "$2" = "--add" ]
	then
	    echo "Adding $eztv_name_show"
	else
	    echo "'$show_with_dot' is not in the database"
	    whatsnews --DL -p
	    exit 0
	fi
    fi

    # Once the show is found it download the episode list

    #xmllint -html --xpath "//tr[@class='forum_header_border']/td[@class='forum_thread_post']/a[@class='epinfo']" torrents_links.html 2> /dev/null | sed 's#</a>#\n#g' | sed 's#<a href.*class="epinfo">##g'
    echo "Fetching '$eztv_name_show' at '$WWW_EZTV$ep_list'"
    curl "$WWW_EZTV/$ep_list" > $EZTV_TORRENT 2> /dev/null

    cat $EZTV_TORRENT | grep -A 3 "<td class=\"forum_thread_post\">" | grep -v "^--" | grep -v "<td class=\"forum_thread_post\">" | sed 's/^\t*//' | grep -v "^</td>$" > $HTML_TORRENTS

    #remove html tag for episode
    cat $HTML_TORRENTS | sed "s/<a href.*title.*alt.*class=\"epinfo\">/$BEGIN/" | sed "s/<\/a>$/|/" > $TORRENTSLINKS_TMP

    #remove html tag for torrents links 
    cat $TORRENTSLINKS_TMP | sed -r 's/(class|align|target|title|onclick)="[^"]*"//g' | sed "s/ *><\/a><a href=\"/$SEP/g" | sed 's/.*<td.*href=\"//' | sed 's/"//g' | sed 's/ *>.*$//' | sed ":a;N;$!ba;s/$SEP\n/$SEP/g" | sed ':a;N;$!ba;s/|\n/|/g' > $TORRENTSLINKS

    rm $EZTV_TORRENT $HTML_TORRENTS $TORRENTSLINKS_TMP

    echo "Downloading $eztv_name_show after $last_dl"

    # Download the torrents file
    dl_from_file $last_dl | tee -a "$DIR/last_$eztv_name_show"
    last_dl=$(tail -1 "$DIR/last_$eztv_name_show" | cut -d' ' -f1)

    if [ "$1" = "--add" ] || [ "$2" = "--add" ]
    then
	whatsnews --DL --add -t $eztv_name_show -n $last_dl
    else
	whatsnews --DL --upd -t  $eztv_name_show -n $last_dl
    fi
    
    
    if [ $? -eq 0 ]
    then
	echo "$eztv_name_show updated to $last_dl"
    else
	echo "$eztv_name_show not updated"
    fi
    
    rm "$DIR/last_$eztv_name_show"
fi

