#!/usr/bin/perl -w
use strict;
use Getopt::Long;
use File::Basename;

my ($help, $style, $width, $output, $fasta);
GetOptions(
    "h|help"     => \$help,
    "s|style:s"  => \$style,
    "w|width:s"  => \$width,
    "o|output:s" => \$output,
);
$style ||= 'single'; $fasta ||= $ARGV[0];
# 
if (defined $width){
    die "Error: --width must be an intger.\n" unless $width =~ /^\d+$/;
    $style = 'multi';
}
die usage() if (defined $help || !defined $fasta);
if ($style ne 'single' && $style ne 'multi' ){
    die "Error: --style must be 'single' or 'multi'.\n";
    exit 1;
}
# 
open FA, "<$fasta" || die "Can't open the fasta file $fasta\n";
$/ = ">"; <FA>;
while(<FA>){
    chomp;
    my ($id, $seq) = split (/\n/, $_, 2);
    $seq =~ s/\n//g;
    if (lc($style) eq 'multi'){
        $seq = format_fasta($seq, $width);
        print ">$id\n$seq\n";
    }else{
        print ">$id\n$seq\n";
    }
}
$/ = "\n";
close FA;
# 
sub format_fasta {
    my ($seq, $num) = @_;
    my $len = length $seq;
    $seq =~ s/([A-Za-z]{$num})/$1\n/g;
    chop($seq) unless $len % $num;
    return $seq;
}

sub usage {
    my $src_name = basename($0);
    print STDERR <<EOF;
Name:
    Perl script to convert display width of sequence.
    -------------------------------------------------
    . Author: Peng Liu                              .
    . E-mail: sxliulian2012\@hotmail.com             .
    .   Data: 2022-02-27 11:06                      .
    -------------------------------------------------
Usage:
    perl $src_name [style: single|multi] [width: int] <input.fa | STDIN>
Params:
    <FILE>       input from a fasta file.
  or
    <STDIN>      input from <STDIN>
Options:
    -s, --style  [str]  output style of input.fa. [single/multi]
    -w, --width  [int]  width of line. [defalut: 80]
    -h, --help          Print this help information.

Example:
    perl $src_name -s single input.fa > output.fa
  or
    perl $src_name -s multi -w 60 input.fa > output.fa
  or
    cat input.fa | perl $src_name -s single - > output.fa
  or 
    cat input.fa | perl $src_name -s multi -w 60 - > output.fa

EOF
    exit 1;
}
__END__