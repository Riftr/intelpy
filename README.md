# IntelPy

> IntelPy is a cross-platform chat log monitor and alert system for the game Eve Online.
>
> ![IntelPy](https://github.com/Riftr/intelpy/blob/master/intelpy/externals/Intelpy-screenshot.png)
>
>

## Features

* Cross-platform
* Alert tracker
* Audible alarms
* Filtering options
* Dark themes for Windows and Linux
* Awareness of the Eve Online map to calculate jumps from alert
* Will watch any in-game channel you want, including system channels

## How to Install IntelPy

### Windows

1. Download the latest Windows release from [here](https://github.com/Riifta/intelpy/releases/latest).
2. Extract the contents to a directory 
3. Run IntelPy.exe
 
### Linux / Run From Source

1. Download the latest source release from [here](https://github.com/Riifta/intelpy/releases/latest)
2. Extract the contents to a directory, such as /opt/intelpy
3. Install the required packages below
4. Run `python /opt/intelpy/intelpy.py`

Flatpak has been submitted and waiting on approval. 

## Required packages (for source)
 
You only need these if you are downloading and running from source. The Windows and Flatpak will
include the right versions themselves. The versions below aren't hard requirements, only what IntelPy has been tested on.

* Python 3.12**
* networkx 3.2.1
* PyQt5 5.15.10
* watchdog 4.0.0
* pygame 2.5.2
* pathlib 1.0.1

** For building with PyInstaller on Windows, you require Python 3.10 instead as well as pyinstaller 5.1.

## Usage

IntelPy watches your Eve Online chat logs for text that matches a solar system relative to your current location (home). 
This is typically used with intel chat channels in eve



1. In game (if needed) turn on logging via the settings menu under Chat. This is usually already enabled by default.

![Chat Setings](https://github.com/Riftr/intelpy/blob/master/intelpy/externals/intelpy-evelogenable.png)

2. IntelPy should usually automatically detect your Eve Online Chatlog path. Check this is correct on the Config tab if you 
have trouble getting it to detect your chat channels.

3. On the Config tab, set the names of the intel channels you want to watch from Eve. You may also need to manually choose
your Eve chatlog location. If you are in the Imperium your intel channels are already configured. 

4. On the Main tab, set your home system (where you are krabbing). Alerts will be triggered relative to this system. The log
screen will notify you of the change by indicating `Home set to: homesystem`. Note that jump bridges are not taken into account as
your enemies shouldn't be able to use them (you have bigger issues if they can).

5. Adjust the slider to set how many jumps away from your home system that you wish to be notified. IntelPy is aware
of the Eve Online solar system map so when someone says the name of a system within that amount of jumps from you, 
the alert sound and notification will trigger. The easiest way for people to alert each other in game is to drag and drop the 
system name from the top left of their game screen to the chat dialog box and press enter. 

**If IntelPy is not picking up your intel channels, you may need to double check you have entered them in the Watched 
Channels configuration, as well as double-check the Eve Logs: section points to the place where Eve Online is logging
your chats for you. The path to which Eve logs everything depends on how you installed it.**

There are a handful of other options also configurable in the Config tab. This includes setting the alarm sound, IntelPy
comes with a number of extra sounds or you may choose your own. You can also set how long until alerts time out from the
recent alerts screen as well as various filter/ignore options as you desire.

### Steam

While IntelPy will try to use sane Chatlog paths on most operating systems, if you have installed Eve Online via Steam 
then your path may need to be manually configured to the appropriate location, especially on Linux.  

On Linux, this will likely be:
`~/.local/share/Steam/steamapps/compatdata/8500/pfx/drive_c/users/steamuser/My Documents/EVE/logs/Chatlogs`

Additionally, you may also need to enable "Show Hidden Files" in order to browse to this path. This can be done by 
right-clicking on an empty space in the chooser and selecting the appropriate option. 

## Licences / Acknowledgements / Attributions

This source code is available under [GPL3](https://www.gnu.org/licenses/gpl-3.0.en.html). 

The project uses Qt 5 under the Qt Community Edition licence.

Eve-related data was made available by CCP and obtained from the Eve static data dump. See CCP Copyright Notice below.

Some Eve data was also obtained from https://www.fuzzwork.co.uk/. Thanks heaps for your data dumps!

### Sound Files

The alarm sounds included with IntelPy were sourced from https://freesound.org. Below are credits and licences for these 
sounds. Changes were made to most of these sounds to shorten the length to make them suitable for use with IntelPy. 

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
