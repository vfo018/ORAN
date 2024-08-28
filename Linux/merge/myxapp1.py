import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
from pyasn1.codec.ber import encoder, decoder
from pyasn1.type import univ, namedtype, char
import threading

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

class ActionItem(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('actionID', univ.Integer()),
        namedtype.NamedType('actionType', char.VisibleString()),
        namedtype.NamedType('actionDefinition', char.VisibleString()),
        namedtype.NamedType('subsequentAction', univ.Boolean())
    )

class SubscriptionRequest(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('reqID', univ.Integer()),
        namedtype.NamedType('ranFuncID', univ.Integer()),
        namedtype.NamedType('eventTrigger', char.VisibleString()),
        namedtype.NamedType('actions', univ.SequenceOf(componentType=ActionItem()))
    )

class KPMData(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('cellID', char.PrintableString()),
        namedtype.NamedType('MAC.PrbUsedDl', univ.Integer()),  # 下行PRB的使用量
        namedtype.NamedType('MAC.PrbAvailDl', univ.Integer()),  # 可用的下行PRB总量
        namedtype.NamedType('RRC.Conn.Avg', univ.Integer()),    # RRC连接态用户的平均数量
        namedtype.NamedType('RRC.Conn.Max', univ.Integer())     # RRC连接态用户的最大数量
    )

# 接收并解码E2 Setup的信息
def receive_e2_setup(encoded_response):
    decoded_response, _ = decoder.decode(encoded_response, asn1Spec=E2NodeCompConfigAddList())
    return decoded_response

# 接收并解码E2 Node Config Update的信息
def receive_e2_node_config_update(encoded_update):
    decoded_update, _ = decoder.decode(encoded_update, asn1Spec=E2NodeConfigUpdate())
    return decoded_update

# 构建KPM订阅请求
def create_subscription_request(req_id, ran_func_id, event_trigger, action_id, action_type, action_definition):
    subscription_request = SubscriptionRequest()
    subscription_request.setComponentByName('reqID', req_id)
    subscription_request.setComponentByName('ranFuncID', ran_func_id)
    subscription_request.setComponentByName('eventTrigger', event_trigger)
    
    action_item = ActionItem()
    action_item.setComponentByName('actionID', action_id)
    action_item.setComponentByName('actionType', action_type)
    action_item.setComponentByName('actionDefinition', action_definition)
    action_item.setComponentByName('subsequentAction', True)
    
    # 获取actions并添加ActionItem
    action_list = subscription_request.getComponentByName('actions')
    action_list.append(action_item)
    
    encoded_request = encoder.encode(subscription_request)
    return encoded_request

# 发送订阅请求 (HTTP)
def send_subscription_request_http(encoded_request, ric_api_url):
    headers = {'Content-Type': 'application/octet-stream'}
    response = requests.post(ric_api_url, data=encoded_request, headers=headers)
    return response

# 接收KPM数据的处理程序
class KPMReceiverHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        if self.path == "/e2nodeconfigupdate":
            # 接收并处理E2 Node Config Update
            e2_node_config_update = receive_e2_node_config_update(post_data)
            global_e2node_id = e2_node_config_update.getComponentByName('globalE2NodeID')
            add_list = e2_node_config_update.getComponentByName('e2NodeCompConfigAddList')
            remove_list = e2_node_config_update.getComponentByName('e2NodeCompConfigRemoveList')

            print(f"Received E2 Node Config Update: globalE2NodeID={global_e2node_id}")
            for item in add_list:
                print(f"Added: InterfaceType={item.getComponentByName('e2NodeComponentInterfaceType')}, "
                      f"ID={item.getComponentByName('e2NodeComponentID')}, Ack={item.getComponentByName('e2NodeComponentConfigurationAcknowledge')}")
            for item in remove_list:
                print(f"Removed: ID={item}")
        
        elif self.path == "/receive_kpm":
            # 接收并处理KPM数据
            kpm_data, _ = decoder.decode(post_data, asn1Spec=KPMData())
            cell_id = kpm_data.getComponentByName('cellID')
            mac_prb_used_dl = kpm_data.getComponentByName('MAC.PrbUsedDl')
            mac_prb_avail_dl = kpm_data.getComponentByName('MAC.PrbAvailDl')
            rrc_conn_avg = kpm_data.getComponentByName('RRC.Conn.Avg')
            rrc_conn_max = kpm_data.getComponentByName('RRC.Conn.Max')
            
            print(f"Received KPM data: cellID={cell_id}, MAC.PrbUsedDl={mac_prb_used_dl}, "
                  f"MAC.PrbAvailDl={mac_prb_avail_dl}, RRC.Conn.Avg={rrc_conn_avg}, RRC.Conn.Max={rrc_conn_max}")
        
        self.send_response(200)
        self.end_headers()

def run_kpm_receiver(server_class=HTTPServer, handler_class=KPMReceiverHTTPRequestHandler, port=8001):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting KPM Receiver server on port {port}...')
    httpd.serve_forever()

def main():
    # 启动KPM接收服务器
    threading.Thread(target=run_kpm_receiver).start()
    
    # 示例E2 Setup响应的编码消息 (假设我们从E2Node接收到的编码消息)
    ric_api_url = "http://localhost:8000/e2setup"
    encoded_e2_setup_response = requests.post(ric_api_url).content
    
    print("Encoded E2 Setup Response:", encoded_e2_setup_response)
    
    e2_node_comp_config_add_list = receive_e2_setup(encoded_e2_setup_response)
    
    req_id = 1  # 订阅请求的唯一ID
    ran_func_id = 1  # 假设KPM的RAN功能ID为1
    event_trigger = 'Periodic Report'  # 假设我们使用周期性报告
    action_type = 'Report'
    action_definition = 'KPM Details'
    
    for cell_config in e2_node_comp_config_add_list:
        cell_id = cell_config.getComponentByName('e2NodeComponentID')
        print(f"Processing cell: {cell_id}")
        
        # 创建订阅请求
        encoded_request = create_subscription_request(req_id, ran_func_id, event_trigger, req_id, action_type, action_definition)

        # 通过HTTP发送订阅请求
        ric_api_url = "http://localhost:8000/kpmsubscription"
        response_http = send_subscription_request_http(encoded_request, ric_api_url)

        if response_http.status_code == 200:
            print(f"Subscription Request for cell {cell_id} sent successfully via HTTP.")
        else:
            print(f"Failed to send Subscription Request for cell {cell_id} via HTTP, status code: {response_http.status_code}")
        
        req_id += 1  # 每个请求都有唯一的reqID

if __name__ == "__main__":
    import threading
    main()
