import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pickle
import pandas as pd
from sklearn.pipeline import Pipeline

db_username = os.environ['DB_USERNAME']
db_password = os.environ['DB_PASSWORD']
db_name = os.environ['DB_NAME']
db_host = os.environ['DB_HOST']
db_port = os.environ['DB_PORT']
db_uri = f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
print(f"Connecting db @{db_uri}")
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy()
db.init_app(app)

# class User(db.Model):
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(50), nullable=False)

#     def __init__(self, name):
#         self.name = name


class Team(db.Model):
    __tablename__ = "teams"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    League = db.Column(db.String(50), nullable=False)
    Year = db.Column(db.Integer, nullable=False)
    OBP = db.Column(db.Integer, nullable=False)
    SLG = db.Column(db.Integer, nullable=False)
    BA = db.Column(db.Integer, nullable=False)
    G = db.Column(db.Integer, nullable=False)
    OSLG = db.Column(db.Integer, nullable=False)
    predict_RD = db.Column(db.Integer, nullable=False)

    def __init__(self, League, Year, OBP, SLG, BA, G, OSLG, predict_RD):
        self.League = League
        self.Year = Year
        self.OBP = OBP
        self.SLG = SLG
        self.BA = BA
        self.G = G
        self.OSLG = OSLG
        predict_RD = predict_RD


@app.route("/")
def home():
    return "Hello from my Containerized Server"

# @app.route('/users', methods=['POST'])
# def add_user():
#     request_data = request.get_json()
#     u_name = request_data['name']
#     new_user = User(
#         name=u_name)
#     db.session.add(new_user)
#     db.session.commit()
#     return "User added successfully"

# @app.route('/users')
# def show_users():
#     users = User.query.all()
#     user_list = {}
#     for user in users:
#         user_list[user.id] = user.name
#     return user_list

@app.route('/predict_rd')
def predict_rd():
    teams = Team.query.all()
    team_dict = dict()
    for team in teams:
        team_dict.update({team.id:[team.League, team.Year, team.OBP, team.SLG, team.BA, team.G, team.OSLG, team.predict_RD]})
    return team_dict

@app.route('/predict_rd', methods=['POST'])
def predict_rd():
    request_data = request.get_json()
    League = request_data['League']
    Year = request_data['Year']
    OBP = request_data['OBP']
    SLG = request_data['SLG']
    BA = request_data['BA']
    G = request_data['G']
    OSLG = request_data['OSLG']

    data = {
        'League':League,
        'Year':Year,
        'OBP':OBP,
        'SLG':SLG,
        'BA':BA,
        'G':G,
        'OSLG':OSLG
    }
    data_df = pd.DataFrame.from_dict(data)
    predict_RD = predict_from_json(data_df)

    new_team = Team(
        League=League, Year=Year, OBP=OBP, SLG=SLG, BA=BA, G=G, OSLG=OSLG, predict_RD=predict_RD)
    db.session.add(new_team)
    db.session.commit()
    return "Tean predicted successfully"

def predict_from_json(data_df):
    with open('model.pkl', 'rb') as f:
        loaded_model = pickle.load(f)

    return loaded_model.predict(data_df)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5555)