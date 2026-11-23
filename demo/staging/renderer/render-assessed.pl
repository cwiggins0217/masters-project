#!/usr/bin/env perl
use strict;
use warnings;
use JSON::PP;
use Digest::SHA qw(sha256_hex);
use Cwd qw(abs_path);
use File::Temp qw(tempfile);
use FindBin;
# Positional arguments avoid assuming how the existing curated renderer is configured.
my ($json,$phase,$xsl,$scan,$output,@params)=@ARGV;
die "Usage: $0 comparison.json pre|post|followup ENTRY.xsl results.xml NEW.html [xsltproc options...]\n" unless defined $output && $phase =~ /\A(pre|post|followup)\z/;
die "Refusing to overwrite $output\n" if -e $output;
sub readbytes { open my $f,'<:raw',$_[0] or die "$!: $_[0]\n"; local $/; return <$f>; }
my $d=decode_json(readbytes($json));
my $expected=$d->{phases}{$phase}{sources}{scan}{sha256} // '';
die "Scan hash differs from selected comparison phase\n" unless $expected eq sha256_hex(readbytes($scan));
my ($fh,$xml)=tempfile(SUFFIX=>'.xml',UNLINK=>1);
open my $bridge,'-|',$^X,"$FindBin::Bin/comparison-to-xml.pl",$json or die "Cannot start converter: $!";
while (my $line=<$bridge>) { print {$fh} $line; }
close $bridge or die "Assessment conversion failed\n";
close $fh or die "Cannot finish assessment XML\n";
# Appended fixed parameters take precedence over any earlier caller options.
my @cmd=('xsltproc',@params,'--stringparam','assessment-uri',abs_path($xml),'--stringparam','assessment-phase',$phase,'--output',$output,$xsl,$scan);
my $rc=system @cmd;
if ($rc != 0) { unlink $output if -f $output; die "xsltproc failed (status $rc)\n"; }
print "Created $output\n";
