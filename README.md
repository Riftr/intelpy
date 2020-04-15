# IntelPy

> IntelPy is a simple, cross-platform chat log monitor for the game Eve Online 
>
> ![IntelPy](https://i.imgur.com/HmTz4rl.png)
>

## How to get started with IntelPy

### Windows

1. Download the latest Windows release from [here](https://github.com/Riifta/intelpy/releases/latest).
2. Extract the contents to a directory 
3. Run IntelPy.exe
 
### Linux

#### Pre-built package

1. Download the latest Linux tar.gz release [here](https://github.com/Riifta/intelpy/releases/latest)
2. Extract the contents to a directory such as /opt/intelpy 
3. Run the IntelPy execuitable 

## Required packages (for building or running the source)
 
The versions below aren't hard requirements, only what IntelPy has been tested on.

* Python 3 3.7 
* PyQt 5 5.14.1 
* pathlib / pathlib2
* Watchdog 0.10.2 
* Networkx 2.4
* Playsound 1.2.2 
* PyGObject 3.36.0 

### Pip one-liner
```shell
$ sudo pip install pyqt5 pathlib watchdog networkx playsound pathlib2 pygobject
```
Once required packages are installed, run ```python Intelpy.py``` to start the application. 

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
