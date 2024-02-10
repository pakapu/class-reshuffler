#/bin/python3

# Helps the user update the labels for YOLO when the classes are all janky,
# such as when using labelImg incorrectly
#
# * lets the user choose how to modify the classes
# * Puts modified files in another directory

from glob import glob
from os import path, mkdir
from sys import exit

print("The Program will search for txt files up to 1 subdirectory in depth!\n")
label_path = input("Please enter the path to the labels directory: ")

if not path.exists(label_path):
    print("ERROR: The path you entered does not exist!")
    exit(1)

files = glob(label_path + "/*.txt") + glob(label_path + "/*/*.txt")
class_map = dict()

print(f"Found {len(files)} files!")

for current_file_path in files:
    f = open(current_file_path, "r")

    current_dir = path.dirname(current_file_path)
    save_dir = current_dir + "/modified/"

    #print(f"Reading file {current_file_path}")
    #print(f"In directory {current_dir}")

    if not path.exists(save_dir):
        mkdir(save_dir)

    save_file_path = save_dir + path.basename(current_file_path)
    #print(f"Writing to file {save_file_path}")
    sf = open(save_file_path, "w")

    for line in f.readlines():
        nums = line.split()
        if len(nums) != 5:
            print(f"ERROR: Wrong amount of numbers on line in file {current_file_path}")
            print(f"Expected 5, found {len(nums)}")
            exit(1)

        #print(f"Read {len(nums)} numbers: {nums}")

        curr_class = int(nums[0])
        #print(f"Found class {curr_class}!")
        if curr_class not in class_map.keys():
            print(f"Class {curr_class} does not have a replacement class!")
            replacement_class = int(input("Enter a replacement class: "))
            class_map[curr_class] = replacement_class

        sf.write(f"{class_map[curr_class]} ")
        for i in nums[1:-1]:
            sf.write(f"{i} ")
        sf.write(f'{nums[-1]}\n')

    sf.close()
    f.close()
