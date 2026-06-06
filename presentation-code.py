import requests
import pandas as pd
# from bs4 import BeautifulSoup
from lxml import html
import pprint

# get the html
cb_url = "https://www.census.gov/programs-surveys/household-pulse-survey/data/datasets.2023.html"
cb_resp = requests.get(cb_url)

# initiate a parser for the page source
cb_src = html.fromstring(cb_resp.content)


elements = cb_src.xpath(
    "//h3[contains(text(), 'PUF')] | //h4 | //a[contains(text(), 'PUF CSV')]"
)
print(elements[0:4])


def extract_info(element):
    tag = element.tag
    text = element.text
    if tag == "a":
        href = element.attrib["href"]
    else:
        href = None
    return {"tag": tag, "text": text, "href": href}

element_info = [extract_info(el) for el in elements]
pprint.pp(element_info[0:3])


# Make a dataframe 
df = pd.DataFrame(element_info) 
df.head()


def extract_tag(row, t):
    if row.tag == t:
        return row.text
    else:
        return None

# Column for h3s
df["h3"] = df.apply(lambda row: extract_tag(row, "h3"), axis=1)

# Column for h4s
df["h4"] = df.apply(lambda row: extract_tag(row, "h4"), axis=1)


# fill h3s down
df["h3"] = df["h3"].ffill()

# fill h4s down within h3 groups
df["h4"] = df.groupby("h3")["h4"].ffill()

# keep only link rows
df = df.loc[df["tag"] == "a",]


df = df[["h3", "h4", "text", "href"]].rename(
    columns={"h3": "phase", "h4": "wave", "text": "name", "href": "url"}
)

df.head()


ed_url = "https://civilrightsdata.ed.gov/data"
ed_resp = requests.get(ed_url)
ed_src = html.fromstring(ed_resp.content)
ed_src.xpath("//table")
