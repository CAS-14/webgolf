import os,sqlite3,shutil
if not os.path.isdir("i"):os.mkdir("i")
p="i/m.db"
if not os.path.exists(p):
    with open("m.sql","r")as f:i=f.read()
    with sqlite3.connect(p)as d:c=d.cursor();c.executescript(i);d.commit()
else:shutil.copyfile(p,p+".bak")