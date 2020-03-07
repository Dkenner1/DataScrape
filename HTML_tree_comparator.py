import requests
import itertools
import json
from bs4 import BeautifulSoup
from queue import LifoQueue


# Function that receives a node and returns a list of all its unique children
def unique_comparator(parent_node):
    row = parent_node.contents
    result = []
    # Create a list of unique children rows
    for node in row:
        if not equals(node, node.next_sibling):
            result.append(node)

    # Check uniqueness of children
    for node in result:
        node.contents = unique_comparator(node)

    return result

    # Compare the two nodes by comparing their attributes


def equals(node, sibling_node):
    for (attr1, attr2) in itertools.izip(node.attrs, sibling_node.attrs):
        if attr1 == attr2:
            return node[attr1] == sibling_node[attr2]
        else:
            return True

    return True
