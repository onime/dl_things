

install:
	cp man/client_last.1 /usr/share/man/man1/
	cp client_last.py /usr/local/bin/client_last
	cp dl_scans.py /usr/local/bin/dl_scans	
	cp dl_torrent.py /usr/local/bin/dl_torrent
	cp dl_sub.py /usr/local/bin/dl_sub

client_last:
	cp client_last.py /usr/local/bin/client_last

dl_scans:
	cp dl_scans.py /usr/local/bin/dl_scans

dl_torrent:
	cp dl_torrent.py /usr/local/bin/dl_torrent

dl_sub:
	cp dl_sub.py /usr/local/bin/dl_sub
