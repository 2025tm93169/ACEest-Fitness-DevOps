from flask import Flask, jsonify, request

app = Flask(__name__)

PROGRAMS = {
    "Fat Loss": {
        "factor": 22,
        "description": "Fat-loss focused training and nutrition plan",
        "workout": ["Back Squat", "Cardio", "Bench Press", "Deadlift", "Recovery"],
    },
    "Muscle Gain": {
        "factor": 35,
        "description": "Muscle-gain focused hypertrophy program",
        "workout": ["Squat", "Bench Press", "Deadlift", "Overhead Press", "Rows"],
    },
    "Beginner": {
        "factor": 26,
        "description": "Simple full-body beginner program",
        "workout": ["Air Squats", "Ring Rows", "Push-ups"],
    },
}


@app.get("/")
def home():
    return jsonify({
        "application": "ACEest Fitness & Gym",
        "status": "running",
        "version": "1.0.0",
    })


@app.get("/health")
def health():
    return jsonify({"status": "UP"})


@app.get("/programs")
def get_programs():
    return jsonify({
        "programs": [
            {"name": name, **data}
            for name, data in PROGRAMS.items()
        ]
    })


@app.get("/programs/<program_name>")
def get_program(program_name):
    program = next(
        (name for name in PROGRAMS if name.lower() == program_name.lower()),
        None,
    )
    if program is None:
        return jsonify({"error": "Program not found"}), 404
    return jsonify({"name": program, **PROGRAMS[program]})


def calculate_calories(weight: float, program: str) -> int:
    """Estimate daily calories using the selected ACEest program factor."""
    if program not in PROGRAMS:
        raise ValueError("Invalid program")
    if weight <= 0:
        raise ValueError("Weight must be greater than zero")
    return int(weight * PROGRAMS[program]["factor"])


@app.post("/calculate-calories")
def calories():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON"}), 400
    weight = data.get("weight")
    program = data.get("program")
    if weight is None or program is None:
        return jsonify({"error": "weight and program are required"}), 400
    try:
        weight = float(weight)
        calories_value = calculate_calories(weight, program)
    except (TypeError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify({"weight": weight, "program": program, "calories": calories_value})


@app.post("/clients")
def create_client():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON"}), 400
    required_fields = ("name", "age", "weight", "program")
    missing = [field for field in required_fields if field not in data]
    if missing:
        return jsonify({"error": "Missing required fields", "fields": missing}), 400
    try:
        age = int(data["age"])
        weight = float(data["weight"])
    except (TypeError, ValueError):
        return jsonify({"error": "age must be an integer and weight must be numeric"}), 400
    if age <= 0 or weight <= 0:
        return jsonify({"error": "age and weight must be greater than zero"}), 400
    program = data["program"]
    if program not in PROGRAMS:
        return jsonify({"error": "Invalid program"}), 400
    return jsonify({
        "message": "Client profile validated",
        "client": {
            "name": str(data["name"]).strip(),
            "age": age,
            "weight": weight,
            "program": program,
            "estimated_calories": calculate_calories(weight, program),
        },
    }), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
