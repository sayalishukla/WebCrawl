# Web Crawl Application

 

## Design
- Take list URL form File for May 2020
- If contents in url have keywords 
    - covid19 or covid-19 coronavirus or Covid19 or Covid-19 or Coronavirus or COVID19
- Then search for keywords
    - economics or finance or business or Economics or Finance or Business or stockmarket or stock or wall street or economic or economy
- Add url which have both of above keywords in result
- When count of result is 1000 then stop

## How To
- Install library dependency
```commandline
python3 venv venv
source venv/bin/activate
pip install -r requirments.txt
```
- To run the project
```commandline
python crwl.py
```
- The results will be printed to console as a list. To save results to file, run as follows
```commandline
python crwl.py > results.txt
```
