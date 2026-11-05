from flask import Flask, request, jsonify
from models import db, Exercise, Workout, WorkoutExercise
from schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema
from flask_migrate import Migrate
from marshmallow import ValidationError

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///workout.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

# Initialize schemas
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)


def get_request_data():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return None, jsonify({
            "error": "Invalid or missing JSON data."
        }), 400

    return data, None, None


@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200



@app.route("/exercises", methods=["POST"])
def create_exercise():
    data, error_response, status_code = get_request_data()

    if error_response:
        return error_response, status_code

    try:
        exercise_data = exercise_schema.load(data)
        exercise = Exercise(**exercise_data)

        db.session.add(exercise)
        db.session.commit()

        return jsonify(exercise_schema.dump(exercise)), 201

    except ValidationError as e:
        return jsonify(e.messages), 400

    except Exception as e:
        db.session.rollback()
        print("CREATE EXERCISE ERROR:", repr(e))
        return jsonify({"error": "Could not create exercise."}), 400


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)

    if not exercise:
        return jsonify({"error": "Exercise not found."}), 404

    result = exercise_schema.dump(exercise)

    result["workouts"] = [
        {
            "id": workout.id,
            "date": workout.date.isoformat(),
            "duration_minutes": workout.duration_minutes
        }
        for workout in exercise.workouts
    ]

    return jsonify(result), 200


@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)

    if not exercise:
        return jsonify({"error": "Exercise not found."}), 404

    try:
        db.session.delete(exercise)
        db.session.commit()

        return jsonify({
            "message": "Exercise deleted successfully."
        }), 200

    except Exception:
        db.session.rollback()
        return jsonify({"error": "Could not delete exercise."}), 400



@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200



@app.route("/workouts", methods=["POST"])
def create_workout():
    data, error_response, status_code = get_request_data()

    if error_response:
        return error_response, status_code

    try:
        workout_data = workout_schema.load(data)

        # Convert dictionary into Workout model
        workout = Workout(**workout_data)

        db.session.add(workout)
        db.session.commit()

        return jsonify(workout_schema.dump(workout)), 201

    except ValidationError as e:
        return jsonify(e.messages), 400

    except Exception as e:
        db.session.rollback()
        print("CREATE WORKOUT ERROR:", repr(e))
        return jsonify({"error": "Could not create workout."}), 400

@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = db.session.get(Workout, id)

    if not workout:
        return jsonify({"error": "Workout not found."}), 404

    result = workout_schema.dump(workout)

    result["workout_exercises"] = [
        {
            "id": item.id,
            "exercise": exercise_schema.dump(item.exercise),
            "reps": item.reps,
            "sets": item.sets,
            "duration_seconds": item.duration_seconds
        }
        for item in workout.workout_exercises
    ]

    return jsonify(result), 200


@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = db.session.get(Workout, id)

    if not workout:
        return jsonify({"error": "Workout not found."}), 404

    try:
        db.session.delete(workout)
        db.session.commit()

        return jsonify({
            "message": "Workout deleted successfully."
        }), 200

    except Exception:
        db.session.rollback()
        return jsonify({"error": "Could not delete workout."}), 400



@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"]
)
def create_workout_exercise(workout_id, exercise_id):

    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)

    if not workout:
        return jsonify({"error": "Workout not found."}), 404

    # Check if exercise already exists in this workout
    existing = WorkoutExercise.query.filter_by(workout_id=workout_id, exercise_id=exercise_id).first()

    if existing:
        return jsonify({
            "error": "This exercise is already in the workout."
        }), 400

    data, error_response, status_code = get_request_data()

    if error_response:
        return error_response, status_code

    data["workout_id"] = workout_id
    data["exercise_id"] = exercise_id

    errors = workout_exercise_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    try:
        workout_exercise = WorkoutExercise(**data)

        db.session.add(workout_exercise)
        db.session.commit()

        return jsonify(
            workout_exercise_schema.dump(workout_exercise)
        ), 201

    except Exception:
        db.session.rollback()
        return jsonify({
            "error": "Could not add exercise to workout."
        }), 400



@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Resource or endpoint not found."
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "error": "Method not allowed."
    }), 405


if __name__ == "__main__":
    app.run(port=5555, debug=True)