from webscrapper import WebScrapper
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home_page(): 
    rankings = WebScrapper.getRankings()
    distinctNames = WebScrapper.getDistinctNames(rankings)
    wikiLinksAndNames = WebScrapper.getWikiLinks(rankings[6], distinctNames)

    wikiLinksAndNames[0].remove('/wiki/Alexei_Papin')
    wikiLinksAndNames[0].remove('/wiki/Hugo_Centeno_Jr.')
    wikiLinksAndNames[0].remove('/wiki/Denys_Berinchyk')
    wikiLinksAndNames[0].remove('/wiki/Tervel_Pulev')
                
    fights = WebScrapper.getUpcomingFights(wikiLinksAndNames[0], wikiLinksAndNames[1])
    return render_template('home.html', fights = fights)

@app.route('/rankings')
def rankings():
    rankings = WebScrapper.getRankings()
    ranks = ['C', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # WBA HW = rankings[2][0], so cruiser would be [2][1]
    return render_template('rankings.html', Ranks = ranks, TBRB = rankings[0], Ring = rankings[1], WBA = rankings[2], WBC = rankings[3], IBF = rankings[4], WBO = rankings[5])


if __name__ == "__main__":
    app.run(debug=True)
    
#rankings = WebScraper.getRankings(self=0)
#print(rankings[0][0])