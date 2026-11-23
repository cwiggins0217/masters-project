#!/usr/bin/env perl
use strict;
use warnings;
use JSON::PP;
use Digest::SHA qw(sha256_hex);
my $path = shift or die "Usage: $0 comparison.json > assessment.xml\n";
open my $fh, '<:raw', $path or die "$path: $!";
local $/; my $raw=<$fh>; my $d=decode_json($raw);
die "Unsupported schema\n" unless ($d->{schema_version}//'') eq '1.0';
sub esc { my $s=shift // ''; $s =~ s/&/&amp;/g; $s =~ s/</&lt;/g; $s =~ s/>/&gt;/g; $s =~ s/"/&quot;/g; $s =~ s/'/&apos;/g; return $s; }
sub el { my ($tag,$value)=@_; return '<'.$tag.'>'.esc($value).'</'.$tag.'>'; }
print '<?xml version="1.0" encoding="UTF-8"?>',"\n<assessment schema=\"1.0\" json-sha256=\"",sha256_hex($raw),"\">\n";
for my $phase (qw(pre post followup)) {
    my $p=$d->{phases}{$phase} or next;
    print '<phase name="',$phase,'">';
    for my $key (qw(test_result_id start_time end_time)) { print el($key,$p->{metadata}{$key}); }
    print el('target',$_) for @{$p->{metadata}{targets}//[]};
    print el('profile',$_) for @{$p->{metadata}{profiles}//[]};
    print '<consistency status="',esc($p->{root_login_consistency}{status} // 'indeterminate'),'">',esc($p->{root_login_consistency}{reason}),'</consistency>';
    if ($phase eq 'followup') {
        print el('capture-note','Researcher recalls independently recapturing effective SSH settings with sshd -T; the capture command and timestamp have not been verified.');
    }
    for my $id (sort keys %{$p->{rules}//{}}) {
        my $r=$p->{rules}{$id};
        print '<rule id="',esc($id),'" status="',esc($r->{status}),'">',el('reason',$r->{reason}),'</rule>';
    }
    for my $key (sort keys %{$p->{settings}//{}}) {
        my $s=$p->{settings}{$key};
        print '<setting name="',esc($key),'" status="',esc($s->{status}),'">',el('value',$s->{value}),el('reason',$s->{reason}),'</setting>';
    }
    for my $key (sort keys %{$p->{sources}//{}}) {
        my $s=$p->{sources}{$key}; my $uri=$s->{path}//'';
        # Local absolute paths only. Never turn input into an arbitrary URI scheme.
        my $href='';
        if ($uri =~ m{^/}) { $uri =~ s/([^A-Za-z0-9_.~\/-])/sprintf('%%%02X',ord($1))/ge; $href='file://'.$uri; }
        print '<source kind="',esc($key),'" href="',esc($href),'">',el('path',$s->{path}),el('sha256',$s->{sha256}),'</source>';
    }
    print '</phase>',"\n";
}
for my $c (@{$d->{comparisons}//[]}) {
    print '<comparison';
    for my $key (qw(from to rule_id assessment)) { print ' ',$key,'="',esc($c->{$key}),'"'; }
    print '>',esc($c->{transition}),'</comparison>',"\n";
}
print el('limitation',$_) for @{$d->{limitations}//[]};
print "</assessment>\n";
