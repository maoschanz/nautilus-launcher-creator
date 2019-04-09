# Nautilus extension: Launcher creator

A nautilus extension providing an advanced dialog in order to create a launcher (.desktop file) for any file.

## How it works

- Right-click on a file, click on the "Create a launcher" menu item

- Give a name to the launcher. If the file isn't executable, you should use the type "Link" instead of "Application" (it will not be displayed in menus)

- Optionally a short description and a list of [categories](https://standards.freedesktop.org/menu-spec/latest/apa.html) and keywords

<!--![](https://i.imgur.com/1NqbxCR.png)-->

- Select an icon

<!--![](https://i.imgur.com/wFneAti.png)-->

<!--- Enjoy-->

<!--![](https://i.imgur.com/aqvKVWM.png)-->

## How to install

- Install the package `python-nautilus` (it's its name on Debian at least).
- Download the code, make `install.sh` executable, and execute it.
- Quit (and restart) Nautilus, and then it should works.


