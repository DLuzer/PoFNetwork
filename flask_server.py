from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['Secret Key'] = 'dannysecret'
socketio = SocketIO(app)

users = {}
num_of_users = 0

base_string = ""
work_range = 0
target = ""
current_count = -1

@app.route('/')
def index():
    return render_template("front_end.html")

@socketio.on("connection")
def handle_connection(conn):
    print("Received: " + conn)

@socketio.on("payload")
def handle_payload(pl):
    pl = str(current_count + 1) + '-' + str(current_count + work_range) + '-' + target + '-' + base_string
    print("Payload in: " + pl)
    emit("payload_in", pl, broadcast = True)

base_string = str(input("Enter base string: "))
work_range = int(input("Enter work range: "))
target = str(input("Enter the target number of leading zeros in the hash: "))
#7299405145

if __name__ == "__main__":
    socketio.run(app) 