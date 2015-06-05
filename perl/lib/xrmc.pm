package xrmc;

our $VERSION = "6.6.0";

use strict;
#use xraylib;

sub parse_inputfile{
	my $inputfile = shift(@_);
	open (my $fh, "<", $inputfile) or die "Could not open $inputfile: $!";
	my %rv;
	while (my $line = <$fh>) {
		chomp($line);
		$line =~ s/;.*//;
		$line =~ s/^\s+//;
		$line =~ s/\s+$//;
		next if (length($line) == 0);

		if (substr($line,0,4) eq "Load") {
			$line =~ s/Load //;
			my $filename = $line;
			#quickly open file to determine device type
			open (my $fh2, "<", $filename) or die "Could not open $filename: $!";
			while (my $line2 = <$fh2>) {
				chomp($line2);
				$line2 =~ s/;.*//;
				$line2 =~ s/^\s+//;
				$line2 =~ s/\s+$//;
				next if (length($line2) == 0);
				if (substr($line2,0,9) eq "Newdevice") {
					$line2 =~ s/Newdevice //;
					my $device = $line2;
					if ($device eq "detectorarray") {
						$rv{detectorarrayfile} = $filename;
						xrmc::parse_detectorarray_inputfile(\%rv);
					}
					elsif ($device eq "composition") {
						$rv{compositionfile} = $filename;
					}
					elsif ($device eq "geom3d") {
						$rv{geom3dfile} = $filename;
					}
					elsif ($device eq "quadricarray") {
						$rv{quadricarrayfile} = $filename;
						xrmc::parse_quadricarray_inputfile(\%rv);
					}
					elsif ($device eq "spectrum") {
						$rv{spectrumfile} = $filename;
					}
					elsif ($device eq "sample") {
						$rv{samplefile} = $filename;
					}
					elsif ($device eq "source") {
						$rv{sourcefile} = $filename;
						xrmc::parse_source_inputfile(\%rv);
					}
					elsif ($device eq "detectorconvolute") {
						$rv{detectorconvolutefile} = $filename;
						xrmc::parse_detectorconvolute_inputfile(\%rv);
					}
					else {
						printf STDERR "Unknown devicetype %s found\n", $device;
						exit(1);
					}
					last;
				}
				
			}
			close($fh2);
		}
		elsif (substr($line,0,3) eq "Run") {
			$line =~ s/Run //;
			$line =~ s/^\s+//;
			$line =~ s/\s+$//;
			$rv{rundevice} = $line;
		}
		elsif (substr($line,0,4) eq "Save") {
			$line =~ s/Save //;
			$line =~ s/^\s+//;
			$line =~ s/\s+$//;
			my @comps = split(/\s+/, $line);
			$rv{savedevice} = $comps[0];
			$rv{saveimagetype} = $comps[1];
			$rv{savefilename} = $comps[2];
		}
	}
	close($fh);

	return \%rv;
}

sub parse_source_inputfile {
	my $input = shift(@_);

	#open source device file
	open (my $fh, "<", $input->{sourcefile}) or die "Could not open $input->{sourcefile}: $!";
	my %source;
	my $counter = 0;
	while (my $line = <$fh>) {
		chomp($line);
		$line =~ s/;.*//;
		$line =~ s/^\s+//;
		$line =~ s/\s+$//;
		next if (length($line) == 0);

		$counter++;
		if ($counter == 2) {
			$source{name} = $line;
			next;
		}
		if (substr($line, 0, 12) eq "SpectrumName") {
			$line =~ s/SpectrumName //;
			$source{spectruminputdevice} = $line;
		}
	}
	close($fh);
	$input->{source} = \%source;
}

sub parse_detectorarray_inputfile {
	my $input = shift(@_);

	#open device file
	open (my $fh, "<", $input->{detectorarrayfile}) or die "Could not open $input->{detectorarrayfile}: $!";
	my %detectorarray;
	my $counter = 0;
	while (my $line = <$fh>) {
		chomp($line);
		$line =~ s/;.*//;
		$line =~ s/^\s+//;
		$line =~ s/\s+$//;
		next if (length($line) == 0);

		$counter++;
		if ($counter == 2) {
			$detectorarray{name} = $line;
			next;
		}
		if (substr($line, 0, 12) eq "SourceName") {
			$line =~ s/SourceName //;
			$detectorarray{sourceinputdevice} = $line;
		}
	}
	close($fh);
	$input->{detectorarray} = \%detectorarray;
}

sub parse_detectorconvolute_inputfile {
	my $input = shift(@_);

	#open device file
	open (my $fh, "<", $input->{detectorconvolutefile}) or die "Could not open $input->{detectorconvolutefile}: $!";
	my %detectorconvolute;
	my $counter = 0;
	while (my $line = <$fh>) {
		chomp($line);
		$line =~ s/;.*//;
		$line =~ s/^\s+//;
		$line =~ s/\s+$//;
		next if (length($line) == 0);

		$counter++;
		if ($counter == 2) {
			$detectorconvolute{name} = $line;
			next;
		}
		if (substr($line, 0, 12) eq "SourceName") {
			$line =~ s/SourceName //;
			$detectorconvolute{sourceinputdevice} = $line;
		}
	}
	close($fh);
	$input->{detectorconvolute} = \%detectorconvolute;
}

sub parse_quadricarray_inputfile {
	my $input = shift(@_);

	#open device file
	open (my $fh, "<", $input->{quadricarrayfile}) or die "Could not open $input->{quadricarrayfile}: $!";
	my %quadricarray;
	my $counter = 0;
	while (my $line = <$fh>) {
		chomp($line);
		$line =~ s/;.*//;
		$line =~ s/^\s+//;
		$line =~ s/\s+$//;
		next if (length($line) == 0);

		$counter++;
		if ($counter == 1) {
			my @splitted = split(/\s+/,$line);
			die "device type differs from quadricarray" if ($splitted[1] ne "quadricarray");
		}
		elsif ($counter == 2) {
			$quadricarray{name} = $line;
			next;
		}
	}
	close($fh);
	$input->{quadricarray} = \%quadricarray;
}

sub write_translatefile {
	my $input = shift @_;
	my $file = shift @_;
	my @delta_coords = @{shift @_};
	$\ = "\n";
	$, = "  ";
	open (my $fh, ">", $file) or die "Could not open $file: $!";
	printf $fh "Device %s\n", $input->{quadricarray}->{name};
	printf $fh "TranslateAll ";
	print $fh @delta_coords; 

	printf $fh "End\n";

	$\ = undef;
	$, = undef;
	close($fh);
}

#sub generate_spectrum_from_file_with_filters {
#	my $raw_spectrum_file = shift @_;
#	my @phases = @{shift @_};
#
#	
#	open (my $fh, "<", $raw_spectrum_file) or die "Could not open $raw_spectrum_file: $!";
#	my @spectrum;
#	while (my $line = <$fh>) {
#		my $interval = [split(/\s+/,$line)];
#		next if ($interval->[0] <= 0.0);
#		push @spectrum, $interval;
#	}
#	close($fh);
#	foreach my $combo (@spectrum) {
#		my $energy = $combo->[0];
#		my $intensity = $combo->[1];
#		my $blb = 1.0;
#		foreach my $phase (@phases) {
#			my $total_cs = 0.0;
#			for (my $i ; $i < scalar(@{$phase->{atomicnumbers}}) ; $i++) {
#				my $Z = $phase->{atomicnumbers}->[$i];
#				my $weight = $phase->{weightfractions}->[$i];
#				$total_cs += $weight*xraylib::CS_Total_Kissel($Z, $energy);
#			}
#			$blb *= exp(-1.0*$total_cs*$phase->{thickness}*$phase->{density});
#		}
#		$intensity *= $blb;
#		if ($intensity < 1E-25) {
#			$intensity = 0.0;
#		}
#		$combo->[1] = $intensity;
#	}
#	return \@spectrum;
#}


sub write_spectrum_inputfile {
	my $input = shift @_;
	$\ = "\n";
	$, = "\t\t";
	open (my $fh, ">", $input->{spectrumfile}) or die "Could not open $input->{spectrumfile}: $!";
	printf $fh "Newdevice spectrum\n";
	printf $fh "%s\n", $input->{spectrum}->{name};
	printf $fh "PolarizedFlag %i\n",$input->{spectrum}->{PolarizedFlag};
	printf $fh "LoopFlag %i\n",$input->{spectrum}->{LoopFlag};
	printf $fh "ContinuousPhotonNum %i\n", $input->{spectrum}->{ContinuousPhotonNum};
	printf $fh "LinePhotonNum %i\n", $input->{spectrum}->{LinePhotonNum};
	printf $fh "RandomEneFlag %i\n", $input->{spectrum}->{RandomEneFlag};
	if (exists($input->{spectrum}->{Lines}) &&  scalar(@{$input->{spectrum}->{Lines}})) {
		printf $fh "Lines\n";
		printf $fh "%i\n",scalar(@{$input->{spectrum}->{Lines}});
		foreach my $line (@{$input->{spectrum}->{Lines}}) {
			print $fh @$line;
		}
	}

	if (exists($input->{spectrum}->{ContinuousSpectrum}) && scalar(@{$input->{spectrum}->{ContinuousSpectrum}})) {
		printf $fh "ContinuousSpectrum\n";
		printf $fh "%i\n",scalar(@{$input->{spectrum}->{ContinuousSpectrum}});
		foreach my $line (@{$input->{spectrum}->{ContinuousSpectrum}}) {
			print $fh @$line;
		}
		printf $fh "Resample 0\n";
	}
	printf $fh "End\n";

	$\ = undef;
	$, = undef;
	close($fh);
}

sub write_inputfile {
	my $inputfile = shift @_;
	my $input = shift @_;

	open (my $fh, ">", $inputfile) or die "Could not open $inputfile for writing: $!";
	printf $fh "Load %s\n", $input->{detectorarrayfile};	
	printf $fh "Load %s\n", $input->{compositionfile};	
	printf $fh "Load %s\n", $input->{geom3dfile};	
	printf $fh "Load %s\n", $input->{quadricarrayfile};	
	printf $fh "Load %s\n", $input->{spectrumfile};	
	printf $fh "Load %s\n", $input->{samplefile};	
	printf $fh "Load %s\n", $input->{sourcefile};	
	printf $fh "Run %s\n",  $input->{detectorarray}->{name};	
	printf $fh "Save %s %s %s\n", $input->{savedevice}, $input->{saveimagetype}, $input->{savefilename};	


	close($fh);


}

sub write_torquefile {
	my $torquefile = shift @_;
	my $inputfile = shift @_;

	open (my $fh, ">", $torquefile) or die "Could not open $torquefile for writing: $!";
	#printf $fh "export LD_LIBRARY_PATH=$ENV{LD_LIBRARY_PATH}:$ENV{HOME}/lib\n";
	printf $fh "/usr/local/bin/xrmc %s\n", $inputfile;
	close($fh);
	
}

sub parse_torquefile {
	my $torquefile = shift @_;

	open (my $fh, "<", $torquefile) or die "Could not open $torquefile for reading: $!";
	my @lines = <$fh>;
	my @splitted = split(/\s+/, $lines[0]);
	close($fh);
	return $splitted[-1];
}

1;
