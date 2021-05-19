import requests
from bs4 import BeautifulSoup

class WebScraper: 
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
        
        return [TBRB, RING, WBA, WBC, IBF, WBO]





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
