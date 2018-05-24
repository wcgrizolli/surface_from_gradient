 
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
	if [ ! -f 'AgrawalECCV06CodeMFiles.zip' ]; then
		wget http://www.cs.cmu.edu/~ILIM/projects/IM/aagrawal/eccv06/AgrawalECCV06CodeMFiles.zip
	fi
	unzip AgrawalECCV06CodeMFiles.zip -d g2sAgrawal/
    mv g2sAgrawal/AgrawalECCV06CodeMFiles/MST_fromlabpc/test.m g2sAgrawal/AgrawalECCV06CodeMFiles/MST_fromlabpc/test_1.m  # the filename test.m causes a warning and therefore we rename it
else
	echo 'ERROR: Directory g2sAgrawal/AgrawalECCV06CodeMFiles Exists. Installation skipped.' >&2
fi

if [ ! -d 'g2sHarker/grad2Surf' ]; then

	if [ ! -f 'grad2SurfV1-0.zip' ]; then
		wget https://www.mathworks.com/matlabcentral/mlc-downloads/downloads/submissions/43149/versions/1/download/zip
		if [ $? -ne 0 ];then
			echo "ERROR: Download failed. Aborting."
			echo "ERROR: You probably need to login here first: https://www.mathworks.com/matlabcentral/fileexchange/43149-surface-reconstruction-from-gradient-fields--grad2surf-version-1-0"
			xdg-open https://www.mathworks.com/matlabcentral/fileexchange/43149-surface-reconstruction-from-gradient-fields--grad2surf-version-1-0
			exit 1
		fi
		mv zip grad2SurfV1-0.zip
	fi
	mkdir g2sHarker
	unzip grad2SurfV1-0.zip -d g2sHarker/grad2Surf
else
	echo 'ERROR: Directory g2sHarker/grad2Surf Exists. Installation skipped.' >&2
fi

if [ ! -d 'g2sHarker/DOPBox/' ]; then

	if [ ! -f 'DOPBoxV1-8.zip' ]; then
		wget https://www.mathworks.com/matlabcentral/mlc-downloads/downloads/submissions/41250/versions/12/download/zip
		if [ $? -ne 0 ];then
			echo "ERROR: Download failed. Aborting."
			echo "ERROR: You probably need to login here first: https://www.mathworks.com/matlabcentral/fileexchange/43149-surface-reconstruction-from-gradient-fields--grad2surf-version-1-0"
			xdg-open https://www.mathworks.com/matlabcentral/fileexchange/43149-surface-reconstruction-from-gradient-fields--grad2surf-version-1-0
			exit 1
		fi
		mv zip DOPBoxV1-8.zip
	fi
	
	unzip DOPBoxV1-8.zip -d g2sHarker/DOPBox
else
	echo 'ERROR: Directory g2sHarker/DOPBox/ Exists. Installation skipped.' >&2
fi


if ls *zip >/dev/null 2>&1; then
    # there are zip files

    echo "### Remove zip files?"
    select yn in "Yes" "No"; do
        echo "Enter the option number and ENTER"
        case $yn in
            Yes ) rm -v AgrawalECCV06CodeMFiles.zip grad2SurfV1-0.zip DOPBoxV1-8.zip; break;;
            No ) echo "MESSAGE: zip files are not removed."; break;;
        esac
    done
fi

echo "Done"



