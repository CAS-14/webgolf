import os
import json
import time

import tools

oldcwd = os.getcwd()

def get(key):
    try:
        with open(tools.inst("config.json"), "r") as f:
            return json.load(f)[key]
    except FileNotFoundError:
        os.system("python3 setup.py")

def main():
    quick_restarts = 0
    last_restart = None

    os.system("python3 -m pip install -r requirements.txt")

    while True:
        tools.log("Starting server...")

        if get("pull_on_run"): os.system("git pull")
        if get("setup_check"): os.system("python3 setup.py")
        # if get("dl_signout"):
        #     os.chdir("..")


        # if os.path.isfile("quickfix.py"):
        #     tools.log("File quickfix.py found! Running it...")
        #     os.system("python3 quickfix.py")
        #     tools.log("Removing quickfix.py")

        #     now = time.time()

        #     # NOT FINISHED

        os.system("authbind python3 -m gunicorn -c serverconfig.py app:app")

        os.system("pkill -f gunicorn")
        tools.log("Server has stopped.")

        if not get("auto_restart"): 
            tools.log("Goodbye!")
            break

        if quick_restarts > 3:
            tools.log("I think the server is stuck in a bootloop. Shutting down.")
            break

        tools.log(f"Restarting... Press Ctrl+C now to stop")

        now = time.time()

        if last_restart and now - last_restart < 30:
            quick_restarts += 1
        
        last_restart = now

        time.sleep(2)

if __name__ == "__main__":
    main()