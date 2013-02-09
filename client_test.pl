#!/usr/bin/perl

use IO::Socket;

$remote = IO::Socket::INET->new(
    Proto => "tcp",
    PeerAddr => "192.168.0.101",
    PeerPort => 2345,
)
    or die "fuck";

$remote->autoflush(1);


$line = <STDIN>;
print $remote $line;

print <$remote>;
close $remote;
