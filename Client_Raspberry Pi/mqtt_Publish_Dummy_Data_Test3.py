#------------------------------------------
#--- Author: Pradeep Singh
#--- Date: 20th January 2017
#--- Version: 1.0
#--- Python Ver: 2.7
#--- Details At: https://iotbytes.wordpress.com/store-mqtt-data-from-sensors-into-sql-database/
#------------------------------------------

import time
import paho.mqtt.client as mqtt
import random, threading, json
from datetime import datetime
import Feedback
import csv
#====================================================
# MQTT Settings 
MQTT_Broker = "iot.eclipse.org"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic_PV_3 = "Sensor/PV_3"
#MQTT_Topic_PV_2 = "Sensor/PV_2"

#====================================================

def on_connect(client, userdata, rc):
	if rc != 0:
		pass
		print("Unable to connect to MQTT Broker...")
	else:
		print("Connected with MQTT Broker: ") + str(MQTT_Broker)

def on_publish(client, userdata, mid):
	pass
		
def on_disconnect(client, userdata, rc):
	if rc !=0:
		pass
		
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_publish = on_publish
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))		

		
def publish_To_Topic(topic, message):
	mqttc.publish(topic,message)
	print ("Published: " + str(message) + " " + "on MQTT Topic: " + str(topic))
	print ("")


#====================================================
# FAKE SENSOR 
# Dummy code used as Fake Sensor to publish some random values
# to MQTT Broker

toggle = 0

sample = open("sample_data.csv", "r")
readCSV = csv.reader(sample)
Voltages = []
Currents = []
for row in readCSV:
	Voltage = row[0]
	Current = row[1]
	Voltages.append(Voltage)
	Currents.append(Current)


def publish_Fake_Sensor_Values_to_MQTT(Voltages, Currents):
	#global toggle
	#if toggle == 0:
	#Humidity_Fake_Value = float("{0:.2f}".format(random.uniform(50, 100)))
	i = 0
	while i < 51:
		threading.Timer(3.0, publish_Fake_Sensor_Values_to_MQTT).start()
		Voltage_Fake_Value = float(Voltages[i])
		Current_Fake_Value = float(Currents[i])
		PV_3_Data = {}
		PV_3_Data['Sensor_ID'] = "PV-3"
		PV_3_Data['Date'] = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f")
		PV_3_Data['Voltage'] = Voltage_Fake_Value
		PV_3_Data['Current'] = Current_Fake_Value
		PV_3_json_data = json.dumps(PV_3_Data)
		Power = Voltage_Fake_Value*Current_Fake_Value
		Power = "{:.2f}".format(Power)
		print ("Publishing PV 3 fake Voltage, Current, Power Value: " + str(Voltage_Fake_Value) + ", " + str(Current_Fake_Value) + ", " + str(Power) + "...")
		publish_To_Topic (MQTT_Topic_PV_3, PV_3_json_data)
		i += 1
		time.sleep(0.2)
	#toggle = 1

	#else:
		#Temperature_Fake_Value = float("{0:.2f}".format(random.uniform(1, 30)))
		#Voltage_Fake_Value = float("{0:.2f}".format(random.uniform(1, 30)))
		#Current_Fake_Value = float("{0:.2f}".format(random.uniform(1, 30)))
		#PV_2_Data = {}
		#PV_2_Data['Sensor_ID'] = "PV-2"
		#PV_2_Data['Date'] = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f")
		#PV_2_Data['Voltage'] = Voltage_Fake_Value
		#PV_2_Data['Current'] = Current_Fake_Value
		#PV_2_json_data = json.dumps(PV_2_Data)
		#Power = "{0:.2f}".format(Voltage_Fake_Value*Current_Fake_Value)


		#print ("Publishing PV 2 fake Voltage, Current, Power, Value: " + str(Voltage_Fake_Value) + ", " + str(Current_Fake_Value) + ", " + str(Power) + "...")
		#publish_To_Topic (MQTT_Topic_PV_2, PV_2_json_data)
		#toggle = 0

publish_Fake_Sensor_Values_to_MQTT(Voltages, Currents)
#====================================================
