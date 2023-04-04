import os
import random
import json
import sqlite3
import shutil

import tools

def exists(*targets):
    return os.path.exists(tools.inst(*targets))

print("-" * 20)
print("Setting up (this is setup.py)...")

# GENERAL SETUP: Instance directory and global config file

print("[SETUP 1/3] Checking general files...")

if not os.path.isdir("instance"):
    os.mkdir("instance")
    print("Instance directory was created")

if not exists("id.txt"):
    with open(tools.util("corncob_lowercase.txt")) as f:
        words = f.read().splitlines()
    instance_words = []
    for i in range(3):
        instance_words.append(random.choice(words))
    INSTANCE_ID = " ".join(instance_words)
    with open(tools.inst("id.txt"), "w") as f:
        f.write(INSTANCE_ID)
    print("Instance ID was generated")

if not exists("config.json"):
    default_config = {
        "pull_on_run": True,
        "setup_check": True,
        "auto_restart": True
    }

    with open(tools.inst("config.json"), "w") as f:
        json.dump(default_config, f, indent=4)

    print("Global config file was created")

# DATABASE SETUP: Generic database setup for each .db and .sql

print("[SETUP 2/3] Checking databases...")

for db in ["muchan", "main", "arwiki", "securechat", "hell", "signout"]:
    db_file = f"{db}.db"
    
    if not exists(db_file):
        print(f"Setting up {db_file}...")

        with open(tools.util(f"{db}.sql"), "r") as f:
            init_script = f.read()

        con = sqlite3.connect(tools.inst(db_file))
        cur = con.cursor()
        cur.executescript(init_script)
        con.commit()
        con.close()

        print("Done!")

    else:
        print(f"{db_file} already exists, making backup instead")
        shutil.copyfile(tools.inst(db_file), f"{tools.inst(db_file)}.bak")
        print("made!")

# SPECIFIC SETUP: Initialize configs

print("[SETUP 3/3] Doing the specifics...")

if not exists("uploads"):
    os.mkdir(tools.inst("uploads"))

# for now, no muchan

# if not exists("muchan.json"):
#     muchan_data = {
#         "latest_post_id": 0,        # latest integer post ID, deleted or not
#         "total_posts_made": 0,      # total post count, deleted or not
#         "admin_pass": "admin51",    # admin password, secure this later lolz
#         "thread_posts": [],         # top-level int post IDs in order
#     }

#     with open(tools.inst("muchan.json"), "w") as f:
#         json.dump(muchan_data, f, indent=4)

#     print("Initialized muchan!")

if not exists("clicker.json"):
    clicker_data = {
        "clicks": 0
    }

    with open(tools.inst("clicker.json"), "w") as f:
        json.dump(clicker_data, f, indent=4)

    print("Created clicker.json")

print("The setup.py has finished!")
print("-" * 20)