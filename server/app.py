
from flask import Flask, request, jsonify
from models import db, Exercise, Workout, WorkoutExercise
from schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema
from datetime import date

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///workout.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    print("Database created successfully!")

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

# EXERCISES CRUD
@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200


@app.route("/exercises", methods=["POST"])
def create_exercise():
    data, error_response, status_code = get_request_data()

    if error_response:
        return error_response, status_code

    errors = exercise_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    exercise = Exercise(**data)

    db.session.add(exercise)
    db.session.commit()

    return jsonify(exercise_schema.dump(exercise)), 201


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)

    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    return jsonify(exercise_schema.dump(exercise)), 200


@app.route("/exercises/<int:id>", methods=["PATCH"])
def update_exercise(id):
    exercise = db.session.get(Exercise, id)

    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    data, error_response, status_code = get_request_data()

    if error_response:
        return error_response, status_code

    errors = exercise_schema.validate(data, partial=True)

    if errors:
        return jsonify(errors), 400

    for key, value in data.items():
        setattr(exercise, key, value)

    db.session.commit()

    return jsonify(exercise_schema.dump(exercise)), 200


@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)

    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    db.session.delete(exercise)
    db.session.commit()

    return jsonify({"message": "Exercise deleted successfully"}), 200


# WORKOUTS CRUD
@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200

@app.route("/workouts", methods=["POST"])
def create_workout():
    data, error_response, status_code = get_request_data()

    if error_response:
        return error_response, status_code

    errors = workout_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    data["date"] = date.fromisoformat(data["date"])

    workout = Workout(**data)

    db.session.add(workout)
    db.session.commit()

    return jsonify(workout_schema.dump(workout)), 201


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = db.session.get(Workout, id)

    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    return jsonify(workout_schema.dump(workout)), 200


@app.route("/workouts/<int:id>", methods=["PATCH"])
def update_workout(id):
    workout = db.session.get(Workout, id)

    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    data, error_response, status_code = get_request_data()

    if error_response:
        return error_response, status_code

    errors = workout_schema.validate(data, partial=True)

    if errors:
        return jsonify(errors), 400

    for key, value in data.items():
        if key == "date":
            value = date.fromisoformat(value)

        setattr(workout, key, value)

    db.session.commit()

    return jsonify(workout_schema.dump(workout)), 200


@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = db.session.get(Workout, id)

    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    db.session.delete(workout)
    db.session.commit()

    return jsonify({"message": "Workout deleted successfully"}), 200


# WORKOUT-EXERCISES CRUD
@app.route("/workout-exercises", methods=["GET"])
def get_workout_exercises():
    workout_exercises = WorkoutExercise.query.all()
    return jsonify(workout_exercises_schema.dump(workout_exercises)), 200


@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"]
)
def create_workout_exercise(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)

    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    data, error_response, status_code = get_request_data()

    if error_response:
        return error_response, status_code

    data["workout_id"] = workout_id
    data["exercise_id"] = exercise_id

    errors = workout_exercise_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    workout_exercise = WorkoutExercise(**data)

    db.session.add(workout_exercise)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Could not add exercise to workout"}), 400

    return jsonify(workout_exercise_schema.dump(workout_exercise)), 201


@app.route("/workout-exercises/<int:id>", methods=["GET"])
def get_workout_exercise(id):
    workout_exercise = db.session.get(WorkoutExercise, id)

    if not workout_exercise:
        return jsonify({"error": "Workout exercise not found"}), 404

    return jsonify(workout_exercise_schema.dump(workout_exercise)), 200


@app.route("/workout-exercises/<int:id>", methods=["PATCH"])
def update_workout_exercise(id):
    workout_exercise = db.session.get(WorkoutExercise, id)

    if not workout_exercise:
        return jsonify({"error": "Workout exercise not found"}), 404

    data, error_response, status_code = get_request_data()

    if error_response:
        return error_response, status_code

    errors = workout_exercise_schema.validate(data, partial=True)

    if errors:
        return jsonify(errors), 400

    for key, value in data.items():
        setattr(workout_exercise, key, value)

    db.session.commit()

    return jsonify(workout_exercise_schema.dump(workout_exercise)), 200

@app.route("/workout-exercises/<int:id>", methods=["DELETE"])
def delete_workout_exercise(id):
    workout_exercise = db.session.get(WorkoutExercise, id)

    if not workout_exercise:
        return jsonify({"error": "Workout exercise not found"}), 404

    db.session.delete(workout_exercise)
    db.session.commit()

    return jsonify({"message": "Workout exercise deleted successfully"}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Resource or endpoint not found."
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "error": "Method not allowed for this endpoint."
    }), 405


# RUN APPLICATION
if __name__ == "__main__":
    app.run(debug=True)
