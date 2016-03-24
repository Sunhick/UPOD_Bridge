#
# Author : Sunil bn <suba5417@colorado.edu>
# Project: YPOD v2.0
#
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="10.201.22.58", port = 5000)
