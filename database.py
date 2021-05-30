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
        #conn.execute(sql)
        
        sql = """
            CREATE TABLE IF NOT EXISTS Fights (
                FIGHT_DATE TEXT NOT NULL,
                DATE_FORMATTED DATE NOT NULL,  
                FIGHTER_A TEXT NOT NULL, 
                FIGHTER_B TEXT NOT NULL,
                A_NICKNAME TEXT NOT NULL, 
                B_NICKNAME TEXT NOT NULL,
                A_RECORD TEXT NOT NULL, 
                B_RECORD TEXT NOT NULL, 
                A_KOs TEXT NOT NULL, 
                B_KOs TEXT NOT NULL, 
                A_DRAWS TEXT NOT NULL, 
                B_DRAWS TEXT NOT NULL,
                A_LINK TEXT NOT NULL, 
                B_LINK TEXT NOT NULL, 
                LOCATION TEXT NOT NULL, 
                A_HEIGHT TEXT NOT NULL, 
                B_HEIGHT TEXT NOT NULL,
                A_REACH TEXT NOT NULL,
                B_REACH TEXT NOT NULL, 
                A_AGE TEXT NOT NULL, 
                B_AGE TEXT NOT NULL
            ) """
        conn.execute(sql) 
        
        conn.commit()
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

def populateFights(conn, fights):
    try:
        cur = conn.cursor()
        
        for fight in fights:
            if fight[1][1] == 'Empty wiki page' or fight[1][1] == 'No wiki page for opponent':
                recordA = fight[0][3] + '-' + fight[0][5]
                to_db = [fight[0][0], fight[0][9], fight[0][1], fight[1][0], fight[0][6], 'N/A', recordA, 'N/A', fight[0][4], 'N/A', fight[0][8], 'N/A', fight[0][7], 'N/A', fight[0][10], fight[0][11], 'N/A', fight[0][12], 'N/A', fight[0][13], 'N/A']
                cur.execute("INSERT INTO Fights VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", to_db)
            else:
                recordA = fight[0][3] + '-' + fight[0][5]
                recordB = fight[1][2] + '-' + fight[1][4]
                to_db = [fight[0][0], fight[0][9], fight[0][1], fight[1][0], fight[0][6], fight[1][5], recordA, recordB, fight[0][4], fight[1][3], fight[0][8], fight[1][7], fight[0][7], fight[1][6], fight[0][10], fight[0][11], fight[1][8], fight[0][12], fight[1][9], fight[0][13], fight[1][10]]
                cur.execute("INSERT INTO Fights VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", to_db) 
                     
        conn.commit()
        cur.close()
            
    except Error as e:
        conn.rollback()
        print(e)

def database():
    database = r'./data/WikipediaData.sqlite'
    conn = None
    try:
        conn = sqlite3.connect(database)
        #print("s")
    except Error as e:
        print(e)
        
    with conn:
        deleteTables(conn)
        #createTables(conn)
        
        rankings = WebScraper.getRankings()
        rankingss = [rankings[0], rankings[1], rankings[2], rankings[3], rankings[4], rankings[5]]
        populateRankings(conn, rankingss)
    
        rankingsss = [rankings[1], rankings[7]]
        distinctNames = WebScraper.getDistinctNames(rankingsss)

        if 'Alexei Papin' in distinctNames: distinctNames.remove('Alexei Papin')
        if 'Manny Pacquiao' in distinctNames: distinctNames.remove('Manny Pacquiao')
        if 'Mateusz Masternak' in distinctNames: distinctNames.remove('Mateusz Masternak')
        if 'George Kambosos Jr.' in distinctNames: distinctNames.remove('George Kambosos Jr.')
        
        fightersLinks = WebScraper.getWikiLinks(rankings[6], distinctNames)
        fights = WebScraper.getUpcomingFights(fightersLinks)
        populateFights(conn, fights) 

database()

