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


delayed_risk = ctrl.Antecedent(np.arange(0, 11, 1), 'delayed_risk')
delayed_risk['unlikely'] = fuzz.trimf(delayed_risk.universe, [0, 0, 5])
delayed_risk['possible'] = fuzz.trimf(delayed_risk.universe, [2.5, 5, 7.5])
delayed_risk['likely'] = fuzz.trimf(delayed_risk.universe, [5, 10, 10])

historical_impact = ctrl.Antecedent(np.arange(0, 11, 1), 'historical_impact')
historical_impact['low'] = fuzz.trimf(historical_impact.universe, [0, 0, 4])
historical_impact['medium'] = fuzz.trimf(historical_impact.universe, [3, 5, 7])
historical_impact['high'] = fuzz.trimf(historical_impact.universe, [6, 10, 10])

resolution_difficulty = ctrl.Antecedent(np.arange(0, 11, 1), 'resolution_difficulty')
resolution_difficulty['easy'] = fuzz.trimf(resolution_difficulty.universe, [0, 0, 4])
resolution_difficulty['moderate'] = fuzz.trimf(resolution_difficulty.universe, [3, 5, 7])
resolution_difficulty['hard'] = fuzz.trimf(resolution_difficulty.universe, [6, 10, 10])


priority = ctrl.Consequent(np.arange(0, 11, 1), 'priority')
priority['low'] = fuzz.trimf(priority.universe, [0, 0, 4])
priority['medium'] = fuzz.trimf(priority.universe, [3, 5, 7])
priority['high'] = fuzz.trimf(priority.universe, [6, 10, 10])


rule1 = ctrl.Rule(urgency['high'] & impact['high'], priority['high'])
rule2 = ctrl.Rule(urgency['medium'] & impact['moderate'] & team_availability['low'], priority['medium'])
rule3 = ctrl.Rule(urgency['low'] & team_availability['high'], priority['low'])
rule6 = ctrl.Rule(urgency['high'] & team_availability['low'], priority['high'])
rule7 = ctrl.Rule(impact['small'] & delayed_risk['unlikely'], priority['low'])
rule8 = ctrl.Rule(urgency['medium'] & team_availability['medium'] & delayed_risk['likely'], priority['medium'])
rule10 = ctrl.Rule(urgency['low'] & impact['small'] & team_availability['high'], priority['low'])
rule11 = ctrl.Rule(historical_impact['high'] & resolution_difficulty['hard'], priority['high'])
rule12 = ctrl.Rule(historical_impact['low'] & resolution_difficulty['easy'], priority['low'])
rule13 = ctrl.Rule(historical_impact['medium'] & resolution_difficulty['moderate'], priority['medium'])
rule14 = ctrl.Rule(urgency['high'] & impact['moderate'] & team_availability['medium'], priority['high'])
rule15 = ctrl.Rule(impact['high'] & urgency['low'] & team_availability['high'], priority['medium'])
rule16 = ctrl.Rule(delayed_risk['likely'] & resolution_difficulty['hard'], priority['high'])
rule17 = ctrl.Rule(delayed_risk['unlikely'] & resolution_difficulty['easy'], priority['low'])
rule18 = ctrl.Rule((historical_impact['medium'] | historical_impact['high']) & team_availability['low'], priority['medium'])
rule19 = ctrl.Rule(urgency['low'] & impact['small'] & delayed_risk['unlikely'], priority['low'])
rule20 = ctrl.Rule(urgency['high'] & impact['high'] & team_availability['high'], priority['medium'])



rule_fallback = ctrl.Rule(urgency['low'] & impact['moderate'] & team_availability['medium'], priority['low'])


priority_ctrl_system = ctrl.ControlSystem([
    rule1, rule2, rule3, 
    rule6, rule7, rule8, rule10,
    rule11, rule12, rule13,
    rule_fallback,
    rule14, rule15, rule16, rule17, rule18, rule19, rule20
])


priority_ctrl = ctrl.ControlSystemSimulation(priority_ctrl_system)


def predict_priority(urgency_val, impact_val, team_val, delay_val, resolution_val, historical_val):
    sim = ctrl.ControlSystemSimulation(priority_ctrl_system)

    sim.input['urgency'] = urgency_val
    sim.input['impact'] = impact_val
    sim.input['team_availability'] = team_val
    sim.input['delayed_risk'] = delay_val
    sim.input['resolution_difficulty'] = resolution_val
    sim.input['historical_impact'] = historical_val
  

    sim.compute()
    print("Izlazni podaci:", sim.output)

    return sim.output.get('priority', None)
