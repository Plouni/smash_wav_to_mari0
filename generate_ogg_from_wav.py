import os
import sys
import json
import wave
import array
from lib.functions import system_command, get_folder_final_info

# Loading config variables
with open('config.json') as f:
    config = json.load(f)

# Loading parent output folder where .pcm will be stored
output_path = config['output_path']

# Name of track config file
tracks_file = config['tracks_file']
# Loading temp folder
temp_folder = config['temp_folder']
# sample rate of output file
out_sample_rate = config['out_sample_rate']

current_path = os.getcwd().replace('\\', '/') + '/'

# By default debug is False unless run directly by main
debug = False


def wav_to_looping(path_in, path_out, start_loop, sample_rate):
    """
    Convert wav to 2 wav
    
    :path_in: path to downloaded .brstm
    :path_out: path to output .wav
    :start_loop: sample start looping
    :sample_rate: sample rate
    """
    
    # Check if stereo or convert it
    nchannels, sampwidth, framerate, nframes = check_and_make_stereo(path_in, path_in)
    
    print(nchannels, sampwidth, framerate, nframes)
    
    
    if path_out is None:
        path_out = path_in.split('/')[-1].split('.wav')[0]
        
    if sample_rate is None:
            sample_rate = framerate
    
    
    # If running from script and deciding not looping, only converting to ogg
    if start_loop is not None:
                
        delay = int(start_loop) / int(sample_rate)
        # Intro File
        intro_file = "{}-intro.ogg".format(output_path+path_out)
        if os.path.exists(intro_file):
            os.remove(intro_file)
        
        system_command('ffmpeg -i {} -acodec copy -to {} -c:a libvorbis -q:a 4 "{}"'.format(path_in, delay, intro_file))
        ogg_normalize(intro_file)
    else:
        delay = 0

    # Outro File
    outro_file = "{}.ogg".format(output_path+path_out)
    if os.path.exists(outro_file):
        os.remove(outro_file)
        
    system_command('ffmpeg -i {} -acodec copy -ss {} -c:a libvorbis -q:a 4 "{}"'.format(path_in, delay, outro_file))
    ogg_normalize(outro_file)
    
    os.remove(path_in)
    
    
def ogg_normalize(path):
    """
    normalize ogg
    
    :path: path to normalize
    """
    system_command('ffmpeg-normalize "{}" -o "{}" -c:a libvorbis -f --sample-rate {}'.format(path, path, out_sample_rate))


def check_and_make_stereo(file1, output):
    """
    Check if song is mono and convert it to stereo if that's the case
    
    :file1: input file
    :output: name of pcm output file
    """
    ifile = wave.open(file1)
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = ifile.getparams()
    
    if nchannels == 1:
    
        array_type = {1:'B', 2: 'h', 4: 'l'}[sampwidth]
        left_channel = array.array(array_type, ifile.readframes(nframes))[::nchannels]
        ifile.close()

        stereo = 2 * left_channel
        stereo[0::2] = stereo[1::2] = left_channel

        ofile = wave.open(file1, 'w')
        ofile.setparams((2, sampwidth, framerate, nframes, comptype, compname))
        ofile.writeframes(stereo.tobytes())
        ofile.close()
        
    return nchannels, sampwidth, framerate, nframes


        
# Clean start loop
def parse_start_loop(start_loop):
    if start_loop != "" and start_loop != "json":
        return float(start_loop)
        
    elif start_loop != "json":
        return None
        
    return start_loop


def main():
    print("# This script will convert all .wav files from folder '{}' to .pcm files #\n".format(temp_folder))
    
    debug = True
    

    # If the script was runned directly without parameters
    if len(sys.argv) < 2:            
        # Number of samples in smash website
        start_loop = input("> Enter start loop: number of samples, 'json' (without quotes) if using a file or press Enter if no looping.\n")
        start_loop = parse_start_loop(start_loop)
            
    # If the script was runned directly with parameters sent by the command line interface
    else:
        parse_start_loop(start_loop)

    # List of .wav inside temp folder
    wav_files = [wav for wav in os.listdir(temp_folder) if ".wav" in wav]

    if len(wav_files) == 0:
        input("No .wav files found inside folder {}. Press enter to finish.\n".format(temp_folder))

    else:
    
        tracks=None
        if start_loop == 'json':
            if tracks_file not in os.listdir(temp_folder):
                input("\nNo json found inside temp folder! Press enter to finish.\n".format(output_path))
                raise Exception("No json found!")
                
            with open(temp_folder + tracks_file, 'r') as f:
                tracks = json.load(f)

        for wav in wav_files:
                
            # Loads from json
            if tracks is not None:
                track_number = wav.split('.wav')[0]
                start_loop = tracks[track_number]["Start_loop"]
                if len(start_loop) == 0:
                    start_loop = None
                
            wav_to_looping(temp_folder+wav, None, start_loop, None)
            
        input("\nProcess complete! .ogg available in folder '{}'. Press enter to finish.\n".format(output_path))


if __name__ == "__main__":
    main()