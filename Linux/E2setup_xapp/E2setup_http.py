import requests
from pyasn1.codec.ber import encoder
from pyasn1.type import univ, char, namedtype

# 定义ASN.1结构
class GlobalE2nodeID(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('globalgNB-ID', char.VisibleString())
    )

class RanFunctionItem(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('ranFunctionID', univ.Integer()),
        namedtype.NamedType('ranFunctionDefinition', char.VisibleString()),
        namedtype.NamedType('ranFunctionRevision', univ.Integer())
    )

class E2NodeComponentConfigItem(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('e2NodeComponentInterfaceType', univ.Integer()),
        namedtype.NamedType('e2NodeComponentID', char.VisibleString()),
        namedtype.NamedType('e2NodeComponentConfigurationAcknowledge', char.VisibleString())
    )

class E2setupResponse(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('messageType', univ.Integer()),  # 消息类型
        namedtype.NamedType('transactionID', univ.Integer()),  # 事务ID
        namedtype.NamedType('globalRICID', char.VisibleString()),  # Global RIC ID
        namedtype.OptionalNamedType('ranFunctionsAccepted', univ.SequenceOf(componentType=RanFunctionItem())),
        namedtype.OptionalNamedType('ranFunctionsRejected', univ.SequenceOf(componentType=RanFunctionItem())),
        namedtype.OptionalNamedType('e2NodeComponentConfigAdditionAckList', univ.SequenceOf(componentType=E2NodeComponentConfigItem()))
    )

# 构建E2 Setup Response
def create_e2_setup_response():
    e2_setup_response = E2setupResponse()

    # 设置消息类型
    e2_setup_response.setComponentByName('messageType', 1)  # 示例值

    # 设置事务ID
    e2_setup_response.setComponentByName('transactionID', 1001)  # 示例值

    # 设置Global RIC ID
    e2_setup_response.setComponentByName('globalRICID', 'RIC_ID_12345')  # 示例值

    # 添加 RAN 功能接受列表
    ran_func_accepted_list = []

    ran_func_item_kpm = RanFunctionItem()
    ran_func_item_kpm.setComponentByName('ranFunctionID', 1)
    ran_func_item_kpm.setComponentByName('ranFunctionDefinition', 'ORAN-E2SM-KPM')
    ran_func_item_kpm.setComponentByName('ranFunctionRevision', 1)
    ran_func_accepted_list.append(ran_func_item_kpm)

    e2_setup_response.setComponentByName('ranFunctionsAccepted', ran_func_accepted_list)

    # 添加 E2 Node Component Configuration Acknowledge 列表
    e2_node_component_ack_list = []

    e2_node_component_item = E2NodeComponentConfigItem()
    e2_node_component_item.setComponentByName('e2NodeComponentInterfaceType', 2)  # 示例值
    e2_node_component_item.setComponentByName('e2NodeComponentID', 'Component_ID_1')  # 示例值
    e2_node_component_item.setComponentByName('e2NodeComponentConfigurationAcknowledge', 'Acknowledge')  # 示例值

    e2_node_component_ack_list.append(e2_node_component_item)
    e2_setup_response.setComponentByName('e2NodeComponentConfigAdditionAckList', e2_node_component_ack_list)

    # 编码为 ASN.1 二进制格式
    encoded_response = encoder.encode(e2_setup_response)

    return encoded_response

# 发送E2 Setup Response
def send_e2_setup_response_http(encoded_response, ric_api_url):
    headers = {'Content-Type': 'application/octet-stream'}
    response = requests.post(ric_api_url, data=encoded_response, headers=headers)
    return response

# 主流程
if __name__ == "__main__":
    # 构建E2 Setup Response消息
    encoded_response = create_e2_setup_response()

    # 使用HTTP传输E2 Setup Response
    ric_api_url = "http://your-ric-endpoint/api/v1/e2setupresponse"  # 替换为实际的RIC API地址
    response_http = send_e2_setup_response_http(encoded_response, ric_api_url)

    if response_http.status_code == 200:
        print("E2 Setup Response sent successfully.")
    else:
        print(f"Failed to send E2 Setup Response, status code: {response_http.status_code}")
