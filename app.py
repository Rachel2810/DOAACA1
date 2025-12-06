from flask import Flask, render_template, request, redirect, session
import joblib
import numpy as np
from datetime import datetime

# IMPORT DB HELPER
from database.db_helper import init_db, insert_prediction, fetch_predictions

app = Flask(__name__)
app.secret_key = "supersecretkey"


# -----------------------------
# Function to clean float formatting in templates
# -----------------------------
@app.template_filter("clean")
def clean_filter(x):
    try:
        x = float(x)
        return int(x) if x.is_integer() else x
    except:
        return x


# -----------------------------
# Load ML Model (Pipeline)
# -----------------------------
model_path = "./model_training/random_forest_model.pkl"
model = joblib.load(model_path)
print("Model loaded:", type(model))


# -----------------------------
# Initialize SQLite database
# -----------------------------
init_db()


# -----------------------------
# Helper function to clean float formatting
# -----------------------------
def clean_value(x):
    return int(x) if float(x).is_integer() else float(x)


# -----------------------------
# function to format datetime in templates
# -----------------------------

from datetime import datetime

@app.template_filter("format_datetime")
def format_datetime(value):
    try:
        dt = datetime.fromisoformat(value)
        return dt.strftime("%d %b %Y, %#I:%M %p")# Example: 06 Dec 2025, 3:42 AM
    except:
        return value

# -----------------------------
# LOGIN ROUTES
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username")
        pwd = request.form.get("password")

        if user == "admin" and pwd == "admin123":
            session["user"] = user
            return redirect("/home")
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# -----------------------------
# HOME PAGE
# -----------------------------
@app.route("/home")
def home():
    if "user" not in session:
        return redirect("/login")
    return render_template("home.html", user=session["user"])


# -----------------------------
# PREDICTION PAGE
# -----------------------------
@app.route("/", methods=["GET"])
@app.route("/predict", methods=["GET", "POST"])
def predict():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        try:
            area = float(request.form.get("area"))
            beds = float(request.form.get("beds"))
            baths = float(request.form.get("baths"))

            area_clean = clean_value(area)
            beds_clean = clean_value(beds)
            baths_clean = clean_value(baths)

            # Predict
            features = np.array([[area, beds, baths]])
            prediction = model.predict(features)[0]
            formatted_price = f"{prediction:,.2f}"

            # SAVE to database (USING DB HELPER)
            insert_prediction(
                session["user"],
                area_clean,
                beds_clean,
                baths_clean,
                formatted_price,
                "random_forest"
            )

            return render_template(
                "predict.html",
                result=formatted_price,
                area=area_clean,
                beds=beds_clean,
                baths=baths_clean
            )

        except Exception as e:
            return render_template("predict.html", error=f"Error: {str(e)}")

    return render_template("predict.html")


# -----------------------------
# HISTORY PAGE
# -----------------------------
@app.route("/history")
def history():
    if "user" not in session:
        return redirect("/login")

    rows = fetch_predictions()
    return render_template("history.html", rows=rows)


# -----------------------------
# Run Flask
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
