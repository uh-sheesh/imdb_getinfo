# -*- coding: utf-8 -*-
"""
This uses the imdbPY library to access information about IMDB movies and shows.
The script uses a list of textual titles for the request, and saves the IMDBCode,
title, year, plot, type, season, episode no, episode title, genres, and duration
to a csv file.

Initially created on Saturday July 3 2021 by @author: uh-sheesh.

To use the script, call 'python input_filename.csv output_filename.csv' from 
the command prompt with appropriate names for input and output.

TODO: Need to update, now a helper function
"""

#import libraries
import imdb
from imdb import Cinemagoer
from imdb import IMDbDataAccessError
import logging
import sys
import os
import pandas as pd
from pathlib import Path
import time
from tqdm import tqdm


def get_details(submitted_movieID):

    # create a working class of the IMDB parser
    ia = Cinemagoer(accessSystem='http', reraiseExceptions=True)

    #item = ia.get_movie(submitted_movieID)

    try:
        # logger throws access errors if the input MovieID does not exist
        # to work around this, the program will just leave these records blank
        logger = logging.getLogger('imdbpy')
        logger.disabled = True
        ia = imdb.IMDb(accessSystem='http',
                       reraiseExceptions=True, loggingLevel="CRITICAL")

        # attempt to save the movie details
        item = ia.get_movie(submitted_movieID)
    except IMDbDataAccessError:
        err_msg += '\n\'' + str(submitted_movieID) + \
            '\' - IMDB Movie code returned no results.'

    try:
        # update the item if it is a tv series
        ia.update(item, 'episodes')
    except:
        pass

    # add each item to the data dictionary
    # try except is used for each item as IMDB may have missing information
    universal_data = {}
    series_data = []

    try:
        universal_data.update({'IMDBCode': item.movieID})
    except KeyError:
        universal_data.update({'IMDBCode': ''})
    try:
        universal_data.update({'Title': item['title']})
    except KeyError:
        universal_data.update({'Title': ''})
    try:
        universal_data.update({'Year': item['year']})
    except KeyError:
        universal_data.update({'Year': ''})
    try:
        universal_data.update({'Series Year': item['series years']})
    except KeyError:
        universal_data.update({'Series Year': ''})
    try:
        universal_data.update({'Plot': item['plot'][0]})
    except KeyError:
        universal_data.update({'Plot': ''})
    try:
        if item['kind'] == 'tv series' or item['kind'] == 'tv mini series':
            universal_data.update({'Type': 'Show'})
        elif item['kind'] == 'movie':
            universal_data.update({'Type': 'Movie'})
        else:
            universal_data.update({'Type': item['kind']})
    except KeyError:
        universal_data.update({'Type': ''})
    try:
        universal_data.update({'DurationMins': item['runtimes'][0]})
    except KeyError:
        universal_data.update({'DurationMins': ''})
    try:
        universal_data.update({'DurationHours': int(item['runtimes'][0]) / 60})
    except KeyError:
        universal_data.update({'DurationHours': ''})
    try:
        universal_data.update({'CommunityRating': item['rating']})
    except KeyError:
        universal_data.update({'CommunityRating': ''})
    try:
        universal_data.update({'CommunityVotes': item['votes']})
    except KeyError:
        universal_data.update({'CommunityVotes': ''})
    try:
        all_cast_list = []
        for cast_member in item.data['cast']:
            all_cast_list.append(cast_member['name'])

        all_cast_string = ', '.join(all_cast_list)

        universal_data.update({'CastMembers': all_cast_string})
    except:
        universal_data.update({'CastMembers': ''})

    try:
        # loop to address each season of a show
        for indv_season in sorted(item['episodes'].keys()):
            all_season = item['episodes'][indv_season]

            # loop to address each episode within a season of a show
            for indv_episode in all_season:

                episode_data = {}

                # update the tv series specific data to the data dictionary
                # SeasonName and Platform are unavailable on IMDB
                try:
                    episode_data.update({'IMDBCode': item.movieID})
                except KeyError:
                    episode_data.update({'IMDBCode': ''})
                try:
                    episode_data.update(
                        {'SeasonNo': 'Season ' + str(indv_season)})
                except KeyError:
                    episode_data.update({'SeasonNo': ''})
                try:
                    episode_data.update({'EpisodeNo': indv_episode})
                except KeyError:
                    episode_data.update({'EpisodeNo': ''})
                try:
                    episode_data.update(
                        {'EpisodeTitle': all_season[indv_episode]['title']})
                except KeyError:
                    episode_data.update({'EpisodeTitle': ''})
                """
                try:
                    episode_data.update({'DurationMins': item['runtimes'][0]})
                except KeyError:
                    episode_data.update({'DurationMins': ''})
                try:
                    episode_data.update(
                        {'DurationHours': int(item['runtimes'][0]) / 60})
                except KeyError:
                    episode_data.update({'DurationHours': ''})
                """
                try:
                    episode_data.update(
                        {'OriginalAirDate': all_season[indv_episode]['original air date']})
                except KeyError:
                    episode_data.update({'OriginalAirDate': ''})

                series_data.append(episode_data)
    except:
        episode_data = {}
        episode_data.update({'SeasonNo': ''})
        episode_data.update({'EpisodeNo': ''})
        episode_data.update({'EpisodeTitle': ''})
        #episode_data.update({'DurationMins': ''})
        #episode_data.update({'DurationHours': ''})
        episode_data.update({'OriginalAirDate': ''})
        series_data.append(episode_data)

    print('done!')
    # print(series_data)
    return universal_data, series_data
# old


'''
def old_getter(i_fname):
    # create a working class of the IMDB parser
    #ia = imdb.IMDb(accessSystem='http', reraiseExceptions=True)

    ia = Cinemagoer(accessSystem='http', reraiseExceptions=True)
    # input file name
    input_file = i_fname
    # get path for current working directory and add desired output subfolder
    output_dir = Path(os.getcwd() + '/data')

    # declare default error message and string to handle any errors
    default_err_msg = err_msg = '\n---------------------\nErrors during search:'

    # read csv file and create a data frame
    df = pd.DataFrame(data=pd.read_csv(output_dir / input_file,
                                       index_col=['IMDBCode',
                                                  'Title', 'Year', 'Plot'],
                                       usecols=['IMDBCode', 'Title', 'Year', 'Plot']).reset_index())

    # Declare a list that is to be converted into a column
    new_cols = ['IMDBCode', 'Title', 'Year', 'Plot', 'Type', 'CombGenre',
                'Genre1', 'Genre2', 'Genre3', 'SeasonNo', 'SeasonName', 'EpisodeNo', 'EpisodeTitle', 'Platform',
                'DurationMins', 'DurationHours']

    # create a dataframe that will be used for the final
    final_df = pd.DataFrame(columns=new_cols)

    # loop through each item and compile data to be saved back to csv
    for new_item in tqdm(df['IMDBCode']):
        # search for the item based on the ID

        try:
            # logger throws access errors if the input MovieID does not exist
            # to work around this, the program will just leave these records blank
            logger = logging.getLogger('imdbpy')
            logger.disabled = True
            ia = imdb.IMDb(accessSystem='http',
                           reraiseExceptions=True, loggingLevel="CRITICAL")

            # attempt to save the movie details
            items = ia.get_movie(new_item)
        except IMDbDataAccessError:
            err_msg += '\n\'' + str(new_item) + \
                '\' - IMDB Movie code returned no results.'
            continue

        # add each item to the data dictionary
        # try except is used for each item as IMDB may have missing information
        data = {}
        try:
            data.update({'IMDBCode': items.movieID})
        except KeyError:
            data.update({'IMDBCode': ''})
        try:
            data.update({'Title': items['title']})
        except KeyError:
            data.update({'Title': ''})
        try:
            data.update({'Year': items['year']})
        except KeyError:
            data.update({'Year': ''})
        try:
            data.update({'Plot': items['plot'][0]})
        except KeyError:
            data.update({'Plot': ''})
        try:
            if items['kind'] == 'tv series' or items['kind'] == 'tv mini series':
                data.update({'Type': 'Show'})
            elif items['kind'] == 'movie':
                data.update({'Type': 'Movie'})
            else:
                data.update({'Type': items['kind']})
        except KeyError:
            data.update({'Type': ''})
        try:
            data.update({'DurationMins': items['runtimes'][0]})
        except KeyError:
            data.update({'DurationMins': ''})
        try:
            data.update({'DurationHours': int(items['runtimes'][0]) / 60})
        except KeyError:
            data.update({'DurationHours': ''})

        # genre counter and combined genre variables
        indv_genre = 0
        comb_genre = ''

        # check if atleast 1 genre is available
        try:
            # search and add all the genres
            while indv_genre < len(items.data['genres']) and indv_genre < 3:

                # create a string with the column title i.e. Genre1, Genre2
                g = 'Genre' + str(indv_genre+1)

                # collect the first 3 genres and combine them
                if indv_genre < 3:
                    comb_genre += items.data['genres'][indv_genre] + ', '

                # update the genres to the data dictionary
                data.update({g: items.data['genres'][indv_genre]})

                # incrememnt the genre number
                indv_genre += 1

        except KeyError:
            pass

        # update the combined genres to the data dictionary
        try:
            data.update({'CombGenre': comb_genre[:-2]})
        except KeyError:
            pass

        # create a temporary dataframe that will be appended to the final dataframe
        item_df = pd.DataFrame(data, index=[0])

        # get info specifically for tv shows such as episodes
        # then update with episode info
        if data['Type'] == 'Show':
            # update the item if it is a tv series
            ia.update(items, 'episodes')

            # loop to address each season of a show
            for indv_season in sorted(items['episodes'].keys()):
                all_season = items['episodes'][indv_season]

                # loop to address each episode within a season of a show
                for indv_episode in all_season:

                    # update the tv series specific data to the data dictionary
                    # SeasonName and Platform are unavailable on IMDB
                    try:
                        data.update({'SeasonNo': 'Season ' + str(indv_season)})
                    except KeyError:
                        data.update({'SeasonNo': ''})
                    #data.update({'SeasonName': ''})
                    try:
                        data.update({'EpisodeNo': indv_episode})
                    except KeyError:
                        data.update({'EpisodeNo': ''})
                    try:
                        data.update(
                            {'EpisodeTitle': all_season[indv_episode]['title']})
                    except KeyError:
                        data.update({'EpisodeTitle': ''})
                    #update({'Platform': ''})
                    try:
                        data.update({'DurationMins': items['runtimes'][0]})
                    except KeyError:
                        data.update({'DurationMins': ''})
                    try:
                        data.update(
                            {'DurationHours': int(items['runtimes'][0]) / 60})
                    except KeyError:
                        data.update({'DurationHours': ''})

                    # add theupdated data dictionary to the dataframe
                    item_df = data

                    # append the temporary dataframe to the final dataframe
                    final_df = final_df.append(item_df, ignore_index=True)
        else:
            # if movie append the temporary dataframe to the final dataframe
            final_df = final_df.append(item_df, ignore_index=True)


    # print complete message
    if err_msg != default_err_msg:
        print('\n' + err_msg)

    # export results to a csv file1
    output_file = 'placeholder_output.csv'
    output_dir.mkdir(parents=True, exist_ok=True)

    # can join path elements with / operator
    final_df.to_csv(output_dir / output_file)
'''


def main(submitted_movieID):

    # get the info for the movieID
    get_details(submitted_movieID)


if __name__ == '__main__':
    try:
        main('0120737')  # lotr
        main('0386676')  # office
        #entered_text = input('Enter the name of an item: ')
        #main(entered_text, 'ITEM')

    except KeyboardInterrupt:
        print('\nProgram Interrupted!')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
