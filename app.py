import datetime
import requests
from bs4 import BeautifulSoup

YEAR = datetime.datetime.now().year
USERNAME = "capjamesg"

url = f"https://github.com/users/{USERNAME}/contributions?from=2024-01-01"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
contributions = soup.find_all("tool-tip")

dates = {}


def transform_contribution_message(message):
    cleaned_message = (
        " ".join(message.split(" ")[-2:])
        .replace(".", "")
        .rstrip("th")
        .rstrip("st")
        .rstrip("nd")
        .rstrip("rd")
    )
    return datetime.datetime.strptime(f"{cleaned_message} {YEAR}", "%B %d %Y")


for contribution in contributions:
    if "No contributions on" in contribution.text:
        today = transform_contribution_message(
            contribution.text.replace("No contributions on ", "")
        )
        dates[today] = 0
    else:
        split_text = contribution.text.split(" ")
        count = int(split_text[0])
        date = transform_contribution_message(contribution.text)
        dates[date] = count

dates = dict(sorted(dates.items()))
dates = {
    k: v
    for k, v in dates.items()
    if k < datetime.datetime.now()
    and k > datetime.datetime.now() - datetime.timedelta(days=90)
}
url = ",".join([f"{v}" for k, v in dates.items()])

print("https://jamesg.blog/assets/sparkline.svg?" + url)
print(sum(dates.values()), "commits")
