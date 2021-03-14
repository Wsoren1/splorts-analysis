import requests as re
import pandas as pd
import numpy as np
import pickle
import atexit

# Object that controls connections to sites and builds pd DataFrames
# Using a lot of the blaseball API, doc links https://docs.sibr.dev/docs/apis/reference/Blaseball-API.v1.yaml


class SiteManager:
    def __init__(self):  # TODO: assign attributes to clean up function syntax, shit's ugly af
        self.metadata_path = r'data\metadata.pickle'
        self.game_cache_path = r'data\game_cache.csv'

        with open(self.metadata_path, "rb") as f:
            self.metadata = pickle.load(f)

        atexit.register(self.save_metadata)

    def get_game(self, season, day):
        datablase = pd.read_csv(self.game_cache_path)
        query = (datablase['day'] == day) & (datablase['season'] == season)
        if len(df := datablase[query]) > 0:
            if len(df) == len(df[df['finalized']]):
                return df
        else:
            r = re.get('https://www.blaseball.com/database/games', params={"day": day, "season": season}).json()
            pulled_data = pd.DataFrame(r)
            self.add_winning(pulled_data)

            datablase = pd.concat([pulled_data, datablase])

            datablase.to_csv("game_cache.csv", index_label=False, index=False)
            return pulled_data

    def get_all_games(self):
        df = pd.read_csv(self.game_cache_path)
        return df[df['finalized']]

    def save_metadata(self):
        with open(self.metadata_path, 'ab') as f:
            pickle.dump(self.metadata, f)

    @staticmethod
    def add_winning(df):
        if 'homeScore' not in df.keys() or 'awayScore' not in df.keys():
            raise Exception("Dataframe has no score fields")
        condition = [df['homeScore'] > df['awayScore'], df['homeScore'] < df['awayScore']]
        output = ["home", "away"]

        results = np.select(condition, output)

        df['winningTeam'] = pd.Series(results)


site = SiteManager()
site.get_game(11, 50)