

install:
	cp man/whatsnews.1 /usr/share/man/man1/
	cp whatsnews.py /usr/local/bin/whatsnews
	cp dl_scans.py /usr/local/bin/dl_scans	
	cp dl_torrent.py /usr/local/bin/dl_torrent
	cp dl_sub.py /usr/local/bin/dl_sub

whatsnews:
	cp whatsnews.py /usr/local/bin/whatsnews

dl_scans:
	cp dl_scans.py /usr/local/bin/dl_scans

dl_torrent:
	cp dl_torrent.py /usr/local/bin/dl_torrent

dl_sub:
	cp dl_sub.py /usr/local/bin/dl_sub
