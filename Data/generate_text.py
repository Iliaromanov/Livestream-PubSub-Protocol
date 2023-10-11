import os
for i in range(20):
    with open(f"./Data/Text/text_data_{i}.txt", "w+") as textfile:
        textfile.write(f"--- {i} --- This is sample text {i}\n")
