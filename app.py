from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/WikipediaData.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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

class Fights(db.Model):
    __tablename__ = 'Fights'
    __table_args__ = { 'extend_existing': True }
    FIGHT_DATE = db.Column(db.String) 
    DATE_FORMATTED = db.Column(db.Date)
    FIGHTER_A = db.Column(db.String, primary_key=True) 
    FIGHTER_B = db.Column(db.String)  
    A_NICKNAME = db.Column(db.String)
    B_NICKNAME = db.Column(db.String)
    A_RECORD = db.Column(db.String)
    B_RECORD = db.Column(db.String)
    A_KOs = db.Column(db.String)
    B_KOs = db.Column(db.String)
    A_DRAWS = db.Column(db.String)
    B_DRAWS = db.Column(db.String)
    A_LINK = db.Column(db.String)
    B_LINK = db.Column(db.String)
    LOCATION = db.Column(db.String)
    A_HEIGHT = db.Column(db.String)
    B_HEIGHT = db.Column(db.String)
    A_REACH = db.Column(db.String)
    B_REACH = db.Column(db.String)


@app.route('/')
def home_page(): 
    fightList = []
    fightList = db.session.query(Fights).order_by(Fights.DATE_FORMATTED.asc()).all()
    return render_template('home.html', fights=fightList)

@app.route('/rankings')
def rankings():
    TBRB, RING, WBA, WBC, IBF, WBO = [], [], [], [], [], []
    
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
    