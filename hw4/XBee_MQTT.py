import paho.mqtt.client as paho
import serial
import time

# XBee setting
serdev = '/dev/ttyUSB0'
s = serial.Serial(serdev,9600,timeout=5)

mqttc = paho.Client()

# Callbacks
def on_connect(self, mosq, obj, rc):
    print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n")

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed OK")

def on_unsubscribe(mosq, obj, mid, granted_qos):
    print("Unsubscribed OK")

# Set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

host = "localhost"
topic= "hw4"
port = 1883

# Connect and subscribe
print("Connecting to " + host + "/" + topic)
mqttc.connect(host, port=1883, keepalive=60)
mqttc.subscribe(topic, 0)
# Settings for connection


s.write("+++".encode())
char = s.read(2)
print("Enter AT mode.")
print(char.decode())

s.write("ATMY 156\r\n".encode())
char = s.read(3)
print("Set MY 156.")
print(char.decode())

s.write("ATDL 256\r\n".encode())
char = s.read(3)
print("Set DL 256.")
print(char.decode())

s.write("ATID 1\r\n".encode())
char = s.read(3)
print("Set PAN ID 1.")
print(char.decode())

s.write("ATWR\r\n".encode())
char = s.read(3)
print("Write config.")
print(char.decode())

s.write("ATMY\r\n".encode())
char = s.read(4)
print("MY :")
print(char.decode())

s.write("ATDL\r\n".encode())
char = s.read(4)
print("DL : ")
print(char.decode())

s.write("ATCN\r\n".encode())
char = s.read(3)
print("Exit AT mode.")
print(char.decode())

print("start sending RPC")


i = 0
xbee_count = []
X = []
Y = []
Z = []

# get the stationary X Y Z
s.write("/GetAccData/run\r".encode())
# get the times 
ACCcount = s.read(2).decode()
# get the x
x_acc = s.read(6).decode()
# get the y
y_acc = s.read(6).decode()
# get the z
z_acc = s.read(6).decode()
time.sleep(1)


# send RPC to remote per second (20 in total)
while i<21:
    print(i)
    s.write("/GetAccData/run\r".encode())
    # get the times 
    ACCcount = s.read(2).decode()
    print(ACCcount)
    xbee_count.append(ACCcount)

    # get the x
    x_acc = s.read(6).decode()
    print(x_acc)
    X.append(x_acc)

    # get the y
    y_acc = s.read(6).decode()
    print(y_acc)
    Y.append(y_acc)

    # get the z
    z_acc = s.read(6).decode()
    print(z_acc)
    Z.append(z_acc)

    time.sleep(1)
    i = i +1




mesg = "Hello, world!"
mqttc.publish(topic, mesg)  
print(mesg)


i = i +1
    
    
s.close()
