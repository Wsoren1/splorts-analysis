import requests as re
import pandas as pd
import numpy as np

# Object that controls connections to sites and builds pd DataFrames
# Using a lot of the blaseball API, doc linx https://docs.sibr.dev/docs/apis/reference/Blaseball-API.v1.yaml


class SiteManager:
    def __init__(self):
        re.get('https://reblase.sibr.dev')

    def get_game(self, season, day):
        datablase = pd.read_csv("game_cache.csv")
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

    @staticmethod
    def add_winning(df):
        if 'homeScore' not in df.keys() or 'awayScore' not in df.keys():
            raise Exception("Dataframe has no score fields")
        condition = [df['homeScore'] > df['awayScore'], df['homeScore'] < df['awayScore']]
        output = ["home", "away"]

        results = np.select(condition, output)

        df['winningTeam'] = pd.Series(results)



site = SiteManager()
print(site.get_game(2, 98))
site.get_game(12, 58)