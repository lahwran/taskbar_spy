import re
import json
import time
from datetime import datetime
import pyvda


import requests

print("starting")
def trigger_reload():

    filename = "c:/Users/Lauren/AppData/Local/caster/rules/taskbar.py"
    with open(filename,"r") as r:
        content = r.read()
    output = re.sub("# lastupdate: .*", f"# lastupdate: {datetime.now()}", content)
    try:
        with open(filename,"w") as w:
            w.write(output)
    except:
        with open(filename, "w") as w:
            w.write(output)
        raise

i = 0
while True:
    if i > 0:
        time.sleep(30)
    i += 1
    print(f"{datetime.now()}: starting update, getting desktop ")
    desktopnumber = pyvda.GetCurrentDesktopNumber()
    print(f"{datetime.now()}: current desktop: {desktopnumber}")
    try:
        with open("lastdesktop", "r") as r:
            lastdesktop = r.read()
    except FileNotFoundError:
        lastdesktop = None
    with open("lastdesktop", "w") as w:
        w.write(str(desktopnumber))
    if lastdesktop != str(desktopnumber):
        print(f"{datetime.now()}: desktop changed, triggering reload early")
        trigger_reload()
    results = requests.get("http://localhost:9559/overview").json()
    print(f"{datetime.now()}: got results")

    contextfile = f"c:/Users/Lauren/AppData/Local/caster/rules/context_{desktopnumber}.json"
    try:
        with open(contextfile,"r") as r:
            oldformatted = r.read()
        oldresults = json.loads(oldformatted)
    except (FileNotFoundError, json.JSONDecodeError):
        oldresults = None
    formatted = json.dumps(results, indent=4)
    with open(contextfile, "w") as w:
        w.write(formatted)
        print(f"{datetime.now()}: saved context file")
    if results == oldresults:
        print(f"{datetime.now()}: no change not triggering reload")
        continue


    if any(("\\rules\\taskbar.py [caster]" in x["name"]) for x in results["taskbar"]):
        print(f"{datetime.now()}: caster project focused, not triggering reload")
        continue
    trigger_reload()
    print(f"{datetime.now()}: update done ")

