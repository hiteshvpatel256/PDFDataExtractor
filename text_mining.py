from voter_data import CommonVoterData, VoterData
import utility
import glob
import constants
import re
from typing import List


def extract_common_detail():

    common_voter_data = CommonVoterData()

    file = open(constants.COMMON_VOTER_DETAIL_TEXTFILE, "r", encoding='utf-8')
    lines = file.readlines()
    file.close()

    lines = utility.remove_empty_lines(lines)

    for line in lines:
        if any(word in line for word in constants.WORDLIST_NAGARPALIKA_NAME) :
            common_voter_data.nagar_parishad_name = line[line.find(':')+1:line.find('मतदाता')]

        elif any(word in line for word in constants.WORDLIST_NAGARPALIKA_BHAG_NO) and 'वार्ड क्रमांक' in line:
            common_voter_data.nagar_parishad_ward_no = utility.find_num(line, 1)
            common_voter_data.nagar_parishad_bhag_no = utility.find_num(line, 2)

        elif any(word in line for word in constants.WORDLIST_NAGARPALIKA_POLLING_BOOTH):
            common_voter_data.polling_booth_details = line[line.rfind(':')+1:]
            common_voter_data.nagar_parishad_ward_name = line[line.find(':')+1:line.find('मतदान')]

        # elif any(word in line for word in constants.WORDLIST_NAGARPALIKA_SUBSECTION):
        #     while 'मूल' not in line:
        #         line=
        #     line = file.readline()
        #     common_voter_data.publication_date = line[2:-1]

    return common_voter_data


def extract_voter_details():
    voter_list = []
    # regex_voter_id = '[_\|\]]'

    # temperory regex
    regex_voter_id = '[_\|\]})!;]'

    # processing voter files and retrieving the information
    list_of_files = glob.glob(constants.VOTER_PNG_PATH+constants.PREFIX_VOTER_TEXTFILE+'*.txt')
    # list_of_files.sort()
    for filepath in list_of_files:
        voter_data = VoterData()

        filename = utility.get_filename_from_path(filepath)
        voter_data.sr_no = filename[filename.rfind('_')+1:]
        voter_data.page_no = filename[filename.find('_')+1:filename.rfind('_')]

        file = open(filepath, "r", encoding='utf-8')
        lines = file.readlines()
        file.close()

        lines = utility.remove_empty_lines(lines)

        for index, line in enumerate(lines):
            if index == 0:
                line = re.sub(regex_voter_id, ' ', line)
                line = line.replace('$', 'S')
                words = line.split()
                if len(words)>2 and words[0]=='5':
                    words[0]='S'
                if len(words)>2 and words[-1].isnumeric() :
                    words[-2]= words[-2]+words[-1]
    
                for index,word in enumerate(words):
                    if len(word) == 1 and word.isalpha() and word != 'A':
                        voter_data.status = word
                    elif len(word) > 1 and not word.isnumeric() and not word.isalpha():
                        voter_data.voter_id = word
                if voter_data.status != '':
                    break
            elif index == 1 and ':' in line:
                voter_data.house_no = line[line.rfind(':')+1:]
            elif index == 2:
                voter_data.voter_name = line[line.rfind(':')+1:]
            elif index == 3:
                voter_data.relative_name = line[line.rfind(':')+1:]
                voter_data.relation = line[:line.find(' ')].replace('कानाम', '')
            elif index == 4:
                voter_data.age = line[line.rfind(':')+1:]
                gender_index = line.find(':')+2
                voter_data.gender = line[gender_index:gender_index+line.find(' ')]
        if voter_data.status == '':
            voter_list.append(voter_data)
    
    # processing newly added voter files and retrieving the information
    list_of_files = glob.glob(constants.VOTER_PNG_PATH+constants.PREFIX_VOTER_TEXTFILE_NEW+'*.txt')
    # list_of_files.sort()

    for filepath in list_of_files:
        voter_data = VoterData()

        voter_data.status = 'N'

        filename = utility.get_filename_from_path(filepath)
        voter_data.sr_no = filename[filename.rfind('_')+1:]
        voter_data.page_no = filename[filename.find('_')+1:filename.rfind('_')]

        file = open(filepath, "r", encoding='utf-8')
        lines = file.readlines()
        file.close()

        lines = utility.remove_empty_lines(lines)

        for index, line in enumerate(lines):
            if index == 0:
                line = re.sub(regex_voter_id, ' ', line)
                line = line.replace('$', 'S')
                words = line.split()
                if len(words)>2 and words[-1].isnumeric():
                    words[-2]= words[-2]+words[-1]

                for word in words:
                    if len(word) > 1 and not word.isnumeric() and not word.isalpha():
                        voter_data.voter_id = word
            elif index == 1 and ':' in line:
                voter_data.house_no = line[line.rfind(':')+1:]
            elif index == 2:
                voter_data.voter_name = line[line.rfind(':')+1:]
            elif index == 3:
                voter_data.relative_name = line[line.rfind(':')+1:]
                voter_data.relation = line[:line.find(' ')].replace('कानाम', '')
            elif index == 4:
                voter_data.age = line[line.rfind(':')+1:]
                gender_index = line.find(':')+2
                voter_data.gender = line[gender_index:gender_index+line.find(' ')]
        voter_list.append(voter_data)

    # processing deleted voter files and retrieving the information
    list_of_files = glob.glob(constants.VOTER_PNG_PATH+constants.PREFIX_VOTER_TEXTFILE_DELETED+'*.txt')
    # list_of_files.sort()

    for filepath in list_of_files:
        voter_data = VoterData()

        filename = utility.get_filename_from_path(filepath)
        voter_data.page_no = filename[filename.find('_')+1:filename.rfind('_')]

        file = open(filepath, "r", encoding='utf-8')
        lines = file.readlines()
        file.close()

        lines = utility.remove_empty_lines(lines)

        for index, line in enumerate(lines):
            if index == 0:
                line = re.sub(regex_voter_id, ' ', line)
                line = line.replace('$', 'S')
                words = line.split()
                if len(words)>2 and words[0]=='5':
                    words[0]='S'
                if len(words)>2 and words[-1].isnumeric() and not words[-2].isnumeric():
                    words[-2]= words[-2]+words[-1]

                for index,word in enumerate(words):
                    if len(word) == 1 and word.isalpha():
                        voter_data.status = word
                    elif index!=len(words)-1 and word.isnumeric() :
                        voter_data.sr_no= word
                    elif len(word) > 1 and not word.isnumeric() and not word.isalpha():
                        voter_data.voter_id = word
            elif index == 1 and ':' in line:
                voter_data.house_no = line[line.rfind(':')+1:]
            elif index == 2:
                voter_data.voter_name = line[line.rfind(':')+1:]
            elif index == 3:
                voter_data.relative_name = line[line.rfind(':')+1:]
                voter_data.relation = line[:line.find(' ')].replace('कानाम', '')
            elif index == 4:
                voter_data.age = line[line.rfind(':')+1:]
                gender_index = line.find(':')+2
                voter_data.gender = line[gender_index:gender_index+line.find(' ')]
        voter_list.append(voter_data)

    # sorting voterlist on the basis of serial number
    voter_list.sort(key=lambda x: int(x.sr_no))

    # unique voter list by removing duplicate sr_no in list of voters
    unique_voter_list = {voter.sr_no: voter for voter in voter_list}.values()

    # solving 0 to O problem in voter_id
    for voter in unique_voter_list:
        if voter.voter_id=='' or  '/' in voter.voter_id  :
            continue
        
        match = re.search('O[0-9]', voter.voter_id)
        if len(voter.voter_id)==10 and match is not None:
            voter.voter_id = voter.voter_id.replace(match.group(0), match.group(0).replace('O', '0'))
        
        if len(voter.voter_id)==11 :
            voter.voter_id = voter.voter_id.replace('0O', '0').replace('O0','0').replace('SS','S')    



    # for index, voter in enumerate(voter_list):
    #     print(voter.sr_no)
        # if index < len(voter_list)-1 and voter.sr_no == voter_list[index+1].sr_no:
        #     print(voter.sr_no)
    
    
    return unique_voter_list
