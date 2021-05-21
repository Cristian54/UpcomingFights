import requests
from bs4 import BeautifulSoup
import re
from datetime import *

class WebScrapper: 
    @staticmethod
    def getRankings():
        URL = 'https://en.wikipedia.org/wiki/List_of_current_boxing_rankings'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        classContent = soup.find(id='mw-content-text')
        tables = classContent.find_all('table', attrs={'class':'wikitable'})
        
        TBRB = []
        RING = []
        WBA = []
        WBC = [] 
        IBF = []
        WBO = []
        colsHtml = []
        
        for table in tables:
            table_body = table.find('tbody')
            rows = table_body.find_all('tr')
            
            tempTBRB = []
            tempRING = []
            tempWBA = []
            tempWBC = []
            tempIBF = []
            tempWBO = []
            counter = 0
            
            for row in rows:
                cols = row.find_all('td')
                colsHtml.append(cols)
                cols = [ele.text.strip() for ele in cols]
                if len(cols) > 3:
                    tenthRanked = [cols[1], cols[2], cols[3], cols[4], cols[5], cols[6]]
                    
                    if counter < 10:
                        if '(S)' in cols[3]:
                            param = cols[3].split("(S)", 1)
                            tempWBA.append(param[0])
                        else: 
                            tempWBA.append(cols[3])
                            
                        tempTBRB.append(cols[1])
                        tempRING.append(cols[2])
                        tempWBC.append(cols[4])
                        tempIBF.append(cols[5])
                        tempWBO.append(cols[6])
                        counter += 1
                        
                    else:
                        counter = 0
                        
                        tempTBRB.append(tenthRanked[0])
                        TBRB.append(tempTBRB)
                        
                        tempRING.append(tenthRanked[1])
                        RING.append(tempRING)
                        
                        tempWBA.append(tenthRanked[2])
                        WBA.append(tempWBA)
                        
                        tempWBC.append(tenthRanked[3])
                        WBC.append(tempWBC)
                        
                        tempIBF.append(tenthRanked[4])
                        IBF.append(tempIBF)
                        
                        tempWBO.append(tenthRanked[5])
                        WBO.append(tempWBO)
        
        return [TBRB, RING, WBA, WBC, IBF, WBO, colsHtml]

    @staticmethod
    def getDistinctNames(rankings):
        namesSet = set()
        namesList = []
        counter = 0
        for company in rankings:
            if counter == 6: break
            counter += 1
            for division in company:
                for name in division:
                    if '(I)' in name:
                        continue
                    namesSet.add(name)
                            
        namesList = list(namesSet)
        return namesList        

    @staticmethod
    def getWikiLinks(tableRowsHtml, names):
        linksSet = set()
        for row in tableRowsHtml:
            for element in row:
                for link in element.find_all('a', href=True):
                    if link.get_text() in names and 'redlink=1' not in link['href']:
                        linksSet.add(link['href'])
                    elif link.get_text() in names and 'redlink=1' in link['href']:
                        names.remove(link.get_text())
        return [list(linksSet), names] 
    
    @staticmethod
    def getUpcomingFights(fightersLinks, names):
        URL = 'https://en.wikipedia.org/wiki/Michael_Hunter_(American_boxer)'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        classContent = soup.find(id='mw-content-text')
        tables = classContent.find_all('table', attrs={'class':'wikitable'})
        
        fightsTable = tables[1].find('tbody')
        row = fightsTable.find_all('tr')[1] 
        fightDate = row.find_all('td')[6]
        fightDateFormatted = datetime.strptime(fightDate.text.strip(), "%b %d, %Y")
        
        if datetime.today() <= fightDateFormatted: 
            #fightInfo = [date, opponents name, opp record, location] 
            fightInfo = [fightDate]
            
            nameHeading = soup.find('h1', id='firstHeading')
            nameText = nameHeading.get_text()
            if ' (American boxer)' in nameText:
                nameText = nameText.replace(' (American boxer)', '')
            elif ' (Mexican boxer)' in nameText:
                nameText = nameText.replace(' (Mexican boxer)', '')
            elif ' (boxer)' in nameText:
                nameText = nameText.replace(' (boxer)', '')
            
            recordTableBody = tables[0].find('tbody')
            rows = recordTableBody.find_all('tr')
            
            #[totalFights, wins, losses, KO wins, draws (if any), name?], this will be a list of lists
            record = []
            
            #rows[0] = tot fights, wins and losses. rows[1] = wins & losses by ko. rows[3] = draws (doesn't exist if fighter has no draws) 
            row = rows[0].find_all('td')
            tempString = ''
            for ele in row:
                tempString += ele.text.strip()
            temp = re.findall(r'\d+', tempString)
            res = list(map(int, temp)) 
            
            for item in res:
                record.append(item)  
                
            row = rows[1].find_all('td')
            record.append(row[1].text.strip())
            
            if len(rows) == 4:
                row = rows[3].find_all('td')
                record.append(row[1].text.strip())
                
            record.append(nameText)
            
            #return [record, fightInfo]
        else:
            return False
        
""" URL = 'https://en.wikipedia.org/wiki/List_of_current_boxing_rankings'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    classContent = soup.find(id='mw-content-text')

    weightClassesHeaders = classContent.find_all("h3")
    weightClasses = []

    for header in weightClassesHeaders:
        strModified = header.get_text().replace('[edit]', '')
        weightClasses.append(strModified)
        #print(strModified, "\n")
        
    #print(weightClasses)

    tables = classContent.find_all('table', attrs={'class':'wikitable'}) 
    table = tables[1]
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    tableHeaders = rows[0].find_all('th')

    rankingCompany = []
    for header in tableHeaders:
        #print(header.text.strip(), "\n")
        rankingCompany.append(header.text.strip())

    #print(rankingBodies) """
