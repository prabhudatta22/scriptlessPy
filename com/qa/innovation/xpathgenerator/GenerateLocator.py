from bs4 import Tag
from typing import List
from element_details import ElementDetails  # assume this is a Python equivalent class
import re

class GenerateLocator:

    def get_attribute_selector(self, attr_name: str, node: Tag) -> str:
        response = ""
        selector = ""

        if node.has_attr(attr_name):
            selector = node.name.lower()
            if attr_name == "class":
                selector = node[attr_name].strip().replace(" ", ".")
            else:
                response = re.sub(r"[\r\n]", ".", node[attr_name])
                selector += f"[{attr_name}='{response}']"

        return selector

    def get_css_selector(self, node: Tag) -> str:
        selector = ""

        if node.get("id"):
            selector = f"#{node['id']}"
        else:
            node_name = node.name
            current_selector = node_name.lower()
            index = self.get_node_index(node, node_name)

            if index > 0:
                current_selector += f":nth-of-type({index})"
            else:
                class_name = node.get("class")
                if class_name:
                    current_selector += "." + ".".join(class_name)

                if node_name.upper() == "INPUT":
                    if node.get("type"):
                        current_selector += f"[type=\"{node['type']}\"]"
                    if node.get("name"):
                        current_selector += f"[name=\"{node['name']}\"]"
                    elif node.get("data-type"):
                        current_selector += f"[data-type=\"{node['data-type']}\"]"

            selector = current_selector + selector

        return re.sub(r"^html[^\\b]*\\bbody\\b", "", selector).strip()

    def get_locator(self, node: Tag, ed: ElementDetails) -> ElementDetails:
        response = ""

        if node.get("id"):
            response = node["id"]
            ed.set_id(response)
            ed.set_locator_type("ID")

        elif node.get("name"):
            response = node["name"]
            ed.set_name(f".//*[@name='{response}']")
            ed.set_locator_type("Name")

        else:
            if not response and node.get("title"):
                response = self.get_attribute_selector("title", node).replace("[", "[@").replace('"', "'")
                ed.set_title(f".//*[@title='{response}']")
                ed.set_locator_type("Title")

            if not response and node.get("href"):
                response = self.get_attribute_selector("href", node).replace("[", "[@").replace('"', "'")
                ed.set_href(f".//*[@href='{response}']")
                ed.set_locator_type("href")

            if not response and node.get("value"):
                response = self.get_attribute_selector("value", node)
                ed.set_value(f".//*[@value='{response}']")
                ed.set_locator_type("value")

            if not response and node.get("class"):
                response = self.get_attribute_selector("class", node)
                ed.set_class_name(f".//*[@class='{response}']")
                ed.set_locator_type("ClassName")

            if not response and not node.get("value"):
                response = self.get_css_selector(node)
                ed.set_locator_type("CSS")
                ed.set_csspath(response)

        return ed

    def get_node_index(self, node: Tag, node_name: str) -> int:
        index = 0
        siblings = node.parent.find_all(node.name, recursive=False)
        for i, sibling in enumerate(siblings):
            if sibling == node:
                index = i + 1  # nth-of-type is 1-based
                break
        return index
