# Personalized Workout Planner

A modern Flask web application that helps users create and track personalized workout plans based on their fitness goals, preferred exercises, and time availability.

## Features

- Create personalized workout plans
- Select fitness goals and preferred exercise types
- Specify weekly availability
- Save plans for later retrieval
- Modern, responsive UI with animations
- Session-based progress tracking

## Installation

1. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Fill in your fitness profile:
   - Select your fitness goals
   - Choose preferred exercise types
   - Mark your available days for working out

2. Click "Generate Workout Plan" to create your personalized plan

3. Your plan will be saved automatically and can be retrieved when you return to the site

## Technology Stack

- Backend: Flask
- Frontend: HTML5, CSS3, JavaScript
- Styling: Tailwind CSS
- Animations: Animate.css
- Storage: JSON files, Flask-Session
