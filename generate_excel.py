import xlsxwriter
from voter_data import CommonVoterData, VoterData
from typing import List


def createExcelForPanchayat(path, common_voter_data: CommonVoterData, voter_list: List[VoterData]):
    workbook = xlsxwriter.Workbook(path[0:-4]+".xlsx")
    worksheet = workbook.add_worksheet()
    titles = ['PAGE NO', 'SR NO', 'VOTER NAME', 'RELATIVE NAME', 'RELATION', 'VOTER ID', 'HOUSE NO', 'AGE', 'GENDER', 'SUB SECTION',  'JILAPARISHAD NAME', 'JILAPARISHAD WARD NO', 'PANCHAYAT SAMITI NAME', 'PANCHAYAT SAMITI WARD NO', 'GRAM PANCHAYAT', 'GRAM PANCHAYAT WARD NO', 'POLLING BOOTH DETAILS', 'VIDHANSABHA NO', 'VIDHANSABHA NAME', 'VILLAGE', 'SUBDISTRICT', 'DISTRICT', 'PUBLICATION DATE', 'STATUS', 'ERROR']

    cell_format = workbook.add_format({'bold': True})
    column = 0
    for item in titles:
        worksheet.write(0, column, item, cell_format)
        column += 1

    row = 1
    for voter in voter_list:
        # print(voter.sr_no)
        worksheet.write(row, 0, voter.page_no)
        worksheet.write(row, 1, voter.sr_no)
        worksheet.write(row, 2, voter.voter_name)
        worksheet.write(row, 3, voter.relative_name)
        worksheet.write(row, 4, voter.relation)
        worksheet.write(row, 5, voter.voter_id)
        worksheet.write(row, 6, voter.house_no)
        worksheet.write(row, 7, voter.age)
        worksheet.write(row, 8, voter.gender)
        worksheet.write(row, 9, voter.sub_section)
        worksheet.write(row, 10, common_voter_data.jila_parishad_name)
        worksheet.write(row, 11, common_voter_data.jila_parishad_ward_no)
        worksheet.write(row, 12, common_voter_data.panchayat_samiti_name)
        worksheet.write(row, 13, common_voter_data.panchayat_samiti_ward_no)
        worksheet.write(row, 14, common_voter_data.gram_panchayat)
        worksheet.write(row, 15, common_voter_data.gram_panchayat_ward_no)
        worksheet.write(row, 16, common_voter_data.polling_booth_details)
        worksheet.write(row, 17, common_voter_data.vidhansabha_no)
        worksheet.write(row, 18, common_voter_data.vidhansabha_name)
        worksheet.write(row, 19, common_voter_data.village)
        worksheet.write(row, 20, common_voter_data.sub_district)
        worksheet.write(row, 21, common_voter_data.district)
        worksheet.write(row, 22, common_voter_data.publication_date)
        worksheet.write(row, 23, voter.status)
        worksheet.write(row, 24, voter.error)
        row += 1
    workbook.close()
    return workbook.filename


def createExcelForNagarParishad(path, common_voter_data: CommonVoterData, voter_list: List[VoterData]):
    workbook = xlsxwriter.Workbook(path[0:-4]+".xlsx")
    worksheet = workbook.add_worksheet()
    titles = ['PAGE NO', 'SR NO', 'VOTER NAME', 'RELATIVE NAME', 'RELATION', 'VOTER ID', 'HOUSE NO', 'AGE', 'GENDER', 'SUB SECTION',    'NAGARPARISHAD NAME', 'NAGARPARISHAD WARD NO', 'NAGARPARISHAD WARD NAME', 'NAGARPARISHAD BHAG NO', 'POLLING BOOTH DETAILS', 'STATUS', 'ERROR']

    cell_format = workbook.add_format({'bold': True})
    column = 0
    for item in titles:
        worksheet.write(0, column, item, cell_format)
        column += 1

    row = 1
    for voter in voter_list:
        # print(voter.sr_no)
        worksheet.write(row, 0, voter.page_no)
        worksheet.write(row, 1, voter.sr_no)
        worksheet.write(row, 2, voter.voter_name)
        worksheet.write(row, 3, voter.relative_name)
        worksheet.write(row, 4, voter.relation)
        worksheet.write(row, 5, voter.voter_id)
        worksheet.write(row, 6, voter.house_no)
        worksheet.write(row, 7, voter.age)
        worksheet.write(row, 8, voter.gender)
        worksheet.write(row, 9, voter.sub_section)
        worksheet.write(row, 10, common_voter_data.nagar_parishad_name)
        worksheet.write(row, 11, common_voter_data.nagar_parishad_ward_no)
        worksheet.write(row, 12, common_voter_data.nagar_parishad_ward_name)
        worksheet.write(row, 13, common_voter_data.nagar_parishad_bhag_no)

        worksheet.write(row, 14, common_voter_data.polling_booth_details)
        worksheet.write(row, 15, voter.status)
        worksheet.write(row, 16, voter.error)
        row += 1

    workbook.close()
    return workbook.filename
