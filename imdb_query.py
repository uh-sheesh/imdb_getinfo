# -*- coding: utf-8 -*-
"""
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
"""

import imdb_get as i_get
import imdb_search as i_search
import re, sys, os

# prints a message on how to use the program
def usage():
    print('Follow these instructions to use the program:',
          '\n1) If using an input file, make sure all files are located in the data folder.',
          '\n   Input file should be a single column, with heading.',
          '\n2) Use either: \'python imdb_query.py input_name.csv output_name.csv\'',
          '\n   or \'python imdb_query.py \'itemname\' output_itemname.csv.',
          '\n3) The output file will be saved in the data folder with the chosen filename.',
          '\n*Note: This script is dependent on imdb_search.py and imdb_get.py.')

def main(i_fname, o_fname):
    #Step 1: use the imdb_search.py file to search for general info
    #check if a csv file is being passed or the name of an item
    if re.search(r'.csv', i_fname):
        i_search.main(i_fname, 'search_results.csv', 'FILE')
    else:
        i_search.main(i_fname, 'search_results.csv', 'ITEM')

    #Step 2: use the imdb_get.py file to search for additional info
    #based on the general info pulled in Step 1.
    i_get.main('search_results.csv', o_fname)

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