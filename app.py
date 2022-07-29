from flask import Flask, render_template, Response
import psycopg2
from flask_cors import CORS
import csv
from datetime import datetime
app = Flask(__name__)
t_host = "ec2-44-206-117-24.compute-1.amazonaws.com"  # either "localhost", a domain name, or an IP address.
t_port = "5432"  # default postgres port
t_dbname = "d5knigjrb5pdph"
t_user = "euxqqreycxujvt"
t_pw = "6fb679bd22aec45667687c79a3e4ed958c81cf584b489302a1bb38a9fe397469"


@app.route('/')
def homepage():

    return """
    <h1>Hello heroku</h1>"""

@app.route('/mandsDemoOrg/getLeads', methods=['GET'])
def data():
    s = 'SELECT * FROM "leads"'
    try:
        db_conn = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_user, password=t_pw)
        db_cursor = db_conn.cursor()
        db_cursor.execute(s)
        column_names = [desc[0] for desc in db_cursor.description]
        leadlist = db_cursor.fetchall()
        ourData = []
        for x in leadlist:
            listing = [x[0], x[1], x[2]]
            ourData.append(listing)

        with open('crypto.csv', "w", encoding="UTF8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(column_names)
            writer.writerows(ourData)

        with open("crypto.csv") as fp:
            newCsv = fp.read()

        return Response(
            newCsv,
            mimetype="text/csv",
            headers={"Content-disposition":
                         "attachment; filename=leads.csv"})
    except Exception as e:
        print(e)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

