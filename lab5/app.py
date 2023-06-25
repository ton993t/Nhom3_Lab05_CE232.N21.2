
import os
from flask import Flask, render_template
import json
import eventlet
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from flask_migrate import Migrate
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from datetime import datetime
import time
from flask_bootstrap import Bootstrap

eventlet.monkey_patch()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'



### DATABASE SETUPS ############

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app,db)

#######  MQTT SETUPS ############
app.config['MQTT_BROKER_URL'] = 'mqtt.flespi.io'  # use the free broker from flespi
app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
app.config['MQTT_USERNAME'] = 'amW0v62B8MNFOrqZlJqHjCvzL64ywqSuADlVzbmwOYZqfffrOvYXVhnwdfVxtBQU'  # set the username here if you need authentication for the broker
app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
app.config['MQTT_KEEPALIVE'] = 1  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes
mqtt = Mqtt(app)


#######
socketio = SocketIO(app)
bootstrap = Bootstrap(app)


####### Model set up #######
class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    date = db.Column(db.String, nullable=False, default=str(time.strftime("%d/%m/%Y, %H:%M:%S")))
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    

    def __init__(self, temperature, humidity, date):
        self.date = date
        self.humidity = humidity
        self.temperature = temperature
    

    def __repr__(self):
        return "<Record: temperature={0}, huminity= {1}, date={2}".format(self.temperature, self.humidity, self.date)
    
######  
app.app_context().push()
    
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('MP')
    print('MP')


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    with app.app_context():
        print('ON MESSAGE')
        data = message.payload.decode().split(",")
        temperature = data[0]
        humidity = data[1]
        print(temperature)
        print(humidity)
        now = datetime.now()
        db.session.add(Project(temperature=temperature, humidity=humidity, date=str(now.strftime("%d/%m/%Y, %H:%M:%S"))))
        db.session.commit()
    socketio.emit('getTemp', data=data)

@socketio.on('getGraphData')
def handle_get_graph_data():
    query_result = Project.query.order_by(sqlalchemy.desc(Project.id)).limit(5).all()
    data = [0 for x in range(5)]
    for i in range(5):
        data[4-i]= str(query_result[i].temperature)+";"+str(query_result[i].humidity)+";"+str(query_result[i].date)
    socketio.emit('drawGraph', data=data)

    
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=False)
    #app.run(host='0.0.0.0', port = 5000)