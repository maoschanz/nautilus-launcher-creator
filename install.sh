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

	cp create-desktop-file.py /usr/share/nautilus-python/extensions/create-desktop-file.py
	cp -r create-desktop-file /usr/share/nautilus-python/extensions
else
	echo "Checking if adequate folders exist..."
	
	if [ ! -d "$HOME/.local/share/nautilus-python" ]; then
		mkdir ~/.local/share/nautilus-python
	fi
	if [ ! -d "$HOME/.local/share/nautilus-python/extensions" ]; then
		mkdir ~/.local/share/nautilus-python/extensions/
	fi

	echo "Installing plugin files in ~/.local/share/nautilus-python/extensions"

	cp create-desktop-file.py ~/.local/share/nautilus-python/extensions/create-desktop-file.py
	cp -r create-desktop-file ~/.local/share/nautilus-python/extensions
	
fi
	
exit 0
