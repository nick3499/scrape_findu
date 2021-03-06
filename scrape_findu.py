#! /bin/python3
'''Scrape KC9DNQ-3 PWS data from findu.com. Available under MIT license.'''
import urllib.request
from bs4 import BeautifulSoup
from datetime import time
import re


_res = urllib.request.urlopen('http://www.findu.com/cgi-bin/raw.cgi?call=KC9DNQ-3&units=english')
_html = _res.read()
_soup = BeautifulSoup(_html, "html.parser")
_data = _soup.find('tt').text
observ_list = _data.splitlines()
# compiled regex pattern
rgx = re.compile(
    r'@([\d]{6})z[\d]{4}.[\w]{3}\/[\d]{5}.[\w]{3}_([\d]+)\/([\d]{3})g([\d]{3})t([\d]{3})r([\d]{3})p([\d]{3})P([\d]{3})b([\d]{5})h([\d]{2})L([\d]{3}).')
# captured group list tuple
grp = rgx.findall(observ_list[1])
# named groups
(timestamp, wind_dir, wind_spd, wind_gst, temperature, rain_hr, rain_24,
rain_mid, barometer, humidity, luminosity) = grp[0]
print('\033[1;33m================\033[0m')
# station | protocol
print(f'\033[1;33mStation\033[0m: KC9DNQ-3 \U0001F30E \
\033[1;33mProtocol\033[0m: APRS')
# day | time
print(f'\033[1;33mDay\033[0m: {timestamp[:2]} \U0001F30E \
\033[1;33mTime\033[0m: \
{time(hour=int(timestamp[2:4]), minute=int(timestamp[4:6])).strftime("%H:%M")}Z')
# temperature
print(f'\033[1;34m===== Temp =====\033[0m\n\033[1;32mTemperature\033[0m: ' +
re.sub(r'\b0{1,2}', '', temperature) +
'\u2109')
# wind: speed | gust | direction
print(f'\033[1;34m===== Wind =====\033[0m\n\
\033[1;32mSpeed\033[0m: ' + re.sub(r'\b0{1,2}', '', wind_spd) + ' mph' +
' \U0001F30E \033[1;32mGust\033[0m: ' + re.sub(r'\b0{1,2}', '', wind_gst) +
' mph' + ' \U0001F30E \033[1;32mDirection\033[0m:', ['N', 'NNE', 'NE', 'ENE',
'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
[round(int(re.sub(r'\b0{1,2}', '', wind_dir)[1:]) / 22.5) % 16])
# rain: last hr | last 24 hrs | since midnight
print(f'\033[1;34m===== Rain =====\033[0m\n\033[1;32mLast hour\033[0m: ' +
re.sub(r'\b0{1,2}', '', rain_hr) + '\u2033 \U0001F30E \033[1;32mLast 24 \
hours\033[0m: ' + re.sub(r'\b0{1,2}', '', rain_24) + '\u2033 \U0001F30E \
\033[1;32mSince midnight\033[0m: ' + re.sub(r'\b0{1,2}', '', rain_mid) +
'\u2033')
# barometer
baro = round(int(re.sub(r'\b0{1,2}', '', barometer)) * 0.1, 1)
print(f'\033[1;34m===== Barometer ======\033[0m\n\
\033[1;32mAtm pressure\033[0m: {baro} \u3386')
# humidity
print(f'\033[1;34m===== Humidity =======\033[0m\n\033[1;32mHumidity\033[0m: ' +
re.sub(r'\b0{1,2}', '', humidity) + '\u0025')
# luminosity
print(f'\033[1;34m===== Luminosity =====\033[0m\n\033[1;32mLuminosity\
\033[0m: ' + re.sub(r'\b0{1,2}', '', luminosity) + ' W/\u33A1')
print('\033[1;33m======================\033[0m')
