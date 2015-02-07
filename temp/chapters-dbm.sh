#!/bin/sh

IFS='
'

wget_verbose=-nv

if [ $1 = -nv ]
then
	wget_verbose=-q
	echo_verbose=-n
fi

i=1

dbmbase="http://www.dragonball-multiverse.com/fr"

#download chapters links
while read line
do
	echo $line > chapter_$i
	i=$(( i + 1 ))

done < dbm-chapters 

for i in chapter_*
do
	xmllint -html --xpath "//a/@href" $i | sed "s/href=//g" | sed 's/"//g' | sed "s/ /\n/g" | sed 1d > link_chapter_$i
	echo "" >> link_chapter_$i	
	
	if [ ! -d dbm_$i ]
	then
		mkdir dbm_$i
	fi
	
	echo $echo_verbose "Downloading $i "

	while read line_link
	do
		if [ $1 != -nv ]
		then
			echo -n Fetching info from page link : $line_link ...
		fi
		img_link=$(curl -s $dbmbase/$line_link | xmllint -html --xpath "//div[@class='img']/img/@src"  - | sed -r 's#(src=|"| |/fr/)*##g')
		
		if [ $1 != -nv ]
		then
			echo Done
		fi
	
		if [ $1 != -nv ]
		then 
			echo Downloading img : $(basename $img_link)
		fi

		wget $wget_verbose -O dbm_$i/$(basename $img_link) $dbmbase/$img_link 		
		
		if [ $1 = -nv ]
		then
			echo -n "#"
		fi

	done < link_chapter_$i
	echo ""
	rm $i link_chapter_$i
done

