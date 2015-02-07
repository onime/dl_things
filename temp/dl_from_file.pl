#!/bin/perl

use File::Fetch;

open F_TORRENT, "/home/yosholo/.config/utils/torrentslinks" or die "Couldn't read file: $!";

my $season_episode,$dl_season,$dl_ep;
if(exists($ARGV[0]))
{
    $season_episode = $ARGV[0];
    $season_episode =~ m/^S([0-9]+)E([0-9]+)$/;
    
    $dl_season = $1;
    $dl_ep  = $2;
    
    $dl_season =~ s/^0+//;
    $dl_ep  =~ s/^0+//;
}

my %num_links;
my $count = 0;

while (<F_TORRENT>)
{
    if(! /720p/i && ! /1080p/i)
    {
	if(/S([0-9]+)E([0-9]+)/ || m/([0-9]+)x([0-9]+)/ )
	{
	    if ($1 != "" && $2 != "")
	    {
		my $season = $1;
		my $ep = $2;
		
		$season =~ s/^([1-9])$/0\1/;
		$ep =~ s/^([1-9])$/0\1/;

		if($season > $dl_season
		   || ($season == $dl_season && $ep > $dl_ep) || $ARGV[0] eq "")
		   
		{
		    
		    my $key = "S".$season."E".$ep;
		    
		    if(!exists($num_links{$key}))
		    {
			my @links = split('\|',$_);
			@links = @links[4..$#links];
			
			for $link (@links)
			{
			    next if( $link =~ m/piratebaytorrents|torrage|zoink/);
			    
			    $link =~ s/\n//;
			    $link = "http:".$link if ($link !~ /^http:/);

			    print "Downloading $link\n";
			    
			    my $ff = File::Fetch->new(uri => $link);			    
			    my $where = $ff->fetch(to=>"/home/yosholo/.config/utils/torrent_file/") or die next;

			    my $filesize = -s $where;
			    
			    if($filesize > 0)
			    {
				#print "$season$ep #### $filesize #### $where\n";
				$key = "S".$season."E".$ep;
				$num_links{$key}=$link;
				last;
			    }
			}
		    }
		}
	    }
	    else
	    {
		print $_;
	    }
	}
    }
    $count++;
}

close F_TORRENT;

for $key (sort keys %num_links)
{
    print $key." ".$num_links{$key}."\n";
}

sub download_one_link
{
    

}
