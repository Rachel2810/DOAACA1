from flask import Flask, render_template, request, redirect, session, jsonify
from services.auth_service import check_login
from services.prediction_service import load_model, run_prediction
from database.db_helper import init_db, insert_history, fetch_history
import os

app = Flask(__name__)
app.config.from_object("config.Config")

# Initialize SQLite DB
init_db()

# Load model on startup
model = load_model()

# ---------------------
# ROUTES
# ---------------------

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if check_login(username, password):
            session["user"] = username
            return redirect("/home")
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@app.route("/home")
def home():
    if "user" not in session:
        return redirect("/")
    return render_template("home.html")


@app.route("/predict", methods=["GET", "POST"])
def predict():
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        try:
            feature1 = float(request.form.get("feature1"))
            feature2 = float(request.form.get("feature2"))
            feature3 = float(request.form.get("feature3"))

            prediction = run_prediction(model, [feature1, feature2, feature3])

            insert_history(feature1, feature2, feature3, prediction, session["user"])

            return render_template("predict.html", result=prediction)
        except Exception as e:
            return render_template("predict.html", error=str(e))

    return render_template("predict.html")


@app.route("/history")
def history():
    if "user" not in session:
        return redirect("/")

    rows = fetch_history()
    return render_template("history.html", rows=rows)


# ---------------------
# API ENDPOINT
# ---------------------
@app.route("/api/predict", methods=["POST"])
def api_predict():
    try:
        data = request.json
        features = data["features"]   # expecting list: [x1, x2, x3]
        prediction = run_prediction(model, features)

        return jsonify({
            "status": "success",
            "prediction": prediction
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400


if __name__ == "__main__":
    app.run(debug=True)
