Flask SQLAlchemy Workout Application Backend
About the Project

This is a workout management application built using Python, Flask, and SQLAlchemy.

It helps personal trainers manage workouts and exercises.

Users can:

Create workouts.
Create exercises.
Add exercises to workouts.
View workouts and exercises.
Delete workouts and exercises.
Technologies Used
Python
Flask
Flask-SQLAlchemy
Flask-Migrate
Marshmallow
SQLite
Pipenv
Project Structure
text
project/
├── server/
│   ├── app.py
│   ├── models.py
│   ├── schemas.py
│   └── seed.py
├── instance/
│   └── workout.db
├── Pipfile
├── Pipfile.lock
├── .gitignore
└── README.md

Installation
1. Clone the project
bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Flask-SQLAlchemy-Workout-Application-Backend

2. Install dependencies
bash
pipenv install

3. Activate the environment
bash
pipenv shell

4. Enter the server folder
bash
cd server

5. Set up the database
bash
flask --app app db init
flask --app app db migrate -m "Initial migration"
flask --app app db upgrade

6. Add sample data
bash
python seed.py

Run the Application

Start the server:

bash
python app.py


Open your browser and visit:

http://127.0.0.1:5555

API Endpoints
Exercises
Method	Endpoint	Purpose
GET	/exercises	View all exercises
GET	/exercises/<id>	View one exercise
POST	/exercises	Create an exercise
DELETE	/exercises/<id>	Delete an exercise
Workouts
Method	Endpoint	Purpose
GET	/workouts	View all workouts
GET	/workouts/<id>	View one workout
POST	/workouts	Create a workout
DELETE	/workouts/<id>	Delete a workout
Add an Exercise to a Workout

POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises

This endpoint adds an exercise to a workout.

Example Request

Create an exercise:

json
{
    "name": "Push Ups",
    "category": "Strength",
    "equipment_needed": false
}


Create a workout:

json
{
    "date": "2026-11-04",
    "duration_minutes": 45,
    "notes": "Upper body workout"
}

Database Models

The project has three models:

Workout: Stores workout details.
Exercise: Stores exercise details.
WorkoutExercise: Connects workouts and exercises.

A workout can have many exercises, and an exercise can be used in different workouts.

Validations

The application checks that:

Names are not empty.
Workout duration is positive.
Repetitions and sets are positive.
Exercise duration is positive.
An exercise is not added twice to the same workout.
Dates are valid.
Author

Moringa School Summative Lab Project.