from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy

class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, Primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    equiment_needed = db.Column(db.Boolean, nullable=False)

    workout_exercises = db.relationship("WorkoutExercise", back_populates="exercise")

    workouts = db.relationship("Workout", secondary="workout_exercise")

class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, Primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship("WorkoutExercise", back_populates="workout", cascade="all, delete-orphan")

    exercise = db.relationship("Workout", secondary="workout_exercise")

class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercise"

    id = db.Column(db.Integer, Primary_key=True)

    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)

    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    durations_seconds = db.Column(db.Integer)

    workout = db.relationship("Workout", back_populates="workout_exercise")

    exercise = db.relationship("Exercise", back_populates="workout_exercise")