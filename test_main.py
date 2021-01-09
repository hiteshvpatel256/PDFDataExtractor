import generate_images
import ocr
import text_mining
import generate_excel
import os
import glob
import utility
import constants

print('started'+utility.get_time())
filepath = '/home/hitesh/Downloads/MP_Sample_PDf/47NN113.pdf'

utility.delete_files(constants.VOTER_PNG_PATH)
utility.delete_files(constants.PAGE_PNG_PATH)

generate_images.pdf_to_png(filepath)

ocr.generate_text()
print('completed' + utility.get_time())

common_voter_data = text_mining.extract_common_detail()
voter_list = text_mining.extract_voter_details()

excel_name = generate_excel.createExcelForNagarParishad(filepath, common_voter_data, voter_list)
