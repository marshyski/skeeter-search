import elasticsearch
import requests, json, yaml, datetime, time, re
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()

config = 'sites.yaml'
yamldir = 'sites/'
sites_config = yamldir + config
sites = yaml.load(file(sites_config, 'r'))
index_name = sites['index_name']
index_type = sites['index_type']
elastic_host = sites['elastic_host']
elastic_port = sites['elastic_port']

es = elasticsearch.Elasticsearch(elastic_host, port=elastic_port)
es.indices.delete(index=index_name, ignore=[400, 404])
es.indices.create(index=index_name, ignore=400)

for URL in sites['sites']:

    try:
       r = requests.get(URL, verify=False)
       r_text = r.text
       soup = BeautifulSoup(r_text)
       title = soup.title.string
       if r.status_code == 200:

          site_text = soup.get_text()

          lines = (line.strip() for line in site_text.splitlines())
          chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
          join = ' '.join(chunk for chunk in chunks if chunk)
          text = re.sub(r'[^a-zA-Z\d\s]', '', join)

          phone_pattern = re.compile(r'(\d{3})\D*(\d{3})\D*(\d{4})\D*(\d*)')
          phone_search = phone_pattern.search(text)
          phone_number = "None"
          if phone_search:
             phone_groups = phone_search.group(0).rsplit(' ', 1)[0]
             phone_number = re.compile('[^0-9]').sub('', phone_groups)

          for script in soup(["script", "style", "title", "a", "footer"]) + \
                        soup.findAll('div', attrs={'class': 'footer'}) + \
                        soup.findAll('div', attrs={'id': 'sidebar'}):
              script.extract()

          site_text = soup.get_text().replace('"', "'")

          lines = (line.strip() for line in site_text.splitlines())
          chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
          text = ' '.join(chunk for chunk in chunks if chunk)

	  date_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')

          if phone_number != "None":
             data = '{' + '"title": "' + title + '", "url": "' + URL + '", "body": "' + text + '", "phone": "' + phone_number + '"}'
          else:
             data = '{' + '"title": "' + title + '", "url": "' + URL + '", "body": "' + text + '"}'

          print data
          res = es.index(index=index_name, doc_type=index_type, id=date_time, body=data)
          print (res['created'])
          time.sleep(1.0)

       else:

          print URL, r.status_code, "[FAIL]"

    except:
          print URL, "[FAIL]"
