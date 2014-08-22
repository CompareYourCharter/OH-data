import xlrd
import csv

xls_path	= "./charter-sheets/"
csv_path	= "../charter-csv/"
districts	= {}
charters	= {}

filename	= 'District to Charter Transfer by Performance Data'
xls_file	= xls_path + 'RAW' + ' ' + filename + '.xlsx'
csv_file	= csv_path + filename + '.csv'
workbook	= xlrd.open_workbook(xls_file)
write_file	= open(csv_file, 'wb')
wr 		= csv.writer(write_file, quoting=csv.QUOTE_ALL)

worksheet = workbook.sheet_by_name('Sheet1')

num_rows 					= worksheet.nrows - 1
num_cells 					= worksheet.ncols - 1
curr_row 					= 0
header_row					= True
headers						= []

for n in range(num_rows):
	headers[n]				= ""

while curr_row < num_rows:
	curr_row += 1
	if curr_row = 5:
		header_row 			= False
		wr.writerow(headers)
	if header_row:
		curr_cell			= -1
		while curr_cell < num_cells:
			curr_cell 		+= 1
			cell_value 		= worksheet.cell_value(curr_row, curr_cell)
			if len(cell_value) > 0:
				headers[curr_cell] += " "
				headers[curr_cell] += cell_value
	else:
		wr.writerow(worksheet.row(curr_row))
		district_IRN			= str(worksheet.cell_value(curr_row, 0))
		school_IRN			= str(worksheet.cell_value(curr_row, 22))
		transfer			= worksheet.cell_value(curr_row, 59)
		district_IRN			= district_IRN.fill(5)
		school_IRN			= school_IRN.fill(6)

		for i in range
		if district_IRN in districts:
			districts[district_IRN] += transfer
		else:
			districts[district_IRN]	= transfer
		if school_IRN in charters:
			charters[school_IRN]	+= transfer
		else:
			charters[school_IRN]	= transfer

write_file.close()
