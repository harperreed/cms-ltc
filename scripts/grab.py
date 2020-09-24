from openpyxl import load_workbook
import zipfile
from excel2json import convert_from_file
import os
import requests



zip_file = "./Test_Positivity_Rates.zip"

bigxlsx_filename = './Test_Positivity_Rates.xlsx'
smallxlsx_filename = "./simpler.xlsx"

tab = 'cms_ltc'
tablename = 'rates'


data_url = "https://data.cms.gov/download/hsg2-yqzz/application%2Fzip"


r = requests.get(data_url, stream=True)
with open(zip_file, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)


with zipfile.ZipFile(zip_file,"r") as zip_ref:
    zip_ref.extractall("./")

wb = load_workbook(filename = bigxlsx_filename)
ws = wb[tab]
ws.delete_rows(1, 6)
wb.save(smallxlsx_filename)


convert_from_file(smallxlsx_filename, "./")

os.remove(smallxlsx_filename)

os.remove(zip_file)
