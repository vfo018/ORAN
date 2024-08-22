from pyasn1.codec.ber import encoder, decoder
from pyasn1.type import univ, namedtype, char
import requests

# 定义ActionItem ASN.1结构
class ActionItem(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('actionID', univ.Integer()),
        namedtype.NamedType('actionType', char.VisibleString()),
        namedtype.NamedType('actionDefinition', char.VisibleString()),
        namedtype.NamedType('subsequentAction', univ.Boolean())
    )

# 定义SubscriptionRequest ASN.1结构
class SubscriptionRequest(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('reqID', univ.Integer()),
        namedtype.NamedType('ranFuncID', univ.Integer()),
        namedtype.NamedType('eventTrigger', char.VisibleString()),
        namedtype.NamedType('actions', univ.SequenceOf(componentType=ActionItem()))
    )

# 创建KPM订阅请求
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

def main():
    req_id = 1  # 订阅请求的唯一ID
    ran_func_id = 1  # 假设KPM的RAN功能ID为1
    event_trigger = 'Periodic Report'  # 假设我们使用周期性报告
    action_type = 'Report'
    action_definition = 'KPM Details'
    
    # 创建订阅请求
    encoded_request = create_subscription_request(req_id, ran_func_id, event_trigger, req_id, action_type, action_definition)

    # 通过HTTP发送订阅请求
    ric_api_url = "http://your-ric-endpoint/api/v1/subscription"  # 替换为实际的RIC API地址
    response_http = send_subscription_request_http(encoded_request, ric_api_url)

    if response_http.status_code == 200:
        print(f"Subscription Request sent successfully via HTTP.")
    else:
        print(f"Failed to send Subscription Request via HTTP, status code: {response_http.status_code}")

if __name__ == "__main__":
    main()
