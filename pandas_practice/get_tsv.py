import requests
import os

response = requests.get(
    "https://raw.githubusercontent.com/justmarkham/DAT8/master/data/chipotle.tsv"
)

pwd = os.getcwd()

os.makedirs(f'{os.path.join(pwd, "input_files")}', exist_ok=True)

with open(f'{os.path.join(pwd, "input_files/chipotle.tsv")}', "wb") as f:
    f.write(response.content)
