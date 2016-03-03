#!/bin/bash
cd `dirname $0`
outputfilename=iprange-latest
#get newest apnic-delegated file
#wget http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-lates
#extractor ip/subnet from delegated-apnic-latest to $outputfilename
#grep 'apnic|CN|ipv4|' delegated-apnic-latest | cut -f4,5 -d'|' | perl -ne 'my @field = split(/\|/,$_); chomp @fields; chomp $field[1]; print $field[0]."/".(32-log($field[1])/log(2))."\n";' > $outputfilename

grep 'apnic|AF|ipv4|' delegated-apnic-latest | cut -f4,5 -d'|' | perl -ne 'my @field = split(/\|/,$_); chomp @fields; chomp $field[1]; print $field[0]."/".(32-log($field[1])/log(2))."\n";' > $outputfilename
#grep 'apnic|AF|ipv4|' delegated-apnic-latest | cut -f4,5 -d'|' > $outputfilename

#wget ftp://ftp.ripe.net/pub/stats/ripencc/delegated-ripencc-latest
#grep 'ripencc|SY|ipv4|' delegated-ripencc-latest | cut -f4,5 -d'|' > $outputfilename
#grep 'ripencc|SY|ipv4|' delegated-ripencc-latest | cut -f4,5 -d'|' | perl -ne 'my @field = split(/\|/,$_); chomp @fields; chomp $field[1]; print $field[0]."/".(32-log($field[1])/log(2))."\n";' > $outputfilename
