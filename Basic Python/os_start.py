import os
print(os.name)

import time
from os import path
from datetime import datetime

print("Item's path:", path.realpath("textfile.txt"))
print("Item's path and filename: ", path.split(path.realpath("textfile.txt"))) 

#get modification time:
t = time.ctime(path.getmtime("textfile.txt"))
print(t)
print(datetime.fromtimestamp(path.getmtime("textfile.txt")))