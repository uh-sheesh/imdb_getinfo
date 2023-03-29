# -*- coding: utf-8 -*-
"""
This uses the imdbPY library to access information about IMDB movies and shows.
The script uses a list of textual titles for the request, and saves the movieID,
year, and plot into a csv file.

Initially created on Saturday July 3 2021 by @author: uh-sheesh.
Last updated: November 26, 2022.

To use the script, call either:
- 'python imdb_search.py input_name.csv output_name.csv'
  i.e. 'python imdb_search.py config.csv search_output.csv' or
- 'python imdb_search.py 'itemname' output_itemname.csv'
  i.e. 'python imdb_search.py 'Anthony Bourdain: Parts Unknown' output_itemname.csv'
from the command prompt with appropriate names for input and output.

TODO need to rewrite now a helper function
"""

#import libraries
from imdb import Cinemagoer
import sys
import os
import re
import pandas as pd
from pathlib import Path


def select_title(i_fname, item_type):

    # create a working class of the IMDB parser
    ia = Cinemagoer()

    # search for the item based on the textual name
    items = ia.search_movie(i_fname)

    # if a single item, ask about ambiguity, else just take the first item
    if item_type == 'ITEM':
        print('Found ' + str(len(
            items)) + ' items based on search \'' + i_fname + '\'.')

        # checks if each item exists and then copies
        item_counter = 1
        for item in items:

            try:
                kind = item['kind']
            except:
                kind = 'UNKNOWN'

            try:
                title = item['title']
            except:
                title = 'UNKNOWN'

            try:
                movieID = item.movieID
            except:
                movieID = '0000001'

            print(item_counter, ' - ', kind, ' - ', title, movieID)
            item_counter += 1

        # save user selection
        selected_option = input(
            'Which item would you like to select? Enter the number: ')

        selected_item = items[int(selected_option)-1]

    else:
        selected_item = items[0]

    return selected_item.movieID


def main(i_fname, type_search):

    # select which title out of all if the name is ambiguous
    mySelectedMovieID = select_title(i_fname, type_search)

    print("Aha! The movieID is: ", mySelectedMovieID)

    end_message = input('Enter any key to Exit.')


if __name__ == '__main__':

    try:
        entered_text = input('Enter the name of an item: ')
        main(entered_text, 'ITEM')

    except KeyboardInterrupt:
        print('\nProgram Interrupted!')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
