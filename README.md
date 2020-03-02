# IntelPy

> IntelPy is a simple, cross-platform chat log monitor for the game Eve Online 

![IntelPy](https://i.imgur.com/Hk8FLAr.png)

## Why another one of these?

I didn't like the other options out there and I wanted to try to make something myself. 

## Which packages do I need to run IntelPy?

### Required packages

* `Python 3` (and possibly `python-distro` on Arch Linux)
* `PyQt 5` (`python-pyqt5` on Arch Linux)
* `pathlib` and
* `pathlib2`  (`python-pathlib` and `python-pathlib2` on Arch Linux)
* `Watchdog` (`python-watchdog`on Arch Linux)
* `Networkx` (`python-networkx` on Arch Linux)
* `Playsound` (may have to install via Pip on Arch Linux, would otherwise be `python-playsound`)
* `Gobject` (`python-gobject` on Arch Linux, a dependency for Playsound)

### :warning: Notes :warning:

* Note to Arch Linux users: Playsound doesn't appear to be in your repositories, so you may need to install via pip

## Installation

### Windows

Just grab the latest Windows release [here](https://github.com/Riifta/intelpy/releases/latest), then copy it to a directory
and run IntelPy.exe. The program contains all the dependencies above and it should just work. 

### Linux

There are three options: download the pre-built package, use pip or manual install (and use your system libraries/packages). 

#### Pre-built package

Just grab the latest Linux release [here](https://github.com/Riifta/intelpy/releases/latest), then copy it to a directory such as /opt/intelpy
and run IntelPy. The program contains all the dependencies above and it should just work. 

#### Pip

Download a copy of the repository and put somewhere such as /opt/intelpy. 

Next, install dependencies via pip:

```shell
$ sudo pip install pyqt5 pathlib watchdog networkx playsound pathlib2 pygobject
```

Run Intelpy.py to start the application.


#### Install from source

Download a copy of the repository. Install the required packages for your OS (see above). Run Intel.py.

Note: a setup.py file as well as an (untested) PKGBUILD is available at this time.

Included are the necessary files to build this application with PyInstaller to make stand-alone packages for your OS if you desire.
These scrips are the `build.sh` and `build.bat` files for Linux and Windows respectively. 

#### Other OSes

IntelPy will probably run under OSX and other POSIX-like systems but I do not have the means to test this. If you encounter errors, please let me know.


## Configuration (optional)

When you first run IntelPy it will attempt to automatically configure itself. Useful configuration options are all done
via the application so you don't need to manually go into your settings.json and edit things yourself. The key options 
it will attempt to configure are your Eve log directory, the alarm sound file to use and where to store the configuration.
IntelPy comes with a number of extra alarm sounds or you can use your own.

On Windows systems, the configuration file will be found under %appdata%, under `Local\IntelPy\settings.json`. There is an
optional dark mode interface you can turn on via this file if you wish by changing `"windows_dark_theme"` to `1`.

On Linux etc systems, the configuration file will be found under `~/.config/IntelPy/settings.json`. 

## Licences

See LICENSE. 

In short, the source code is available under [GPL3](https://www.gnu.org/licenses/gpl-3.0.en.html) and the sound files as per Acknowledgements below. 

Eve related data was made available from CCP from the Eve static data dump. See CCP Copyright Notice below. 

## Acknowledgements / Attributions

The alarm sounds included in IntelPy were sourced from https://freesound.org. Below are credits and licences for these 
sounds. Changes were made to most of these shorten the length to make them suitable for use with IntelPy. 

* military_alarm.wav by KIZILSUNGUR  License: Creative Commons 0
* alarming 1.flac by Timbre | License: Attribution Noncommercial
* 1 alarm long c.wav by jobro | License: Attribution
* Alarm Siren, Fast Oscillations by Kinoton | License: Creative Commons 0
* alarms.wav by guitarguy1985 | License: Creative Commons 0
* alarm_fatal.wav by sirplus | License: Creative Commons 0
* DIN Alarm European.MP3 by Fizzlecube | License: Creative Commons 0
* 003 - Invasion Alarm.mp3 by o_ultimo | License: Attribution
* Alarm No. 1 by Vendarro | License: Creative Commons 0

Links to sound licences:
* Creative Commons 0: https://creativecommons.org/publicdomain/zero/1.0/
* Attribution: https://creativecommons.org/licenses/by/3.0/
* Attribution Noncommercial: http://creativecommons.org/licenses/by-nc/3.0/


### CCP Copyright Notice

EVE Online, the EVE logo, EVE and all associated logos and designs are the intellectual property of CCP hf. All artwork, screenshots, characters, vehicles, storylines, world facts or other recognizable features of the intellectual property relating to these trademarks are likewise the intellectual property of CCP hf. EVE Online and the EVE logo are the registered trademarks of CCP hf. All rights are reserved worldwide. All other trademarks are the property of their respective owners. CCP hf. has granted permission to pyfa to use EVE Online and all associated logos and designs for promotional and information purposes on its website but does not endorse, and is not in any way affiliated with, pyfa. CCP is in no way responsible for the content on or functioning of this program, nor can it be liable for any damage arising from the use of this program.