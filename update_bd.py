from solver import Interactive as solver
from connection import Connection as cn
import pandas as pd
pd.options.mode.chained_assignment = None

class IntoSql:

    def getting_games_df(self):
        df = solver().game()
        df_games = df.drop_duplicates(subset = 'id', keep = 'last')
        df_games = df_games[['id', 'word_sent', 'total_time', 'time_find_word', 'attempts', 'length', 'vowels', 'win']]
        games = list(df_games.itertuples(index=False, name=None))
        df_attemps = df [['word_sent', 'score', 'date', 'attempts', 'id']]
        attempts = list(df_attemps.itertuples(index=False, name=None))
        return games, attempts

    def update_tables(self):
        games, attempts = self.getting_games_df()
        connection = cn()
        conn = connection.connection()
        cursor = conn.cursor()
        for i in games:
            cursor.execute('''INSERT INTO games(game_id, word_to_guess, total_time, time_guess, attempts, length, vowels, win) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', i)
        for i in attempts:
            cursor.execute("INSERT INTO attempts(word_sent, score, date, attempt, game_id) VALUES (%s, %s, %s, %s, %s)", i)
        conn.commit()   
        # Closing the connection
        conn.close()
        print("Records inserted........")
        #return games, attempts


IntoSql().update_tables()