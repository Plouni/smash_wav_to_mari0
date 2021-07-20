# smash_wav_to_mari0

Generate ogg files that you can use in Mari0 AE, by downloading songs found in smashcustommusic.net  
  
Why this website? I don't work for them but it has looping points for almost every song! And with Python it's easy to download the song, retrieve the looping points and split it in two files (regular .ogg and -intro.ogg file) that you can use in Mari0 AE!  
With my code, songs are also normalized (so they are not too loud) and compressed (to save space).


## Requirements
To download the songs, you'll need to have Python 3 installed with the following libraries:
* `requests`
* `bs4`
* `urllib`
* `ffmpeg-normalize`

You'll also need to have ffmpeg installed on your PC (and, if using windows, you'll also need to add ffmpeg to your PATH variable). 


## Project structure
.  
|_ lib/  
  |_ `__init__.py`  
  |_ `functions.py`   
|_ output/  
|_ tools/  
  |_ `VGAudioCli.exe`  
|_ temp/  
|_ `config.json`  
|_ `download_from_id_song.py`  
|_ `download_song_from_id_game.py`  
|_ `generate_pcm_from_wav.py`  
|_ `generate_tracks_file.py`  
|_ `Readme.md`  

Folder details:
* lib: folder that contains common functions used by the python scripts
* output: default folder where output .ogg will be stored (can be changed inn config file)
* tools:
  * `VGAudioCli.exe` is used here to convert a brstm file to a wav file
* temp: temporary folder where downloaded wav and generated ogg will be stored

It is also important to have the config and all python files at the root of the project or it won't work.


## How to use

### Simple Usage
The easiest way is to simply click the Python scripts. They all have different uses:
* `download_from_id_song.py`: asks for a song id from smashcustommusic.net and will download the song and convert it to an ogg file. You can also choose the name of the output ogg file
* `download_song_from_id_game.py`: asks for a game id from smashcustommusic.net and will download all songs from this game and convert them to ogg files
* `generate_ogg_from_wav.py`: transforms wav files inside the temp folder to normalized ogg files. You can provide the starting loop point manually or by providing a json file (more on this below)
* `generate_tracks_file.py`: generate a json file that you can use if you want to use your own looping points (more on this below)

To get the game id from smashcustommusic.net, take the number at the end of the URL of a game.  
For example: `Zelda ALTTP` URL is https://smashcustommusic.net/game/95 ==> game ID is `95`

To get the song id from smashcustommusic.net, take the number at the end of the URL of a song.  
For example: `Zelda ALTTP Castle Theme` URL is https://smashcustommusic.net/song/11816 ==> song ID is `11816`

### Command line Usage
You can also run the Python script with the command line by using:  
`python name_of_python_script.py param1 param2 param3`  
But by doing this, you have to enter the parameters in the right order. Here is the order for each script:
* `download_from_id_song.py`: song id, name of output song (optional)
* `download_song_from_id_game.py`: game id
* `generate_ogg_from_wav.py`: start looping point (enter a number, json if using a json file or enter nothing if not needed).
* `generate_tracks_file.py`: path of the folder where the music you want to convert are stored

### Using your own looping points
If the song you want to loop is not on the smashcustommusic.net website, or if you want to use your own looping point, here are the steps you'll have to follow:  
1. move the songs you want to convert to the `temp` folder. These should be wav files already trimmed at the end of the loop point
2. run `generate_tracks_file.py` and you should select the `temp` folder. This will generate a json file at the root of the project
3. move the json file generated in step 2 to the `temp` folder
4. edit the json file and set the start loop points you want to use
5. run `generate_ogg_from_wav.py` and choose `json` as the start loop point


## Config file
Here are the settings you can customize in the config file:
* `output_path`: path to output folder where output files will be stored
* `out_sample_rate`: sample rate of output ogg file. Lower means less quality
* `tracks_file`: name of json file that will be used if using `generate_ogg_from_wav.py` with a json file
* `stop_words`: list of "stop words". Any song that contains any of the "stop words" won't be downloaded (if you want to exclude remixes for example)
* `temp_folder`: path to temp
* `tools_folder`: path to tools folder
* `download_only`: set it to true if you only want to use this script to download songs from smashcustommusic.net as brstm files


## Credits 
Thealexbarney is the creator of `VGAudioCli.exe`