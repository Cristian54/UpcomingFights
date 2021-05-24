from webscrapper import WebScraper
import sqlite3
from sqlite3 import Error

def deleteTables(conn):
    conn.execute("DELETE FROM Fights")
    conn.execute("DELETE FROM Rankings")
    
    conn.commit()
    
def createTables(conn):
    try:
        sql = """ 
            CREATE TABLE IF NOT EXISTS Rankings (
                RANK INT NOT NULL, 
                TBRB TEXT NOT NULL, 
                RING TEXT NOT NULL, 
                WBA TEXT NOT NULL, 
                WBC TEXT NOT NULL, 
                IBF TEXT NOT NULL, 
                WBO TEXT NOT NULL, 
                WEIGHT_CLASS TEXT NOT NULL
            ) """
        conn.execute(sql)
        
        sql = """
            CREATE TABLE IF NOT EXISTS Fights (
                FIGHT_DATE TEXT NOT NULL, 
                FIGHTER_A TEXT NOT NULL, 
                FIGHTER_B TEXT NOT NULL,
                A_NICKNAME TEXT NOT NULL, 
                B_NICKNAME TEXT NOT NULL,
                A_RECORD TEXT NOT NULL, 
                B_RECORD TEXT NOT NULL, 
                A_KOs TEXT NOT NULL, 
                B_KOs TEXT NOT NULL, 
                A_LINK TEXT, 
                B_LINK TEXT
            ) """
        conn.execute(sql) 
        
        conn.commit()
       # print("Tables successfully created")
    except Error as e:
        conn.rollback()
        print(e)      

def populateRankings(conn, rankings):
    try:
        cur = conn.cursor()
        
        Ranks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        weights = ['HW', 'CW', 'LHW', 'SMW', 'MW', 'LMW', 'WW', 'SLW', 'LW', 'SFW', 'FW', 'SBW', 'BW', '115', '112', '108', '105']
        counter = 0
        index = 0
        for tbrb, ring, wba, wbc, ibf, wbo in zip(rankings[0], rankings[1], rankings[2], rankings[3], rankings[4], rankings[5]):
            for rank, t, r, wa, wc, ib, wo in zip(Ranks, tbrb, ring, wba, wbc, ibf, wbo):
                to_db = [rank, t, r, wa, wc, ib, wo, weights[index]]
                cur.execute("INSERT INTO Rankings VALUES (?, ?, ?, ?, ?, ?, ?, ?)", to_db)
                counter += 1
                if counter == 11: 
                    counter = 0
                    index += 1
                    
        conn.commit()
        cur.close()
            
    except Error as e:
        conn.rollback()
        print(e)

def database():
    database = r'data/WikipediaData.sqlite'
    conn = None
    try:
        conn = sqlite3.connect(database)
    except Error as e:
        print(e)
        
    with conn:
        #deleteTables(conn)
        #createTables(conn)
        
        rankings = WebScraper.getRankings()
        #rankingss = [rankings[0], rankings[1], rankings[2], rankings[3], rankings[4], rankings[5]]
        #populateRankings(conn, rankingss)
        
database()
