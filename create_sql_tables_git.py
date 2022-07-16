import psycopg2

commands = (

"""CREATE TABLE games(
    game_id VARCHAR(50) PRIMARY KEY,
    word_to_guess VARCHAR(30),
    total_time FLOAT,
    time_guess FLOAT ,
    attempts INTEGER NOT NULL,
    length INTEGER NOT NULL,
    vowels INTEGER NOT NULL,
    win BOOLEAN NOT NULL DEFAULT TRUE

)""", 

""" CREATE TABLE attempts ( 
id serial PRIMARY KEY ,
word_sent VARCHAR(30) ,
score FLOAT NOT NULL,
date TIMESTAMP NOT NULL ,
attempt INTEGER NOT NULL,
game_id VARCHAR(50) NOT NULL,
FOREIGN KEY (game_id) REFERENCES games (game_id)
) """

)

#Establishing the connection
conn = psycopg2.connect(
    host= host
    database= db,
    user="valenrami5",
    password= pwd)
#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Droping tables if already exists.
cursor.execute("DROP TABLE IF EXISTS attemps")
cursor.execute("DROP TABLE IF EXISTS games")
for command in commands:        
    cursor.execute(command)
print("Table created successfully........")
conn.commit()
#Closing the connection
conn.close()