from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def main():
    pass

if __name__ == "__main__":
    app.run(port = 80, host = '0.0.0.0', debug = False)