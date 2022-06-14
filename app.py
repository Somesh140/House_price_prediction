from flask import Flask

app=Flask(__name__)

@app.route("/",methods=['GET','POST'])
def index():
    return "starting ml project CI CD pipeline established"

if __name__=="__main__":
    app.run(debug=True)
