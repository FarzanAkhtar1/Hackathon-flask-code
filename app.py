subscriptionKey = ""
faceServiceName = ""
faceGroupName = ""


# import the Flask class from the flask module
import http.client, urllib.request, urllib.parse, urllib.error, base64
from flask import Flask, render_template, redirect, url_for, request, session, flash, Markup
from functools import wraps
import ast

# create the application object
app = Flask(__name__)

# Need to be random
app.secret_key = "my precious"

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap


# use decorators to link the function to a url
@app.route('/')
@login_required
def home():
    results = fetchQuery("localhost", "farzan", "farzan", "circle", "select * from posts")
    #print(results)
    return render_template('index.html', posts=results)  # render a template

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        string = "User name: " + request.form['username'] + "<br>"
        text = string + "User image :" + request.form['password'] + "<br>"
        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': subscriptionKey,
        }

        params = urllib.parse.urlencode({
        })
        body = "{'name': '" + request.form['username'] + "'}"


        try:
            conn = http.client.HTTPSConnection(faceServiceName + '.cognitiveservices.azure.com')
            
            conn.request("POST", "/face/v1.0/largepersongroups/" + faceGroupName + "/persons?%s" % params, body, headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            print(data.decode("utf-8"))

            text = text + "Person ID: " + ast.literal_eval(data.decode("utf-8"))["personId"] + "<br>"


            flash(Markup(text))
            #flash(data)
            conn.close()
        except Exception as e:
            flash(e)    

        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': subscriptionKey,
        }
        params = urllib.parse.urlencode({'detectionModel': 'detection_01'})
        body = "{'url': '" + request.form['password'] + "'}"


        try:
            conn = http.client.HTTPSConnection(faceServiceName + '.cognitiveservices.azure.com')
            conn.request("POST", "/face/v1.0/largepersongroups/" + faceGroupName + "/persons/" + ast.literal_eval(data.decode("utf-8"))["personId"] + "/persistedfaces?%s" % params, body, headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            flash("Persisted Face ID: "+ ast.literal_eval(data.decode("utf-8"))['persistedFaceId'])
            conn.close()
        except Exception as e:
            print(e) 

        return redirect(url_for('login'))
    return render_template('login.html', error=error)



# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
