#create a file : 

#sample_file = open("textfile.txt", "w+")
#sample_file.write("This is some sample text in our sample file.")
#sample_file.close()


#add more text in file :
sample_file = open("textfile.txt", "a+")

sample_file.write("This is more some sample text in our sample file.")
sample_file.write("This is even more some sample text in our sample file.")

sample_file.close()
