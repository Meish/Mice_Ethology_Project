# import seaborn as sns
# import pandas as pd
from utils import read_excel, read_yaml, read_json
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import glob
from genericVideo import vidReader


def read_metadata(path_to_metadata):
    print("reading the metadata")
    metadata = read_excel(path_to_metadata)
    return metadata


def show_metdata_graphs(metadata):

    metadata["Mouse Genotype"].value_counts().plot(
        kind="pie", shadow=True, autopct="%1.1f%%"
    )
    plt.show()

    metadata["With Cable"].value_counts().plot(
        kind="pie", shadow=True, autopct="%1.1f%%"
    )
    plt.show()

    metadata["Location Recorded"].value_counts().plot(
        kind="pie", shadow=True, autopct="%1.1f%%"
    )
    plt.show()

def exploratory_analysis(path_to_folder):
        
        video = vidReader(os.path.join(path_to_folder, 'Mouse158_20161017_18-02-32_Top_J85.seq'))
        print(video.toString())

    ### Extract one frame from the movie
        frame_num = 10
        mouse_num = 0
    
        frame = video.getFrame(frame_num)
        plt.imshow(frame)
        plt.show()

    ### show pose estimates for this image
        json_result = read_json(os.path.join(path_to_folder, 'Mouse158_20161017_18-02-32_pose_top_v1_8.json'))
        npz_result = np.load(os.path.join(path_to_folder, 'Mouse158_20161017_18-02-32_raw_feat_top_v1_8.npz'))
        npz_result.f.bbox[:,:, frame_num]
        npz_result.f.data_smooth[mouse_num,frame_num, :]


def main(config):

    print("Started the main process")

    ### Extract Metadata
    metadata = read_metadata(config["path_to_metadata"])

    ### Analyze Metadata
    if config["verbose"]:
        print(metadata.describe())

    ### visualize metadata
    if config["present_graphs"]:
        show_metdata_graphs(metadata)
        

    ### read a movie
    examples_folder = config['path_to_examples_folder']
    path_to_example_directory = os.path.join(examples_folder, config['example_name'])
    if config["exploratory analysis"] and os.path.isdir(path_to_example_directory):
        exploratory_analysis(path_to_example_directory)
    
    ### create a small gui that receives images and annotates them. 
    example_subdirectories = os.listdir(examples_folder)
    assert(len(example_subdirectories)) == 5
    
    
    print("process finished")






if __name__ == "__main__":
    config = read_yaml("config.yaml")
    main(config)
    sys.exit(0)
