# coding=utf-8

import socket
import time
from datetime import datetime

import bluepy
import paho.mqtt.client as mqtt
import simplejson as json
from bluepy.btle import Scanner

Bracelet_Map = {}


class BraceletDelegate:
    def __init__(self, client):
        self.client = client
        self.hostname = socket.gethostname()

    def handleNotification(self, cHandle, data):
        pass

    def handleDiscovery(self, scanEntry, isNewDev, isNewData):
        d = {}
        d['rssi'] = scanEntry.rssi
        d['addr'] = scanEntry.addr
        d['addrType'] = scanEntry.addrType
        for (adtype, desc, value) in scanEntry.getScanData():
            d[desc.replace(' ', '')] = value
        if 'CompleteLocalName' in d and d['CompleteLocalName'].startswith('HW702A'):
            t = time.time()
            print '{} {} {} {}'.format(datetime.now(), d['CompleteLocalName'], d['rssi'], d['Manufacturer'])
            heart_beat = int(d['Manufacturer'][-2:], 16)

            if self.client:
                client.publish('ble2mqtt' + '/' + d['CompleteLocalName'] + '/' + self.hostname,
                               payload=json.dumps({'heart_beat': heart_beat,
                                                   'timestamp': int(t),
                                                   'rssi': d['rssi'],
                                                   'hostname': self.hostname,
                                                   'Manufacturer': d['Manufacturer'],
                                                   'bracelet_name': d['CompleteLocalName']}),
                               qos=0,
                               retain=False)

                # self.socketio.emit('server_response',
                #                    {'heart_beat': heart_beat,
                #                     'bracelet_name': d['CompleteLocalName']},
                #                    namespace='/test')
                Bracelet_Map[d['CompleteLocalName']] = d['Manufacturer']


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("119.3.168.84", 1883, 60)
    bracelet_delegate = BraceletDelegate(client)
    scanner = Scanner()
    scanner.withDelegate(bracelet_delegate)
    cycle_flag = True
    while cycle_flag:
        try:
            scanner.scan(100.0, True)
        except bluepy.btle.BTLEException, err:
            print '1', err
    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()
