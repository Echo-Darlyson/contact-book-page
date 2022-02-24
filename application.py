from flask import Flask, render_template, request
import psycopg2, config

# Database
params = config.config() # return the params of the db
con = psycopg2.connect(**params)
cur = con.cursor()

# Flask application
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("bootstrap-template/index.html")

@app.route("/query", methods=["POST"])
def query():
    name = request.form["query_contact"]
    if name.capitalize() != "All":
        cur.execute(f"select * from contacts where name='{name}'")
    else:
        cur.execute("select * from contacts")
    recset = cur.fetchall()
    return render_template("bootstrap-template/index.html", recset1=recset)

@app.route("/create", methods=["POST"])
def create():
    name = request.form["create_contact"]
    phone = request.form["create_phone"]
    cur.execute(f"insert into contacts values ('{name}', '{phone}')")
    con.commit()
    cur.execute(f"select * from contacts where phone='{phone}'")
    rec = cur.fetchone()
    return render_template("bootstrap-template/index.html", rec1=rec)

@app.route("/delete", methods=["POST"])
def delete():
    name = request.form["delete_contact"]
    cur.execute(f"delete from contacts where name='{name}'")
    con.commit()
    cur.execute("select count(*) from contacts")
    numberOfRows = cur.fetchone()[0]
    cur.execute("select * from contacts")
    recset = cur.fetchall()
    if recset != None:
        return render_template("bootstrap-template/index.html", recset2=recset, rows=numberOfRows)
    else:
        return render_template("bootstrap-template/index.html", recset2=recset, rows=numberOfRows)

@app.route("/update", methods=["POST"])
def update():
    name = request.form["update_contact"]
    phone = request.form["update_phone"]
    cur.execute(f"update contacts set phone='{phone}' where name='{name}'")
    con.commit()
    cur.execute(f"select * from contacts where phone='{phone}'")
    rec = cur.fetchone()
    return render_template("bootstrap-template/index.html", rec2=rec)