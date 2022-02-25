import seaborn as sns
import pandas as pd
from utils import read_excel, read_yaml 
import matplotlib.pyplot as plt

def calculate_addition(x, y):
    if isinstance(x, int) and isinstance(y, int):
        return x + y
    else:
        print("X and Y should be integers")
        return

def read_metadata(path_to_metadata):
    print("reading the metadata")
    metadata = read_excel(path_to_metadata)
    return metadata

def show_metdata_graphs(metadata, config):
    
    # sns.histplot(data = metadata, x= 'Mouse Genotype', hue = 'Location Recorded', multiple="stack")
    # plt.xticks(rotation=45)
    # plt.show()
    
    metadata['Mouse Genotype'].value_counts().plot(kind='pie', shadow=True, autopct='%1.1f%%')
    plt.show()

    metadata['With Cable'].value_counts().plot(kind='pie', shadow=True, autopct='%1.1f%%')
    plt.show()
    
    metadata['Location Recorded'].value_counts().plot(kind='pie', shadow=True, autopct='%1.1f%%')
    plt.show()

def main(config):

    print("Started the main process")
    
    ### Extract Metadata
    metadata = read_metadata(config['path_to_metadata'])
    
    ### Analyze Metadata
    if config['verbose']:
        print(metadata.describe())
    
    if config['present_graphs']:
        show_metdata_graphs(metadata, config)

    

if __name__ == "__main__":
    config = read_yaml('config.yaml') 
    main(config)
