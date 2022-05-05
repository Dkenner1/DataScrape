import requests
import json
import MySQLdb
from queries import add_type
from bs4 import BeautifulSoup

diml_db = MySQLdb.connect(
    host="####",
    user="###",
    passwd="####",
    database="####"
)
diml_cursor = diml_db.cursor()


def fc_link_create():
    # initializations
    type_data = []
    base_url = "https://www.fusioncharts.com/dev/chart-attributes/"
    url = "https://www.fusioncharts.com/dev/chart-attributes/area2d"

    # Pull html doc
    response = requests.get(url)
    HTML_soup = BeautifulSoup(response.text, "html.parser")

    # Find the subtree of the HTML doc that contains all the possible selections
    HTML_select = HTML_soup.findAll(class_="list-unstyled")[1]

    # From the subtree pull out all the text sections
    chart_list = HTML_select.findAll("span")
    for charts in chart_list:
        try:
            name = charts["data-alias"]
            expanded_name = charts.getText()
            url = base_url + name
            type_data.append((name, expanded_name, url))
        except KeyError:
            print("Error with chart: " + charts.getText() + "\n\n")

    # Output to terminal to check results
    # for url in url_list:
    #     print(url)

    return type_data


if __name__ == '__main__':
    type_arr = fc_link_create()
    with open("FC_type.json", 'w') as json_file_output:
        json.dump(type_arr, json_file_output)
    for chart in type_arr:
        add_type(chart[0], chart[1], chart[2])

    with open("FC_Links.txt", 'w') as txt_file_output:
        for type_key in type_arr:
            txt_file_output.write(type_key[2] + "\n")
