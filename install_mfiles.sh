 
#! /bin/bash


listprogram4check="wget unzip octave" 
MISSINGPROGRAM=false

for program in $listprogram4check
do
	if ! [ -x "$(command -v $program)" ]; then
		echo 'ERROR' $program 'is not installed.' >&2
		MISSINGPROGRAM=true
	else
		echo 'MESSAGE:' $program 'is installed.' >&2
	fi
done

if $MISSINGPROGRAM; then
	echo 'ERROR: Program not found. Aborting.'
	exit 1
fi




if [ ! -d 'g2sAgrawal/AgrawalECCV06CodeMFiles' ]; then
	wget -P g2sAgrawal/ http://www.cs.cmu.edu/~ILIM/projects/IM/aagrawal/eccv06/AgrawalECCV06CodeMFiles.zip
	unzip g2sAgrawal/AgrawalECCV06CodeMFiles.zip -d g2sAgrawal/
	rm g2sAgrawal/AgrawalECCV06CodeMFiles.zip 
else
	echo 'ERROR: Directory g2sAgrawal/AgrawalECCV06CodeMFiles Exists. Installation skipped.' >&2
fi