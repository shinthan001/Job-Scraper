# Job-Scraper
This project is to scrape job information of any desired position/location using scrapy and selenium. I implemented 2 simple spiders to crawl JobStreet and Careers.gov.sg.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Example Dataset](#example-datset)
- [Exploratory Data Analysis](#exploratory-data-analysis)
- [Future Project](#future-project)

## Installation
1. Clone the repository:
```bash
 git clone https://github.com/shinthan001/Job-Scraper/tree/main
```

2. Install dependencies:
```bash
 pip install requirements.txt
 ```

3. Download WebDriver and save it in a directory. [Google WebDriver](https://googlechromelabs.github.io/chrome-for-testing/) 

4. Optional: Download and setup [MongoDB](https://www.mongodb.com/try/download/shell).

## Usage

1. In `./job_scraper/job_scraper/spiders/settings.py`, please modify your webdriver path, desired keywords and location accordingly. Add proxy settings if needed.

2. If you have set up MongoDB on your local host, please modify server, port, db and collection name.

    <img src='./img/img_1.png' width='50%' height='50%'>
<br />

3. Change directory to `./job_scraper/job_scraper/spiders/` and run spiders.
```bash
 scrapy runspider jobStreet.py #jobportal: https://www.jobstreet.com/
```
```bash
 scrapy runspider careersGov.py #jobportal: https://www.careers.gov.sg/
```

4. If you are not using MongoDB, run spider using following command to save output data.
```bash
 scrapy runspider jobStreet.py -O yourfile:format
```

## Example Datset
- Example dataset can be found [here](https://www.kaggle.com/datasets/shinthan001/scraped-jobs). The data was scraped based on `KEYWORDS=Data Scientist` and 
`LOCATION=Singapore`.

## Exploratory Data Analysis

- Basic EDA of aforementioned dataset can be viewed here [./Basic EDA.ipynb](Basic%20EDA.ipynb). 

    <img src='./img/img_2.png' width='50%' height='50%'>
    <br />

## Future Project
- With the use of proper datasets, I'm working on Named Entity Recognition (NER) to extract skills described in job descriptions.
