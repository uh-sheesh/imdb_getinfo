# -*- coding: utf-8 -*-
'''
*** To be updated
This uses the imdbPY library to access information about IMDB movies and shows.
The script combines 2 other python scripts (imdb_search.py and imdb_get.py).
The imdb_search.py script uses a list of textual titles for the request, and
saves the movieID, year, and plot into a csv file. The imdb_get.py uses a list 
of textual titles for the request, and saves the IMDBCode, title, year, plot, 
type, season, episode no, episode title, genres, and duration to a csv file.

Initially created on Thursday July 29 2021 by @author: uh-sheesh.

To use the script, call either:
- 'python imdb_search.py input_name.csv output_name.csv'
  i.e. 'python imdb_query.py config.csv search_output.csv' or
- 'python imdb_search.py 'itemname' output_itemname.csv'
  i.e. 'python imdb_query.py 'Anthony Bourdain: Parts Unknown' output_itemname.csv'
from the command prompt with appropriate names for input and output.


*** all functionality working, needs to be cleaned up and new comments outlined
'''

import imdb_get as i_get
import imdb_search as i_search
import sys
import os
import pandas as pd

# system variables
cont_app = False

# get path for current working directory and add desired output subfolder
output_dir = os.getcwd() + '/data/'

# prints a message on how to use the program


def usage():
    print('Follow these instructions to use the program:',
          '\n1) If using an input file, make sure all files are located in the data folder.',
          '\n   Input file should be a single column, with heading.',
          '\n2) Use either: \'python imdb_query.py input_name.csv output_name.csv\'',
          '\n   or \'python imdb_query.py \'itemname\' output_itemname.csv.',
          '\n3) The output file will be saved in the data folder with the chosen filename.',
          '\n*Note: This script is dependent on the helper functions for imdb_search.py and imdb_get.py.')


def query(i_fname):
    # Step 1: use the imdb_search.py file to search for general info
    movieID = i_search.select_title(i_fname, 'ITEM')

    # Step 2: use the imdb_get.py file to search for additional info
    # based on the general info pulled in Step 1.
    title_data, episode_data = i_get.get_details(movieID)

    #print('Universal Data:\n', title_data)
    #print('Series Data:\n', episode_data)
    #print("got data!")

    return title_data, episode_data


def export_data(title_data, episode_data, o_fname):
    # save the dictionary and list to excel file
    dfuni = pd.DataFrame(data=title_data, index=[1])
    dfseries = pd.DataFrame(data=episode_data)

    with pd.ExcelWriter(output_dir + o_fname) as writer:
        dfuni.to_excel(writer, sheet_name='Series_Data')
        dfseries.to_excel(writer, sheet_name='Temporal_Data')
    print("Dictionaries converted into excel...")


def input_validate(input_item):
    # declare the messages that will be used for both the title and location input
    title_items = ['Enter the title of the movie, tv-show or item: ',
                   'You cannot leave the title blank.', 'Search term: ']
    location_items = ['Enter the output file name, or leave blank for default: ',
                      'Default location will be used.', 'Save location: ']
    item_array = []

    while True:
        if input_item == 'title':
            item_array = title_items
        elif input_item == 'location':
            item_array = location_items

        entered_input = input(item_array[0])
        if entered_input == '' and input_item == 'title':
            print(item_array[1])
            continue
        if entered_input == '' and input_item == 'location':
            entered_input = 'results.xlsx'
            print(item_array[1])
            print(item_array[2], entered_input)
            break
        else:
            print(item_array[2], entered_input)
            break

    return entered_input


def file_openner(open_file, save_location):
    if open_file.lower() == 'y' or open_file.lower() == 'yes':

        file = output_dir + save_location

        # if windows
        if os.name == 'nt':
            os.startfile(file)
        # if mac or linux
        else:
            os.system("open data/" + save_location)
        print('Output file opened with default application.')
    else:
        print('The search results have been saved in the selected location.')


def main():

    # validate the title and save location
    title_input = input_validate('title')
    save_location_input = input_validate('location')

    # attempt to query
    title_data, episode_data = query(title_input)

    # try to export the data to excel file in multiple sheets
    export_data(title_data, episode_data, save_location_input)

    # ask user if app should open the output file
    open_file_input = input('Open the results file (Y/N)? ')
    file_openner(open_file_input, save_location_input)

    print('Thanks for using this application!')
    my_input = input('Enter any key to exit.')


if __name__ == '__main__':
    try:
        main()

    except IndexError:
        usage()
    except KeyboardInterrupt:
        print('\nProgram Interrupted!')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
