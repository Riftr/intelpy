# IntelPy

> IntelPy is a simple, cross-platform chat log monitor for the game Eve Online 
>
> ![IntelPy](https://i.imgur.com/WQ8pife.png)

## Required packages

### Windows

Ignore this section and simply download the latest Windows release. It should work out of the box.

### Linux

* `Python 3` (`python` and possibly `python-distro` on Arch Linux, should already be installed for most users)
* `PyQt 5` (`python-pyqt5` on Arch Linux)
* `pathlib` and
* `pathlib2`  (`python-pathlib` and `python-pathlib2` on Arch Linux)
* `Watchdog` (`python-watchdog`on Arch Linux)
* `Networkx` (`python-networkx` on Arch Linux)
* `Playsound` (install via pip if your distro does not have this)
* `PyGObject` (`python-gobject` on Arch Linux, a dependency for Playsound. May need to also install via pip)

### :warning: Notes :warning:

* Note to Arch Linux users: Playsound doesn't appear to be in your repositories, so you may need to install both it and pygobject it via pip

## Installation

### Windows

Download the latest Windows release .zip file [here](https://github.com/Riifta/intelpy/releases/latest), then copy it to a directory
and run IntelPy.exe. 

### Linux

There are three options: download the pre-built package, use pip or manual install (and use your system libraries/packages). 

#### Pre-built package

Download the latest Linux tar.gz release [here](https://github.com/Riifta/intelpy/releases/latest), then copy it to a directory such as /opt/intelpy
and run IntelPy. The program contains all the dependencies above and it should just work. 

#### Pip

Download the latest tar.gz source code release [here](https://github.com/Riifta/intelpy/releases/latest) and extract somewhere such as /opt/intelpy. 

Next, install dependencies via pip:

```shell
$ sudo pip install pyqt5 pathlib watchdog networkx playsound pathlib2 pygobject
```

Run ```python Intelpy.py``` to start the application.


#### Install from source

Download the latest source code package [here](https://github.com/Riifta/intelpy/releases/latest) and extract somewhere such as /opt/intelpy

Included are the necessary files to build this application with PyInstaller to make stand-alone packages for your OS if you desire.
The script to build these packages are the `build.sh` and `build.bat` files for Linux and Windows respectively. `build.sh` may also
work for OSX but this is untested at this time.

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

## Usage

Getting started is easy:

1. If you are in the Imperium your intel channels are already configured. If not, go to the Config tab and enter
the full name of the in-game intel channel in the Watched Channels configuration.

2. In game, turn on logging via the settings menu under Chat. This is usually already enabled by default. 

![Chat Setings](https://i.imgur.com/SWErZWy.png)

3. Set your home system (the one where you are krabbing) by entering the name and clicking the Set Home button. The log
screen will notify you of the change by indicating `Home set to: homesystem`.
 
3. Adjust the slider to set how many jumps away from your home system that you wish to be notified. IntelPy is aware
of the Eve Online solar system map so when someone says the name of a system within that amount of jumps from you, 
the alert sound and notification will trigger. The easiest way for people to alert each other is to drag and drop the 
system name from the top left of their game screen to the chat dialog box and press enter. 

If IntelPy is not picking up your intel channels, you may need to double check you have entered them in the Watched 
Channels configuration, as well as double check the Eve Logs: section points to the place where Eve Online is logging
your chats for you. 

There are a handful of other options also configurable in the Config tab. This includes setting the alarm sound; IntelPy
comes with a number of extra sounds or you may choose your own. You can also set how long until alerts time out from the
recent alerts screen as well as various filter/ignore options as you desire.

## Licences / Acknowledgements / Attributions

This source code is available under [GPL3](https://www.gnu.org/licenses/gpl-3.0.en.html). 

Eve-related data was made available by CCP and obtained from the Eve static data dump. See CCP Copyright Notice below.

Some Eve data was also obtained from https://www.fuzzwork.co.uk/. Thanks heaps for your data dumps!

### Sound Files

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

EVE Online, the EVE logo, EVE and all associated logos and designs are the intellectual property of CCP hf. All artwork, screenshots, characters, vehicles, storylines, world facts or other recognizable features of the intellectual property relating to these trademarks are likewise the intellectual property of CCP hf. EVE Online and the EVE logo are the registered trademarks of CCP hf. All rights are reserved worldwide. All other trademarks are the property of their respective owners. CCP hf. has granted permission to IntelPy to use EVE Online and all associated logos and designs for promotional and information purposes on its website but does not endorse, and is not in any way affiliated with, IntelPy. CCP is in no way responsible for the content on or functioning of this program, nor can it be liable for any damage arising from the use of this program.