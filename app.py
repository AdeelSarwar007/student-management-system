from flask import Flask, render_template,request,redirect
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")
@app.route("/home")
def home1():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":

        name = request.form["student_name"]

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor() 

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS student(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        """)

        cursor.execute(
            "INSERT INTO student(name) VALUES(?)",
            (name,)
        )

        conn.commit()
        conn.close()

        print("Student Added Successfully")

    return render_template("add.html")
@app.route("/students")
def students():

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM student")
    rows = cursor.fetchall()

    conn.close()

    return render_template(
        "student.html",
        students=rows
    )
@app.route("/delete/<int:id>")
def delete_student(id):

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM student WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/students")
@app.route("/search", methods=["GET", "POST"])
def search():

    students = []

    if request.method == "POST":

        name = request.form["name"]

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM student WHERE name LIKE ?",
            ('%' + name + '%',)
        )

        students = cursor.fetchall()

        conn.close()

    return render_template(
        "search.html",
        students=students
    )
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update_student(id):

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]

        cursor.execute(
            "UPDATE student SET name=? WHERE id=?",
            (name, id)
        )

        conn.commit()
        conn.close()

        return redirect("/students")

    cursor.execute(
        "SELECT * FROM student WHERE id=?",
        (id,)
    )

    student = cursor.fetchone()

    conn.close()

    return render_template(
        "update.html",
        student=student
    )

@app.route("/test")
def test():
    return "Test Route Working"

if __name__ == "__main__":
    app.run(debug=True)


