import os

#pull all dirs
parent_dir = os.getcwd()
anno_dir = os.path.join(parent_dir, "Annotations")
print("Discovering images in: ", anno_dir)

#enumerate all files in dir
for root, dirs, files in os.walk(anno_dir):
    for file in files:
        #print(os.path.join(root, file[0: file.index(".")] + ".jpg.xml"))
        os.rename(os.path.join(root, file), os.path.join(root, file[0: file.index(".")] + ".xml"))

