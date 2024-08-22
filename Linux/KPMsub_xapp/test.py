from pyasn1.codec.ber import decoder
from pyasn1.type import univ, namedtype, char

# 定义基本的ASN.1结构，无标签
class SimpleE2NodeComponentConfigItem(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('e2NodeComponentInterfaceType', univ.Integer()),
        namedtype.NamedType('e2NodeComponentID', char.PrintableString()),
        namedtype.NamedType('e2NodeComponentConfigurationAcknowledge', univ.Boolean())
    )

class SimpleE2NodeCompConfigAddList(univ.SequenceOf):
    componentType = SimpleE2NodeComponentConfigItem()

def test_decoding(encoded_data):
    try:
        decoded_data, _ = decoder.decode(encoded_data, asn1Spec=SimpleE2NodeCompConfigAddList())
        print("Decoded data:", decoded_data)
    except Exception as e:
        print("Decoding failed:", str(e))

# 示例数据 (替换为实际的编码数据)
encoded_data = b'...'  
test_decoding(encoded_data)
