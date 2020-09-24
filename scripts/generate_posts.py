import json
import logging
from slugify import slugify
from datetime import datetime

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests_oauthlib").setLevel(logging.WARNING)
logging.getLogger("oauthlib.oauth1.rfc5849").setLevel(logging.WARNING)
logging.getLogger("googleapiclient.discovery").setLevel(logging.ERROR)


j = "./cms_ltc.json"



posts_path = "./content/rates/"
post_template = """---
title: "###TITLE###"
date: ###DATE###
draft: false
type: county
tags: [###TAGS###]
categories: [###CATEGORIES###]
County: ###County###
State: ###State###
FIPS: ###FIPS###
FEMA_Region: ###FEMA_Region###
Population: ###Population###
NCHS_Urban_Rural_Classification: ###NCHS_Urban_Rural_Classification###
Tests_in_prior_14_days: ###Tests_in_prior_14_days###
Fourteen_day_test_rate_per_100000: ###14_day_test_rate_per_100000###
Percent_Positivity_in_prior_14_days: ###Percent_Positivity_in_prior_14_days###
Level: ###LEVEL###
url: ###URL###
---


"""

"""
             {
        "County": "Aleutians East Borough, AK",
        "FIPS": 2013.0,
        "State": "AK",
        "FEMA Region": 10.0,
        "Population": 3337.0,
        "NCHS Urban Rural Classification": "Non-core",
        "Tests in prior 14 days": 132.0,
        "14-day test rate per 100,000": 3956.0,
        "Percent Positivity in prior 14 days": 0.061,
        "Test Positivity Classification - 14 days": "Yellow"
    },
"""

with open(j) as json_file:
    data = json.load(json_file)

for i in data:
    post = post_template
    post = post.replace("###TITLE###", i["County"])
    post = post.replace("###County###", i["County"].split(",")[0])
    post = post.replace("###FIPS###", str(i["FIPS"]))
    post = post.replace("###State###", i["State"])
    post = post.replace("###FEMA_Region###", str(i["FEMA Region"]))
    post = post.replace("###Population###", str(i["Population"]))
    post = post.replace("###NCHS_Urban_Rural_Classification###", i["NCHS Urban Rural Classification"])
    post = post.replace("###Tests_in_prior_14_days###", str(i["Tests in prior 14 days"]))
    post = post.replace("###14_day_test_rate_per_100000###", str(i["14-day test rate per 100,000"]))
    post = post.replace("###Percent_Positivity_in_prior_14_days###", str(i["Percent Positivity in prior 14 days"]))
    post = post.replace("###LEVEL###", i["Test Positivity Classification - 14 days"])
    tags = "FIPS:" + str(i["FIPS"]) +",FEMA:" + str(i["FEMA Region"]) +"," +i["NCHS Urban Rural Classification"] +"," +i["Test Positivity Classification - 14 days"]
    post = post.replace("###TAGS###", tags)
    categories = i["State"]
    post = post.replace("###CATEGORIES###", categories)
    url = "/states/" + i["State"] +"/" + slugify(i["County"].split(",")[0])
    post = post.replace("###TITLE###", i["County"])
    post = post.replace("###URL###", url)
    post = post.replace("###DATE###", datetime.now().strftime("%Y-%m-%d")) 
    post_filename = "./content/counties/" + slugify(i["County"].split(",")[0]) +  ".md" 

    logging.info("Saving post: " + post_filename)
    file = open(post_filename,"w")
    file.write(post)
    file.close()
    