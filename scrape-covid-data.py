import json
import requests
import tabula
from bs4 import BeautifulSoup
import subprocess 

# Get LATimes daily County cases
latimesurl = 'https://www.latimes.com/projects/california-coronavirus-cases-tracking-outbreak/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

latimes_page = requests.get(latimesurl, headers=headers)

soup = BeautifulSoup(latimes_page.content, 'html.parser')
california = int(
    soup.find('div', class_='big-number').contents[0].replace(',', ''))
# print(california)

latimesocurl = 'https://www.latimes.com/projects/california-coronavirus-cases-tracking-outbreak/orange-county/'
latimesoc_page = requests.get(latimesocurl, headers=headers)
soup = BeautifulSoup(latimesoc_page.content, 'html.parser')
orange = int(
    soup.find('div', class_='big-number').contents[0].replace(',', ''))
# print(orange)

latimeslaurl = 'https://www.latimes.com/projects/california-coronavirus-cases-tracking-outbreak/los-angeles-county/'
latimesla_page = requests.get(latimeslaurl, headers=headers)

soup = BeautifulSoup(latimesla_page.content, 'html.parser')
los_angeles = int(
    soup.find('div', class_='big-number').contents[0].replace(',', ''))

# print(los_angeles)

#timeline = json.loads(soup.find('script', id="counties-timeseries-data").text)
# print(timeline)
#san_diego = timeline[36]['new_confirmed_cases_per_100k'][-1]
# print(san_diego)

##san_diego = timeline[36]['case_table'][-1]
#orange = timeline[29]['case_table'][-1]
#los_angeles = timeline[18]['case_table'][-1]


# Get San Diego County Daily by ZIP. Need to parse PDF tables
sd_by_zip_pdf_url = "https://www.sandiegocounty.gov/content/dam/sdc/hhsa/programs/phs/Epidemiology/COVID-19%20Summary%20of%20Cases%20by%20Zip%20Code.pdf"

sd_tables_by_zip = tabula.read_pdf(
    sd_by_zip_pdf_url, pages="all", multiple_tables=True)

#print(int(float(sd_tables_by_zip[2].iloc[4][2])))
my_zip = int(sd_tables_by_zip[2].iloc[4][1])


# Get San Diego County Daily by City
sd_by_city_pdf_url = "https://www.sandiegocounty.gov/content/dam/sdc/hhsa/programs/phs/Epidemiology/COVID-19%20Daily%20Update_City%20of%20Residence.pdf"

sd_tables_by_city = tabula.read_pdf(
    sd_by_city_pdf_url, pages="all", multiple_tables=True)


(rows, cols) = sd_tables_by_city[0].shape

san_marcos_idx = 1
#print(sd_tables_by_city[0].iloc[1][0])
for i in range(rows):
    if i != 0 and sd_tables_by_city[0].iloc[i][0].find("San Marcos") != -1:
        san_marcos_idx = i
#print(san_marcos_idx)

san_marcos = int(sd_tables_by_city[0].iloc[san_marcos_idx][1].split()[0].replace(',', ''))
san_diego_county = int(sd_tables_by_city[0].iloc[-1][1].split()[
                        0].replace(',', ''))

# Get US Daily
us_daily_url = 'https://covidtracking.com/api/v1/us/daily.json'

us_daily = requests.get(us_daily_url)

us_daily_json = json.loads(us_daily.content)
us_positive = us_daily_json[0]['positive']

report = f'{my_zip};{san_marcos};{san_diego_county};{orange};{los_angeles};{california};{us_positive}'
print(report)

# print(f'{my_zip};{san_marcos};{us_positive}')
subprocess.run("pbcopy", universal_newlines=True, input=report)