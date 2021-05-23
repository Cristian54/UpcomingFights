import requests
from bs4 import BeautifulSoup
import re
from datetime import *

class WebScraper: 
    @staticmethod
    def getRankings():
        URL = 'https://en.wikipedia.org/wiki/List_of_current_boxing_rankings'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'lxml')
        
        classContent = soup.find(id='mw-content-text')
        tables = classContent.find_all('table', attrs={'class':'wikitable'})
        
        TBRB = []
        RING = []
        WBA = []
        WBC = [] 
        IBF = []
        WBO = []
        BOXREC = []
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
            tempBR = []
            counter = 0
            
            for row in rows:
                cols = row.find_all('td')
                colsHtml.append(cols)
                cols = [ele.text.strip() for ele in cols]
                if len(cols) > 3:
                    tenthRanked = [cols[1], cols[2], cols[3], cols[4], cols[5], cols[6], cols[0]]
                    
                    if counter < 10:
                        if '(S)' in cols[3]:
                            param = cols[3].split("(S)", 1)
                            tempWBA.append(param[0])
                        else: 
                            tempWBA.append(cols[3])
                        
                        tempBR.append(cols[0])
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
                        
                        tempBR.append(tenthRanked[6])
                        BOXREC.append(tempBR)
        
        return [TBRB, RING, WBA, WBC, IBF, WBO, colsHtml, BOXREC]

    @staticmethod
    def getDistinctNames(rankings):
        namesSet = set()
        for company in rankings:
            for division in company:
                for name in division:
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
        return list(linksSet) 
    
    @staticmethod
    def getUpcomingFights(fightersLinks):
        #fightsInfo[[record, fightInfo], [another fight], [], []]
        fightsInfo = []
        
        for link in fightersLinks:
            URL = 'https://en.wikipedia.org' + link
            #print(URL)
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, 'lxml')
                
            classContent = soup.find(id='mw-content-text')
            tables = classContent.find_all('table', attrs={'class':'wikitable'})
            
            if len(tables) < 1:
                continue
            
            firstTable = tables[0].find('tbody')
            firstRow = firstTable.find_all('tr')[0]
            
            if link == '/wiki/Dillian_Whyte': 
                recordTableBody = tables[2].find('tbody')
                fightsTable = tables[3].find('tbody')
                rowZero = fightsTable.find_all('tr')[0]
                rowOne = fightsTable.find_all('tr')[1]
                
            elif len(firstRow) == 6:
                recordTableBody = firstTable
                fightsTable = tables[1].find('tbody')
                rowZero = fightsTable.find_all('tr')[0]
                rowOne = fightsTable.find_all('tr')[1]
                
            elif len(firstRow) > 6 or len(firstRow) < 6:
                recordTableBody = tables[1].find('tbody')
                fightsTable = tables[2].find('tbody')
                rowZero = fightsTable.find_all('tr')[0]
                rowOne = fightsTable.find_all('tr')[1]
            
            
            if len(rowZero.find_all('th')) == 8:
                fightDate = rowOne.find_all('td')[5]
            else: fightDate = rowOne.find_all('td')[6]
            
            if fightDate.text.strip().startswith(('2018', '2019', '2020', 'TBA')):
                fightersLinks.remove(link)
                continue
            
            #Formats so far: (Apr 12, 2020) (12 Apr 2020) (12 April 2020) (2021-05-22)
            months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            if fightDate.text.strip().startswith(('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')):
                fightDateFormatted = datetime.strptime(fightDate.text.strip(), "%b %d, %Y")
            elif any(month in fightDate.text.strip() for month in months):
                fightDateFormatted = datetime.strptime(fightDate.text.strip(), "%d %B %Y")
            elif fightDate.text.strip().startswith('2021'):
                fightDateFormatted = datetime.strptime(fightDate.text.strip(), "%Y-%m-%d")
            else:
                fightDateFormatted = datetime.strptime(fightDate.text.strip(), "%d %b %Y")
                
            if datetime.today() <= fightDateFormatted + timedelta(days=1):
                opponentName = rowOne.find_all('td')[3]
                oppLinks = opponentName.find_all('a', href=True)
                for oppLink in oppLinks:
                    if oppLink['href'] in fightersLinks:
                        fightersLinks.remove(oppLink['href'])
                    
                oppRecord = rowOne.find_all('td')[2]
                fightLocation = rowOne.find_all('td')[7]
                
                #fightInfo = [date, opponents name, opp record, location] 
                fightInfo = [fightDate.text.strip(), opponentName.text.strip(), oppRecord.text.strip(), fightLocation.text.strip()]
                
                nameHeading = soup.find('h1', id='firstHeading')
                nameText = nameHeading.get_text()
                if ' (American boxer)' in nameText:
                    nameText = nameText.replace(' (American boxer)', '')
                elif ' (boxer)' in nameText:
                    nameText = nameText.replace(' (boxer)', '')
                elif ' (Mexican boxer)' in nameText:
                    nameText = nameText.replace(' (Mexican boxer)', '')
                    
                rows = recordTableBody.find_all('tr')
                    
                #[totalFights, wins, losses, KO wins, draws (if any), name]
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
                    
                temp = []
                temp.append(record)
                temp.append(fightInfo)
                fightsInfo.append(temp)
                
                """ print('---------FIGHT-------')
                print(temp)
                print('---------FIGHT-------') """
                    
            else:
                continue
         
        return fightsInfo 


    @staticmethod
    def getUpcomingFightsV2(link, fightersLinks):
        #fightsInfo[[record, fightInfo], [another fight], [], []]
        #fightsInfo = []

        URL = 'https://en.wikipedia.org' + link
        #print(URL)
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'lxml')
            
        classContent = soup.find(id='mw-content-text')
        tables = classContent.find_all('table', attrs={'class':'wikitable'})
        
        if len(tables) < 1:
            return []
        
        firstTable = tables[0].find('tbody')
        firstRow = firstTable.find_all('tr')[0]
        
        if link == '/wiki/Dillian_Whyte': 
            recordTableBody = tables[2].find('tbody')
            fightsTable = tables[3].find('tbody')
            rowZero = fightsTable.find_all('tr')[0]
            rowOne = fightsTable.find_all('tr')[1]
            
        elif len(firstRow) == 6:
            recordTableBody = firstTable
            fightsTable = tables[1].find('tbody')
            rowZero = fightsTable.find_all('tr')[0]
            rowOne = fightsTable.find_all('tr')[1]
            
        elif len(firstRow) > 6 or len(firstRow) < 6:
            recordTableBody = tables[1].find('tbody')
            fightsTable = tables[2].find('tbody')
            rowZero = fightsTable.find_all('tr')[0]
            rowOne = fightsTable.find_all('tr')[1]
        
        
        if len(rowZero.find_all('th')) == 8:
            fightDate = rowOne.find_all('td')[5]
        else: fightDate = rowOne.find_all('td')[6]
        
        if fightDate.text.strip().startswith(('2018', '2019', '2020', 'TBA')):
            return []
        
        #Formats so far: (Apr 12, 2020) (12 Apr 2020) (12 April 2020) (2021-05-22)
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        if fightDate.text.strip().startswith(('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')):
            fightDateFormatted = datetime.strptime(fightDate.text.strip(), "%b %d, %Y")
        elif any(month in fightDate.text.strip() for month in months):
            fightDateFormatted = datetime.strptime(fightDate.text.strip(), "%d %B %Y")
        elif fightDate.text.strip().startswith('2021'):
            fightDateFormatted = datetime.strptime(fightDate.text.strip(), "%Y-%m-%d")
        else:
            fightDateFormatted = datetime.strptime(fightDate.text.strip(), "%d %b %Y")
            
        if datetime.today() <= fightDateFormatted + timedelta(days=1):
            opponentName = rowOne.find_all('td')[3]
            oppLinks = opponentName.find_all('a', href=True)
            oppL = ''
            for oppLink in oppLinks:
                if oppLink['href'] in fightersLinks:
                    oppL = oppLink['href']
                
            oppRecord = rowOne.find_all('td')[2]
            fightLocation = rowOne.find_all('td')[7]
            
            #fightInfo = [date, opponents name, opp record, location] 
            fightInfo = [fightDate.text.strip(), opponentName.text.strip(), oppRecord.text.strip(), fightLocation.text.strip(), oppL]
            
            nameHeading = soup.find('h1', id='firstHeading')
            nameText = nameHeading.get_text()
            if ' (American boxer)' in nameText:
                nameText = nameText.replace(' (American boxer)', '')
            elif ' (boxer)' in nameText:
                nameText = nameText.replace(' (boxer)', '')
            elif ' (Mexican boxer)' in nameText:
                nameText = nameText.replace(' (Mexican boxer)', '')
                
            rows = recordTableBody.find_all('tr')
                
            #[totalFights, wins, losses, KO wins, draws (if any), name]
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
                
            temp = []
            temp.append(record)
            temp.append(fightInfo)
            return temp
                
        else:
            return []
