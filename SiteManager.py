import requests as re
import pandas as pd
import numpy as np

# Object that controls connections to sites and builds pd DataFrames


class SiteManager:
    def __init__(self):
        re.get('https://reblase.sibr.dev')

    def get_game(self, season, day):
        r = re.get('https://www.blaseball.com/database/games', params={"day": day, "season": season}).json()
        data = pd.DataFrame(r)
        # data.set_index('id', inplace=True) # TODO: figure out why this breaks add_winning??

        self.add_winning(data)

        data.to_csv("game_data.csv", index_label=False, index=False)

        return data

    @staticmethod
    def add_winning(df):
        # TODO: assuming input is complete game with homescore and awayscore, change to handle errors
        condition = [df['homeScore'] > df['awayScore'], df['homeScore'] < df['awayScore']]
        output = ["home", "away"]

        results = np.select(condition, output)

        df['winningTeam'] = pd.Series(results)



# site = SiteManager()
# print(site.get_game(12, 50))
