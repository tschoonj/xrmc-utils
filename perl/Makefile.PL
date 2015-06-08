use ExtUtils::MakeMaker;

    WriteMakefile(
        NAME            => 'xrmc',
        VERSION_FROM    => 'lib/xrmc.pm',
	EXE_FILES       => ['bin/xrmc-dscan', 'bin/xrmc-dmesh'],
	PREREQ_PM       => {"Scalar::Util" => 0, "Syntax::Feature::Junction" => 0}
    );
