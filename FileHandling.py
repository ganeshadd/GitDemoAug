#Open file
# Relative Path:Knowledge\input.txt 
# Absolute Path: C:\Users\ganes\AugDemo\input.txt
file =open("Knowledge\\input.txt","a+")

file.write("hello Ganesh!\n")
file.write("Welcome to file handling in python")

# Close the connectin/file 
file.close()

#Read operation
file =open("Knowledge\\input.txt","r")

# Store content in a variable 
content = file.read()

# Close the connectin/file 
file.close()

#print content
print(content)