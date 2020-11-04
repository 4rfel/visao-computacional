import os
path = "treated_images"
directory_list = list()
for root, dirs, files in os.walk(path, topdown=False):
    for name in dirs:
        directory_list.append(os.path.join(root, name))

# print(len(directory_list), directory_list)
for i in directory_list:
    # aa = 0
    for root, dirs, files_path in os.walk(i, topdown=False):
        files = files_path
        # print("A")
    print(files)
    # print(size_files)

    
