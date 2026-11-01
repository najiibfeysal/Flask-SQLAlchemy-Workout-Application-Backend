from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy

class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, Primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    equiment_needed = db.Column(db.Boolean, nullable=False)

class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, Primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercise"

    id = db.Column(db.Integer, Primary_key=True)

    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)

    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    durations_seconds = db.Column(db.Integer)