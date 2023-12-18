import paho.mqtt.client as mqtt
import time
import json
import threading

last_motion_sensor_state = None
last_noise_sensor_state = None
timer = None

def on_message_noise(client, userdata, msg):
    raw = str(msg.payload.decode('utf-8'))
    global last_noise_sensor_state
    last_noise_sensor_state = raw


def on_message_triple_sensor(client, userdata, msg):
    raw = str(msg.payload.decode('utf-8'))
    data = json.loads(raw)
    # just grab the motion sensor
    if 4 == data['id']:
        global last_motion_sensor_state
        last_motion_sensor_state = data


def turn_off_lamps():
    print('turning off floor lamp living room')
    topic = 'hue2mqtt/light/00:17:88:01:08:b3:4a:4e-0b/set'
    payload = ''.join({"on", "false"})
    print('turning off tiffany lamp living room')
    #client.publish(topic, payload, qos=0)


def control_environment(no_one_present):
    global timer
    if no_one_present:
        #print("Starting a 10 min timer to turn of the lamps")
        if timer is None:
            timer = threading.Timer(10.0, turn_off_lamps)
            timer.start()
            print('Timer started')
    else:
        #print("aborting the timer")
        if timer is not None:
            timer.cancel()
            timer = None
            print('timer cancelled')
        


client = mqtt.Client("smarthue_server")
client.message_callback_add('sensor/noise', on_message_noise)
client.message_callback_add('hue2mqtt/sensor/+', on_message_triple_sensor)

client.connect('192.168.178.2', 1883)
# start a new thread
client.loop_start()
client.subscribe("sensor/noise")
client.subscribe("hue2mqtt/sensor/#")

while True:
    motion_detected = False
    if last_motion_sensor_state is not None:
        motion_detected = last_motion_sensor_state['state']['presence']

    noise_detected = False
    if last_noise_sensor_state is not None:
        if "0" in last_noise_sensor_state:
            noise_detected = True
        else:
            noise_detected = False
    
    no_one_present = True
    if not noise_detected and not motion_detected:
        no_one_present = True
    else:
        no_one_present = False
    
    control_environment(no_one_present)
    
    time.sleep(1)



# TODO
# make it running like the hue2mqtt and register it as a systemd service