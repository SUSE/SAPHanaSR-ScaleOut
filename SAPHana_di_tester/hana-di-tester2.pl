#!/usr/bin/perl
#
# HANA Data Integrity Tester
# Written by Markus Guertler
# License: GPL
#

package main;

use warnings;
use strict;

use Getopt::Long;
use Sys::Syslog;
use threads;

use HDBSQLDriver;

my %opts;

# GetOpts parser
my $p = Getopt::Long::Parser->new();
$p->getoptions(
	\%opts,
	'user_store_key|U=s',
	'threads|t=i',
	'records|r=i',
	'cycles|c=i',
	'syslog|s',
	'daemon|d',
	'quiet|q',
	'hdbsql_path|p',
	'help|h'
	);

# Set default values
my $uskey = $opts{user_store_key};
my $nr_threads = $opts{threads} || 2;
my $nr_records = $opts{records} || 200; 
my $nr_cycles = $opts{records} || 50;
my $enable_syslog = $opts{syslog} || undef;
my $be_quiet = $opts{quiet} || undef;
my $is_daemon = $opts{daemon} || undef;
$enable_syslog = 1 if ($is_daemon);
my $hdbsql_path = $opts{hdbsql_path} || '/usr/sap/HA3/HDB14/exe';
my $hdbsql_cmd = $hdbsql_path."/hdbsql";
my $hdbsql_options = "-j -C -a -x";
my $test_table = "data_integrity_testing";
my $record_value_max = 100000;

# Usage
&usage if (!$uskey or $opts{help});

# Daemonize if configured to run as daemon
&daemonize() if ($is_daemon);

# Prepare everything
&prepare();

# Start the worker threads
my @threads;
&out ("-> Starting $nr_threads worker threads...");
for (my $count = 0; $count < $nr_threads; $count++)
{
	$threads[$count] = threads->create(\&integrity_testing);
}

# Join them at the end
foreach my $thread (threads->list())
{
	$thread->join();
}

# Join the worker threads at the end of all work
# (Since the threads are running in an endless loop, this point shoud never be reached)
#foreach (@threads)
#{
#	$_->join();
#}

# Usage
# Expects: -
# Returns: -
sub usage
{
	print <<EOF;
  
usage: $0 -U <HANA user store key> [optional parameters]

Tool, that continously checks the data integrity of a HANA database, by 
writing a specified number of records, randomly modifying these records,
and verifying the number and contents of the records.  

Mandatory parameters:
    --user_store_key | -U    Valid HANA user store key
    
Optional parameters:
    --threads | -t           Number of worker threads
                             (defaults to $nr_threads)
    --records | -r           Number of records to create per thread
                             (defaults to $nr_records)
    --cycles  | -c           Number of data record modifications
                             before checking data integrity of all records
                             (defaults to $nr_cycles) 
    --syslog  | -s           print output to syslog instead of STDOUT
    --quiet   | -q           Don't print any output
    --daemon  | -d           starts as a daemon (inherits -s)
    --hdbsql_path  | -h      path to hdbsql command
                             (defaults to $hdbsql_path)
                             
Example: $0 -U SLEHALOC
EOF
	exit 1;
}

#
#
# FUNCTIONS
#
# 

# Prepare everything, i.e. executable checks, create table, delete old content
# from table
# Expects: -
# Returns: -
sub prepare
{
	&out ("-> Prepare integrity testing...");
	# Check hdbsql command
	&out ("   * Check if hdbsql command is available and executable...");
	&error ("Couldn't find hdbsql command or command is not executable!\n(I was trying: $hdbsql_cmd)") if ( !-e $hdbsql_cmd);
	
	# Get hdbsql handles
	my $hdbsql = HDBSQLDriver->new(
		uskey => $uskey,
		hdbsql_path => $hdbsql_path
	);
	
	exit 0;
	
	# Check HANA database connectivity
	&out ("   * Test hdbsql connectivity...");
	&hdbsql ("SELECT * FROM DUMMY");
	# Drop the test table
	&out ("   * Drop table $test_table...");
	&hdbsql ("DROP TABLE $test_table",1);
	# Create the test table
	&out ("   * Create table $test_table...");
	&hdbsql ("CREATE TABLE $test_table (KEY INT PRIMARY KEY, VAL INT)",1);
	# Test select on the test table
	&out ("   * Test select on $test_table...");
	&hdbsql ("SELECT * FROM $test_table");
	&out ("...prepare completed!\n");
}

# Daemonizes this process
# Expects: -
# Returns: -
sub daemonize
{
   use POSIX;
   POSIX::setsid or die "setsid: $!";
   my $pid = fork ();
   if ($pid < 0) {
      die "fork: $!";
   } elsif ($pid) {
      exit 0;
   }
   foreach (0 .. (POSIX::sysconf (&POSIX::_SC_OPEN_MAX) || 1024))
      { POSIX::close $_ }
   open (STDIN, "</dev/null");
   open (STDOUT, ">/dev/null");
   open (STDERR, ">&STDOUT");
   if ($opts{pidfile})
   {
   	  open PIDFILE, "> $opts{pidfile}" or &error ("Couldn't open pidfile for writing!");
   	  print PIDFILE "$$";
   	  close PIDFILE;
   }
 }
 
 # Executes a HDB SQL command and returns output as an array with one item per
 # line
 # Expects: command as string
 # Expects: true | false to indicate to ignore the return code or not to ignore it
 # Returns: reference to an array with one record per command output line
 sub hdbsql
 {
 	my $cmd = shift;
 	my $ignore_rc = shift || undef;
 	my $stderr_dev_null;
 	$ignore_rc ? $stderr_dev_null = "2>/dev/null" : $stderr_dev_null = "";
 	my $full_command = "$hdbsql_cmd $hdbsql_options -U $uskey '$cmd' $stderr_dev_null";
 	my @output;
 	open HDBSQL, "$full_command |" or &error ("Could not execute command: $full_command");
 	while (<HDBSQL>)
 	{
 		chomp $_;
 		push (@output,$_);
 	}
 	close HDBSQL;
 	&error ("hdbsql returned an error: $?") if ($? and !$ignore_rc);
 	
 	return (\@output);
 }
 
# Prints error message and exits
# Expects: $error_message and optional $exit_code
sub error
{
	my $error = shift;
	my $exitcode = shift || 1;
	print STDERR $error."\n";
	syslog ('err',$error) if ($enable_syslog);
	$is_daemon ? die : exit $exitcode;
}

# Prints messages to stdout if option --quiet is not set
# Prints message to syslog if option syslog is set
# Expects: $message
sub out
{
	my $msg = shift;
	print "$msg\n" if (!$be_quiet);
	syslog ('info',$msg) if ($enable_syslog);
}



#
#
# THREADED CODE
#
# 
 
# Does the integrity testing
# Expects: -
# Returns: -
sub integrity_testing
{
	my $tid = threads->tid();
	my $key_offset = ($tid) * $nr_records;
	my @data;
	
	&integrity_testing_warming_up($tid,$key_offset,\@data);
	&integrity_testing_verify_data($tid,$key_offset,\@data);
	
	# Happy endless loop...
	while (1 == 1)
	{
		&integrity_testing_modify_data($tid,$key_offset,\@data);
		&integrity_testing_verify_data($tid,$key_offset,\@data);
	}
	
}

# Initialize table for this thread by inserting $nr_records data records with random numbers
# Expects: $tid, $key_offset, \@data
# Returns: -
sub integrity_testing_warming_up
{
	my $tid = shift;
	my $key_offset = shift;
	my $data_ref = shift;
	&out("-> Thread $tid: Warming up by inserting $nr_records records");
	for (my $count = 0; $count < $nr_records; $count++)
	{
		my $key = $key_offset + $count;
		my $random_number = int(rand($record_value_max))+1;
		&out("   * Thread $tid: Inserted $count records...") if ($count % 20 == 0 && $count);
		#&out("INSERT INTO $test_table VALUES ($key,$random_number");
		&hdbsql("INSERT INTO $test_table VALUES ($key,$random_number)");
		$data_ref->[$count] = $random_number;	
	}
	&out("Thread $tid: Warming up done\n");
}

# Checks the data integrity of the data records in the database against the locally stored copy of the same records
# Expects: $tid, $key_offset, \@data
# Returns: -
sub integrity_testing_verify_data
{
	my $tid = shift;
	my $key_offset = shift;
	my $data_ref = shift;
	
	my $key_max = $key_offset + $nr_records;
	
	&out("-> Thread $tid: Comparing data records with locally stored data");
	
	my $output_ref = &hdbsql("SELECT * FROM $test_table WHERE key >= $key_offset AND key < $key_max");
	
	if (@$output_ref < $nr_records)
	{
		&error("Number of received records by select smaller than number of inserted records!");
	}
	
	foreach (@$output_ref)
	{
		my ($key,$value) = split(/,/,$_);
		if ($value != $data_ref->[$key-$key_offset])
		{
			&error("Thread $tid: Data record mismatch! Data integrity test failed!");
		}
	}
	&out("Thread $tid: Integrity verfication successful!\n");
}

# Randomly modificates records by deleting and re-inserting them with new random values (no update, more stress) :-) 
# Expects: $tid, $key_offset, \@data
# Returns: -
sub integrity_testing_modify_data
{
	my $tid = shift;
	my $key_offset = shift;
	my $data_ref = shift;
	&out("-> Thread $tid: Modifying (deleting / re-inserting) $nr_cycles amount of records!");
	
	for (my $count = 0; $count < $nr_cycles; $count++)
	{
		my $random_key = int(rand($nr_records)) + $key_offset;
		my $random_number = int(rand($record_value_max))+1;
		&out("   * Thread $tid: Modified $count records...") if ($count % 20 == 0 && $count);
		#&out("INSERT INTO $test_table VALUES ($key,$random_number");
		&hdbsql("DELETE FROM $test_table WHERE key = $random_key");
		&hdbsql("INSERT INTO $test_table VALUES ($random_key,$random_number)");
		$data_ref->[$random_key-$key_offset] = $random_number;	
	}
	&out("Thread $tid: Data modifications done\n");
}

