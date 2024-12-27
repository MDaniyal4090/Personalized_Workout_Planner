from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import json
import os
from datetime import datetime
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Ensure the data directory exists
if not os.path.exists('data'):
    os.makedirs('data')

# Comprehensive exercise database with variations and rep ranges
EXERCISE_DATABASE = {
    'strength': {
        'upper_body': [
            {'name': 'Push-ups', 'variations': ['Standard', 'Diamond', 'Wide-grip', 'Decline'], 'rep_range': '12-15'},
            {'name': 'Pull-ups', 'variations': ['Standard', 'Chin-ups', 'Wide-grip', 'Neutral-grip'], 'rep_range': '8-12'},
            {'name': 'Dips', 'variations': ['Bench dips', 'Parallel bar dips', 'Ring dips'], 'rep_range': '10-12'},
            {'name': 'Bench Press', 'variations': ['Barbell', 'Dumbbell', 'Incline', 'Decline'], 'rep_range': '8-12'},
            {'name': 'Rows', 'variations': ['Barbell', 'Dumbbell', 'Inverted', 'Cable'], 'rep_range': '10-15'}
        ],
        'lower_body': [
            {'name': 'Squats', 'variations': ['Bodyweight', 'Jump', 'Sumo', 'Bulgarian split'], 'rep_range': '12-15'},
            {'name': 'Lunges', 'variations': ['Walking', 'Reverse', 'Side', 'Jump'], 'rep_range': '12-15 each leg'},
            {'name': 'Deadlifts', 'variations': ['Romanian', 'Single-leg', 'Sumo', 'Standard'], 'rep_range': '8-12'},
            {'name': 'Calf Raises', 'variations': ['Standing', 'Seated', 'Single-leg', 'Jump'], 'rep_range': '15-20'},
            {'name': 'Glute Bridges', 'variations': ['Single-leg', 'Weighted', 'Elevated', 'March'], 'rep_range': '12-15'}
        ]
    },
    'cardio': [
        {'name': 'Running', 'variations': ['Sprints', 'Intervals', 'Long-distance', 'Hill runs'], 'duration': '20-30 min'},
        {'name': 'Cycling', 'variations': ['HIIT', 'Steady-state', 'Hill climbs', 'Intervals'], 'duration': '30-45 min'},
        {'name': 'Jump Rope', 'variations': ['Basic bounce', 'Double unders', 'Alternating feet', 'High knees'], 'duration': '10-15 min'},
        {'name': 'Swimming', 'variations': ['Freestyle', 'Breaststroke', 'Intervals', 'Water jogging'], 'duration': '30-45 min'},
        {'name': 'Rowing', 'variations': ['HIIT', 'Steady-state', 'Intervals', 'Power strokes'], 'duration': '20-30 min'}
    ],
    'flexibility': [
        {'name': 'Yoga', 'variations': ['Vinyasa', 'Power', 'Restorative', 'Yin'], 'duration': '30-60 min'},
        {'name': 'Dynamic Stretching', 'variations': ['Leg swings', 'Arm circles', 'Hip rotations', 'Ankle mobility'], 'duration': '10-15 min'},
        {'name': 'Static Stretching', 'variations': ['Full body', 'Lower body', 'Upper body', 'Core'], 'duration': '15-20 min'},
        {'name': 'Mobility Work', 'variations': ['Joint mobility', 'Animal flows', 'Controlled articular rotations'], 'duration': '15-20 min'}
    ],
    'hiit': [
        {'name': 'Burpees', 'variations': ['Standard', 'Mountain climber burpees', 'Pull-up burpees', 'Box jump burpees'], 'rep_range': '10-15'},
        {'name': 'Mountain Climbers', 'variations': ['Standard', 'Cross-body', 'Slow', 'Plyo'], 'rep_range': '30 seconds'},
        {'name': 'Jump Squats', 'variations': ['Standard', 'Split jumps', 'Box jumps', '180-degree jumps'], 'rep_range': '12-15'},
        {'name': 'Kettlebell Swings', 'variations': ['Russian', 'American', 'Single-arm', 'Double kettlebell'], 'rep_range': '15-20'},
        {'name': 'Plank Variations', 'variations': ['Standard', 'Side plank', 'Up-downs', 'Shoulder taps'], 'duration': '30-45 sec'}
    ]
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_goals', methods=['POST'])
def save_goals():
    data = request.json
    user_id = session.get('user_id')
    if not user_id:
        user_id = str(uuid.uuid4())
        session['user_id'] = user_id
    
    plan = {
        'goals': data.get('goals'),
        'preferred_exercises': data.get('exercises'),
        'availability': data.get('availability'),
        'created_at': datetime.now().isoformat()
    }
    
    filename = f'data/{user_id}_plan.json'
    with open(filename, 'w') as f:
        json.dump(plan, f)
    
    workout_plan = generate_workout_plan(plan)
    return jsonify({'success': True, 'plan': workout_plan})

@app.route('/get_plan')
def get_plan():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'No plan found'})
    
    filename = f'data/{user_id}_plan.json'
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            plan = json.load(f)
        return jsonify(plan)
    return jsonify({'error': 'No plan found'})

def generate_workout_plan(user_data):
    weekly_plan = {}
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Calculate workout intensity based on goals
    intensity_map = {
        'weight_loss': {'intensity': 'High', 'rest': '30 sec'},
        'muscle_gain': {'intensity': 'Medium-High', 'rest': '60-90 sec'},
        'endurance': {'intensity': 'Medium', 'rest': '45 sec'},
        'flexibility': {'intensity': 'Low-Medium', 'rest': '30 sec'}
    }
    
    # Default intensity if no matching goals
    workout_intensity = {'intensity': 'Medium', 'rest': '45 sec'}
    for goal in user_data['goals']:
        if goal in intensity_map:
            workout_intensity = intensity_map[goal]
            break
    
    for day in days:
        if day in user_data['availability']:
            exercises = []
            
            # Select exercises based on user preferences
            for exercise_type in user_data['preferred_exercises']:
                if exercise_type in EXERCISE_DATABASE:
                    if exercise_type == 'strength':
                        # Add both upper and lower body exercises
                        upper = EXERCISE_DATABASE[exercise_type]['upper_body']
                        lower = EXERCISE_DATABASE[exercise_type]['lower_body']
                        exercises.extend([
                            {**upper[i % len(upper)], 'variation': upper[i % len(upper)]['variations'][i % len(upper[i % len(upper)]['variations'])]}
                            for i in range(2)
                        ])
                        exercises.extend([
                            {**lower[i % len(lower)], 'variation': lower[i % len(lower)]['variations'][i % len(lower[i % len(lower)]['variations'])]}
                            for i in range(2)
                        ])
                    else:
                        exercises_list = EXERCISE_DATABASE[exercise_type]
                        exercises.extend([
                            {**exercises_list[i % len(exercises_list)], 
                             'variation': exercises_list[i % len(exercises_list)]['variations'][i % len(exercises_list[i % len(exercises_list)]['variations'])]}
                            for i in range(2)
                        ])
            
            weekly_plan[day] = {
                'exercises': exercises,
                'intensity': workout_intensity['intensity'],
                'rest_between_sets': workout_intensity['rest'],
                'sets': '3-4',
                'notes': 'Warm up properly before starting. Listen to your body and adjust intensity as needed.'
            }
    
    return weekly_plan

if __name__ == '__main__':
    app.run(debug=True)
