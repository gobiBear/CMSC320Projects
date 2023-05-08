from bs4 import BeautifulSoup as bs
import numpy as np
import requests
import pandas as pd
import sys
import datetime



# Step 3
url = 'https://cdaw.gsfc.nasa.gov/CME_list/radio/waves_type2.html'
r = requests.get(url)
status_code = r.status_code

# If bad status code do sys.exit()
if(status_code != 200):
    sys.exit('GET request failed')
content = r.content
soup = bs(content, 'html.parser')
table = soup.find('pre')

# Table starts at line 13 of pre tag and ends on line before end of pre tag
data = table.get_text().splitlines()[12:-1]
columns = ['start_date', 'start_time', 'end_date', 'end_time', 'start_frequency', 'end_frequency', 'flare_location', 'flare_region',
           'flare_importance', 'cme_date', 'cme_time', 'cme_angle', 'cme_width', 'cme_speed', 'plot']

rows = []
for line in data:
    row = line.split()[0:15]
    rows.append(row)


nasa_df = pd.DataFrame(rows, columns=columns)
nasa_df.index += 1

nasa_df['flare_location'].replace('------', np.nan, inplace=True)
nasa_df['flare_region'].replace('-----', np.nan, inplace=True)
nasa_df['flare_importance'].replace('----', np.nan, inplace=True)
nasa_df['flare_importance'].replace('FILA', np.nan, inplace=True)
nasa_df['cme_date'].replace('--/--', np.nan, inplace=True)
nasa_df['cme_time'].replace('--:--', np.nan, inplace=True)
nasa_df['cme_angle'].replace('----', np.nan, inplace=True)
nasa_df['cme_width'].replace('----', np.nan, inplace=True)
nasa_df['cme_speed'].replace('----', np.nan, inplace=True)
nasa_df['plot'].replace('----', np.nan, inplace=True)

nasa_df['is_halo'] = np.where(nasa_df['cme_angle'] == 'Halo', True, False)
nasa_df['width_lower_bound'] = np.where(nasa_df['cme_width'].str.contains('>') , True, False)

nasa_df['cme_angle'].replace('Halo', 'NA', inplace=True)
nasa_df['cme_width'] = nasa_df['cme_width'].str.replace('\D', '')

nasa_df["start_time"] = pd.to_datetime(nasa_df['start_date'] + ' ' + nasa_df['start_time'], errors='ignore')
nasa_df["end_time"] = pd.to_datetime(nasa_df['start_date'].str[0:5] + nasa_df['end_date'] + ' ' + nasa_df['end_time'], errors='ignore')
nasa_df["cme_time"] = pd.to_datetime(nasa_df['start_date'].str[0:5] + nasa_df['cme_date'] + ' ' + nasa_df['cme_time'], errors='ignore')

nasa_df.drop(labels=['start_date', 'end_date', 'cme_date'], axis=1, inplace=True)
nasa_df.rename(columns={'start_time': 'start_datetime', 'end_time': 'end_datetime', 'cme_time': 'cme_datetime'}, inplace=True)


nasa_df['sort_let'] = nasa_df['flare_importance'].str[0]
nasa_df['sort_num'] = nasa_df['flare_importance'].str.extract('(\d+\.\d*)').astype(float)

nasa_df.sort_values(['sort_let','sort_num'],inplace=True, ascending=False,ignore_index=True)
nasa_df.drop(labels=['sort_let','sort_num'], axis=1, inplace=True)

top_fifty = nasa_df.iloc[0:50]
print(top_fifty)



