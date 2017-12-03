import xml.etree.ElementTree as ET


class ConfigManager:

    def __init__(self, config_file="Config.xml"):
        self.tree = ET.parse(config_file)
        self.root = self.tree.getroot()
        self.holder = []

    def recursive_get_xml(self, start_point, level):
        start = start_point
        for child in start:
            self.holder.append([level, child.tag, child.attrib])
            if child is not None:
                self.recursive_get_xml(child, level+1)
