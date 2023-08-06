import paho.mqtt.client as mqtt
import json
from random import random
from util.global_var import *
import time


def cicitest():
    ip = '10.0.40.24'
    port = 1883
    alive = 60
    client = mqtt.Client()
    client.connect(ip,port=port)
    client.publish('JX_AID_EVENT',json.dumps(body))

client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
mqttClient = mqtt.Client(client_id,transport='tcp')

body = {
        "eventID": 516303,
        "eventType": 903,
        "eventStartPos": {
            "lat": 30.702222404273385,
            "lon": 120.77792644095756
        },
        "eventEndPos": {
            "lat": 30.70251160831637,
            "lon": 120.77789343329623
        },
        "eventObjects": [
            {
                "sec": 1650356576,
                "nsec": 712639093,
                "time": 1650356576712,
                "id": 5649083,
                "location": {
                    "longitude": 120.77789343329623,
                    "latitude": 30.70251160831637
                },
                "type": 0,
                "car_info": {
                    "plate_num": "ZA333336",
                    "car_type": "small_coach,large_coach",
                    "car_color": "balck"
                },
                "speed": {
                    "x": 5.933015174203753,
                    "y": 0,
                    "z": 0
                },
                "velocity": 21.35885462713351,
                "heading": 17.85046200880917,
                "size": {
                    "length": 4.546875,
                    "width": 1.9501953125,
                    "height": 1.716796875
                },
                "lane_id": 35,
                "road_id": 0,
                "areaStatus": "eastCross",
                "firstComeIntoTime": 1650356572012,
                "stopOrNot": "false",
                "queueOrNot": "false",
                "currentStopTime": 0,
                "avgSpeed": 25.244085873040714,
                "eventType": "大型车右转不停车"
            }
        ],
        "distance": 32.194046799993906,
        "description": "north",
        "eventSource": 0,
        "duration": 14.7,
        "timeStamp": 1651888870000
    }
# 连接MQTT服务
def mqtt_connect():
    HOST = MQTTIP # MQTT服务器地址
    PORT = MQTTPORT  # MQTT端口
    # MQTTPORT.username_pw_set("username", "password") # mqtt服务器账号密码
    mqttClient.connect(HOST, PORT, 60)  # 超时时间为60秒
    mqttClient.loop_start()  # 启用子线程连接
# 发布消息
def mqtt_publish(topic,body):
    """
    发布消息
    """
    mqtt_connect()
    mqttClient.publish(topic, json.dumps(body), 0)
    mqttClient.loop_stop()  # 断开连接

# 消息处理函数
def on_message_come(client, userdata, msg):
    print("主题:"+msg.topic+" 消息:"+str(msg.payload))


# subscribe 消息
def on_subscribe(topic):
    mqttClient.subscribe(topic, 0)
    mqttClient.on_message = on_message_come  # 消息到来处理函数

def run(topic):
    mqtt_connect()
    on_subscribe(topic)
    while True:
        pass


if __name__ == "__main__":
    ip = '10.0.40.24'
    port = 1883
    body = {
        "eventID": 516303,
        "eventType": 903,
        "eventStartPos": {
            "lat": 30.702222404273385,
            "lon": 120.77792644095756
        },
        "eventEndPos": {
            "lat": 30.70251160831637,
            "lon": 120.77789343329623
        },
        "eventObjects": [
            {
                "sec": 1650356576,
                "nsec": 712639093,
                "time": 1650356576712,
                "id": 5649083,
                "location": {
                    "longitude": 120.77789343329623,
                    "latitude": 30.70251160831637
                },
                "type": 0,
                "car_info": {
                    "plate_num": "ZA333336",
                    "car_type": "small_coach,large_coach",
                    "car_color": "balck"
                },
                "speed": {
                    "x": 5.933015174203753,
                    "y": 0,
                    "z": 0
                },
                "velocity": 21.35885462713351,
                "heading": 17.85046200880917,
                "size": {
                    "length": 4.546875,
                    "width": 1.9501953125,
                    "height": 1.716796875
                },
                "lane_id": 35,
                "road_id": 0,
                "areaStatus": "eastCross",
                "firstComeIntoTime": 1650356572012,
                "stopOrNot": "false",
                "queueOrNot": "false",
                "currentStopTime": 0,
                "avgSpeed": 25.244085873040714,
                "eventType": "大型车右转不停车"
            }
        ],
        "distance": 32.194046799993906,
        "description": "north",
        "eventSource": 0,
        "duration": 14.7,
        "timeStamp": 1651888870000
    }
    # run("JX_AID_EVENT")
    mqtt_publish("JX_AID_EVENT",body)




