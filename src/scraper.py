'''
Script to scrape NFL team data for given seasons
'''

import os
import pandas as pd
import numpy as np


class nflScraper(object):
    '''
    This class scrapes Pro-Football-Reference.com for the 3 stats most highly correlated with NFL win %:
        - Turnover differential (turnovers created - turnovers committed)
        - Point differential (points for - points against)
        - One-score game win %
        
    class parameters:
        season - (int or str); season desired for statistics pull (should be consistent across method calls)
        team - str; if team != "All", only retrieves desired statistics for one team
    '''

    def __init__(self, team='All'):
        self.team = team
        self.candlestick_stats = None

    @staticmethod
    def format_df(df):
        '''Remove division formatting from a PRF table df'''
        divisions = ['NFC West', 'NFC South',
                     'NFC North', 'NFC East',
                     'AFC West', 'AFC South',
                     'AFC North', 'AFC East']
        # Dropping standings footnotes (*/+) from team names
        df['Tm'] = df['Tm'].str.replace('*','')
        df['Tm'] = df['Tm'].str.replace('+','')

        # Setting team name to df index
        df.set_index('Tm', inplace=True)
        df = df.drop(divisions, axis=0)

        return df

    def get_standings(self, season=2021):
        '''Scrapes PRF for NFL standings in a given season (int or str of year), '''

        url = f"https://www.pro-football-reference.com/years/{season}/"
        dfs = pd.read_html(url)
        df = pd.concat(dfs)  # Combines AFC and NFC standings

        self.standings = self.format_df(df)

    def get_ypg(self, season=2021):
        '''
        Scraping Yards per Game (ypg) data for each team (both on offense and defense -- Opp YPG)
        '''
        url = f"https://www.pro-football-reference.com/years/{season}/#team_stats"
        dfs = pd.read_html(url)

        df = pd.concat(dfs)
        print(df)


    
    def combine_data():
        '''Combines standings and ypg stats and formats'''

if __name__ == "__main__":    
    n = nflScraper()
    n.get_standings(2021)
    print('-----------------------------')
    n.get_ypg(2021)

