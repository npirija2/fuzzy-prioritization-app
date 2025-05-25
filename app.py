from flask import Flask, render_template, request
from fuzzy_system import predict_priority
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        urgency = float(request.form['urgency'])
        impact = float(request.form['impact'])
        team_availability = float(request.form['team_availability'])
        past_similar_issue = float(request.form['past_similar_issue'])
        delayed_risk = float(request.form['delayed_risk'])
        
        result = predict_priority(urgency, impact, team_availability, past_similar_issue, delayed_risk)
        if result is not None:
            result = round(result, 2)
        return render_template('index.html', result=result)
    return render_template('index.html', result=None)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
   
    app.run(host='0.0.0.0', port=port, debug=False)
