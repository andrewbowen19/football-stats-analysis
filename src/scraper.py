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
        off_url = f"https://widgets.sports-reference.com/wg.fcgi?css=1&site=pfr&url=%2Fyears%2F2021%2F&div=div_team_stats"
        def_url = f"https://www.pro-football-reference.com/years/2021/opp.htm#team_stats"
        dfs = pd.read_html(off_url, header=1, displayed_only=False)

        odf = pd.concat(dfs)
        ddf = pd.read_html(def_url, header=1)[0].drop([32,33,34], axis=0)

        # Merging offensive and defensive YPG Dfs
        # Grabbing a few columns then setting class attr
        df = pd.merge(odf, ddf, how='left', on='Tm', suffixes=("", "_opp"))
        df.set_index('Tm', inplace=True)
        df = df[['Rk', 'G', 'PF', 'Yds',
                 'Ply', 'Y/P', 'TO', 'FL',
                 '1stD', 'Cmp', 'Att']]

        self.ypg = df

    
    def combine_data(self, season=2021):
        '''Combines standings and ypg stats and formats'''
        # Get standings and ypg dfs, then merge 'em
        self.get_standings()
        self.get_ypg()
        df = pd.merge(self.standings, self.ypg, how='left', left_index=True, right_index=True)

        df = df[['W', 'L', 'T', 'W-L%', 'PF_x', 'PA', 'PD', 'MoV', 'SoS', 'SRS', 'OSRS',
                 'DSRS', 'Rk', 'G', 'Yds', 'Ply', 'Y/P', 'TO', 'FL', '1stD',
                 'Cmp', 'Att']]
        return df


if __name__ == "__main__":    
    n = nflScraper()
    # n.get_standings(2021)
    dfs = []
    for s in range(2021, 2000, -1):
        df = n.combine_data(season=s)

        df['Season'] = [s for x in range(0, len(df))]
        print(df.head())
        dfs.append(df)
        print('-----------------------------')

    df = pd.concat(dfs)
    print(df)

    csv_path = os.path.join("..", "data", "nfl-stats-by-season.csv")
    df.to_csv(csv_path)