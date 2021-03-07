import os
import random

#pull all dirs
parent_dir = os.getcwd()
img_dir = os.path.join(parent_dir, "JPEGImages")
sets_dir = os.path.join(parent_dir, "ImageSets", "Main")
print("Discovering images in: ", img_dir)

#enumerate all files in dir
files_list = []
for root, dirs, files in os.walk(img_dir):
    for file in files:
        files_list.append(file)

#create size and holdback size
size = len(files_list)
test_hold = int(size * 0.1)

print("Using a test holdback of {0} images out of {1}".format(test_hold, size))

#remove file extension
files_list = [file[0: file.index(".")] for file in files_list]

#create image data sets
test = random.choices(files_list, k=test_hold)
train = [file for file in files_list if not (file in test)]
val = test

# write the data sets to the files
with open(os.path.join(sets_dir, "train.txt"), mode='wt', encoding='utf-8') as my_file:
    for elem in train:
        my_file.write(elem)
        my_file.write('\n')
    my_file.flush()
    my_file.close()

with open(os.path.join(sets_dir, "test.txt"), mode='wt', encoding='utf-8') as my_file:
    for elem in test:
        my_file.write(elem)
        my_file.write('\n')
    my_file.flush()
    my_file.close()

with open(os.path.join(sets_dir, "val.txt"), mode='wt', encoding='utf-8') as my_file:
    for elem in val:
        my_file.write(elem)
        my_file.write('\n')
    my_file.flush()
    my_file.close()

with open(os.path.join(sets_dir, "trainval.txt"), mode='wt', encoding='utf-8') as my_file:
    for elem in train:
        my_file.write(elem)
        my_file.write('\n')
    my_file.flush()
    my_file.close()



