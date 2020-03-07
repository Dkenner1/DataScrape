import requests
import simplejson as json
from bs4 import BeautifulSoup
from queries import add_key, add_keychart_lnk

# Reads and iterates through a file with all charts
def fc_link_iterator(web_page_file):
    attributes = []
    # FC_links file includes all the FC graph types
    url_arr = open(web_page_file).read().splitlines()
    for url in url_arr:
        attributes.append(fc_attribute_scrape(url))
    return attributes


# Scrape HTML file.
def fc_attribute_scrape(web_page_link):
    output_arr = {}

    # Grab and parse URL
    response = requests.get(web_page_link)
    html_soup = BeautifulSoup(response.text, "html.parser")

    # loop all attribute areas.
    attribute_list = html_soup.find_all(class_="attribute-wrapper")
    if len(attribute_list) == 0:
        print("WARNING: No attributes.")
    else:
        for attribute in attribute_list:
            tup = {}
            parameters = attribute.find_all(class_="param")
            if len(parameters) == 0:
                print("WARNING: No attribute parameters.")
            else:
                arr_head = attribute.find(class_="code-text key").getText()

                # obtain 'group' details
                temp = attribute.find(class_="table-name")
                desc = attribute.find(class_="description")
                group_name = temp.getText()
                print("Group: '" + group_name + "'")

                # loop all parameters
                for param in parameters:
                    key = param.find(class_="code-text key").getText()
                    type_text = param.find(class_="code-text value").getText()
                    description = param.find(class_="description").getText()

                    ranges = param.find(class_="range-val")
                    fc_range = ""
                    if ranges is not None:
                        fc_range = ranges.getText()

                    tup[key] = (type_text, description, fc_range)
                    attribute_recid = add_key(key.strip(), arr_head.strip(), type_text.strip(), description, fc_range)
                    add_keychart_lnk(attribute_recid, group_name.strip())

                output_arr[group_name] = (desc.getText(), arr_head, tup)

        print("\nJSON String Output:\n")
        print(output_arr)
        # Following command commits changes to the tables
        #diml_db.commit()
        return output_arr


if __name__ == '__main__':
    attributes_arr = fc_link_iterator("FC_Links.txt")
    with open("FC_scrape.json", 'a') as json_file_output:
        json.dump(attributes_arr, json_file_output)
