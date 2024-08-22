import socket
import sctp
from pyasn1.codec.ber import encoder, decoder
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

class E2setupRequest(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('globalE2NodeID', GlobalE2nodeID()),
        namedtype.NamedType('ranFunctionsAdded', univ.SequenceOf(componentType=RanFunctionItem())),
        namedtype.OptionalNamedType('e2NodeComponentConfigUpdateList', univ.SequenceOf(componentType=char.VisibleString()))
    )

class E2setupResponse(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('globalE2NodeID', GlobalE2nodeID()),
        namedtype.NamedType('ranFunctionsAccepted', univ.SequenceOf(componentType=RanFunctionItem()))
    )

# 构建E2 Setup请求
def create_e2_setup_request():
    e2_setup_request = E2setupRequest()

    # 设置全局E2节点ID
    global_e2_node_id = GlobalE2nodeID()
    global_e2_node_id.setComponentByName('globalgNB-ID', 'gNB_ID_123')
    e2_setup_request.setComponentByName('globalE2NodeID', global_e2_node_id)

    # 构建 RAN 功能列表
    ran_func_list = []

    # 添加 ORAN-E2SM-KPM 功能
    ran_func_item_kpm = RanFunctionItem()
    ran_func_item_kpm.setComponentByName('ranFunctionID', 1)
    ran_func_item_kpm.setComponentByName('ranFunctionDefinition', 'ORAN-E2SM-KPM')
    ran_func_item_kpm.setComponentByName('ranFunctionRevision', 1)
    ran_func_list.append(ran_func_item_kpm)

    # 添加 ORAN-E2SM-RC 功能
    ran_func_item_rc = RanFunctionItem()
    ran_func_item_rc.setComponentByName('ranFunctionID', 2)
    ran_func_item_rc.setComponentByName('ranFunctionDefinition', 'ORAN-E2SM-RC')
    ran_func_item_rc.setComponentByName('ranFunctionRevision', 1)
    ran_func_list.append(ran_func_item_rc)

    e2_setup_request.setComponentByName('ranFunctionsAdded', ran_func_list)

    # 构建E2节点组件配置更新列表
    e2_node_comp_list = []
    e2_node_comp_list.append('F1 Setup Request ASN Buffer')
    e2_node_comp_list.append('F1 Setup Response ASN Buffer')

    e2_setup_request.setComponentByName('e2NodeComponentConfigUpdateList', e2_node_comp_list)

    # 编码为 ASN.1 二进制格式
    encoded_request = encoder.encode(e2_setup_request)

    return encoded_request

# 通过SCTP传输E2 Setup请求
def send_e2_setup_sctp(encoded_request, ric_ip, ric_port):
    # 创建 SCTP 套接字
    sctpsock = sctp.sctpsocket_tcp(socket.AF_INET)
    sctpsock.connect((ric_ip, ric_port))

    # 发送 E2 Setup 请求
    sctpsock.sctp_send(encoded_request)

    # 接收 E2 Setup 响应
    response = sctpsock.recv(4096)
    
    # 关闭 SCTP 连接
    sctpsock.close()

    return response

# 处理E2 Setup响应
def get_e2_setup_response_sctp(response):
    # 解码收到的E2 Setup响应
    setup_response, _ = decoder.decode(response, asn1Spec=E2setupResponse())

    # 处理解码后的响应
    process_setup_response(setup_response)

def process_setup_response(setup_response):
    # 提取全局E2节点ID和RAN功能列表
    global_e2_node_id = setup_response.getComponentByName('globalE2NodeID')
    ran_func_list = setup_response.getComponentByName('ranFunctionsAccepted')

    print(f"Extracted Global E2 Node ID: {global_e2_node_id}")
    print(f"Extracted RAN Function List: {ran_func_list}")

# 主流程
if __name__ == "__main__":
    # 构建E2 Setup Request消息
    encoded_request = create_e2_setup_request()

    # 使用SCTP传输E2 Setup请求
    ric_ip = "192.168.1.100"  # 替换为实际的RIC IP地址
    ric_port = 36422  # 替换为实际的RIC SCTP端口
    response_sctp = send_e2_setup_sctp(encoded_request, ric_ip, ric_port)
    
    # 处理响应
    get_e2_setup_response_sctp(response_sctp)
