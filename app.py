from flask import Flask, jsonify

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
