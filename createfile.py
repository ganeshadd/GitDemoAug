import os

os.makedirs("Knowledge2", exist_ok=True)

file_path ="Knowledge2/newfile.txt"

with open(file_path,"x") as file:
    file.write("Hello Ganesh!")

with open(file_path,"r") as file:
    content = file.read()
    print(content)

