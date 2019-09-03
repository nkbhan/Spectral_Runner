# Spectral Runner

Naren Bhandari, nbhandar\
15-112 Term Project\
Section N

## Dependencies

You will need to install 

* Numpy
* Scipy
* Pygame

You can use `pip` to install these as follows

    pip install numpy scipy pygame

Also, install the font called `MorePerfectDOSVGA.ttf` by opening the `Fonts` folder and opening the ttf file and following the instructions.

## About 
Spectral Runner is rhythm game inspired by Audio Surf and Guitar Hero that takes a song and creates a list of beat onsets for various frequencies, using a beat detection algorithm (see below). Based on this list of beats, one of two game modes is instantiated:

#### Groove Mode
In Groove Mode, the player maneuvers down a track on which blocks are being generated on different parts of the track that correspond to the onset of different musical events (in the midrange frequencies usually). This is inspired by Audio Surf.

#### Drum Mode
In Drum Mode, blocks are still being generated, but now the player cannot move but has three different buttons corresponding to low frequencies (like a bass drum), mid range frequencies (like a snare drum) and high frequencies (like hi-hats). They must be clicked in time with the falling blocks emulating a drum set... sort of. This is inspired by Guitar Hero.

## How To Play

Feel free to add a songs to the `Music` folder.
Just make sure it is a `wav` file. The beat data has been generated for all the songs included, but if a new song is added don't freak out when the audio processing is happening and the game looks frozen. It isn't, I promise.

Pick a mode, pick a song, and go!

#### Groove Mode

Use the arrow keys to move the player left and right. Hit as many blocks as you can in a row. The longer your streak the more bonus points you get.

#### Drum Mode
Use the arrow keys (left, down, right) corresponding to the different player objects to hit the falling blocks in time with the music. Try and time the clicks correctly. If you are off and miss a block, you lose out on bonus points. Like above, the longer your streak, the more bonus point syou get.
Be warned, this mode is **much harder**, so git gud. 


## Beat Detection

Based on the math outlined in [this paper](http://www.nyu.edu/classes/bello/MIR_files/2005_BelloEtAl_IEEE_TSALP.pdf) by Bello, et al. I used a spectral flux feature detector with an adaptive threshold function to find the onsets of beats in various frequency ranges. 

In short, for every chunk of audio data, a discrete fourier transform (from numpy) is calculated to get the frequency spectrum. The spectrum is divided into certain regions. For each region, an average magnitude is calculated. For each successive chunk and frequency range, the difference of these magnitudes is calculated. This is the instantaneous spectral flux. Since I only care about beat onsets and not offsets (starts not ends of beats), the spectral flux is rectified, i.e., the negative values are set to 0.

After this is done, the algorithm calculates an average spectral flux around each chunk and frequency range with a window of 21 chunks centred at the current chunk. 

The next step is calculating the difference of the instantaneous flux and the average flux multiplied by a threshold constant (I sttled on 2 for this value after trial and error). 

Finally, the peaks of this difference are found. These peaks are the beat onsets.

These are stored in an array and indexed in such a way that the indeces can be mapped to time in the song. (Also, the data is stored in a pickle file so that this analysis is only done once). 

## Credits

External Modules used:

* Pygame
* Numpy
* Scipy

explosion sprite sheet from\
[https://mrbubblewand.wordpress.com/](https://mrbubblewand.wordpress.com/)

'more perfect dos vga' font from\
[http://laemeur.sdf.org/fonts/](http://laemeur.sdf.org/fonts/)

beat detection paper\
[http://www.nyu.edu/classes/bello/MIR_files/2005_BelloEtAl_IEEE_TSALP.pdf](http://www.nyu.edu/classes/bello/MIR_files/2005_BelloEtAl_IEEE_TSALP.pdf)

Inspired by Audio Surf and Guitar Hero

MVC game loop design inspired by 112 lecture notes

Songs included

* *Accelerated* by Miami Nights 1984
* *Books of War* by MF Doom ft. RZA
* *Cut and Run* by Kevin Macleod
* *Decay* by Home
* *Ephemeral* by Intervals
* *Hypergiant* by Nick Johnston
* *Life's A Bitch* by Nas ft. AZ
* *Remembrance Day* by God Is an Astronaut
* *Sleepy Tea* by Chon
* *Spoken* by Etherwood
* *Starship Trooper* by Yes
* *Tank* by The Seatbelts
* *Teen Pregnancy* by Blank Banshee
* *Ties That Bind* by Alter Bridge
* *Time Flies* by Porcupine Tree
