# skeeter-search

Scrape web content, index into ElasticSearch and render with Calaca UI

----------

# We've all dreamed about creating a search engine, this is where it starts


**Technologies used:**

 - ElasticSearch
 - Calaca ElasticSearch UI (AngularJS)
 - Python Requests
 - Python BeautifulSoup


**Install Dependencies:**

*Server:*

 - ElasticSearch (Listening on IPv4 0.0.0.0 not 127.0.0.1 or :::) 
 - Java 7.x / OpenJDK 7
 - `pip install requirements.txt` 
 - `python -m SimpleHTTPServer` or `nginx` or `apache`
 - Entry in `elasticsearch.yml` `http.cors.enabled: true`

 **Last step is configure ElasticSearch mappings for all indexes to not be analyzed:**
 
 
       curl -XPUT localhost:9200/_template/template_1 -d '
       {
          "template":"*",
          "settings":{
             "index.refresh_interval":"5s"
          },
          "mappings":{
             "_default_":{
                "_all":{
                   "enabled":true
                },
                "dynamic_templates":[
                   {
                      "string_fields":{
                         "match":"*",
                         "match_mapping_type":"string",
                         "mapping":{
                            "type":"string",
                            "index":"not_analyzed",
                            "omit_norms":true
                         }
                      }
                   }
                ]
             }
          }
       }'


**Configuration (YAML):**

*sites/sites.yaml*

    # Sites you want to index
    sites: sites: ['http://marshyski.com', 'http://marshyski.com/man-behind-the-keyboard', 'http://marshyski.com/music', 'http://ghostcounty.com/']
    
    # ElasticSearch Settings
    elastic_host : 127.0.0.1
    elastic_port : 9200
    index_name : websites
    index_type : sites

----------

**Example JSON Object:**

       {
          "title": "Marshy Ski",
          "url": "http://marshyski.com/music",
          "body": "Music Stream Demos Update Required To play the media you will need to either update your browser to a recent version or update your . Stream Videos Just emo-shredding on my acoustic. Just singing a little bit for the camera. ** Download Still Frame Past Time's EP When Did This Happen ."
        }

with Phone number (not accurate 100%)

       {
          "title": "Ghost County - The Band",
          "url": "http://ghostcounty.com",
          "body": "Ghost County Ghost County E.P. Available Shows The Ghost County Story Comprised of four lifelong friends, Ghost County is a band of individuals who collectively embody the working class area they come from. Born and bred in Shenandoah, Pa, a small town where humble beginnings are the norm, each member developed a strong passion for music throughout their childhoods and formative years as musicians. After numerous stints with many different bands they decided to join together for a musical project that captures the essence of heavy and often bluesy rock music. The group formed in 2011, vowing to create something genuine and sincere that stems from a place they call their own. Nothing expresses their commitment to this movement better than the release of their first EP in July 2014. This initial offering of songs marks the progression and continuance of Ghost County's ever evolving journey. Their tale is an ongoing one that is purely dedicated to aiding the revival of blues based hard rock music. Truthfully, the story has just begun. Contact Ghost County Feel free to email us about booking, questions, or to just say hello! Johnny Mahmod (Singer) [ × ]Close Josh Metkus (Guitar/Bass) [ × ]Close John Wishnefsky (Drummer) [ × ]Close Justin Metkus (Guitar / Bass) [ × ]Close",
          "phone": "5705900029"
      }
  
----------

**Tested Againsted:**

 - CentOS/RHEL 6.x
 - Mac OS X 13.4.0

----------

**Screenshot**

![Screenshot](https://s3.amazonaws.com/timski-pictures/skeeter-screenshot.png)


**This project was named after my dog, skeeter**

![The Skeeter](https://s3.amazonaws.com/timski-pictures/theskeeter.jpg)
