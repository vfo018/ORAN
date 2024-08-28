import time
import threading
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
from pyasn1.codec.ber import encoder, decoder
from pyasn1.type import univ, namedtype, char

# 定义ASN.1结构
class E2NodeComponentConfigItem(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('e2NodeComponentInterfaceType', univ.Integer()),
        namedtype.NamedType('e2NodeComponentID', char.PrintableString()),
        namedtype.NamedType('e2NodeComponentConfigurationAcknowledge', univ.Boolean())
    )

class E2NodeCompConfigAddList(univ.SequenceOf):
    componentType = E2NodeComponentConfigItem()

class KPMData(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('cellID', char.PrintableString()),
        namedtype.NamedType('kpmValue', univ.Integer())
    )

# 模拟生成E2 Setup响应
def generate_e2_setup_response():
    e2node_comp_config_list = E2NodeCompConfigAddList()
    
    config_item = E2NodeComponentConfigItem()
    config_item.setComponentByName('e2NodeComponentInterfaceType', 1)
    config_item.setComponentByName('e2NodeComponentID', 'cellID123')
    config_item.setComponentByName('e2NodeComponentConfigurationAcknowledge', True)
    
    e2node_comp_config_list.append(config_item)
    
    encoded_response = encoder.encode(e2node_comp_config_list)
    return encoded_response

# 模拟生成KPM数据
def generate_kpm_data():
    kpm_data = KPMData()
    kpm_data.setComponentByName('cellID', 'cellID123')
    kpm_data.setComponentByName('kpmValue', 100)  # 假设KPM值为100
    
    encoded_kpm_data = encoder.encode(kpm_data)
    return encoded_kpm_data

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
