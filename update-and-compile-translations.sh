#!/bin/bash

echo "Generating .pot file..."
xgettext --files-from=files-list --output=launcher-creator/locale/launcher-creator.pot

IFS='
'
liste=`ls ./launcher-creator/locale/`

for dossier in $liste
do
	if [ "$dossier" != "launcher-creator.pot" ]; then
		echo "Updating translation for: $dossier"
		msgmerge ./launcher-creator/locale/$dossier/LC_MESSAGES/launcher-creator.po ./launcher-creator/locale/launcher-creator.pot > ./launcher-creator/locale/$dossier/LC_MESSAGES/launcher-creator.temp.po
		mv ./launcher-creator/locale/$dossier/LC_MESSAGES/launcher-creator.temp.po ./launcher-creator/locale/$dossier/LC_MESSAGES/launcher-creator.po
		echo "Compiling translation for: $dossier"
		msgfmt ./launcher-creator/locale/$dossier/LC_MESSAGES/launcher-creator.po -o ./launcher-creator/locale/$dossier/LC_MESSAGES/launcher-creator.mo
	fi
done

exit 0
