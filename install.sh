#!/bin/bash


if (( $EUID == 0 )); then
	echo "Checking if adequate folders exist..."
	
	if [ ! -d "/usr/share/nautilus-python" ]; then
		mkdir /usr/share/nautilus-python
	fi
	if [ ! -d "/usr/share/nautilus-python/extensions" ]; then
		mkdir /usr/share/nautilus-python/extensions/
	fi
	
	echo "Installing plugin files in /usr/share/nautilus-python/extensions/"

	cp launcher-creator.py /usr/share/nautilus-python/extensions/launcher-creator.py
	cp -r launcher-creator /usr/share/nautilus-python/extensions
else
	echo "Checking if adequate folders exist..."
	
	if [ ! -d "$HOME/.local/share/nautilus-python" ]; then
		mkdir ~/.local/share/nautilus-python
	fi
	if [ ! -d "$HOME/.local/share/nautilus-python/extensions" ]; then
		mkdir ~/.local/share/nautilus-python/extensions/
	fi

	echo "Installing plugin files in ~/.local/share/nautilus-python/extensions"

	cp launcher-creator.py ~/.local/share/nautilus-python/extensions/launcher-creator.py
	cp -r launcher-creator ~/.local/share/nautilus-python/extensions
	
fi
	
exit 0
