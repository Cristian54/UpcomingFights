from webscrapper import WebScrapper
from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route('/')
def home_page(): 
    return render_template('home.html')

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