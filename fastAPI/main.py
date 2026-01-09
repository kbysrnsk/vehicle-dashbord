from fastapi import FastAPI, Request
import boto3
from boto3.dynamodb.conditions import Key
import json
import time
from decimal import Decimal
import paho.mqtt.client as mqtt

app = FastAPI()

# MQTT クライアント作成 
mqtt_client = mqtt.Client() 
# TLS 設定（必要なら） 
mqtt_client.tls_set( 
    ca_certs="../simulator/IoTCore/connect_device_package/root-CA.crt", 
    certfile="../simulator/IoTCore/connect_device_package/vehicle-dashbord-simulator.cert.pem", 
    keyfile="../simulator/IoTCore/connect_device_package/vehicle-dashbord-simulator.private.key" 
) 
# 接続 
mqtt_client.connect( 
    "a187h3keb8ptu6-ats.iot.ap-northeast-1.amazonaws.com", 
    8883, 
    keepalive=60 
) 
mqtt_client.loop_start()

TOPIC_LOCK = "vehicle/lock/{vehicle_id}"

def convert_decimal(obj): 
    if isinstance(obj, list): 
        return [convert_decimal(i) for i in obj] 
    if isinstance(obj, dict): 
        return {k: convert_decimal(v) for k, v in obj.items()} 
    if isinstance(obj, Decimal): 
        return float(obj) 
    return obj

@app.get("/GetDashbordData/{vehicle_id}")
def GetDashbordData(vehicle_id: str):
    #DB接続
    dynamodb = boto3.resource('dynamodb')
    #テレメトリ取得
    table = dynamodb.Table('vehicle-dashbord')
    response = table.query(
        KeyConditionExpression=Key('vehicle_id').eq(vehicle_id),
        ScanIndexForward=False,  # 降順（新しい順）
        Limit=10                  # 10件取得
    )
    items = [convert_decimal(i) for i in response["Items"]] 
    # 通信断を判断 
    disconnect_record = next( 
        (item for item in items if item.get("disconnect") is True),
         None 
    ) 

    if disconnect_record: 
        latest_state = disconnect_record 
        is_disconnected = True 
    else: 
        latest_state = items[0] 
        is_disconnected = False
    latest_state["disconnect"] = is_disconnected
    table_target = dynamodb.Table('vehicle-dashbord-target') 
    res_target = table_target.query( 
        KeyConditionExpression=Key('vehicle_id').eq(vehicle_id), 
        ScanIndexForward=False, 
        Limit=1, 
        ConsistentRead=True 
    ) 
    latest_target = res_target["Items"][0] if res_target["Count"] > 0 else {}


    return { 
       "state": convert_decimal(latest_state), 
       "target": convert_decimal(latest_target)
    }

@app.post("/UpdateTarget/{vehicle_id}")
async def UpdateTarget(vehicle_id: str, request: Request):
    data = await request.json()
    #DB接続
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('vehicle-dashbord-target')

    table.put_item( 
        Item={ 
            "vehicle_id": vehicle_id, 
            "timestamp": int(time.time() * 1000), 
            "target" : {
                "target_temp": Decimal(str(data["target_temp"]))
            }
        } 
    )

    return

@app.post("/UpdateLock/{vehicle_id}")
async def UpdateLock(vehicle_id: str, request: Request):
    data = await request.json()

    vehicle_id = vehicle_id 
    door_locked = data["door_locked"]
    
    payload = json.dumps({ "door_locked": door_locked }) 
    topic = TOPIC_LOCK.format(vehicle_id=vehicle_id) 
    # MQTT publish 
    mqtt_client.publish(topic, payload, qos=1)
    return
    

