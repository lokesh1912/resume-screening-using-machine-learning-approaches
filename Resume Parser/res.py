from flask import Flask

app=Flask(__name__)

@app.route("/")
def fal():
    return "heloo"

if __name__=="__main__" :
    app.run(debug=True)