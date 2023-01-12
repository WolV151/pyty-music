# pyty-music
A CLI-based YouTube Music application.

## About
This is a basic YouTube Music app. It does not have a graphical user interface and is fully CLI-based. The main reason for creating this is because my old
laptop was not so powerful and could not run a video game and a browser with music so smoothly. I loved listening to YouTube Music as a radio so I
decided to create this app with the unofficial [ytmusicapi](https://pypi.org/project/ytmusicapi/). I needed a basic program that can play songs continuously
in the manner of YouTube Music.

## Usage 
The main program is in mus_main.py. An input for searching will immediately be prompted. Enter the name of a song or a video. The possible results will
be displayed in a list, along with the type - video or song. Select a result. The app will create a list with similar songs after the search result. After
all the song links in the list have been converted to playable media, they will be played with VLC media player.

The search input will be available again. The newly searched songs will be appended to the end of the list.

Additionally a special input (default "!c") can be entered to enter "control mode". In this mode, songs can be skipped in the list, the volume can be controlled and the player can be paused.

## Configuration
Default keys for "control mode" can be viewed and edited in mus_conf.ini. Some default values can also be edited.
