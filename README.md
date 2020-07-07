# Peopertify is Recomendation System to find the best property based on keyword using Cosine Similiarity TF-IDF Method


### Run Appliaction
1. Run mongoDB
2. Run Crawler: 
    - ` $ scrapy crawl dotproperty`
    - ` $ scrapy crawl rumahcom`
3. Run Appliaction
    - ` $ python run.py`


#### If need Scrapy Splash to get/crawl dynamic content web
Run 
- `$ docker run -p 8050:8050 scrapinghub/splash`
