import requests
from bs4 import BeautifulSoup
import os
import sys
import urllib
import json
import generate_ogg_from_wav
from lib.functions import system_command, get_folder_final_info
import socket

import requests

socket.setdefaulttimeout(120)

# Loading config variables
with open('config.json') as f:
    config = json.load(f)

# Loading parent output folder where .pcm will be stored
output_path = config['output_path']

# Loading tools folder where msupcm.exe and wav2msu.exe are stored
tools_folder = config['tools_folder']

current_path = os.getcwd().replace('\\', '/') + '/'
# Loading temp folder where downloaded .pcm will be stored
temp_folder = config['temp_folder']

# If download only, no converting/ normalizing
download_only = config['download_only']


headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    
url = "https://smashcustommusic.net/song/"


def download_song(song_id, name_song, path_folder, format='brstm'):
    """
    Download a song from smash website using its id
    
    :song_id: id of song in smash website
    :name_song: name of song
    :path_folder: path to downloaded file
    :return: name of output song
    """
    
    URL_down = "https://smashcustommusic.net/{}/{}".format(format, song_id)

    song_file = '{}.{}'.format(name_song, format)
    path_out = path_folder + song_file

    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "en-US,en;q=0.9,fr;q=0.8",
"Connection": 'keep-alive',
"Cookie": "theme=1",
"Host": "smashcustommusic.net",
"Referer": "https://smashcustommusic.net/song/" + str(song_id),
"sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
"sec-ch-ua-mobile": "?0",
"Sec-Fetch-Dest": "document",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-Site": "same-origin",
"Sec-Fetch-User": "?1",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}

    r=requests.get(URL_down, headers=headers)
    open(path_out, 'wb').write(r.content)
        
    return song_file
    
    
def get_metadata(id_song):
    """
    Get song metadata (such as looping points and sampling rate) using song id
    
    :song_id: id of song in smash website    
    :return: song metadata as dict
    """
    
    url = "https://smashcustommusic.net/song/" + str(id_song)
    req = requests.get(url , headers)
    soup = BeautifulSoup(req.content, 'html.parser')

    rows = soup.find_all("tr")
    data = {}
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        if len(cols)==2:
            # Get rid of empty values
            data[cols[0]]= cols[1]
            
    return data
    
 
def brstm_to_wav(path_in, path_out, remove_brstm=True):
    """
    Convert brstm to 16 bit wav
    
    :path_in: path to downloaded .brstm
    :path_out: path to output .wav
    """
    
    system_command(tools_folder + 'VGAudioCli.exe "{}" "{}" -f pcm16'.format(path_in, path_out))
    if remove_brstm:
        os.remove(path_in)
        

def main():
    print('# This script will download a .brstm file from smashcustommusic.net and convert it to a .pcm file #\n')

    # If the script was runned directly without parameters
    if len(sys.argv) < 2:
        id_song = int(input('> Enter Song ID:\n'))
        song_out = input('> Enter Name of output song (without ext). Just press Enter if not needed:\n')
        if len(song_out) == 0:
            song_out = None
            
    # If the script was runned directly with parameters sent by the command line interface
    else:
        id_song = int(sys.argv[1])
        if len(sys.argv) > 2:
            song_out = sys.argv[2]
        else:
            song_out = None
         
    smash_brstm_process(id_song, song_out)
    
    input("\nProcess complete! .ogg available in folder '{}'. Press enter to finish.\n".format(output_path))

    
def smash_brstm_process(id_song, song_out, verbose=True, stop_if_exists=False):
    """
    Download brstm from smashcustommusic
    Convert brstm to pcm if auto_convert_brstm_to_pcm_with_vgaudio_librosa is true
    
    :id_song: id of song in smash website
    :song_out: song nale without ext
    :verbose: True if we print info. Should be False if called from another script
    :stop_if_exists: True if we want to stop process if song already downloaded
    :return: 0 if song was skipped because it already exists. 1 otherwise 
    """

    data = get_metadata(id_song)
            
    sample_rate = data['Sampling Rate:']
    start_loop = data['Start Loop Point:']
    # end_loop = data['End Loop Point:']
    name_song = data['Song Name:'].replace(' ', '_').replace(':', '').replace('/', '').replace('/', '')

    if verbose:
        print("Downloading", name_song)
    
    # Path to downloaded song
    path_brstm_folder = current_path + temp_folder + '/'

    if not download_only :
        # Download .brstm song and retrieve name of brstm file (with extension)
        brstm_file = download_song(id_song, name_song, path_brstm_folder, format='brstm')
               
        wav_file = name_song + '.wav'
        # Convert brstm to .wav
        brstm_to_wav(path_brstm_folder + brstm_file, path_brstm_folder + wav_file)
        
        # Loop and normalize wav to ogg
        generate_ogg_from_wav.wav_to_looping(path_brstm_folder + wav_file, song_out, start_loop, sample_rate)
        
        
    else:
        # Download .brstm song and retrieve name of brstm file (with extension)
        download_song(id_song, name_song, path_folder_final, format='brstm')
          
    return 1
    

    
if __name__ == "__main__":
    main()