import socket
import sctp
from pyasn1.codec.ber import encoder
from pyasn1.type import univ, namedtype, char

# 定义E2 Node Config Update结构
class E2NodeConfigUpdate(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('globalE2NodeID', char.PrintableString()),
        namedtype.NamedType('configList', univ.SequenceOf(componentType=char.PrintableString()))
    )

# 定义E2 Setup结构
class E2SetupRequest(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('globalE2NodeID', char.PrintableString()),
        namedtype.NamedType('ranFunctionList', univ.SequenceOf(componentType=char.PrintableString()))
    )

# 定义订阅删除结构
class SubscriptionDeleteRequest(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('reqID', univ.Integer()),
        namedtype.NamedType('ranFuncID', univ.Integer())
    )

# 发送E2 Node Config Update
def send_e2_node_config_update_sctp(encoded_update, ric_ip, ric_port):
    sctpsock = sctp.sctpsocket_tcp(socket.AF_INET)
    sctpsock.connect((ric_ip, ric_port))
    sctpsock.sctp_send(encoded_update)
    response = sctpsock.recv(4096)
    sctpsock.close()
    return response

# 发送E2 Setup请求
def send_e2_setup_request_sctp(encoded_request, ric_ip, ric_port):
    sctpsock = sctp.sctpsocket_tcp(socket.AF_INET)
    sctpsock.connect((ric_ip, ric_port))
    sctpsock.sctp_send(encoded_request)
    response = sctpsock.recv(4096)
    sctpsock.close()
    return response

# 发送订阅删除请求
def send_subscription_delete_request_sctp(encoded_delete, ric_ip, ric_port):
    sctpsock = sctp.sctpsocket_tcp(socket.AF_INET)
    sctpsock.connect((ric_ip, ric_port))
    sctpsock.sctp_send(encoded_delete)
    response = sctpsock.recv(4096)
    sctpsock.close()
    return response

# 创建订阅删除请求
def create_subscription_delete_request(req_id, ran_func_id):
    delete_request = SubscriptionDeleteRequest()
    delete_request.setComponentByName('reqID', req_id)
    delete_request.setComponentByName('ranFuncID', ran_func_id)
    return encoder.encode(delete_request)

# 情景 1: E2 Node Config Update 当有新的DU被添加
def e2_node_config_update_new_du_sctp(ric_ip, ric_port):
    update_request = E2NodeConfigUpdate()
    update_request.setComponentByName('globalE2NodeID', 'GlobalE2NodeID-123')
    update_request.setComponentByName('configList', ['DU1-Config'])

    encoded_update = encoder.encode(update_request)
    response = send_e2_node_config_update_sctp(encoded_update, ric_ip, ric_port)
    print("E2 Node Config Update Response for new DU:", response)

    setup_request = E2SetupRequest()
    setup_request.setComponentByName('globalE2NodeID', 'GlobalE2NodeID-123')
    setup_request.setComponentByName('ranFunctionList', ['Function1', 'Function2'])

    encoded_setup_request = encoder.encode(setup_request)
    response = send_e2_setup_request_sctp(encoded_setup_request, ric_ip, ric_port)
    print("E2 Setup Response:", response)

# 情景 2: E2 Node Config Update 当DU被移除
def e2_node_config_update_remove_du_sctp(ric_ip, ric_port):
    update_request = E2NodeConfigUpdate()
    update_request.setComponentByName('globalE2NodeID', 'GlobalE2NodeID-123')
    update_request.setComponentByName('configList', ['Remove-DU1'])

    encoded_update = encoder.encode(update_request)
    response = send_e2_node_config_update_sctp(encoded_update, ric_ip, ric_port)
    print("E2 Node Config Update Response for DU Removal:", response)

    delete_request_kpm = create_subscription_delete_request(req_id=1, ran_func_id=1)
    response_delete_kpm = send_subscription_delete_request_sctp(delete_request_kpm, ric_ip, ric_port)
    print("KPM Subscription Delete Response:", response_delete_kpm)

    delete_request_rc = create_subscription_delete_request(req_id=2, ran_func_id=2)
    response_delete_rc = send_subscription_delete_request_sctp(delete_request_rc, ric_ip, ric_port)
    print("RC Subscription Delete Response:", response_delete_rc)

# 情景 3: E2 Node Config Update 当小区上线
def e2_node_config_update_cell_up_sctp(ric_ip, ric_port):
    update_request = E2NodeConfigUpdate()
    update_request.setComponentByName('globalE2NodeID', 'GlobalE2NodeID-123')
    update_request.setComponentByName('configList', ['CellUp-Config'])

    encoded_update = encoder.encode(update_request)
    response = send_e2_node_config_update_sctp(encoded_update, ric_ip, ric_port)
    print("E2 Node Config Update Response for Cell Up:", response)

# 情景 4: E2 Node Config Update 当小区下线
def e2_node_config_update_cell_down_sctp(ric_ip, ric_port):
    update_request = E2NodeConfigUpdate()
    update_request.setComponentByName('globalE2NodeID', 'GlobalE2NodeID-123')
    update_request.setComponentByName('configList', ['CellDown-Config'])

    encoded_update = encoder.encode(update_request)
    response = send_e2_node_config_update_sctp(encoded_update, ric_ip, ric_port)
    print("E2 Node Config Update Response for Cell Down:", response)

# 主程序，根据需要选择执行哪个情景
def main_sctp():
    print("选择执行情景：")
    print("1: 新的DU被添加")
    print("2: DU被移除")
    print("3: 小区上线")
    print("4: 小区下线")
    
    choice = input("请输入选择的数字: ")
    
    ric_ip = "192.168.1.100"
    ric_port = 36422
    
    if choice == "1":
        e2_node_config_update_new_du_sctp(ric_ip, ric_port)
    elif choice == "2":
        e2_node_config_update_remove_du_sctp(ric_ip, ric_port)
    elif choice == "3":
        e2_node_config_update_cell_up_sctp(ric_ip, ric_port)
    elif choice == "4":
        e2_node_config_update_cell_down_sctp(ric_ip, ric_port)
    else:
        print("无效的选择，请重新运行程序并选择正确的选项。")

if __name__ == "__main__":
    main_sctp()
