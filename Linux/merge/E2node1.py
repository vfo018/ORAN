import time
import threading
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
from pyasn1.codec.ber import encoder, decoder
from pyasn1.type import univ, namedtype, char
import json

# 定义ASN.1结构
class E2NodeComponentConfigItem(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('e2NodeComponentInterfaceType', univ.Integer()),
        namedtype.NamedType('e2NodeComponentID', char.PrintableString()),
        namedtype.NamedType('e2NodeComponentConfigurationAcknowledge', univ.Boolean())
    )

class E2NodeCompConfigAddList(univ.SequenceOf):
    componentType = E2NodeComponentConfigItem()

class E2NodeCompConfigRemoveList(univ.SequenceOf):
    componentType = char.PrintableString()

class E2NodeConfigUpdate(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('globalE2NodeID', char.PrintableString()),
        namedtype.NamedType('e2NodeCompConfigAddList', E2NodeCompConfigAddList()),
        namedtype.NamedType('e2NodeCompConfigRemoveList', E2NodeCompConfigRemoveList())
    )

class KPMData(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('cellID', char.PrintableString()),
        namedtype.NamedType('MAC.PrbUsedDl', univ.Integer()),  # 下行PRB的使用量
        namedtype.NamedType('MAC.PrbAvailDl', univ.Integer()),  # 可用的下行PRB总量
        namedtype.NamedType('RRC.Conn.Avg', univ.Integer()),    # RRC连接态用户的平均数量
        namedtype.NamedType('RRC.Conn.Max', univ.Integer())     # RRC连接态用户的最大数量
    )

current_scenario = 1  # 默认情景

# 生成E2 Node Config Update信令
def generate_e2_node_config_update(global_e2node_id, add_list, remove_list):
    e2node_config_update = E2NodeConfigUpdate()
    e2node_config_update.setComponentByName('globalE2NodeID', global_e2node_id)
    
    if add_list:
        e2node_comp_config_add_list = E2NodeCompConfigAddList()
        for item in add_list:
            config_item = E2NodeComponentConfigItem()
            config_item.setComponentByName('e2NodeComponentInterfaceType', item['type'])
            config_item.setComponentByName('e2NodeComponentID', item['id'])
            config_item.setComponentByName('e2NodeComponentConfigurationAcknowledge', item['ack'])
            e2node_comp_config_add_list.append(config_item)
        e2node_config_update.setComponentByName('e2NodeCompConfigAddList', e2node_comp_config_add_list)

    if remove_list:
        e2node_comp_config_remove_list = E2NodeCompConfigRemoveList()
        for item in remove_list:
            e2node_comp_config_remove_list.append(item)
        e2node_config_update.setComponentByName('e2NodeCompConfigRemoveList', e2node_comp_config_remove_list)

    return encoder.encode(e2node_config_update)

# 模拟生成KPM数据
def generate_kpm_data():
    kpm_data = KPMData()
    kpm_data.setComponentByName('cellID', 'cellID123')

    if current_scenario == 1:
        kpm_data.setComponentByName('MAC.PrbUsedDl', 50)
        kpm_data.setComponentByName('MAC.PrbAvailDl', 100)
        kpm_data.setComponentByName('RRC.Conn.Avg', 30)
        kpm_data.setComponentByName('RRC.Conn.Max', 60)
    elif current_scenario == 2:
        kpm_data.setComponentByName('MAC.PrbUsedDl', 70)
        kpm_data.setComponentByName('MAC.PrbAvailDl', 90)
        kpm_data.setComponentByName('RRC.Conn.Avg', 40)
        kpm_data.setComponentByName('RRC.Conn.Max', 80)
    elif current_scenario == 3:
        kpm_data.setComponentByName('MAC.PrbUsedDl', 60)
        kpm_data.setComponentByName('MAC.PrbAvailDl', 110)
        kpm_data.setComponentByName('RRC.Conn.Avg', 35)
        kpm_data.setComponentByName('RRC.Conn.Max', 65)
    elif current_scenario == 4:
        kpm_data.setComponentByName('MAC.PrbUsedDl', 80)
        kpm_data.setComponentByName('MAC.PrbAvailDl', 95)
        kpm_data.setComponentByName('RRC.Conn.Avg', 45)
        kpm_data.setComponentByName('RRC.Conn.Max', 85)
    
    encoded_kpm_data = encoder.encode(kpm_data)
    return encoded_kpm_data

# 处理情景变化并触发相应的信令交互
def handle_scenario(scenario):
    global_e2node_id = "GlobalE2NodeID123"
    
    if scenario == 1:  # DU Addition
        print("Handling DU Addition")
        # 生成E2 Node Config Update信令
        add_list = [{'type': 1, 'id': 'DU123', 'ack': True}]
        remove_list = []
        e2_node_config_update = generate_e2_node_config_update(global_e2node_id, add_list, remove_list)
        send_e2_node_config_update(e2_node_config_update)
        time.sleep(1)
        # 发送 E2 Setup 请求
        send_e2_setup_request()
        
    elif scenario == 2:  # DU Removal
        print("Handling DU Removal")
        # 生成E2 Node Config Update信令
        add_list = []
        remove_list = ['DU123']
        e2_node_config_update = generate_e2_node_config_update(global_e2node_id, add_list, remove_list)
        send_e2_node_config_update(e2_node_config_update)
        time.sleep(1)
        # 发送 KPM 订阅删除请求
        send_kpm_subscription_delete()
        
    elif scenario == 3:  # Cell Addition
        print("Handling Cell Addition")
        # 生成E2 Node Config Update信令
        add_list = [{'type': 2, 'id': 'Cell456', 'ack': True}]
        remove_list = []
        e2_node_config_update = generate_e2_node_config_update(global_e2node_id, add_list, remove_list)
        send_e2_node_config_update(e2_node_config_update)
        time.sleep(1)
        
    elif scenario == 4:  # Cell Removal
        print("Handling Cell Removal")
        # 生成E2 Node Config Update信令
        add_list = []
        remove_list = ['Cell456']
        e2_node_config_update = generate_e2_node_config_update(global_e2node_id, add_list, remove_list)
        send_e2_node_config_update(e2_node_config_update)
        time.sleep(1)

# 发送E2 Setup请求
def send_e2_setup_request():
    print("Sending E2 Setup Request after DU Addition")
    encoded_request = generate_e2_setup_response()
    headers = {'Content-Type': 'application/octet-stream'}
    response = requests.post("http://localhost:8001/e2setup", data=encoded_request, headers=headers)
    if response.status_code == 200:
        print("E2 Setup Request sent successfully.")
    else:
        print(f"Failed to send E2 Setup Request. Status code: {response.status_code}")

# 发送 KPM 订阅删除请求
def send_kpm_subscription_delete():
    print("Sending KPM Subscription Delete Request after DU Removal")
    # 模拟的KPM订阅删除请求，这里可以具体编码
    headers = {'Content-Type': 'application/octet-stream'}
    response = requests.post("http://localhost:8001/kpmsubscriptiondelete", headers=headers)
    if response.status_code == 200:
        print("KPM Subscription Delete Request sent successfully.")
    else:
        print(f"Failed to send KPM Subscription Delete Request. Status code: {response.status_code}")

# 发送 E2 Node Config Update 信令
def send_e2_node_config_update(encoded_update):
    print("Sending E2 Node Config Update")
    headers = {'Content-Type': 'application/octet-stream'}
    response = requests.post("http://localhost:8001/e2nodeconfigupdate", data=encoded_update, headers=headers)
    if response.status_code == 200:
        print("E2 Node Config Update sent successfully.")
    else:
        print(f"Failed to send E2 Node Config Update. Status code: {response.status_code}")

# HTTP服务器处理程序
class E2NodeHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        if self.path == "/e2setup":
            # 模拟生成E2 Setup响应并返回
            encoded_response = generate_e2_setup_response()
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            self.end_headers()
            self.wfile.write(encoded_response)
        
        elif self.path == "/kpmsubscription":
            # 接收订阅请求并启动KPM数据发送线程
            print("Received subscription request")
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            self.end_headers()
            self.start_kpm_data_sending()

        elif self.path == "/scenario":
            global current_scenario
            scenario_data = json.loads(post_data)
            current_scenario = int(scenario_data['scenario'])
            print(f"Scenario set to {current_scenario}")
            self.send_response(200)
            self.end_headers()
            handle_scenario(current_scenario)

    def start_kpm_data_sending(self):
        def send_kpm_data():
            while True:
                encoded_kpm_data = generate_kpm_data()
                headers = {'Content-Type': 'application/octet-stream'}
                response = requests.post("http://localhost:8001/receive_kpm", data=encoded_kpm_data, headers=headers)
                if response.status_code == 200:
                    print("KPM data sent successfully.")
                else:
                    print("Failed to send KPM data.")
                time.sleep(1)  # 每隔一秒发送一次

        threading.Thread(target=send_kpm_data).start()

def run(server_class=HTTPServer, handler_class=E2NodeHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting E2Node mock server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
