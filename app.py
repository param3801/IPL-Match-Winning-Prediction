from flask import Flask, render_template,request
import pickle
import sklearn
import pandas as pd


app = Flask(__name__)
print(sklearn.__version__)

pipe = pickle.load(open("pipe.pkl",'rb'))
team = ['Rajasthan Royals', 'Royal Challengers Bangalore',
       'Kolkata Knight Riders', 'Mumbai Indians', 'Delhi Capitals',
       'Punjab Kings', 'Chennai Super Kings', 'Sunrisers Hyderabad',
       'Gujarat Titans', 'Lucknow Super Giants']
cities = ['Bangalore', 'Chandigarh', 'Delhi', 'Mumbai', 'Kolkata', 'Jaipur',
       'Hyderabad', 'Chennai', 'Cape Town', 'Port Elizabeth', 'Durban',
       'Centurion', 'East London', 'Johannesburg', 'Kimberley',
       'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
       'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
       'Rajkot', 'Kanpur', 'Bengaluru', 'Indore', 'Dubai', 'Sharjah',
       'Navi Mumbai', 'Lucknow', 'Guwahati', 'Mohali']
@app.route("/")
def home():
    return render_template('index.html',cities = cities, teams=team)
@app.route("/",methods=['GET','POST'])
def predict():

    if request.method == 'POST':

        batting_team = request.form.get('Batting')
        bowling_team = request.form.get('bolling')
        city = request.form.get('city')
        total_runs_x= int(request.form.get('target').strip())
        current_run = int(request.form.get('currrent_run').strip())

        over = int(request.form.get('over').strip())
        required_run= total_runs_x - current_run
        ball_left= 120 - over*6
        wicket = int(request.form.get('wicket').strip())
        wicket_left= 10 - wicket
        if over==0:
            over = 1
        crr= current_run/over
        rrr= required_run/(ball_left/6)
        if rrr>1000:
            rrr = 50
        if required_run<0 or current_run < 0 or over < 0:
            error = "Negative values are not allowed!"
            return render_template('index.html',error = error, cities=cities, teams=team)

        data={
        'batting_team':[batting_team],
        'bowling_team':[bowling_team],
        'city':[city],
        'required_run':[required_run],
        'ball_left':[ball_left],
        'wicket_left':[wicket_left],
          'total_runs_x':[total_runs_x],
            'crr':[crr], 'rrr':[rrr]
        }
    # X_test = [batting_team,bowling_team,city,required_run,ball_left,wicket_left,total_runs_x,crr,rrr]
    # X_columns = ['batting_team', 'bowling_team', 'city', 'required_run', 'ball_left','wicket_left', 'total_runs_x', 'crr', 'rrr']
        df = pd.DataFrame(data)
        k = pipe.predict_proba(df)
        print(k)
        win_pro_of_ball_team = (k[0][0]*100).round()
        win_pro_of_bat_team = (k[0][1]*100).round()

        print(win_pro_of_ball_team)
        print(win_pro_of_bat_team)
        return render_template("index.html", win_pro_of_bat_team=win_pro_of_bat_team,win_pro_of_ball_team=win_pro_of_ball_team
                           ,batting_team=batting_team, bowling_team=bowling_team
                           ,cities = cities, teams=team
                           )

if __name__ == '__main__':
    app.run(debug=True)