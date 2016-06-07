#!/usr/bin/perl;

###############################################################################
#
# Simple HDBSQLDriver
# !!! Driver uses hdbsql command as proxy - not a real DBD driver!!!
# Written by Markus Guertler (SUSE)
# License GPL
# (Might be outsource to an separate module in the future)
#
###############################################################################

package HDBSQLDriver;

use Carp;
use IPC::Open3;
use IO::Select;
use strict;
use warnings;

# Constructor
sub new {
    my($class,%opts) = @_;
    
    my $self = {};
    
    bless ($self,$class);
	
	$self->{USKEY}=$opts{uskey} or croak ('Please supply a valid user store key!');
	$self->{HDBSQL_PATH}=$opts{hdbsql_path} or croak ('Please supply a valid path to hdbsql command');
	$self->{HDBSQL_OPTIONS}="-j -C -a -x";
	
	$self->{HDBSQL_CMD} = $self->{HDBSQL_PATH}.'/hdbsql';
	
	if (! -e $self->{HDBSQL_CMD})
	{
		croak ('hdbsql command not found or not executable: $self->(HDBSQL_CMD)');
	} 
	
	$self->{PID} = open3($self->{WRITE_HDL},$self->{READ_HDL},$self->{ERROR_HDL}, $self->{HDBSQL_CMD}.' '. $self->{HDBSQL_OPTIONS}.' -U '.$self->{USKEY});
	
	$self->{selread} = new IO::Select();
	$self->{selread}->add($self->{READ_HDL},$self->{ERROR_HDL});
	$self->_read_buffer;
	
	return ($self);
}

sub _read_buffer
{
	my $self = shift;	 
		
	my $count = 0;
	my $data;
	
	while (my @fhs = $self->{selread}->can_read(0.1))
	{
		foreach my $fh (@fhs)
		{
			$data = <$fh>;
			print "xxx\n";
			print ": $data";
		}
	}
}

# Destructor
sub DESTROY
{
	my $self = shift;
	my $wrh = $self->{WRITE_HDL};
	print $wrh "quit";
	waitpid($self->{PID}, 1);
}

1;