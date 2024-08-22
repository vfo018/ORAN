import requests
from pyasn1.codec.ber import encoder
from pyasn1.type import univ, namedtype, char

# 定义ConfigList结构
class ConfigList(univ.SequenceOf):
    componentType = char.PrintableString()

# 定义E2 Node Config Update结构
class E2NodeConfigUpdate(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('globalE2NodeID', char.PrintableString()),
        namedtype.NamedType('configList', ConfigList())
    )

# 定义E2 Setup结构
class E2SetupRequest(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('globalE2NodeID', char.PrintableString()),
        namedtype.NamedType('ranFunctionList', ConfigList())
    )

# 定义订阅删除结构
class SubscriptionDeleteRequest(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('reqID', univ.Integer()),
        namedtype.NamedType('ranFuncID', univ.Integer())
    )

# 发送E2 Node Config Update
def send_e2_node_config_update_http(encoded_update):
    ric_api_url = "http://localhost:8000/api/v1/e2configupdate"
    headers = {'Content-Type': 'application/octet-stream'}
    response = requests.post(ric_api_url, data=encoded_update, headers=headers)
    return response

# 发送E2 Setup请求
def send_e2_setup_request_http(encoded_request):
    ric_api_url = "http://localhost:8000/api/v1/e2setup"
    headers = {'Content-Type': 'application/octet-stream'}
    response = requests.post(ric_api_url, data=encoded_request, headers=headers)
    return response

# 发送订阅删除请求
def send_subscription_delete_request_http(encoded_delete):
    ric_api_url = "http://localhost:8000/api/v1/subscriptiondelete"
    headers = {'Content-Type': 'application/octet-stream'}
    response = requests.post(ric_api_url, data=encoded_delete, headers=headers)
    return response

# 创建订阅删除请求
def create_subscription_delete_request(req_id, ran_func_id):
    delete_request = SubscriptionDeleteRequest()
    delete_request.setComponentByName('reqID', req_id)
    delete_request.setComponentByName('ranFuncID', ran_func_id)
    return encoder.encode(delete_request)

# 情景 1: E2 Node Config Update 当有新的DU被添加
def e2_node_config_update_new_du_http():
    update_request = E2NodeConfigUpdate()
    update_request.setComponentByName('globalE2NodeID', 'GlobalE2NodeID-123')

    config_list = ConfigList()
    config_list.extend(['DU1-Config'])
    update_request.setComponentByName('configList', config_list)

    encoded_update = encoder.encode(update_request)
    response = send_e2_node_config_update_http(encoded_update)
    print("E2 Node Config Update Response for new DU:", response)

    setup_request = E2SetupRequest()
    setup_request.setComponentByName('globalE2NodeID', 'GlobalE2NodeID-123')

    ran_function_list = ConfigList()
    ran_function_list.extend(['Function1', 'Function2'])
    setup_request.setComponentByName('ranFunctionList', ran_function_list)

    encoded_setup_request = encoder.encode(setup_request)
    response = send_e2_setup_request_http(encoded_setup_request)
    print("E2 Setup Response:", response)

# 情景 2: E2 Node Config Update 当DU被移除
def e2_node_config_update_remove_du_http():
    update_request = E2NodeConfigUpdate()
    update_request.setComponentByName('globalE2NodeID', 'GlobalE2NodeID-123')

    config_list = ConfigList()
    config_list.extend(['Remove-DU1'])
    update_request.setComponentByName('configList', config_list)

    encoded_update = encoder.encode(update_request)
    response = send_e2_node_config_update_http(encoded_update)
    print("E2 Node Config Update Response for DU Removal:", response)

    delete_request_kpm = create_subscription_delete_request(req_id=1, ran_func_id=1)
    response_delete_kpm = send_subscription_delete_request_http(delete_request_kpm)
    print("KPM Subscription Delete Response:", response_delete_kpm)

    delete_request_rc = create_subscription_delete_request(req_id=2, ran_func_id=2)
    response_delete_rc = send_subscription_delete_request_http(delete_request_rc)
    print("RC Subscription Delete Response:", response_delete_rc)

# 情景 3: E2 Node Config Update 当小区上线
def e2_node_config_update_cell_up_http():
    update_request = E2NodeConfigUpdate()
    update_request.setComponentByName('globalE2NodeID', 'GlobalE2NodeID-123')

    config_list = ConfigList()
    config_list.extend(['CellUp-Config'])
    update_request.setComponentByName('configList', config_list)

    encoded_update = encoder.encode(update_request)
    response = send_e2_node_config_update_http(encoded_update)
    print("E2 Node Config Update Response for Cell Up:", response)

# 情景 4: E2 Node Config Update 当小区下线
def e2_node_config_update_cell_down_http():
    update_request = E2NodeConfigUpdate()
    update_request.setComponentByName('globalE2NodeID', 'GlobalE2NodeID-123')

    config_list = ConfigList()
    config_list.extend(['CellDown-Config'])
    update_request.setComponentByName('configList', config_list)

    encoded_update = encoder.encode(update_request)
    response = send_e2_node_config_update_http(encoded_update)
    print("E2 Node Config Update Response for Cell Down:", response)

# 主程序，根据需要选择执行哪个情景
def main_http():
    print("选择执行情景：")
    print("1: 新的DU被添加")
    print("2: DU被移除")
    print("3: 小区上线")
    print("4: 小区下线")
    
    choice = input("请输入选择的数字: ")
    
    if choice == "1":
        e2_node_config_update_new_du_http()
    elif choice == "2":
        e2_node_config_update_remove_du_http()
    elif choice == "3":
        e2_node_config_update_cell_up_http()
    elif choice == "4":
        e2_node_config_update_cell_down_http()
    else:
        print("无效的选择，请重新运行程序并选择正确的选项。")

if __name__ == "__main__":
    main_http()
