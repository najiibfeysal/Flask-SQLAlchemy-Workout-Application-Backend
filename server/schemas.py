from marshmallow import Schema, fields, validates, ValidationError

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment_needed = fields.Bool(required=True)

    @validates("name")
    def validate_name(self, value):
        if not value.strip():
            raise ValidationError("Name cannot be empty.")
        if len(value.strip()) > 100:
            raise ValidationError("Name cannot exceed 100 characters.")

    @validates("category")
    def validate_category(self, value):
        if not value.strip():
            raise ValidationError("Category cannot be empty.")
        if len(value.strip()) > 100:
            raise ValidationError("Category cannot exceed 100 characters.")


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True)
    notes = fields.Str(allow_none=True)

    @validates("duration_minutes")
    def validate_duration(self, value):
        if value <= 0:
            raise ValidationError("Workout duration must be positive.")


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int(allow_none=True)
    sets = fields.Int(allow_none=True)
    duration_seconds = fields.Int(allow_none=True)

    @validates("reps")
    def validate_reps(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Repetitions must be positive.")

    @validates("sets")
    def validate_sets(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Sets must be positive.")

    @validates("duration_seconds")
    def validate_duration(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Exercise duration must be positive.")