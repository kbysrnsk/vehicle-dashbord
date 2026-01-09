import time
import copy
import random
import json
import paho.mqtt.client as mqtt

# 車両状態
class VehicleStatus:
    IDLE = 0
    RUNNING = 1
    IG_OFF = 2
    IG_ON = 3

class ScenarioState:
    STOPPED = 0
    STARTING = 1
    ACCELERATING = 2
    CRUISING = 3
    DECELERATING = 4


class Vehicle: 
    # --- 初期状態（init処理） ---
    def __init__(self, vehicle_id): 
        # 状態管理用カウンタ
        self.stopped_cnt = 0
        # シナリオ用カウンタ
        self.scenario_stop_cnt =  0
        # IGoffタイマー
        self.ig_timer = 0
        self.ig_off_duration = 0
        self.IG_OFF_INTERVAL = 500
        self.IG_OFF_TIME = 50
        # DB用データ
        self.state = {
            "vehicle_id" : vehicle_id,
            "timestamp" : int(time.time() * 1000),
            "status" : VehicleStatus.IDLE,
            "IG" : True,
            "speed" : 0, 
            "battery" : 80, 
            "door_locked" : True, 
            "mileage" : 10000, 
            "online" : True, 
            "temperature" : {
                "in" : 20.0,
                "out" : 15.0
            },
            "tire_pressure" : {
                "front_left" : 230,
                "front_right" : 226,
                "rear_left" : 231,
                "rear_right" : 220
            },
            "position" : {
                "lat": 34.7055,
                "lng": 135.4983,
            }
        }
        # ターゲット値初期化
        self.target = {
            "target_temp" : None
        }
        # ドアロックイベントフラグ
        self.event_lock = False

        # 前回データを丸ごとコピー 
        self.prev_state = copy.deepcopy(self.state)
        # シナリオ状態更新
        self.scenario = ScenarioState.STOPPED
        print(f"[INIT] Vehicle {vehicle_id} initialized")

    # 閾値設定
    threshold = { 
        "speed": 3,
        "battery": 1, 
        "temperature_in": 1,
        "temperature_out": 1
        # "mileage": 1,
        # "status": 0,
    }
    ignore_keys = {
        "vehicle_id", 
        "timestamp",
        "tire_pressure",
        "position"
    }

    # 車両データ更新
    def update(self): 
        # 走行シナリオ
        self.run_scenario()
        # 今回値を更新 
        self.state["timestamp"] = int(time.time() * 1000) 
        # 車速丸め込み 
        self.state["speed"] = max(0, min(self.state["speed"], 120)) 
        self.state["battery"] += random.uniform(-0.01, 0)
        self.state["battery"] = max(0, min(self.state["battery"], 100)) 

        # ロック制御
        if self.event_lock: 
            self.event_lock = False 
            return True
        # 状態遷移
        self.update_status()

        # 温度制御
        self.apply_target()

        # 前回値と比較
        ret = self.has_diff()
        # if ret == True:
        #     # 前回値を丸ごと保存 
        #     self.prev_state = copy.deepcopy(self.state)
        return ret

    # 前回値比較
    def has_diff(self):
        for key in self.state:
            if key in self.ignore_keys:
                continue

            prev = self.prev_state[key]
            curr = self.state[key]

            # ★ temperature は特別扱い
            if key == "temperature":
                # in の比較
                if abs(curr["in"] - prev["in"]) >= self.threshold["temperature_in"]:
                    return True
                # out の比較
                if abs(curr["out"] - prev["out"]) >= self.threshold["temperature_out"]:
                    return True
                continue

            # 通常の比較
            if key in self.threshold:
                if abs(curr - prev) >= self.threshold[key]:
                    return True
            else:
                if curr != prev:
                    return True

        return False


    # 車両状態更新
    def update_status(self): 
        speed = self.state["speed"] 
        # speed=0 のとき 
        if speed == 0: 
            self.stopped_cnt += 1

            # 3秒以上停止していたら stopped 
            if self.stopped_cnt >= 30: 
                self.state["status"] = VehicleStatus.IDLE
                self.stopped_cnt = 0 
        else: 
            # speed>0 なら走行中 
            self.state["status"] = VehicleStatus.RUNNING 
            self.stopped_cnt = 0

    def run_scenario(self):
        # IGOFFタイマー
        self.ig_timer += 1 
        # IG を OFF にするタイミング 
        if self.ig_timer >= self.IG_OFF_INTERVAL and self.state["IG"] == 1: 
            print("=== IG OFF triggered ===") 
            self.state["IG"] = False 
            self.state["speed"] = 0 
            self.state["status"] = VehicleStatus.IG_OFF 
            self.state["online"] = False
            self.ig_off_duration = 0

        # IG OFF 中の処理 
        if self.state["IG"] == False: 
            self.ig_off_duration += 1 
            # IG ON に戻す 
            if self.ig_off_duration >= self.IG_OFF_TIME: 
                print("=== IG ON restored ===") 
                self.state["IG"] = True 
                self.state["online"] = True
                self.ig_timer = 0 # 次の周期へ 
            return # IG OFF 中は走行シナリオを進めない


        # 走行シナリオ
        if self.scenario == ScenarioState.STOPPED:
            self.state["speed"] = 0
            self.scenario_stop_cnt += 1

            if self.scenario_stop_cnt >= 100:
                # 発進へ移行
                self.scenario = ScenarioState.STARTING
                self.scenario_stop_cnt = 0

        elif self.scenario == ScenarioState.STARTING:
            self.scenario_stop_cnt = 0
            self.state["speed"] += 0.5
            if self.state["speed"] >= 10:
                self.scenario = ScenarioState.ACCELERATING

        elif self.scenario == ScenarioState.ACCELERATING:
            self.scenario_stop_cnt = 0
            self.state["speed"] += 1.0
            if self.state["speed"] >= 60:
                self.scenario = ScenarioState.CRUISING

        elif self.scenario == ScenarioState.CRUISING:
            self.scenario_stop_cnt = 0
            # ±1 km/h の揺らぎだけ
            self.state["speed"] += random.uniform(-1, 1)
            if random.random() < 0.05:  # 5% の確率で減速開始
                self.scenario = ScenarioState.DECELERATING

        elif self.scenario == ScenarioState.DECELERATING:
            self.scenario_stop_cnt = 0
            self.state["speed"] -= 3.0
            if self.state["speed"] <= 0:
                self.state["speed"] = 0
                self.scenario = ScenarioState.STOPPED
        
        self.state["speed"] = round(self.state["speed"], 1)

    def apply_target(self):
        # target.temp が設定されていれば、室内温度を近づける
        target_temp = self.target.get("target_temp")
        if target_temp is not None:
            current = self.state["temperature"]["in"]

            # 0.1℃ずつ近づける
            if abs(current - target_temp) > 0.1:
                if current < target_temp:
                    current += 0.1
                else:
                    current -= 0.1

            self.state["temperature"]["in"] = round(current, 1)
            # print("temp_in:", self.state["temperature"]["in"])






    
def connect_mqtt(endpoint, port, cert_path, key_path, ca_path, vehicle):
    client = mqtt.Client()
    connected = {"flag": False}

    def on_connect(client, userdata, flags, rc, properties=None):
        if rc == 0:
            print("接続成功")
            connected["flag"] = True
            # subscribe設定
            client.subscribe(TOPIC_TARGET, qos=1)
            client.subscribe(TOPIC_LOCK, qos=1)
        else:
            print("接続失敗 rc=", rc)

    def on_message(client, userdata, msg): 
        print("=== Message Received ===") 
        print("Topic:", msg.topic) 
        payload = msg.payload.decode() 
        print("Payload:", payload)
        
        try:
            data = json.loads(payload)
            if "target_temp" in data:
                vehicle.target["target_temp"] = data["target_temp"]
                print("Updated target:", vehicle.target)

            if "door_locked" in data: 
                # 車両が IDLE のときだけロック状態を更新 
                if vehicle.state["status"] == VehicleStatus.IDLE: 
                    vehicle.state["door_locked"] = data["door_locked"] 
                    vehicle.event_lock = True 
                    # 即時 publish させる 
                    print("Door lock updated:", vehicle.state["door_locked"]) 
                else: 
                    print("Ignored lock command (vehicle not IDLE)")
            
        except Exception as e:
            print("JSON parse error:", e)


    client.on_connect = on_connect
    client.on_message = on_message

    client.tls_set(
        ca_certs=ca_path,
        certfile=cert_path,
        keyfile=key_path
    )

    client.will_set( 
        topic=TOPIC_LWT, 
        payload=json.dumps({ 
            "vehicle_id": vehicle.state["vehicle_id"], 
            "timestamp":"",
            "online":False,
            "disconnect": True
        }), 
        qos=1, 
        retain=False 
    )


    for attempt in range(1, 4):
        print(f"MQTT 接続試行 {attempt}/3 …")

        try:
            client.connect(endpoint, port, keepalive=60)
            client.loop_start()

            # 接続完了を最大 5 秒待つ
            for _ in range(10):
                if connected["flag"]:
                    print("MQTT 接続完了")
                    return client
                time.sleep(0.5)

            print("接続待ちタイムアウト")

        except Exception as e:
            print("接続エラー:", e)

        # 次の試行まで 2 秒待つ
        time.sleep(2)

    print("MQTT 接続失敗")
    return None

def publish_initial(object, client, topic):

    def on_publish(client, userdata, mid): 
        print("初回送信完了:", mid)
        client.on_publish = None

    client.on_publish = on_publish

    payload = json.dumps(object.state)
    ret = client.publish(topic, payload)
    return ret

def publish_data(object, client, topic):
    payload = json.dumps(object.state)
    ret = client.publish(topic, payload)
    return ret
    
# 車両ID固定
vehicle_id = '8f3c2b4e-9d12-4a7f-8c3e-52b1f6a9d7c4'
# データ送信先設定
ENDPOINT = "a187h3keb8ptu6-ats.iot.ap-northeast-1.amazonaws.com"
PORT = 8883
# TOPIC
TOPIC_TELEMETRY = f"vehicle/telemetry/{vehicle_id}"
TOPIC_INIT = f"vehicle/init/{vehicle_id}"
TOPIC_TARGET = f"vehicle/target/{vehicle_id}"
TOPIC_LOCK = f"vehicle/lock/{vehicle_id}"
TOPIC_LWT = f"vehicle/willset/{vehicle_id}"

ca_certs="IoTCore/connect_device_package/root-CA.crt"
certfile="IoTCore/connect_device_package/vehicle-dashbord-simulator.cert.pem"
keyfile="IoTCore/connect_device_package/vehicle-dashbord-simulator.private.key"


# -----処理開始----- #

# ===== 起動時処理 =====
# クラス生成
vehicle = Vehicle(vehicle_id)

# クラウド接続
client = connect_mqtt(ENDPOINT, PORT, certfile, keyfile, ca_certs, vehicle)
if client is None:
    exit()

# 初回データ送信
result = publish_initial(vehicle, client, TOPIC_TELEMETRY)
if result.rc != 0:
    print("初回送信要求失敗")
    exit()



# ===== メインループ =====
interval = 0.1
next_time = time.time()
regular_publish_cnt = 0

# 強制通信断
force_disconnect_timer = 0 
FORCE_DISCONNECT_INTERVAL = 800 # 80秒ごとに切断を試行 
FORCE_DISCONNECT_PROB = 0.1 # 10% の確率で切断発生 
force_disconnected = False
FORCE_DISCONNECT_HOLD = 100
skip_publish = False

while True:
    # 強制通信断
    force_disconnect_timer += 1
    # まだ切断されていない場合のみ
    if not force_disconnected:
        if force_disconnect_timer >= FORCE_DISCONNECT_INTERVAL:
            if random.random() < FORCE_DISCONNECT_PROB:
                print("=== Forced MQTT Disconnect (unexpected) ===")
                force_disconnected = True
                force_disconnect_timer = 0
                skip_publish = True
                client.loop_stop() 
                time.sleep(0.1)
                try:
                    client._sock.close()
                except:
                    pass

                # publish は止まる
                continue

    # 強制切断後の再接続
    if force_disconnected:
        # 60秒後に再接続を試みる
        if force_disconnect_timer >= FORCE_DISCONNECT_HOLD:
            print("=== Trying to reconnect MQTT (using connect_mqtt) ===")
            try:
                client = connect_mqtt(ENDPOINT, PORT, certfile, keyfile, ca_certs, vehicle)
                if client is not None:
                    force_disconnected = False
                    skip_publish = False
                    force_disconnect_timer = 0
                    publish_data(vehicle, client, TOPIC_TELEMETRY) 
                    vehicle.prev_state = copy.deepcopy(vehicle.state)
                    print("=== Reconnected successfully ===")
                else:
                    print("Reconnect failed: connect_mqtt returned None")
            except Exception as e:
                print("Reconnect failed:", e)

            # 再接続中は publish しない
            continue

    # 車両情報通常更新
    result = vehicle.update()
    if not skip_publish and (result == True or regular_publish_cnt == 50):
        result = publish_data(vehicle, client, TOPIC_TELEMETRY)
        vehicle.prev_state = copy.deepcopy(vehicle.state)
        # print("publish result:", result.rc)
        # print("speed:",vehicle.state["speed"])
        regular_publish_cnt = 0

    next_time += interval
    sleep_time = next_time - time.time()
    if sleep_time > 0:
        time.sleep(sleep_time)
