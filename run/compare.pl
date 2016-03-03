#!/usr/bin/perl
use strict;

my @ipaddr;
my %net;
open(FF,"$ARGV[0]") or die $!;
my $count = 0;
while(<FF>){
  s/[\015\012]//;
  $ipaddr[$count] = $_;
  $count = $count + 1;
}
close(FF);

open(FF,"$ARGV[1]") or die $!;
while(<FF>){
  s/[\015\012]//;
  my ($t1,$t2) = split(/\//,$_);
  $net{$t1} = $t2;
}
close(FF);
my $count1 = 0;
foreach my $net1 (keys %net){
  my $netmask = $net{$net1};
  my $net_bits1 = &bitsIP($net1,$netmask);
  foreach my $ip (@ipaddr){
     my $net_bits2 = &bitsIP($ip,$netmask);
     if($net_bits2 eq $net_bits1){
        print $ip."\n";
        $count1 = $count1 + 1;
        next;
     }
  }
}
print "total ip count:".$count."\n";
print "find ip count:".$count1."\n";
#--取得bits of net address
sub bitsIP(){
  my ($ip,$netmask)= @_;
  my @ip =split(/\./,$ip);
  my $b = unpack("B32", pack("C4",$ip[0],$ip[1],$ip[2],$ip[3]));
  my $substr= substr($b,0,$netmask);
  return $substr;
}