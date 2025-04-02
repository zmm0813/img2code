import xml.etree.ElementTree as ET

def parse_voc_xml(xml_path):
    """
    解析 VOC 格式的 XML 文件，提取目标检测的标签信息。

    :param xml_path: XML 文件路径
    :return: 解析后的 JSON 格式数据
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    objects = []
    for obj in root.findall("object"):
        name = obj.find("name").text
        bndbox = obj.find("bndbox")
        xmin = int(bndbox.find("xmin").text)
        ymin = int(bndbox.find("ymin").text)
        xmax = int(bndbox.find("xmax").text)
        ymax = int(bndbox.find("ymax").text)

        objects.append({
            "type": name,
            "position": {
                "x": xmin,
                "y": ymin,
                "width": xmax - xmin,
                "height": ymax - ymin
            }
        })

    return {"elements": objects}
