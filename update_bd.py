from solver import Interactive as solver
from connection import Connection as cn
import pandas as pd
pd.options.mode.chained_assignment = None

class IntoSql:

    def getting_games_df(self):
        df, id, score_list, word_send_list, time_list, time_array_list, current_attemps_list, time_list_first_word = solver().game()
        df_games = df[df['score']==1]
        df_games['length']=df_games['word_sent'].str.len()
        df_games = df_games[['id', 'word_sent', 'time_find_word', 'length', 'attemps' ]]
        games = list(df_games.itertuples(index=False, name=None))
        df_attemps = df [['word_sent', 'time_array', 'attemps', 'id']]
        attemps = list(df_attemps.itertuples(index=False, name=None))
        return games, attemps

    def update_tables(self):
        games, attemps = self.getting_games_df()
        connection = cn()
        conn = connection.connection()
        cursor = conn.cursor()
        for i in games:
            cursor.execute('''INSERT INTO games(game_id, word_to_guess, time_guess, length, attemps) VALUES (%s, %s, %s, %s, %s)''', i)
        for i in attemps:
            cursor.execute("INSERT INTO attemps(word_send, time_array, attempt, game_id) VALUES (%s, %s, %s, %s)", i)
        conn.commit()
        # Closing the connection
        conn.close()
        print("Records inserted........")
        return games, attemps


IntoSql().update_tables()