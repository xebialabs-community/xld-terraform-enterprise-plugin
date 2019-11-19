import os
directory="."
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.txt'):
            print file