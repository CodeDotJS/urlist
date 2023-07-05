<h3 align="center"><img src="media/logo.png" width="30%"></h3>

<h4 align="center">URLs from URL(s)</h4>

---

### Purpose

- This script extracts all the URLs from a text file containing a list of websites, and saves them in JSON format.
- Handles missing schemas and fixes relative URLs to ensure accurate results.
- Uses multithreading to concurrently process multiple websites, so it's fast!

---

### Usage

- Install the required modules

```sh
$ pip install aiohttp beautifulsoup4 fake_useragent
```

- Download the script

```sh
$ curl -OL https://raw.githubusercontent.com/CodeDotJS/urlist/master/extractor.py
```

- Run

```sh
$ python extractor.py
```

__Note:__ If you need to save all the links present in the JSON to a text file, you can download

```sh
$ curl -OL https://raw.githubusercontent.com/CodeDotJS/urlist/master/generateTxt.py
```

### Reason

I needed a tool to generate thousands of active URLs and dump them as JSON, so I built one.


### License

MIT
