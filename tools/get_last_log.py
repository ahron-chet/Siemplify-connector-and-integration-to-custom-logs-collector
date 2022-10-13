import sqlite3
import json
import ast
path = input("please enter path to database: ")
c = sqlite3.connect(path)
curr = c.cursor()
curr.execute("select log,Time from cases")
data = [curr.fetchall()[-1]]
j = ast.literal_eval(data[0][0])
for i in j.keys():
    print(f"{i:<30}{str(j[i]):>40}")

print(f"{'time recived ':<30}{data[-1][-1]:>40}")