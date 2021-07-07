# -*- coding: utf-8 -*-
"""
This uses the imdbPY library to access information about IMDB movies and shows.
The script uses a list of textual titles for the request, and saves the movieID,
year, and plot into a csv file.

Initially created on Saturday July 3 2021 by @author: uh-sheesh.

To use the script, call 'python input_filename.csv output_filename.csv' from 
the command prompt with appropriate names for input and output.
"""

#import libraries
import imdb
import sys
import os
import pandas as pd
from pathlib import Path
import time
from tqdm import tqdm


def main(i_fname, o_fname):
    #create a working class of the IMDB parser
    ia = imdb.IMDb()

    #input file name
    input_file = i_fname  # TODO change to argument
    #get path for current working directory and add desired output subfolder
    output_dir = Path(os.getcwd() + '/data')

    #string to handle any errors
    error_message = 'Errors during search:'    
    
    #read csv file and create a data frame
    df = pd.DataFrame(data=pd.read_csv(output_dir / input_file, 
                                       index_col= ['IMDBCode', 'Title', 'Year', 'Plot'], 
                                       usecols=['IMDBCode', 'Title', 'Year', 'Plot']).reset_index())
    
    # Declare a list that is to be converted into a column
    new_cols = ['IMDBCode', 'Title', 'Year', 'Plot', 'Type', 'Season', 
                'EpisodeNo', 'EpisodeTitle', 'CombGenre', 'Genre1', 'Genre2', 'Genre3',
                'Genre4', 'Genre5', 'DurationMins', 'DurationHours']
    
    #create a dataframe that will be used for the final
    final_df = pd.DataFrame(columns= new_cols)

    #loop through each item and compile data to be saved back to csv
    for new_item in tqdm(df['IMDBCode']):
        #search for the item based on the ID
        items = ia.get_movie(new_item)
        
        #add each item to the data dictionary
        #try except is used for each item as IMDB may have missing information
        data = {}
        try: data.update({'IMDBCode': items.movieID})
        except KeyError: pass
        try: data.update({'Title': items['title']})
        except KeyError: pass
        try: data.update({'Year': items['year']})
        except KeyError: pass
        try: data.update({'Plot': items['plot'][0]})
        except KeyError: pass
        try: data.update({'Type': items['kind']})
        except KeyError: pass
        try: data.update({'DurationMins': items['runtimes'][0]}) 
        except KeyError: pass
        try: data.update({'DurationHours': int(items['runtimes'][0]) / 60})
        except KeyError: pass
    
        #genre counter and combined genre variables
        indv_genre = 0
        comb_genre = ''
        
        #check if atleast 1 genre is available
        try:
            #search and add all the genres
            while indv_genre < len(items.data['genres']):
                
                #create a string with the column title i.e. Genre1, Genre2
                g = 'Genre' + str(indv_genre+1)
                
                #collect the first 3 genres and combine them
                if indv_genre < 3:
                    comb_genre += items.data['genres'][indv_genre] + ', '
                
                #update the genres to the data dictionary
                data.update({g: items.data['genres'][indv_genre]})

                #incrememnt the genre number
                indv_genre +=1
                
        except KeyError: pass
        
        #update the combined genres to the data dictionary
        try: data.update({'CombGenre': comb_genre[:-2]})
        except KeyError: pass
    
        #create a temporary dataframe that will be appended to the final dataframe
        item_df = pd.DataFrame(data, index=[0])
        
        #get info specifically for tv shows such as episodes
        #then update with episode info
        if items['kind'] == 'tv series':
            #update the item if it is a tv series
            ia.update(items, 'episodes')
            
            #loop to address each season of a show
            for indv_season in sorted(items['episodes'].keys()):
                all_season = items['episodes'][indv_season]
                
                #loop to address each episode within a season of a show
                for indv_episode in all_season:
       
                    #update the tv series specific data to the data dictionary
                    try: data.update({'Season': indv_season})
                    except KeyError: pass
                    try: data.update({'EpisodeNo': indv_episode})
                    except KeyError: pass
                    try: data.update({'EpisodeTitle': all_season[indv_episode]['title']})
                    except KeyError: pass
                    try: data.update({'DurationMins': items['runtimes'][0]})
                    except KeyError: pass
                    try: data.update({'DurationHours': int(items['runtimes'][0]) / 60})
                    except KeyError: pass
                    
                    #add theupdated data dictionary to the dataframe
                    item_df = data

                    #append the temporary dataframe to the final dataframe
                    final_df = final_df.append(item_df, ignore_index=True)
        else:
            #if movie append the temporary dataframe to the final dataframe
            final_df = final_df.append(item_df, ignore_index=True)

        #add to the progress bar on each iteration
        time.sleep(1)
        
    #print complete message
    if error_message != 'Errors during search:':
        print(error_message)

    #export results to a csv file1
    output_file = o_fname
    output_dir.mkdir(parents=True, exist_ok=True)

    # can join path elements with / operator
    final_df.to_csv(output_dir / output_file)

#prints a message on how to use the program
def usage():
    print('Follow these instructions to use the program:',
          '\n1) Make sure all files are located in the data folder.',
          '\n2) Command should be in \'python input_filename.csv output_filename.csv\' format.',
          '\n3) Input file should be a single column, with heading.',)

if __name__ == '__main__':
    try:
        main(sys.argv[1], sys.argv[2])
    except IndexError:
        usage()
    except KeyboardInterrupt:
        print('\nProgram Interrupted!')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)