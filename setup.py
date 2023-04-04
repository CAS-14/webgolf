p="i/m.db";import os,sqlite3 as s,shutil as u
if not os.path.isdir("i"):os.mkdir("i")
if not os.path.exists(p):
    with open("m.sql","r")as f:i=f.read()
    with s.connect(p)as d:c=d.cursor();c.executescript(i);d.commit()
else:u.copyfile(p,p+".bak")