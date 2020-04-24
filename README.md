# scrape_findu

- Scrape findu.com for weather archive&mdash;the latest record.
- Python 3, urllib.request(), BeautifulSoup(), datetime.time(), regex

## Tested With

- Python 3.7.5
- Ubuntu 19.10 (Eoan)
- Bash 5.0.3 (x86_64-pc-linux-gnu)

## Run App

In a Unix-like terminal emulator, enter the following arguments in the Bash CLI:

```shell
$ /bin/python3 scrape_findu.py
```

User needs to be in the working directory for those arguments to execute correctly.

`$ ./scrape_findu.py` may also run the app, depending upon how permissions pan out (see _Shebang Line_ section).

Also be aware of usage limitations.

## Shebang Line

`#! /bin/python3`

Following the [shebang](https://en.wikipedia.org/wiki/Shebang_(Unix)) (`#!`) is the [interpreter directive](https://en.wikipedia.org/wiki/Interpreter_directive) (`/bin/python3`). The shebang line enables a Python executable file to execute using `./`, as shown in the previous section.

>...in a [Unix-like](https://en.wikipedia.org/wiki/Unix-like) operating system, the [program loader](https://en.wikipedia.org/wiki/Loader_(computing)) mechanism parses the rest of the file's initial line as an interpreter directive. The loader executes the specified [interpreter](https://en.wikipedia.org/wiki/Interpreter_(computing)) program, passing to it, as an argument, the path that was initially used when attempting to run the script, so that the program may use the file as input data.

In other words, the _loader_ parses `/bin/python3` as a Unix argument, which explains why the `./scrape_findu.py` argument can be used to run the file like a program (if permissions are favorable).

## Imports

```python
import urllib.request
from bs4 import BeautifulSoup
from datetime import time
import re
```

The classes and functions of the [urllib.request](https://docs.python.org/3/library/urllib.request.html#module-urllib.request) module help open URLs&mdash;especially the HTTP protocol&mdash;for authentication, redirections, cookies, etc._

>[Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) is a Python library for pulling data out of HTML and XML files. It works with your favorite parser to provide idiomatic ways of navigating, searching, and modifying the parse tree.

>datetime.time(): Return [time](https://docs.python.org/3/library/datetime.html#datetime.time) object with same hour, minute, second, microsecond and fold.

>re.compile(pattern, flags=0): Compile a [regular expression pattern](https://docs.python.org/3/library/re.html#re-objects) into a regular expression object, which can be used for matching, using its [match()](https://docs.python.org/3/library/re.html#re.Pattern.match), [search()](https://docs.python.org/3/library/re.html#re.Pattern.search) and other methods...

[re.sub](https://docs.python.org/3/library/re.html#re.sub)() searches for a regex pattern in a string, and replaces the substring with another string, or an empty string (`''`).

## Variables

```python3
_res = urllib.request.urlopen('http://www.findu.com/cgi-bin/raw.cgi?call=KC9DNQ-3&units=english')
_html = _res.read()
_soup = BeautifulSoup(_html, "html.parser")
_data = _soup.find('tt').text
observ_list = _data.splitlines()
rgx = re.compile(
    r'@([0-9]{6})z[0-9]{4}.[A-Z0-9]{3}\/[0-9]{5}.[A-Z0-9]{3}_([0-9]{3})\/([0-9]{3})g([0-9]{3})t([0-9]{3})r([0-9]{3})p([0-9]{3})P([0-9]{3})b([0-9]{5})h([0-9]{2})[l|L]([0-9]{3})')
grp = rgx.findall(observ_list[1])
(timestamp, wind_dir, wind_spd, wind_gst, temperature, rain_hr, rain_24, rain_mid, barometer, humidity, luminosity) = grp[0]
```

- `urllib.request.urlopen()` requests weather data archive from [FindU](http://www.findu.com/). [HTTPResponse](https://docs.python.org/3/library/http.client.html#httpresponse-objects) instance wraps HTTP response into an iterable object for access to request headers and entity body. Which can be accessed using [with](https://docs.python.org/2.5/whatsnew/pep-343.html) statement.
- [HTTPResponse.read()](https://docs.python.org/3/library/http.client.html#http.client.HTTPResponse.read) reads and returns response body.
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) supports _html.parser_ library. Also, BS4 relies on the [lxml](https://lxml.de/) parser, so that module may need to be installed. Basically, BS4 parses and organizes HTML syntax using a document tree. In the case of this app, BS4 accesses the `text` in the `<tt>` container, which contains archived weather data transmitted by a personal weather station (`_soup.find('tt').text`).
- splitlines() method basically comma separates the lines of weather data into a Python list. Line breaks are left out, but were used to determine where the string should be split into list elements.
- [re.compile()](https://docs.python.org/3/library/re.html#re.compile) basically compiles a regex pattern into a regex object.
- [re.findall()](https://docs.python.org/3/library/re.html#re.findall) returns a list of grouped weather data based on the compiled regex pattern. For example, the regex pattern `([0-9]{3})` groups a three number value `000`.
- `(timestamp, wind_dir, wind_spd, wind_gst, temperature, rain_hr, rain_24, rain_mid, barometer, humidity, luminosity) = grp[0]` names each listed group so that they become more easily identifiable in the `print()` calls.
- `datetime.time(hour=int(timestamp[2:4]), minute=int(timestamp[4:6])).strftime("%H:%M")` formats the six-digit string. The first two numbers indicate the day of the current month. The last four digits indicate military zulu time, which explains the 'Z'. Military zulu time is the same as UTC and Greenwich time. The splices separate 6 digits into three parts: _day_, _hour_, _min_.
- `re.sub(r'\b0{1,2}', '', wind_spd)` substitutes a leading zero with an empty space (`''`). `{1,2}` indicates that one or two zeros will be removed, and if the third digit is a zero, it will remain. `\b` tells regex to eliminate zeros on the left only.
- `['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'][round(int(re.sub(r'\b0{1,2}', '', wind_dir)[1:]) / 22.5) % 16]` receives a numerical degrees value and returns a cardinal direction.

## Twitter Hashtags

- [#100DaysOfCode](https://twitter.com/hashtag/100DaysOfCode?f=live)
- [#PythonProgramming](https://twitter.com/hashtag/PythonProgramming?f=live)
- [#PythonCode](https://twitter.com/hashtag/PythonCode?f=live)
- [#WeatherApp](https://twitter.com/hashtag/WeatherApp?f=live)
- [#APRS](https://twitter.com/hashtag/APRS?f=live)
- [#BeautifulSoup](https://twitter.com/hashtag/BeautifulSoup?f=live)
- [#Regex](https://twitter.com/hashtag/Regex?f=live)
