# -*- coding: utf-8 -*-
"""
This uses the imdbPY library to access information about IMDB movies and shows.
The script uses a list of textual titles for the request, and saves the movieID,
year, and plot into a csv file.

Initially created on Saturday July 3 2021 by @author: uh-sheesh.

To use the script, call either:
- 'python imdb_search.py input_name.csv output_name.csv'
  i.e. 'python imdb_search.py config.csv search_output.csv' or
- 'python imdb_search.py 'itemname' output_itemname.csv'
  i.e. 'python imdb_search.py 'Anthony Bourdain: Parts Unknown' output_itemname.csv'
from the command prompt with appropriate names for input and output.
"""

#import libraries
import imdb
import sys
import os
import re
import pandas as pd
from pathlib import Path
import time
from tqdm import tqdm

def main(i_fname, o_fname, type_search):
    # create a working class of the IMDB parser
    ia = imdb.IMDb()

    # input item name, either file or the search item
    input_item = i_fname
    # get path for current working directory and add desired output subfolder
    output_dir = Path(os.getcwd() + '/data')

    # string to handle any errors
    error_message = 'Errors during search:'

    # if the item is a file, add the csv to data frame, else just add the item
    if type_search == 'FILE':
        # read csv file and create a data frame
        df = pd.DataFrame(data=pd.read_csv(output_dir / input_item, index_col=0),
                          columns=['IMDBCode', 'Year', 'Plot'])
    elif type_search == 'ITEM':
        df = pd.DataFrame(columns=['IMDBCode', 'Year', 'Plot'])
        df['Title'] = [i_fname]
        df.set_index('Title', inplace=True)

    # convert the Plot column type to string
    df['Plot'] = df['Plot'].astype("string")

    # loop through each item and compile data to be saved back to csv
    for i in tqdm(df.index):
        # search for the item based on the textual name
        items = ia.search_movie(i)

        # if IMDB Movie code was found, if not return to beginning of loop
        if not items:
            error_message += '\n\'' + i + '\' - ID could not be found based on title.'
            continue
        else:
            # if IMDB Movie code is found, save code to dataframe
            df.at[i, 'IMDBCode'] = items[0].movieID

        # use the get_movie method to get more complete info about the ID
        item = ia.get_movie(df.at[i, 'IMDBCode'])

        # save the first plot found if there is a plot
        try:
            df.at[i, 'Plot'] = item['plot'][0]
        except:
            error_message += '\n\'' + i + '\' - Plot could not be found.'

        # save the year if there is a year
        try:
            df.at[i, 'Year'] = item['year']
        except:
            error_message += '\n\'' + i + '\' - Year could not be found.'

        # add to the progress bar on each iteration
        time.sleep(1)

    # print error message
    if error_message != 'Errors during search:':
        print(error_message)

    # print complete message
    print('Search complete for', len(df.index), 'search terms!')

    # export results to a csv file1
    output_item = o_fname
    output_dir.mkdir(parents=True, exist_ok=True)

    # can join path elements with / operator
    df.to_csv(output_dir / output_item)

# prints a message on how to use the program
def usage():
    print('Follow these instructions to use the program:',
          '\n1) If using an input file, make sure all files are located in the data folder.',
          '\n   Input file should be a single column, with heading.',
          '\n2) Use either: \'python imdb_search.py input_name.csv output_name.csv\'',
          '\n   or \'python imdb_search.py \'itemname\' output_itemname.csv.',
          '\n3) The output file will be saved in the data folder with the chosen filename.')

if __name__ == '__main__':
    try:
        # check if a csv file is being passed or the name of an item
        if re.search(r'.csv', sys.argv[1]):
            main(sys.argv[1], sys.argv[2], 'FILE')
        else:
            main(sys.argv[1], sys.argv[2], 'ITEM')

    except IndexError:
        usage()
    except KeyboardInterrupt:
        print('\nProgram Interrupted!')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)