use ExtUtils::MakeMaker;

    WriteMakefile(
        NAME            => 'xrmc',
        VERSION_FROM    => 'lib/xrmc.pm',
	EXE_FILES       => ['bin/xrmc-dscan', 'bin/xrmc-dmesh']
    );
