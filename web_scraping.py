import requests
from bs4 import BeautifulSoup


class Scraping_web:

    def __init__(self, type):
        self.job_data = {}
        self.cnt = 0
        if type == "engineering":
            url = f"https://berlinstartupjobs.com/{type}"
            self.engineering(url)
        else:
            url = f"https://berlinstartupjobs.com/skill-areas/{type}"
            self.scraping(url, type)

    def scraping(self, url, type):
        response = requests.get(url, headers={
                                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"})
        soup = BeautifulSoup(response.content, "html.parser")
        jobs = soup.find(
            "ul", class_="jobs-list-items").find_all("li", class_="bjs-jlid")
        for job in jobs:
            link = job.find("h4", class_="bjs-jlid__h").find("a")
            company_name = job.find("a", class_="bjs-jlid__b").text
            detail = job.find("div", class_="bjs-jlid__description").text
            self.job_data[f"{type}{self.cnt}"] = [
                company_name, link.text, link["href"], detail.strip()]
            self.cnt += 1

    def engineering(self, url):
        response = requests.get(url, headers={
                                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"})
        soup = BeautifulSoup(response.content, "html.parser")
        botton = len(
            soup.find("ul", class_="bsj-nav").find_all(class_="page-numbers")[:-1])
        for num in range(botton):
            temp_url = f"{url}/page/{num + 1}"
            self.scraping(temp_url, "engineering")


def print_job(type, object):
    count = len(object.job_data)
    for cnt in range(count):
        company_name, title, link, detail = object.job_data[f"{type}{cnt}"]
        print("===================================================================================================")
        print("company_name : ", company_name)
        print("title : ", title)
        print("link : ", link)
        print("detail : ", detail)
        print("===================================================================================================")


skills = [
    "python",
    "typescript",
    "javascript",
    "rust"
]

print("********************Engineering*********************")
engineering = Scraping_web("engineering")
print_job("engineering", engineering)
print("\n")

for skill in skills:
    print(f"********************{skill}*********************")
    object = Scraping_web(skill)
    print_job(skill, object)
    print("\n")
