import os
import sys
import json

# Loading config variables
with open('config.json') as f:
    config = json.load(f)

# Name of track config file
tracks_file = config['tracks_file']

def main():
    print('# This script will generate a track file that you can fill if doing looping manually #\n')

    # If the script was runned directly without parameters
    if len(sys.argv) < 2:
        path = input('> Enter path to folder where music are stored:\n')
            
    # If the script was runned directly with parameters sent by the command line interface
    else:
        path = sys.argv[1]


    tracks = {mus: {"Start_loop": ""} for mus in os.listdir(path) if mus.split('.')[-1] in ["ogg", "wav", "mp3"]}
    
    with open(tracks_file, "w+") as f:
        json.dump(tracks, f, indent = 4)
            
    input("Process complete! Press enter to finish.\n")
    
if __name__ == "__main__":
    main()