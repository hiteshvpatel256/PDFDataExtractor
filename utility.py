import os
import constants
import glob
import re
import time
from typing import List
# from PyPDF2 import PdfFileMerger


# returns true if line contains numeric digit
def num_there(line):
    return any(i.isdigit() for i in line)


# find number at perticular location in given line
def find_num(line, location):
    nums_match = re.findall(r'\d+', line)
    if len(nums_match) >= location:
        return nums_match[location-1]
    return


def delete_files(directory):
    files = glob.glob(directory+'*')
    for f in files:
        os.remove(f)


def get_time():
    current_time = time.strftime("%H:%M:%S", time.localtime())
    return current_time


def get_filename_from_path(filepath: str):
    filename = filepath[filepath.rfind(os.path.sep)+1:-4]
    return filename


def remove_empty_lines(lines: List[str]):
    new_lines = []
    for line in lines:
        line = line.replace('\n', '')
        if line.rstrip():
            new_lines.append(line)
    return new_lines


# def remove_permission_error(filename):
#     merger = PdfFileMerger()
#     tmp_filename = 'copyOfOriginal.pdf'
#     file = open(filename, 'rb')
#     merger.append(file)

#     with open(tmp_filename, "wb") as fout:
#         merger.write(fout)

#     file.close()

#     with open(filename, 'wb+') as output, open(tmp_filename, 'rb') as input:
#         output.write(input.read())
