import csv
import hashlib
import os
import pathlib
import random
import time

from selenium import webdriver

teams = []

current_dir = pathlib.Path(__file__).parent


def fs_sanitize(string):
    hash_ = hashlib.sha256(string.encode('utf-8'))
    return f"{hash_.hexdigest()}.png"


with open(current_dir.joinpath('Analytics data 20180701-20191031.csv')) as fh:
    reader = csv.reader(fh)
    for row in reader:
        if 'team=' not in row[0]:
            continue
        teams.append(row[0])

work_dir = pathlib.Path('/tmp/pokemonvisualdiff')
actual_results = work_dir.joinpath('actual/')
expected_results = work_dir.joinpath('expected/')
diff_dir = work_dir.joinpath('diff/')

for p in [actual_results, expected_results, diff_dir]:
    p.mkdir(parents=True, exist_ok=True)

map_handle = work_dir.joinpath('map.txt').open('w')

manager = {
    "actual": {
        "driver": None,
        "dir": actual_results,
        "base_url": 'http://localhost:4200'
    },
    "expected": {
        "driver": None,
        "dir": expected_results,
        "base_url": 'https://createpokemon.team'
    }
}

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1920,2160')
for run in manager:
    manager[run]["driver"] = webdriver.Chrome(options=chrome_options)

for team in random.sample(teams, 400):
    fs_friendly_url = fs_sanitize(team)
    print(f"Processing {team}; will write {fs_friendly_url}")
    map_handle.write(f"{fs_friendly_url}\t{team}\n")

    for run in manager.values():
        base_url = run["base_url"]
        run["driver"].get(f"{base_url}{team}")
    time.sleep(5)
    for run in manager.values():
        screenshot_path = run["dir"].joinpath(fs_friendly_url)
        run["driver"].save_screenshot(screenshot_path.as_posix())

    command = "compare -compose src {actual} {expected} {diff}".format(
        actual=manager["actual"]["dir"].joinpath(fs_friendly_url).as_posix(),
        expected=manager["expected"]["dir"].joinpath(fs_friendly_url).as_posix(),
        diff=diff_dir.joinpath(fs_friendly_url).as_posix()
    )
    os.system(command)

for run in manager.values():
    run["driver"].quit()

map_handle.close()
