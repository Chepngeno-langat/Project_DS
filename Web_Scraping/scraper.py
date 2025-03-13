import requests
from bs4 import BeautifulSoup

# Retrieve html
URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

# find elements by id
results = soup.find(id="ResultsContainer")
# print(results.prettify())

# find elements by class name
job_cards = results.find_all("div", class_="card-content")
    
# Find only specific jobs
python_jobs = results.find_all(
    "h2", string=lambda text: "python" in text.lower()
    )
# print(len(python_jobs))
    
# parent elements
python_job_cards = [
    h2_element.parent.parent.parent for h2_element in python_jobs
]
print(python_job_cards)

for job_card in python_job_cards:
    title_element = job_card.find("h2", class_="title")
    company_element = job_card.find("h3", class_="company")
    location_element = job_card.find("p", class_="location")
    link_url = job_card.find_all("a")[1]["href"]
    print(title_element.text.strip())
    print(company_element.text.strip())
    print(location_element.text.strip())
    print(f"Apply here: {link_url}\n")
    print("----------------")
    print()


