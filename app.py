from flask import Flask, render_template, request, redirect, url_for, session
from fuzzy_system import predict_priority
import os

app = Flask(__name__)
app.secret_key = 'tajni_kljuc'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        urgencies = request.form.getlist('urgency')
        impacts = request.form.getlist('impact')
        team_availabilities = request.form.getlist('team_availability')
        delayed_risks = request.form.getlist('delayed_risk')
        resolution_difficulties = request.form.getlist('resolution_difficulty')
        historical_impacts = request.form.getlist('historical_impact')

        tasks = []
        for i in range(len(urgencies)):
            urgency = int(urgencies[i])
            impact = int(impacts[i])
            team_availability = int(team_availabilities[i])
            delayed_risk = int(delayed_risks[i])
            resolution_difficulty = int(resolution_difficulties[i])
            historical_impact = int(historical_impacts[i])

            priority = predict_priority(urgency, impact, team_availability, delayed_risk, resolution_difficulty, historical_impact)
            tasks.append({'priority': priority})

        tasks_sorted = sorted(
            [task for task in tasks if task['priority'] is not None],
            key=lambda x: x['priority'],
            reverse=True
        )


        return render_template('index.html', results=tasks_sorted)

    return render_template('index.html', results=None)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
