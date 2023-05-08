from bs4 import BeautifulSoup as bs
import numpy as np
import requests
import pandas as pd
import sys

# Part 1 step 1
url = "https://www.spaceweatherlive.com/en/solar-activity/top-50-solar-flares.html"
r = requests.get(url)
status_code = r.status_code

# If bad status code do sys.exit()
if(status_code != 200):
    sys.exit("GET request failed")
content = r.content
soup = bs(content, 'html.parser')

# Use prettify to look at html code
html = soup.prettify()

# Grab table
table = soup.find("div", class_="table-responsive-md")
table_text = table.prettify()

columns = ["rank", "x_class", "date", "region", "start_time", "max_time", "end_time", "movie"]
table = pd.read_html(table_text)
print(len(table))
df = table[0]
df.columns = columns
df.index += 1

# Step 2
# remove last column
df.drop(df.columns[len(df.columns)-1], axis=1, inplace=True)

# combine time columns with date column and change to type datetime
df["start_time"] = pd.to_datetime(df['date'] + ' ' + df['start_time'])
df["max_time"] = pd.to_datetime(df['date'] + ' ' + df['max_time'])
df["end_time"] = pd.to_datetime(df['date'] + ' ' + df['end_time'])

# remove date column and rename time columns
df.drop(labels="date", axis=1, inplace=True)
df.rename(columns={'start_time': 'start_datetime', 'max_time': 'max_datetime', 'end_time': 'end_datetime'}, inplace=True)
df["region"].replace('-', np.nan, inplace=True)


