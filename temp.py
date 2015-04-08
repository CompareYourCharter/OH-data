filename  = 'District to Charter Transfer by Performance Data'
xls_file  = xls_path + 'RAW ' + filename + '.xlsx'
workbook  = xlrd.open_workbook(xls_file)

worksheet   = workbook.sheet_by_name('COMMUNITY_SCHOOL_DEDUCTION_FY14')

# One row per district per charter supported

csv_file  = csv_path + filename + '.csv'
write_file  = open(csv_file, 'w')
wr    = csv.writer(write_file, quoting=csv.QUOTE_ALL)

csv_file2 = web_path + 'Transfer Data.csv'
write_file2 = open(csv_file2, 'w')
wr2     = csv.writer(write_file2, quoting=csv.QUOTE_ALL)

num_rows          = worksheet.nrows - 1
num_cells           = worksheet.ncols - 1
header_row          = True
headers           = ['']

web_headers = ['District IRN', 'District Name', 'School IRN', 'School Name', 'Transfer']
wr2.writerow(web_headers)

curr_row          = 6
while curr_row < num_rows:
  curr_row += 1
  school_IRN = worksheet.cell_value(curr_row, 2)
  district_IRN = worksheet.cell_value(curr_row, 0)
  school_IRN = fixIRN(school_IRN)
  district_IRN = fixIRN(district_IRN)
  if school_IRN not in charters:
    charters[school_IRN]    = {}
  if district_IRN not in districts:
    districts[district_IRN]   = {}

  charter_ids.append(school_IRN)

curr_row          = 0

while curr_row < num_rows:
  curr_row        += 1
  if curr_row == 7:
    header_row      = False
    for each in headers:
      each      = clean(each)
    wr.writerow(headers)
    new_headers     = []
    for each in headers:
      each      = filename + ' - ' + each
      each      = clean(each)
      new_headers.append(each)
    headers       = new_headers 
  if header_row:
    curr_cell     = -1
    while curr_cell < num_cells:
      curr_cell     += 1
      cell_value    = worksheet.cell_value(curr_row, curr_cell)
      if len(headers) > curr_cell:
        headers.append(cell_value)
      else:
        headers[curr_cell - 1] += " "
        headers[curr_cell - 1] = cell_value
  else:
    row       = worksheet.row_values(curr_row)
    wr.writerow(row)

    district_IRN        = row[0]
    district_Name       = row[1]
    school_IRN          = row[2]
    school_Name         = row[3]
    transfer            = row[13]
    district_IRN        = fixIRN(district_IRN)
    school_IRN          = fixIRN(school_IRN)
    ADMtransfer         = row[52]

    str_transfer      = '%.2f' % transfer

    short_row = [district_IRN, district_Name, school_IRN, school_Name, str_transfer]
    wr2.writerow(short_row)

    if 'Charter Transfer' in districts[district_IRN]:
      districts[district_IRN]['Charter Transfer']   += transfer
    else:
      districts[district_IRN]['Charter Transfer'] = transfer

    if 'Public Funding' in charters[school_IRN]:
      charters[school_IRN]['Public Funding']    += transfer
    else:
      charters[school_IRN]['Public Funding']    = transfer

    if 'ADM' in charters[school_IRN]:
      charters[school_IRN]['ADM']     += ADMtransfer
    else:
      charters[school_IRN]['ADM']     = ADMtransfer

for charter in charters:
  if 'Public Funding' in charters[charter]:
    charters[charter]['Public Funding']     = \
      '%.2f' % charters[charter]['Public Funding']

for district in districts:
  if 'Charter Transfer' in districts[district]:
    districts[district]['Charter Transfer']     = \
      '%.2f' % districts[district]['Charter Transfer']

write_file.close()
write_file2.close()