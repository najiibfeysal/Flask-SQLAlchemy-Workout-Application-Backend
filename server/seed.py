from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import date

with app.app_context():

    print("Clearing existing records...")

    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    db.session.commit()

    print("Creating exercises...")

    exercises = [
        Exercise(name="Push Ups", category="Strength", equipment_needed=False),
        Exercise(name="Squats", category="Strength", equipment_needed=False),
        Exercise(name="Treadmill Running", category="Cardio", equipment_needed=True),
        Exercise(name="Bench Press", category="Strength", equipment_needed=True),
        Exercise(name="Plank", category="Core", equipment_needed=False)
    ]

    db.session.add_all(exercises)
    db.session.commit()

    print("Creating workouts...")

    workouts = [
        Workout(date=date.today(), duration_minutes=45, notes="Upper body workout"),
        Workout(date=date.today(), duration_minutes=30, notes="Cardio training"),
        Workout(date=date.today(), duration_minutes=60, notes="Full body workout")
    ]

    db.session.add_all(workouts)
    db.session.commit()

    print("Adding exercises to workouts...")

    workout_exercises = [
        WorkoutExercise(workout_id=workouts[0].id, exercise_id=exercises[0].id, reps=15, sets=3),
        WorkoutExercise(workout_id=workouts[0].id, exercise_id=exercises[3].id, reps=10, sets=3),
        WorkoutExercise(workout_id=workouts[1].id, exercise_id=exercises[2].id, duration_seconds=1200),
        WorkoutExercise(workout_id=workouts[2].id, exercise_id=exercises[1].id, reps=20, sets=4),
        WorkoutExercise(workout_id=workouts[2].id, exercise_id=exercises[4].id, duration_seconds=60, sets=3)
    ]

    db.session.add_all(workout_exercises)
    db.session.commit()

    print("Database seeded successfully!")

    print("Exercises:", Exercise.query.count())
    print("Workouts:", Workout.query.count())
    print("Workout exercises:", WorkoutExercise.query.count())
