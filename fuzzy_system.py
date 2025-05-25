import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

urgency = ctrl.Antecedent(np.arange(0, 11, 1), 'urgency')
urgency['low'] = fuzz.trimf(urgency.universe, [0, 0, 5])
urgency['medium'] = fuzz.trimf(urgency.universe, [2, 5, 8])
urgency['high'] = fuzz.trimf(urgency.universe, [6, 10, 10])

impact = ctrl.Antecedent(np.arange(0, 11, 1), 'impact')
impact['small'] = fuzz.trimf(impact.universe, [0, 0, 4])
impact['moderate'] = fuzz.trimf(impact.universe, [3, 5, 7])
impact['high'] = fuzz.trimf(impact.universe, [6, 10, 10])

team_availability = ctrl.Antecedent(np.arange(0, 11, 1), 'team_availability')
team_availability['low'] = fuzz.trimf(team_availability.universe, [0, 0, 4])
team_availability['medium'] = fuzz.trimf(team_availability.universe, [3, 5, 7])
team_availability['high'] = fuzz.trimf(team_availability.universe, [6, 10, 10])

past_similar_issue = ctrl.Antecedent(np.arange(0, 11, 1), 'past_similar_issue')
past_similar_issue['never'] = fuzz.trimf(past_similar_issue.universe, [0, 0, 1])
past_similar_issue['few'] = fuzz.trimf(past_similar_issue.universe, [1, 3, 5])
past_similar_issue['often'] = fuzz.trimf(past_similar_issue.universe, [4, 10, 10])

delayed_risk = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'delayed_risk')
delayed_risk['unlikely'] = fuzz.trimf(delayed_risk.universe, [0, 0, 0.5])
delayed_risk['possible'] = fuzz.trimf(delayed_risk.universe, [0.25, 0.5, 0.75])
delayed_risk['likely'] = fuzz.trimf(delayed_risk.universe, [0.5, 1, 1])


priority = ctrl.Consequent(np.arange(0, 11, 1), 'priority')
priority['low'] = fuzz.trimf(priority.universe, [0, 0, 4])
priority['medium'] = fuzz.trimf(priority.universe, [3, 5, 7])
priority['high'] = fuzz.trimf(priority.universe, [6, 10, 10])

rule1 = ctrl.Rule(urgency['high'] & impact['high'], priority['high'])

rule2 = ctrl.Rule(urgency['medium'] & impact['moderate'] & team_availability['low'], priority['medium'])

rule3 = ctrl.Rule(urgency['low'] & team_availability['high'], priority['low'])

rule4 = ctrl.Rule(past_similar_issue['often'] & delayed_risk['likely'], priority['high'])

rule5 = ctrl.Rule(past_similar_issue['never'] & delayed_risk['unlikely'], priority['low'])


rule6 = ctrl.Rule(urgency['high'] & team_availability['low'], priority['high'])

rule7 = ctrl.Rule(impact['small'] & delayed_risk['unlikely'], priority['low'])


rule8 = ctrl.Rule(urgency['medium'] & team_availability['medium'] & delayed_risk['likely'], priority['medium'])


rule9 = ctrl.Rule(impact['high'] & past_similar_issue['often'], priority['high'])

rule10 = ctrl.Rule(urgency['low'] & impact['small'] & team_availability['high'], priority['low'])


priority_ctrl_system = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10])
priority_ctrl = ctrl.ControlSystemSimulation(priority_ctrl_system)

def predict_priority(urgency_val, impact_val, team_val, past_val, delay_val):
    priority_ctrl = ctrl.ControlSystemSimulation(priority_ctrl_system)

    priority_ctrl.input['urgency'] = urgency_val
    priority_ctrl.input['impact'] = impact_val
    priority_ctrl.input['team_availability'] = team_val
    priority_ctrl.input['past_similar_issue'] = past_val
    priority_ctrl.input['delayed_risk'] = delay_val

    priority_ctrl.compute()
    print("Izlazni podaci:", priority_ctrl.output) 

    return priority_ctrl.output.get('priority', None)  

