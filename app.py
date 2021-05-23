from webscrapper import WebScraper
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/WikipediaData.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Rankings(db.Model):
    __tablename__ = 'Rankings'
    __table_args__ = { 'extend_existing': True }
    RANK = db.Column(db.Integer) 
    TBRB = db.Column(db.String)
    RING = db.Column(db.String) 
    WBA = db.Column(db.String)  
    WBC = db.Column(db.String)
    IBF = db.Column(db.String)
    WBO = db.Column(db.String)
    WEIGHT_CLASS = db.Column(db.String)
    dummyCol = db.Column(db.Integer, primary_key=True)

@app.route('/')
def home_page(): 
    """ rankings = WebScrapper.getRankings()
    distinctNames = WebScrapper.getDistinctNames(rankings)
    wikiLinksAndNames = WebScrapper.getWikiLinks(rankings[6], distinctNames)

    wikiLinksAndNames[0].remove('/wiki/Alexei_Papin')
    wikiLinksAndNames[0].remove('/wiki/Hugo_Centeno_Jr.')
    wikiLinksAndNames[0].remove('/wiki/Denys_Berinchyk')
    wikiLinksAndNames[0].remove('/wiki/Tervel_Pulev')
                
    fights = WebScrapper.getUpcomingFights(wikiLinksAndNames[0], wikiLinksAndNames[1]) """
    
    test = [['Canelo', 'Plant'], ['Fury', 'Joshua'], ['Spence', 'Pac']]
    return render_template('home.html', fights=test)

@app.route('/rankings')
def rankings():
    TBRB = []
    RING = []
    WBA = []
    WBC = [] 
    IBF = []
    WBO = []
    
    temp = []
    ranks = ['C', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    weights = ['HW', 'CW', 'LHW', 'SMW', 'MW', 'LMW', 'WW', 'SLW', 'LW', 'SFW', 'FW', 'SBW', 'BW', '115', '112', '108', '105']
    
    for weight in weights:
        temp = db.session.query(Rankings.TBRB).filter(Rankings.WEIGHT_CLASS == weight).all()
        TBRB.append(temp)
        temp = []
        
        temp = db.session.query(Rankings.RING).filter(Rankings.WEIGHT_CLASS == weight).all()
        RING.append(temp)
        temp = []
        
        temp = db.session.query(Rankings.WBA).filter(Rankings.WEIGHT_CLASS == weight).all()
        WBA.append(temp)
        temp = []
        
        temp = db.session.query(Rankings.WBC).filter(Rankings.WEIGHT_CLASS == weight).all()
        WBC.append(temp)
        temp = []
        
        temp = db.session.query(Rankings.IBF).filter(Rankings.WEIGHT_CLASS == weight).all()
        IBF.append(temp)
        temp = []
        
        temp = db.session.query(Rankings.WBO).filter(Rankings.WEIGHT_CLASS == weight).all()
        WBO.append(temp)
        temp = []
    return render_template('rankings.html', Ranks = ranks, TBRB = TBRB, Ring = RING, WBA = WBA, WBC = WBC, IBF = IBF, WBO = WBO)


if __name__ == "__main__":
    app.run(debug=True)
    