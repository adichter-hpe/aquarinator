from numpy import empty
from random import randrange
from flask import Flask, render_template, request
import pyrebase, re
from datetime import datetime


app = Flask(__name__)
config = {
    "apiKey": "AIzaSyCcV6PK2HiV-gw_A2YwtpQChjmjZpRzWz0",
    "authDomain": "aquarinator.firebaseapp.com",
    "databaseURL": "https://aquarinator-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "aquarinator",
    "storageBucket": "aquarinator.appspot.com",
    "messagingSenderId": "781335927219",
    "appId": "1:781335927219:web:891a83fe25fd12027dd3c6",
    "measurementId": "G-SYW64LTQZR"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

def add_measurement(moisture): 
    timestamp = str(datetime.now())[11:-10]
    key = re.sub('\.|\-|\:|\ ', '', str(datetime.now()))
    data = {'timestamp': timestamp, 'moisture': moisture}
    db.child('moisture_mesurements').child(key).set(data)

def get_labels_values(data):
    labels = []
    values = []
    pro_data = []
    if data.val() is None:
        return [],[]

    for i in data.each():
        pro_data.append(i.val())
    if len(pro_data) <= 30:
        i = len(pro_data)
        j = 0
        while i > 0:
            labels.append(pro_data[j]['time'])
            values.append(pro_data[j]['moisture'])
            i-=1
            j+=1
    elif len(pro_data) > 30:
        i = 30
        j = len(pro_data) - 30
        while i > 0:
            labels.append(pro_data[j]['time'])
            values.append(pro_data[j]['moisture'])
            i-=1
            j+=1
    return labels, values

@app.route('/', methods = ['GET', 'POST'])
def base_control():
    data = db.child('moisture_mesurements').get()
    labels, values = get_labels_values(data)
    if len(values) > 0 :
        humidity = str(int(values[-1]*100))+ '%'
    elif len(values) == 0:
        humidity = 'no measurement yet...'
    
    print(type(data))
    if request.method == 'POST':
        i = 29
        # adding random values to db:

        #while i > 0: 
        #    add_measurement(randrange(10)/10)
        #    i-=1
        
        # Hier bewässerungsfunktion einfügen
    return render_template('base_control.html',
                            labels = labels,
                            values = values,
                            humidity = humidity)

@app.route('/advanced')
def advanced():
    return render_template('advanced.html')


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')