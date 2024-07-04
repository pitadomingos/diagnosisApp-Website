from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = '13035'  # Needed for flash messages and session management

# Define menu items with corresponding endpoints
MENU = [
    {"name": "Create New Patient", "url": "create_patient"},
    {"name": "View Patient Information", "url": "view_patient_info"},
    {"name": "View Lab Test Results", "url": "view_lab_results"},
    {"name": "Consultation", "url": "consultation"},
    {"name": "Print Patient Report", "url": "print_patient_report"},
    {"name": "Exit", "url": "exit"}
]

users = {"Pita Domingos": {"password": "password", "groups": ["admin"]},
         "Pita": {"password": "password", "groups": ["admin"]}}
groups = {"admin": ["Pita Domingos"], "user": [],
          "user": ["Pita"], "user": []}
          

@app.route("/", methods=["GET", "POST"])
def credentials():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username]["password"] == password:
            session['username'] = username
            return redirect(url_for("home_page"))
        else:
            flash("Invalid credentials. Please provide the correct credentials")
    return render_template("credentials.html")

@app.route("/home_page/")
def home_page():
    if 'username' not in session:
        return redirect(url_for("credentials"))
    username = session['username']
    menu = MENU.copy()
    if "admin" in users[username]["groups"]:
        menu.append({"name": "Admin", "url": "admin"})
    return render_template("home.html", menu=menu, username=username)

# Define the routes for the menu items with authentication checks
@app.route("/create_patient")
def create_patient():
    if 'username' not in session:
        return redirect(url_for("credentials"))
    return render_template("create_patient.html")

@app.route("/view_patient_info")
def view_patient_info():
    if 'username' not in session:
        return redirect(url_for("credentials"))
    return render_template("view_patient_info.html")

@app.route("/view_lab_results")
def view_lab_results():
    if 'username' not in session:
        return redirect(url_for("credentials"))
    return render_template("view_lab_results.html")

@app.route("/consultation")
def consultation():
    if 'username' not in session:
        return redirect(url_for("credentials"))
    return render_template("consultation.html")

@app.route("/print_patient_report")
def print_patient_report():
    if 'username' not in session:
        return redirect(url_for("credentials"))
    return render_template("print_patient_report.html")

@app.route("/exit")
def exit():
    session.pop('username', None)
    return redirect(url_for("credentials"))

# Admin route
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if 'username' not in session or "admin" not in users[session['username']]["groups"]:
        return redirect(url_for("credentials"))

    if request.method == "POST":
        if "create_user" in request.form:
            new_username = request.form["new_username"]
            new_password = request.form["new_password"]
            users[new_username] = {"password": new_password, "groups": ["user"]}
            groups["user"].append(new_username)
            flash(f"User {new_username} created successfully")
        elif "create_group" in request.form:
            new_group = request.form["new_group"]
            if new_group not in groups:
                groups[new_group] = []
                flash(f"Group {new_group} created successfully")
            else:
                flash(f"Group {new_group} already exists")

    return render_template("admin.html", users=users, groups=groups)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
