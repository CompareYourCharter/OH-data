import xlrd
import csv
import sys

xls_path	= "./charter-sheets/"
csv_path	= "./charter-csv/"
web_path	= "./charter-web/"
districts	= {}
charters	= {}

def clean(value):
	if type(value) is float:
		value		= '%.0f' % value
	if type(value) is unicode:
		value		= str(value)				
	if type(value) is str:
		" ".join(value.split())
		value		= value.lstrip()
		value		= value.rstrip()
	return value

def fixIRN(value):
	if type(value) is float:
		value		= '%.0f' % value
	value			= str(value)
	value			= value.zfill(6)
	return value

def pull(dictionary, key):
	if key not in dictionary:
		return 'NA'
	else:
		try:
			if dictionary[key] in ('--', 'NR'):
				return 'NA'
			else:
				return dictionary[key]
		except:
			return 'NA'

def point_to_grade(value):
	if value < 0 or value > 4.0:
		return '--'
	else:
		if value > 3.7:
			return 'A'
		elif value > 3.3:
			return 'A-'
		elif value > 3.0:
			return 'B+'
		elif value > 2.7:
			return 'B'
		elif value > 2.3:
			return 'B-'
		elif value > 2.0:
			return 'C+'
		elif value > 1.7:
			return 'C'
		elif value > 1.3:
			return 'C-'
		elif value > 1.0:
			return 'D+'
		elif value > 0.7:
			return 'D'
		elif value > 0.3:
			return 'D-'
		else:
			return 'F'		

grade_dict					= {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0}

######### SHEETS WITH BOTH CHARTER AND DISTRICT DATA ########

# District to Charter Transfer by Performance Data

filename	= 'District to Charter Transfer by Performance Data'
xls_file	= xls_path + 'RAW' + ' ' + filename + '.xlsx'
workbook	= xlrd.open_workbook(xls_file)

worksheet 	= workbook.sheet_by_name('Sheet1')

# One row per district per charter supported

csv_file	= csv_path + filename + '.csv'
write_file	= open(csv_file, 'w')
wr 		= csv.writer(write_file, quoting=csv.QUOTE_ALL)

csv_file2	= web_path + 'Transfer Data.csv'
write_file2	= open(csv_file2, 'w')
wr2 		= csv.writer(write_file2, quoting=csv.QUOTE_ALL)

num_rows 					= worksheet.nrows - 1
num_cells 					= worksheet.ncols - 1
header_row					= True
headers						= ['']

web_headers	= ['District IRN', 'District Name', 'School IRN', 'School Name', 'Transfer']
wr2.writerow(web_headers)

curr_row 					= 5
while curr_row < num_rows:
	curr_row 				+= 1
	school_IRN				= worksheet.cell_value(curr_row, 22)
	district_IRN				= worksheet.cell_value(curr_row, 0)
	school_IRN				= fixIRN(school_IRN)
	district_IRN				= fixIRN(district_IRN)
	if school_IRN not in charters:
		charters[school_IRN]		= {}
	if district_IRN not in districts:
		districts[district_IRN]		= {}

curr_row					= 0

while curr_row < num_rows:
	curr_row 				+= 1
	if curr_row == 6:
		header_row 			= False
		for each in headers:
			each 			= clean(each)
		wr.writerow(headers)
		new_headers			= []
		for each in headers:
			each			= filename + ' - ' + each
			each 			= clean(each)
			new_headers.append(each)
		headers				= new_headers	
	if header_row:
		curr_cell			= -1
		while curr_cell < num_cells:
			curr_cell 		+= 1
			cell_value 		= worksheet.cell_value(curr_row, curr_cell)
			if len(headers) > curr_cell:
				headers.append(cell_value)
			else:
				headers[curr_cell - 1] += " "
				headers[curr_cell - 1] = cell_value
	else:
		row				= worksheet.row_values(curr_row)
		wr.writerow(row)

		district_IRN			= worksheet.cell_value(curr_row, 0)
		district_Name			= worksheet.cell_value(curr_row, 1)
		school_IRN			= worksheet.cell_value(curr_row, 22)
		school_Name			= worksheet.cell_value(curr_row, 23)
		transfer			= worksheet.cell_value(curr_row, 59)
		district_IRN			= fixIRN(district_IRN)
		school_IRN			= fixIRN(school_IRN)

		str_transfer			= '%.2f' % transfer

		short_row	= [district_IRN, district_Name, school_IRN, school_Name, str_transfer]
		wr2.writerow(short_row)

		if 'Charter Transfer' in districts[district_IRN]:
			districts[district_IRN]['Charter Transfer'] 	+= transfer
		else:
			districts[district_IRN]['Charter Transfer']	= transfer

		if 'Public Funding' in charters[school_IRN]:
			charters[school_IRN]['Public Funding']		+= transfer
		else:
			charters[school_IRN]['Public Funding']		= transfer

for charter in charters:
	if 'Public Funding' in charters[charter]:
		charters[charter]['Public Funding']			= \
			'%.2f' % charters[charter]['Public Funding']

for district in districts:
	if 'Charter Transfer' in districts[district]:
		districts[district]['Charter Transfer']			= \
			'%.2f' % districts[district]['Charter Transfer']

write_file.close()
write_file2.close()

# Charter-District Third Grade Reading Guarantee

filename	= 'Charter-District Third Grade Reading Guarantee'
xls_file	= xls_path + 'RAW' + ' ' + filename + '.xlsx'
workbook	= xlrd.open_workbook(xls_file)

worksheet 	= workbook.sheet_by_name('community_school_2014')

# One row per charter

csv_file	= csv_path + filename + ' Charters' + '.csv'
write_file	= open(csv_file, 'w')
wr 		= csv.writer(write_file, quoting=csv.QUOTE_ALL)

num_rows 					= worksheet.nrows - 1
num_cells 					= worksheet.ncols - 1
header_row					= True
headers						= []
footer_row					= False

curr_row 					= 0
while curr_row < num_rows:
	curr_row 				+= 1
	school_IRN				= worksheet.cell_value(curr_row, 1)
	school_IRN				= fixIRN(school_IRN)
	if school_IRN not in charters:
		charters[school_IRN]		= {}

curr_row					= -1

while curr_row < num_rows:
	curr_row 				+= 1
	if curr_row == 1:
		header_row 			= False
		for each in headers:
			each 			= clean(each)
		wr.writerow(headers)
		new_headers			= []
		for each in headers:
			each			= filename + ' - ' + each
			each 			= clean(each)
			new_headers.append(each)
		headers				= new_headers	
	if header_row:
		curr_cell			= -1
		while curr_cell < num_cells:
			curr_cell 		+= 1
			cell_value 		= str(worksheet.cell_value(curr_row, curr_cell))
			headers.append(cell_value)
	elif not(footer_row):
		row				= worksheet.row_values(curr_row)
		if 'Community School Total' in row[0]:
			footer_row		= True
		else:
			wr.writerow(row)
			school_IRN			= worksheet.cell_value(curr_row, 1)
			school_IRN			= fixIRN(school_IRN.zfill(6))

			curr_cell			= -1
			while curr_cell < num_cells:
				curr_cell 		+= 1
				cell_value 		= clean(worksheet.cell_value(curr_row, curr_cell))
				if school_IRN in charters:
					charters[school_IRN][headers[curr_cell]]	= cell_value
				else:
					charters[school_IRN]				= {}
					charters[school_IRN][headers[curr_cell]]	= cell_value

write_file.close()

worksheet 	= workbook.sheet_by_name('public_district_2014')

# One row per district

csv_file	= csv_path + filename + ' Districts' + '.csv'
write_file	= open(csv_file, 'w')
wr 		= csv.writer(write_file, quoting=csv.QUOTE_ALL)

num_rows 					= worksheet.nrows - 1
num_cells 					= worksheet.ncols - 1
curr_row 					= -1
header_row					= True
headers						= []
footer_row					= False

while curr_row < num_rows:
	curr_row 				+= 1
	if curr_row == 1:
		header_row 			= False
		for each in headers:
			each 			= clean(each)
		wr.writerow(headers)
		new_headers			= []
		for each in headers:
			each			= filename + ' - ' + each
			each 			= clean(each)
			new_headers.append(each)
		headers				= new_headers
	if header_row:
		curr_cell			= -1
		while curr_cell < num_cells:
			curr_cell 		+= 1
			cell_value 		= str(worksheet.cell_value(curr_row, curr_cell))
			headers.append(cell_value)
	elif not(footer_row):
		row				= worksheet.row_values(curr_row)
		if 'Traditional Public District Total' in row[0]:
			footer_row		= True
		else:
			wr.writerow(row)
			district_IRN			= worksheet.cell_value(curr_row, 1)
			district_IRN			= fixIRN(district_IRN)

			curr_cell			= -1
			while curr_cell < num_cells:
				curr_cell 		+= 1
				cell_value 		= clean(worksheet.cell_value(curr_row, curr_cell))
				if district_IRN in districts:
					districts[district_IRN][headers[curr_cell]]	= cell_value
				else:
					districts[district_IRN]				= {}
					districts[district_IRN][headers[curr_cell]]	= cell_value

write_file.close()

# Charter-District Expenditure Data

filename	= 'Charter-District Expenditure Data'
xls_file	= xls_path + 'RAW' + ' ' + filename + '.xls'
workbook	= xlrd.open_workbook(xls_file)

worksheet 	= workbook.sheet_by_name('EFM_Data')

# One row per charter

csv_file	= csv_path + filename + '.csv'
write_file	= open(csv_file, 'w')
wr 		= csv.writer(write_file, quoting=csv.QUOTE_ALL)

num_rows 					= worksheet.nrows - 1
num_cells 					= worksheet.ncols - 1
header_row					= True
headers						= []
footer_row					= False

curr_row 					= 0
while curr_row < num_rows:
	curr_row 				+= 1
	IRN					= worksheet.cell_value(curr_row, 0)
	IRN					= fixIRN(IRN)
	org_type				= worksheet.cell_value(curr_row, 2)
	if org_type == 'Community School':
		if IRN not in charters:
			charters[IRN]		= {}
	else:
		if IRN not in districts:
			districts[IRN]		= {}

curr_row					= -1

while curr_row < num_rows:
	curr_row 				+= 1
	if curr_row == 1:
		header_row 			= False
		for each in headers:
			each 			= clean(each)
		wr.writerow(headers)
		new_headers			= []
		for each in headers:
			each			= filename + ' - ' + each
			each 			= clean(each)
			new_headers.append(each)
		headers				= new_headers	
	if header_row:
		curr_cell			= -1
		while curr_cell < num_cells:
			curr_cell 		+= 1
			cell_value 		= str(worksheet.cell_value(curr_row, curr_cell))
			headers.append(cell_value)
	elif not(footer_row):
		row				= worksheet.row_values(curr_row)
		if len(row[0]) < 1:
			footer_row		= True
		else:
			wr.writerow(row)

			IRN				= worksheet.cell_value(curr_row, 0)
			IRN				= fixIRN(IRN)

			if IRN in charters:
				curr_cell		= -1
				while curr_cell < num_cells:
					total_expenses		= 0
					curr_cell 	+= 1
					cell_value 	= clean(worksheet.cell_value(curr_row, curr_cell))
					charters[IRN][headers[curr_cell]]		= cell_value
					total_expenses		+= worksheet.cell_value(curr_row, 3)
					total_expenses		+= worksheet.cell_value(curr_row, 4)
					total_expenses		+= worksheet.cell_value(curr_row, 5)
					total_expenses		+= worksheet.cell_value(curr_row, 6)
					total_expenses		+= worksheet.cell_value(curr_row, 7)
					total_expenses		+= worksheet.cell_value(curr_row, 8)
					classroom_percent	= float(total_expenses)
					classroom_percent	-= worksheet.cell_value(curr_row, 7)
					classroom_percent	= classroom_percent / total_expenses
					classroom_percent	= classroom_percent * 100
					classroom_percent	= round(classroom_percent, 1)
					admin_percent		= 100.0 - classroom_percent
					classroom_percent	= "%.1f" % classroom_percent
					admin_percent		= "%.1f" % admin_percent
					
					charters[IRN]['% Spent in Classroom']	= classroom_percent
					charters[IRN]['% Spent on Administration']= admin_percent

			if IRN in districts:
				curr_cell		= -1
				while curr_cell < num_cells:
					curr_cell 	+= 1
					cell_value 	= clean(worksheet.cell_value(curr_row, curr_cell))
					districts[IRN][headers[curr_cell]]	= cell_value
					total_expenses		+= worksheet.cell_value(curr_row, 3)
					total_expenses		+= worksheet.cell_value(curr_row, 4)
					total_expenses		+= worksheet.cell_value(curr_row, 5)
					total_expenses		+= worksheet.cell_value(curr_row, 6)
					total_expenses		+= worksheet.cell_value(curr_row, 7)
					total_expenses		+= worksheet.cell_value(curr_row, 8)
					classroom_percent	= float(total_expenses)
					classroom_percent	-= worksheet.cell_value(curr_row, 7)
					classroom_percent	= classroom_percent / total_expenses
					classroom_percent	= classroom_percent * 100
					classroom_percent	= round(classroom_percent, 1)
					admin_percent		= 100.0 - classroom_percent
					classroom_percent	= "%.1f" % classroom_percent
					admin_percent		= "%.1f" % admin_percent
					
					districts[IRN]['% Spent in Classroom']	= classroom_percent
					districts[IRN]['% Spent on Administration']= admin_percent
	
write_file.close()


###################### REPORT CARDS #########################

# Charter Report Card

filename	= 'Charter Report Card'
xls_file	= xls_path + 'RAW' + ' ' + filename + '.xls'
workbook	= xlrd.open_workbook(xls_file)

worksheet 	= workbook.sheet_by_name('COMMSCHL')

# One row per charter

csv_file	= csv_path + filename + '.csv'
write_file	= open(csv_file, 'w')
wr 		= csv.writer(write_file, quoting=csv.QUOTE_ALL)

num_rows 					= worksheet.nrows - 1
num_cells 					= worksheet.ncols - 1
header_row					= True
headers						= []
footer_row					= False

curr_row 					= 0
while curr_row < num_rows:
	curr_row 				+= 1
	IRN					= worksheet.cell_value(curr_row, 1)
	IRN					= fixIRN(IRN)
	if IRN in charters:
		charters[IRN]			= {}

curr_row					= -1

while curr_row < num_rows:
	curr_row 				+= 1
	if curr_row == 1:
		header_row 			= False
		for each in headers:
			each 			= clean(each)
		wr.writerow(headers)
		new_headers			= []
		for each in headers:
			each			= filename + ' - ' + each
			each 			= clean(each)
			new_headers.append(each)
		headers				= new_headers	
	if header_row:
		curr_cell			= -1
		while curr_cell < num_cells:
			curr_cell 		+= 1
			cell_value 		= str(worksheet.cell_value(curr_row, curr_cell))
			headers.append(cell_value)
	elif not(footer_row):
		row				= worksheet.row_values(curr_row)
		if len(row[0]) < 1:
			footer_row		= True
		else:
			wr.writerow(row)
			school_IRN			= worksheet.cell_value(curr_row, 0)
			school_IRN			= fixIRN(school_IRN)
			school_name			= worksheet.cell_value(curr_row, 1)
			school_address			= worksheet.cell_value(curr_row, 6)

			school_district_IRN		= worksheet.cell_value(curr_row, 2)
			school_district_IRN		= fixIRN(school_district_IRN)
			school_district_name		= worksheet.cell_value(curr_row, 3)

			school_county			= worksheet.cell_value(curr_row, 4)
			school_gradespan		= worksheet.cell_value(curr_row, 10)
			school_open			= worksheet.cell_value(curr_row, 11)

			school_ltr_stand		= worksheet.cell_value(curr_row, 16)
			school_perf_score		= worksheet.cell_value(curr_row, 17)
			school_ltr_perf			= worksheet.cell_value(curr_row, 19)
			school_ltr_overall_value	= worksheet.cell_value(curr_row, 20)
			school_ltr_gifted_value		= worksheet.cell_value(curr_row, 21)
			school_ltr_disable_value	= worksheet.cell_value(curr_row, 22)
			school_ltr_bottom_value		= worksheet.cell_value(curr_row, 23)
			school_ltr_AMO			= worksheet.cell_value(curr_row, 24)
			school_enrollment		= worksheet.cell_value(curr_row, 29)
			school_attend_rate		= worksheet.cell_value(curr_row, 102)

			letters				= [school_ltr_perf, \
								school_ltr_overall_value, \
								school_ltr_gifted_value, \
								school_ltr_disable_value, \
								school_ltr_bottom_value, \
								school_ltr_AMO, \
								school_ltr_stand]

			grade_sum = 0
			no_of_grades = 0		
			for grade in letters:
				if grade in grade_dict:
					grade_sum	+= grade_dict[grade]
					no_of_grades	+= 1

			if grade_sum == 0:
				school_avg_grade = '--'
			else:
				avg_grade_point		= grade_sum / no_of_grades
				school_avg_grade = point_to_grade(avg_grade_point)

			try:
				school_grad_rate	= float(worksheet.cell_value(curr_row, 107))
				school_grad_rate	= school_grad_rate \
							/ float(worksheet.cell_value(curr_row, 108))
				school_grad_rate	= '%.1f' % (100 * school_grad_rate)
			except:
				school_grad_rate	= '--'
			city_state_zip				= worksheet.cell_value(curr_row, 7)
			group					= city_state_zip.split(",")
			school_city				= group[0]
			school_group				= group[1].split(" ")
			school_state				= school_group[1]
			school_postal_code			= school_group[-1]

			# Basic School Information
				# School Name
			charters[school_IRN]['Name']		= school_name
				# Address
			charters[school_IRN]['Address']		= school_address
			charters[school_IRN]['City']		= school_city
			charters[school_IRN]['State']		= school_state
			charters[school_IRN]['Postal Code']	= school_postal_code
				# County
			charters[school_IRN]['County']		= school_county
				# District
			charters[school_IRN]['District IRN']	= school_district_IRN
			charters[school_IRN]['District Name']	= school_district_name
				# Grades served
			charters[school_IRN]['Grades Served']	= school_gradespan
				# Open Status
			charters[school_IRN]['Open Status']	= school_open
				# Average Grade
			charters[school_IRN]['Avg Grade']	= school_avg_grade

			# Studnets and Faculty
				# # of students
			charters[school_IRN]['# of students']	= school_enrollment

			# Performance Data
				# Report Card metrics
					# Letter grade standards met
			charters[school_IRN]['Letter grade standards met']	= school_ltr_stand
					# Letter grade performance index
			charters[school_IRN]['Letter grade performance index']	= school_ltr_perf
					# Performance index score
			charters[school_IRN]['Performance index score']		= school_perf_score
					# Letter grade overall value-add
			charters[school_IRN]['Letter grade overall value-add']	= school_ltr_overall_value
					# Letter grade gifted value-add
			charters[school_IRN]['Letter grade gifted value-add']	= school_ltr_gifted_value
					# Letter grade disabled value-add
			charters[school_IRN]['Letter grade disabled value-add']	= school_ltr_disable_value
					# Letter grade lowest 20% value-add
			charters[school_IRN]['Letter grade lowest 20% value-add']= school_ltr_bottom_value
					# Letter grade of AMO
			charters[school_IRN]['Letter grade of AMO']		= school_ltr_AMO
				# Attendance rate
			charters[school_IRN]['Attendance rate']			= school_attend_rate
				# Graduation rate
			charters[school_IRN]['Graduation rate']			= school_grad_rate

			curr_cell			= -1
			while curr_cell < num_cells:
				curr_cell 		+= 1
				cell_value 		= clean(worksheet.cell_value(curr_row, curr_cell))
				if school_IRN in charters:
					charters[school_IRN][headers[curr_cell]]	= cell_value
				else:
					charters[school_IRN]				= {}
					charters[school_IRN][headers[curr_cell]]	= cell_value

write_file.close()

# District Report Card

filename	= 'District Report Card'
xls_file	= xls_path + 'RAW' + ' ' + filename + '.xlsx'
workbook	= xlrd.open_workbook(xls_file)

worksheet 	= workbook.sheet_by_name('DISTRICT')

# One row per district

csv_file	= csv_path + filename + '.csv'
write_file	= open(csv_file, 'w')
wr 		= csv.writer(write_file, quoting=csv.QUOTE_ALL)

num_rows 					= worksheet.nrows - 1
num_cells 					= worksheet.ncols - 1
header_row					= True
headers						= []
footer_row					= False

curr_row 					= 0
while curr_row < num_rows:
	curr_row 				+= 1
	IRN					= worksheet.cell_value(curr_row, 1)
	IRN					= fixIRN(IRN)
	if IRN in districts:
		districts[IRN]			= {}

curr_row					= -1

while curr_row < num_rows:
	curr_row 				+= 1
	if curr_row == 1:
		header_row 			= False
		for each in headers:
			each 			= clean(each)
		wr.writerow(headers)
		new_headers			= []
		for each in headers:
			each			= filename + ' - ' + each
			each 			= clean(each)
			new_headers.append(each)
		headers				= new_headers	
	if header_row:
		curr_cell			= -1
		while curr_cell < num_cells:
			curr_cell 		+= 1
			cell_value 		= str(worksheet.cell_value(curr_row, curr_cell))
			headers.append(cell_value)
	elif not(footer_row):
		row				= worksheet.row_values(curr_row)
		if len(row[0]) < 1:
			footer_row		= True
		else:
			wr.writerow(row)
			district_IRN			= worksheet.cell_value(curr_row, 0)
			district_IRN			= fixIRN(district_IRN)

			if district_IRN not in districts:
				districts[district_IRN]	= {}

			district_name			= worksheet.cell_value(curr_row, 1)
			district_address		= worksheet.cell_value(curr_row, 4)

			district_ltr_stand		= worksheet.cell_value(curr_row, 11)
			district_perf_score		= worksheet.cell_value(curr_row, 12)
			district_ltr_perf		= worksheet.cell_value(curr_row, 14)
			district_ltr_overall_value	= worksheet.cell_value(curr_row, 15)
			district_ltr_gifted_value	= worksheet.cell_value(curr_row, 16)
			district_ltr_disable_value	= worksheet.cell_value(curr_row, 17)
			district_ltr_bottom_value	= worksheet.cell_value(curr_row, 18)
			district_ltr_AMO		= worksheet.cell_value(curr_row, 19)
			district_enrollment		= worksheet.cell_value(curr_row, 24)
			district_attend_rate		= worksheet.cell_value(curr_row, 97)



			letters				= [district_ltr_perf, \
								district_ltr_overall_value, \
								district_ltr_gifted_value, \
								district_ltr_disable_value, \
								district_ltr_bottom_value, \
								district_ltr_AMO, \
								district_ltr_stand]

			grade_sum = 0
			no_of_grades = 0		
			for grade in letters:
				if grade in grade_dict:
					grade_sum	+= grade_dict[grade]
					no_of_grades	+= 1

			if grade_sum == 0:
				district_avg_grade = '--'
			else:
				avg_grade_point		= grade_sum / no_of_grades
				district_avg_grade	= point_to_grade(avg_grade_point)

			try:
				district_grad_rate	= float(worksheet.cell_value(curr_row, 102))
				district_grad_rate	= district_grad_rate \
							/ float(worksheet.cell_value(curr_row, 103))
				district_grad_rate	= '%.1f' % (100 * district_grad_rate)
			except:
				district_grad_rate	= '--'
			city_state_zip				= worksheet.cell_value(curr_row, 5)
			group					= city_state_zip.split(",")
			district_city				= group[0]
			district_group				= group[1].split(" ")
			district_state				= district_group[1]
			district_postal_code			= district_group[-1]

			# Basic School Information
				# School Name
			districts[district_IRN]['Name']			= district_name
				# Address
			districts[district_IRN]['Address']		= district_address
			districts[district_IRN]['City']			= district_city
			districts[district_IRN]['State']		= district_state
			districts[district_IRN]['Postal Code']		= district_postal_code
			districts[district_IRN]['Avg Grade']		= district_avg_grade	

			# Studnets and Faculty
				# # of students
			districts[district_IRN]['# of students']	= district_enrollment

			# Performance Data
				# Report Card metrics
					# Letter grade standards met
			districts[district_IRN]['Letter grade standards met']	= district_ltr_stand
					# Letter grade performance index
			districts[district_IRN]['Letter grade performance index']= district_ltr_perf
					# Performance index score
			districts[district_IRN]['Performance index score']	= district_perf_score
					# Letter grade overall value-add
			districts[district_IRN]['Letter grade overall value-add']	= \
									district_ltr_overall_value
					# Letter grade gifted value-add
			districts[district_IRN]['Letter grade gifted value-add']	= \
									district_ltr_gifted_value
					# Letter grade disabled value-add
			districts[district_IRN]['Letter grade disabled value-add']	= \
									district_ltr_disable_value
					# Letter grade lowest 20% value-add
			districts[district_IRN]['Letter grade lowest 20% value-add']	= \
									district_ltr_bottom_value
					# Letter grade of AMO
			districts[district_IRN]['Letter grade of AMO']	= district_ltr_AMO
				# Attendance rate
			districts[district_IRN]['Attendance rate']	= district_attend_rate
				# Graduation rate
			districts[district_IRN]['Graduation rate']	= district_grad_rate

write_file.close()

#################### ANNUAL CHARTER REPORTS ######################

# Charter Annual Report Academic Performance and Demographic Data

filename	= 'Charter Annual Report Academic Performance and Demographic Data'
xls_file	= xls_path + 'RAW' + ' ' + filename + '.xls'
workbook	= xlrd.open_workbook(xls_file)

worksheet 	= workbook.sheet_by_name('TABLE 1A_Trad Demo & Acad  ')

# One row per charter

csv_file	= csv_path + filename + ' Trad' + '.csv'
write_file	= open(csv_file, 'w')
wr 		= csv.writer(write_file, quoting=csv.QUOTE_ALL)

num_rows 					= worksheet.nrows - 1
num_cells 					= worksheet.ncols - 1
curr_row 					= -1
header_row					= True
headers						= []
footer_row					= False

while curr_row < num_rows:
	curr_row 				+= 1
	if curr_row == 1:
		header_row 			= False
		for each in headers:
			each 			= clean(each)
		wr.writerow(headers)
		new_headers			= []
		for each in headers:
			each			= filename + ' - ' + each
			each 			= clean(each)
			new_headers.append(each)
		headers				= new_headers	
	if header_row:
		curr_cell			= -1
		while curr_cell < num_cells:
			curr_cell 		+= 1
			cell_value 		= str(worksheet.cell_value(curr_row, curr_cell))
			headers.append(cell_value)
	elif not(footer_row):
		row				= worksheet.row_values(curr_row)
		if len(row[0]) < 1:
			footer_row		= True
		else:
			wr.writerow(row)
			school_IRN			= worksheet.cell_value(curr_row, 2)
			school_IRN			= fixIRN(school_IRN)	

			try:
				school_fy		= worksheet.cell_value(curr_row, 4)
				school_fy		= school_fy[-2:]
				school_fy		= int(school_fy)
				years_in_op		= 14 - school_fy
				if years_in_op == 0:
					charters[school_IRN]['Years in operation']	= 'First'
				else:
					charters[school_IRN]['Years in operation']	= str(years_in_op)
			except:
				pass

			school_sponsor			= worksheet.cell_value(curr_row, 1)
			school_virtual			= worksheet.cell_value(curr_row, 7)
			school_spec			= worksheet.cell_value(curr_row, 8)
			school_grad_rate		= worksheet.cell_value(curr_row, 24)
			charters[school_IRN]['Virtual']				= school_virtual
			charters[school_IRN]['Specialization']			= school_spec
			charters[school_IRN]['Sponsor']				= school_sponsor
			charters[school_IRN]['Graduation rate']			= school_grad_rate

			curr_cell			= -1
			while curr_cell < num_cells:
				curr_cell 		+= 1
				cell_value 		= clean(worksheet.cell_value(curr_row, curr_cell))
				if school_IRN in charters:
					charters[school_IRN][headers[curr_cell]]	= cell_value
				else:
					charters[school_IRN]				= {}
					charters[school_IRN][headers[curr_cell]]	= cell_value

write_file.close()

worksheet 	= workbook.sheet_by_name('TABLE 1B_DORP Demo & Acad')

# One row per charter

csv_file	= csv_path + filename + ' DORP' + '.csv'
write_file	= open(csv_file, 'w')
wr 		= csv.writer(write_file, quoting=csv.QUOTE_ALL)

num_rows 					= worksheet.nrows - 1
num_cells 					= worksheet.ncols - 1
curr_row 					= -1
header_row					= True
headers						= []
footer_row					= False

while curr_row < num_rows:
	curr_row 				+= 1
	if curr_row == 1:
		header_row 			= False
		for each in headers:
			each 			= clean(each)
		wr.writerow(headers)
		new_headers			= []
		for each in headers:
			each			= filename + ' - ' + each
			each 			= clean(each)
			new_headers.append(each)
		headers				= new_headers	
	if header_row:
		curr_cell			= -1
		while curr_cell < num_cells:
			curr_cell 		+= 1
			cell_value 		= str(worksheet.cell_value(curr_row, curr_cell))
			headers.append(cell_value)
	elif not(footer_row):
		row				= worksheet.row_values(curr_row)
		if len(row[0]) < 1:
			footer_row		= True
		else:
			wr.writerow(row)
			school_IRN			= worksheet.cell_value(curr_row, 2)
			school_IRN			= fixIRN(school_IRN)

			try:
				school_fy		= worksheet.cell_value(curr_row, 4)
				school_fy		= school_fy[-2:]
				school_fy		= int(school_fy)
				years_in_op		= 14 - school_fy
				if years_in_op == 0:
					charters[school_IRN]['Years in operation']	= 'First'
				else:
					charters[school_IRN]['Years in operation']	= str(years_in_op)
			except:
				pass

			school_sponsor			= worksheet.cell_value(curr_row, 1)
			school_virtual			= worksheet.cell_value(curr_row, 7)
			school_spec			= worksheet.cell_value(curr_row, 8)
			school_grad_rate		= worksheet.cell_value(curr_row, 13)
			charters[school_IRN]['Virtual']				= school_virtual
			charters[school_IRN]['Specialization']			= school_spec
			charters[school_IRN]['Sponsor']				= school_sponsor
			charters[school_IRN]['Graduation rate']			= school_grad_rate

			curr_cell			= -1
			while curr_cell < num_cells:
				curr_cell 		+= 1
				cell_value 		= clean(worksheet.cell_value(curr_row, curr_cell))
				if school_IRN in charters:
					charters[school_IRN][headers[curr_cell]]	= cell_value
				else:
					charters[school_IRN]				= {}
					charters[school_IRN][headers[curr_cell]]	= cell_value

write_file.close()

# Charter Annual Report Enrollment History Data

filename	= 'Charter Annual Report Enrollment History Data'
xls_file	= xls_path + 'RAW' + ' ' + filename + '.xls'
workbook	= xlrd.open_workbook(xls_file)

worksheet 	= workbook.sheet_by_name('TABLE 2_Enrollment History')

# One row per charter

csv_file	= csv_path + filename + '.csv'
write_file	= open(csv_file, 'w')
wr 		= csv.writer(write_file, quoting=csv.QUOTE_ALL)

num_rows 					= worksheet.nrows - 1
num_cells 					= worksheet.ncols - 1
curr_row 					= -1
header_row					= True
headers						= []
footer_row					= False

while curr_row < num_rows:
	curr_row 				+= 1
	if curr_row == 1:
		header_row 			= False
		for each in headers:
			each 			= clean(each)
		wr.writerow(headers)
		new_headers			= []
		for each in headers:
			each			= filename + ' - ' + each
			each 			= clean(each)
			new_headers.append(each)
		headers				= new_headers
	if header_row:
		curr_cell			= -1
		while curr_cell < num_cells:
			curr_cell 		+= 1
			cell_value 		= str(worksheet.cell_value(curr_row, curr_cell))
			headers.append(cell_value)
	elif not(footer_row):
		row				= worksheet.row_values(curr_row)
		if row[0] == 'Total':
			footer_row		= True
		else:
			wr.writerow(row)
			school_IRN			= worksheet.cell_value(curr_row, 2)
			school_IRN			= fixIRN(school_IRN)
			
			try:
				school_enrollment	= float(worksheet.cell_value(curr_row, 18))
				school_enrollment	+= .5
				school_enrollment	= int(school_enrollment)
				charters[school_IRN]['# of students']	= school_enrollment
			except:
				pass

			curr_cell			= -1
			while curr_cell < num_cells:
				curr_cell 		+= 1
				cell_value 		= clean(worksheet.cell_value(curr_row, curr_cell))
				if school_IRN in charters:
					charters[school_IRN][headers[curr_cell]]	= cell_value
				else:
					charters[school_IRN]				= {}
					charters[school_IRN][headers[curr_cell]]	= cell_value

write_file.close()

# Charter Annual Report Foundation Funding Data

filename	= 'Charter Annual Report Foundation Funding Data'
xls_file	= xls_path + 'RAW' + ' ' + filename + '.xls'
workbook	= xlrd.open_workbook(xls_file)

worksheet 	= workbook.sheet_by_name('TABLE 3_Foundation Funding')

# One row per charter

csv_file	= csv_path + filename + '.csv'
write_file	= open(csv_file, 'w')
wr 		= csv.writer(write_file, quoting=csv.QUOTE_ALL)

num_rows 					= worksheet.nrows - 1
num_cells 					= worksheet.ncols - 1
curr_row 					= -1
header_row					= True
headers						= []
footer_row					= False

while curr_row < num_rows:
	curr_row 				+= 1
	if curr_row == 1:
		header_row 			= False
		for each in headers:
			each 			= clean(each)
		wr.writerow(headers)
		new_headers			= []
		for each in headers:
			each			= filename + ' - ' + each
			each 			= clean(each)
			new_headers.append(each)
		headers				= new_headers	
	if header_row:
		curr_cell			= -1
		while curr_cell < num_cells:
			curr_cell 		+= 1
			cell_value 		= str(worksheet.cell_value(curr_row, curr_cell))
			headers.append(cell_value)
	elif not(footer_row):
		row				= worksheet.row_values(curr_row)
		if len(row[0]) < 1:
			footer_row		= True
		else:
			wr.writerow(row)
			school_IRN			= worksheet.cell_value(curr_row, 0)
			school_IRN			= fixIRN(school_IRN)

			if school_IRN not in charters:
				charters[school_IRN]	= {}

			curr_cell			= -1
			while curr_cell < num_cells:
				curr_cell 		+= 1
				cell_value 		= clean(worksheet.cell_value(curr_row, curr_cell))
				charters[school_IRN][headers[curr_cell]]	= cell_value

write_file.close()

# Charter Annual Report Sponsor Performance Data

filename	= 'Charter Annual Report Sponsor Performance Data'
xls_file	= xls_path + 'RAW' + ' ' + filename + '.xls'
workbook	= xlrd.open_workbook(xls_file)

worksheet 	= workbook.sheet_by_name('Table7_ Authorizer Performance')

# One row per sponsor

csv_file	= csv_path + filename + '.csv'
write_file	= open(csv_file, 'w')
wr 		= csv.writer(write_file, quoting=csv.QUOTE_ALL)

num_rows 					= worksheet.nrows - 1
num_cells 					= worksheet.ncols - 1
curr_row 					= 2
header_row					= True
headers						= ['']
footer_row					= False

while curr_row < num_rows:
	curr_row 				+= 1
	prior_cell				= ''
	if curr_row == 3:
		header_row 			= False
		headers = \
			['Sponsor IRN', \
			'Sponsor Name', \
			'School Year', \
			'N of Schools - General Education Schools', \
			'N of Schools - Special Education Schools', \
			'N of Schools - Dropout Recovery Schools', \
			'Sponsors Aggregate PI Score - Based on General Education Community Schools', \
			'Sponsor Prohibited from Sponsoring Additional Schools in School Year \
			2014-2015 Due to Poor Academic Performance and/or Noncompliance with \
			Reporting Requirements', \
			'Overall Value-Added Grade - General Education Schools - A', \
			'Overall Value-Added Grade - General Education Schools - B', \
			'Overall Value-Added Grade - General Education Schools - C', \
			'Overall Value-Added Grade - General Education Schools - D', \
			'Overall Value-Added Grade - General Education Schools - F', \
			'Overall Value-Added Grade - General Education Schools - NA', \
			'Overall Value-Added Grade - Special Education Schools - A', \
			'Overall Value-Added Grade - Special Education Schools - B', \
			'Overall Value-Added Grade - Special Education Schools - C', \
			'Overall Value-Added Grade - Special Education Schools - D', \
			'Overall Value-Added Grade - Special Education Schools - F', \
			'Overall Value-Added Grade - Special Education Schools - NA', \
			'Performance Index Grade - General Education Schools - A', \
			'Performance Index Grade - General Education Schools - B', \
			'Performance Index Grade - General Education Schools - C', \
			'Performance Index Grade - General Education Schools - D', \
			'Performance Index Grade - General Education Schools - F', \
			'Performance Index Grade - General Education Schools - NA', \
			'Performance Index Grade - Special Education Schools - A', \
			'Performance Index Grade - Special Education Schools - B', \
			'Performance Index Grade - Special Education Schools - C', \
			'Performance Index Grade - Special Education Schools - D', \
			'Performance Index Grade - Special Education Schools - F', \
			'Performance Index Grade - Special Education Schools - NA', \
			'Indicators Met Grade - General Education Schools - A', \
			'Indicators Met Grade - General Education Schools - B', \
			'Indicators Met Grade - General Education Schools - C', \
			'Indicators Met Grade - General Education Schools - D', \
			'Indicators Met Grade - General Education Schools - F', \
			'Indicators Met Grade - General Education Schools - NA', \
			'Indicators Met Grade - Special Education Schools - A', \
			'Indicators Met Grade - Special Education Schools - B', \
			'Indicators Met Grade - Special Education Schools - C', \
			'Indicators Met Grade - Special Education Schools - D', \
			'Indicators Met Grade - Special Education Schools - F', \
			'Indicators Met Grade - Special Education Schools - NA', \
			'AMO Grade - General Education Schools - A', \
			'AMO Grade - General Education Schools - B', \
			'AMO Grade - General Education Schools - C', \
			'AMO Grade - General Education Schools - D', \
			'AMO Grade - General Education Schools - F', \
			'AMO Grade - General Education Schools - NA', \
			'AMO Grade - Special Education Schools - A', \
			'AMO Grade - Special Education Schools - B', \
			'AMO Grade - Special Education Schools - C', \
			'AMO Grade - Special Education Schools - D', \
			'AMO Grade - Special Education Schools - F', \
			'AMO Grade - Special Education Schools - NA', \
			'Four Year Graduation Grade - General Education Schools - A', \
			'Four Year Graduation Grade - General Education Schools - B', \
			'Four Year Graduation Grade - General Education Schools - C', \
			'Four Year Graduation Grade - General Education Schools - D', \
			'Four Year Graduation Grade - General Education Schools - F', \
			'Four Year Graduation Grade - General Education Schools - NA', \
			'Four Year Graduation Grade - Special Education Schools - A', \
			'Four Year Graduation Grade - Special Education Schools - B', \
			'Four Year Graduation Grade - Special Education Schools - C', \
			'Four Year Graduation Grade - Special Education Schools - D', \
			'Four Year Graduation Grade - Special Education Schools - F', \
			'Four Year Graduation Grade - Special Education Schools - NA', \
			'Five Year Graduation Grade - General Education Schools - A', \
			'Five Year Graduation Grade - General Education Schools - B', \
			'Five Year Graduation Grade - General Education Schools - C', \
			'Five Year Graduation Grade - General Education Schools - D', \
			'Five Year Graduation Grade - General Education Schools - F', \
			'Five Year Graduation Grade - General Education Schools - NA', \
			'Five Year Graduation Grade - Special Education Schools - A', \
			'Five Year Graduation Grade - Special Education Schools - B', \
			'Five Year Graduation Grade - Special Education Schools - C', \
			'Five Year Graduation Grade - Special Education Schools - D', \
			'Five Year Graduation Grade - Special Education Schools - F', \
			'Five Year Graduation Grade - Special Education Schools - NA']
		for each in headers:
			clean(each)
		wr.writerow(headers)
	if header_row:
		pass
	elif not(footer_row):
		row				= worksheet.row_values(curr_row)
		if len(row[0]) > 10:
			footer_row		= True
		else:
			wr.writerow(row)

write_file.close()


##################### DISABILITY DATA ########################

# Charter Disability Data

filename	= 'Charter Disability Data'
xls_file	= xls_path + 'RAW' + ' ' + filename + '.xls'
workbook	= xlrd.open_workbook(xls_file)

worksheet 	= workbook.sheet_by_name('BLDG_DISABILITY_13')

# Two rows per charter

csv_file	= csv_path + filename + '.csv'
write_file	= open(csv_file, 'w')
wr 		= csv.writer(write_file, quoting=csv.QUOTE_ALL)

num_rows 					= worksheet.nrows - 1
num_cells 					= worksheet.ncols - 1
curr_row 					= -1
header_row					= True
headers						= []
footer_row					= False

while curr_row < num_rows:
	curr_row 				+= 1
	if curr_row == 1:
		header_row 			= False
		for each in headers:
			each			= clean(each)
		wr.writerow(headers)
		headers = [ \
			'Disabled - Read 3rd grade 2012-13 % proficient or above', \
			'Disabled - Math 3rd grade 2012-13 % proficient or above', \
			'Disabled - Read 4th Grade 2012-13 % proficient or above', \
			'Disabled - Math 4th Grade 2012-13 % proficient or above', \
			'Disabled - Read 5th grade 2012-13 % proficient or above', \
			'Disabled - Math 5th grade 2012-13 % proficient or above', \
			'Disabled - Science 5th grade 2012-13 % proficient or above', \
			'Disabled - Read 6th Grade 2012-13 % proficient or above', \
			'Disabled - Math 6th Grade 2012-13 % proficient or above', \
			'Disabled - Read 7th Grade 2012-13 % proficient or above', \
			'Disabled - Math 7th Grade 2012-13 % proficient or above', \
			'Disabled - Read 8th Grade 2012-13 % proficient or above', \
			'Disabled - Math 8th Grade 2012-13 % proficient or above', \
			'Disabled - Science 8th grade 2012-13 % proficient or above', \
			'Disabled - Read OGT 2012-13 % proficient or above', \
			'Disabled - Math OGT 2012-13 % proficient or above', \
			'Disabled - Write OGT 2012-13 % proficient or above', \
			'Disabled - Social Studies OGT 2012-13 % proficient or above', \
			'Disabled - Science OGT 2012-13 % proficient or above', \
			'Disabled - Read 11th grade 2012-13 % at or above proficient', \
			'Disabled - Math 11th grade 2012-13 % at or above proficient', \
			'Disabled - Write 11th grade 2012-13 % at or above proficient', \
			'Disabled - Social Studies 11th grade 2012-13 % at or above proficient', \
			'Disabled - Science 11th grade 2012-13 % at or above proficient', \
			'Disabled - Attendance rate 2012-13', \
			'Disabled - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'Disabled - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'Disabled - Enrollment', \
			'Disabled - % of total enrollment', \
			'Nondisabled - Read 3rd grade 2012-13 % proficient or above', \
			'Nondisabled - Math 3rd grade 2012-13 % proficient or above', \
			'Nondisabled - Read 4th Grade 2012-13 % proficient or above', \
			'Nondisabled - Math 4th Grade 2012-13 % proficient or above', \
			'Nondisabled - Read 5th grade 2012-13 % proficient or above', \
			'Nondisabled - Math 5th grade 2012-13 % proficient or above', \
			'Nondisabled - Science 5th grade 2012-13 % proficient or above', \
			'Nondisabled - Read 6th Grade 2012-13 % proficient or above', \
			'Nondisabled - Math 6th Grade 2012-13 % proficient or above', \
			'Nondisabled - Read 7th Grade 2012-13 % proficient or above', \
			'Nondisabled - Math 7th Grade 2012-13 % proficient or above', \
			'Nondisabled - Read 8th Grade 2012-13 % proficient or above', \
			'Nondisabled - Math 8th Grade 2012-13 % proficient or above', \
			'Nondisabled - Science 8th grade 2012-13 % proficient or above', \
			'Nondisabled - Read OGT 2012-13 % proficient or above', \
			'Nondisabled - Math OGT 2012-13 % proficient or above', \
			'Nondisabled - Write OGT 2012-13 % proficient or above', \
			'Nondisabled - Social Studies OGT 2012-13 % proficient or above', \
			'Nondisabled - Science OGT 2012-13 % proficient or above', \
			'Nondisabled - Read 11th grade 2012-13 % at or above proficient', \
			'Nondisabled - Math 11th grade 2012-13 % at or above proficient', \
			'Nondisabled - Write 11th grade 2012-13 % at or above proficient', \
			'Nondisabled - Social Studies 11th grade 2012-13 % at or above proficient', \
			'Nondisabled - Science 11th grade 2012-13 % at or above proficient', \
			'Nondisabled - Attendance rate 2012-13', \
			'Nondisabled - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'Nondisabled - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'Nondisabled - Enrollment', \
			'Nondisabled - % of total enrollment']
		for each in headers:
			each			= clean(each)
	if header_row:
		curr_cell			= -1
		while curr_cell < num_cells:
			curr_cell 		+= 1
			cell_value 		= str(worksheet.cell_value(curr_row, curr_cell))
			headers.append(cell_value)
	elif not(footer_row):
		row				= worksheet.row_values(curr_row)
		if len(row[0]) < 1:
			footer_row		= True
		else:
			wr.writerow(row)
			school_IRN			= worksheet.cell_value(curr_row, 0)
			school_IRN			= fixIRN(school_IRN)

			if school_IRN not in charters:
				charters[school_IRN]	= {}

			curr_cell			= 9
			while curr_cell < num_cells:
				curr_cell 		+= 1
				row_type		= worksheet.cell_value(curr_row, 9)
				cell_value 		= clean(worksheet.cell_value(curr_row, curr_cell))
				if row_type == 'Disabled':
					row_constant	= -10
					enroll_percent	= worksheet.cell_value(curr_row, 38)
					if type(enroll_percent) is float:
						charters[school_IRN]['% of kids with special needs'] = '%.1f' % enroll_percent
					else:
						charters[school_IRN]['% of kids with special needs'] = enroll_percent

				else:
					row_constant	= 19
				header				= headers[curr_cell + row_constant]
				charters[school_IRN][header]	= cell_value

write_file.close()

# District Disability Data

filename	= 'District Disability Data'
xls_file	= xls_path + 'RAW' + ' ' + filename + '.xls'
workbook	= xlrd.open_workbook(xls_file)

worksheet 	= workbook.sheet_by_name('DIST_DISABILITY_13')

# Two rows per district

csv_file	= csv_path + filename + '.csv'
write_file	= open(csv_file, 'w')
wr 		= csv.writer(write_file, quoting=csv.QUOTE_ALL)

num_rows 					= worksheet.nrows - 1
num_cells 					= worksheet.ncols - 1
curr_row 					= -1
header_row					= True
headers						= []
footer_row					= False

while curr_row < num_rows:
	curr_row 				+= 1
	if curr_row == 1:
		header_row 			= False
		for each in headers:
			each			= clean(each)
		wr.writerow(headers)
		headers = [ \
			'Disabled - Read 3rd grade 2012-13 % proficient or above', \
			'Disabled - Math 3rd grade 2012-13 % proficient or above', \
			'Disabled - Read 4th Grade 2012-13 % proficient or above', \
			'Disabled - Math 4th Grade 2012-13 % proficient or above', \
			'Disabled - Read 5th grade 2012-13 % proficient or above', \
			'Disabled - Math 5th grade 2012-13 % proficient or above', \
			'Disabled - Science 5th grade 2012-13 % proficient or above', \
			'Disabled - Read 6th Grade 2012-13 % proficient or above', \
			'Disabled - Math 6th Grade 2012-13 % proficient or above', \
			'Disabled - Read 7th Grade 2012-13 % proficient or above', \
			'Disabled - Math 7th Grade 2012-13 % proficient or above', \
			'Disabled - Read 8th Grade 2012-13 % proficient or above', \
			'Disabled - Math 8th Grade 2012-13 % proficient or above', \
			'Disabled - Science 8th grade 2012-13 % proficient or above', \
			'Disabled - Read OGT 2012-13 % proficient or above', \
			'Disabled - Math OGT 2012-13 % proficient or above', \
			'Disabled - Write OGT 2012-13 % proficient or above', \
			'Disabled - Social Studies OGT 2012-13 % proficient or above', \
			'Disabled - Science OGT 2012-13 % proficient or above', \
			'Disabled - Read 11th grade 2012-13 % at or above proficient', \
			'Disabled - Math 11th grade 2012-13 % at or above proficient', \
			'Disabled - Write 11th grade 2012-13 % at or above proficient', \
			'Disabled - Social Studies 11th grade 2012-13 % at or above proficient', \
			'Disabled - Science 11th grade 2012-13 % at or above proficient', \
			'Disabled - Attendance rate 2012-13', \
			'Disabled - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'Disabled - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'Disabled - Enrollment', \
			'Disabled - % of total enrollment', \
			'Nondisabled - Read 3rd grade 2012-13 % proficient or above', \
			'Nondisabled - Math 3rd grade 2012-13 % proficient or above', \
			'Nondisabled - Read 4th Grade 2012-13 % proficient or above', \
			'Nondisabled - Math 4th Grade 2012-13 % proficient or above', \
			'Nondisabled - Read 5th grade 2012-13 % proficient or above', \
			'Nondisabled - Math 5th grade 2012-13 % proficient or above', \
			'Nondisabled - Science 5th grade 2012-13 % proficient or above', \
			'Nondisabled - Read 6th Grade 2012-13 % proficient or above', \
			'Nondisabled - Math 6th Grade 2012-13 % proficient or above', \
			'Nondisabled - Read 7th Grade 2012-13 % proficient or above', \
			'Nondisabled - Math 7th Grade 2012-13 % proficient or above', \
			'Nondisabled - Read 8th Grade 2012-13 % proficient or above', \
			'Nondisabled - Math 8th Grade 2012-13 % proficient or above', \
			'Nondisabled - Science 8th grade 2012-13 % proficient or above', \
			'Nondisabled - Read OGT 2012-13 % proficient or above', \
			'Nondisabled - Math OGT 2012-13 % proficient or above', \
			'Nondisabled - Write OGT 2012-13 % proficient or above', \
			'Nondisabled - Social Studies OGT 2012-13 % proficient or above', \
			'Nondisabled - Science OGT 2012-13 % proficient or above', \
			'Nondisabled - Read 11th grade 2012-13 % at or above proficient', \
			'Nondisabled - Math 11th grade 2012-13 % at or above proficient', \
			'Nondisabled - Write 11th grade 2012-13 % at or above proficient', \
			'Nondisabled - Social Studies 11th grade 2012-13 % at or above proficient', \
			'Nondisabled - Science 11th grade 2012-13 % at or above proficient', \
			'Nondisabled - Attendance rate 2012-13', \
			'Nondisabled - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'Nondisabled - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'Nondisabled - Enrollment', \
			'Nondisabled - % of total enrollment']
		for each in headers:
			each			= clean(each)
	if header_row:
		curr_cell			= -1
		while curr_cell < num_cells:
			curr_cell 		+= 1
			cell_value 		= str(worksheet.cell_value(curr_row, curr_cell))
			headers.append(cell_value)
	elif not(footer_row):
		row				= worksheet.row_values(curr_row)
		if len(row[0]) < 1:
			footer_row		= True
		else:
			wr.writerow(row)
			district_IRN			= worksheet.cell_value(curr_row, 0)
			if type(district_IRN) is float:
				district_IRN		= str(round(district_IRN)).rstrip('0').rstrip('.')
			district_IRN			= district_IRN.zfill(6)

			curr_cell			= 4
			while curr_cell < num_cells:
				curr_cell 		+= 1
				row_type		= worksheet.cell_value(curr_row, 4)
				cell_value 		= clean(worksheet.cell_value(curr_row, curr_cell))
				if row_type == 'Disabled':
					row_constant	= -5
					enroll_percent	= worksheet.cell_value(curr_row, 33)
					if type(enroll_percent) is float:
						districts[district_IRN]['% of kids with special needs'] = '%.1f' % enroll_percent
					else:
						districts[district_IRN]['% of kids with special needs'] = enroll_percent
				else:
					row_constant	= 24
				header			= headers[curr_cell + row_constant]
				if district_IRN in districts:
					districts[district_IRN][header]			= cell_value
				else:
					districts[district_IRN]				= {}
					districts[district_IRN][header]			= cell_value

write_file.close()

##################### GIFTED DATA ########################

# Charter Gifted Data

filename	= 'Charter Gifted Data'
xls_file	= xls_path + 'RAW' + ' ' + filename + '.xls'
workbook	= xlrd.open_workbook(xls_file)

worksheet 	= workbook.sheet_by_name('BLDG_GIFTED_13')

# Two rows per charter

csv_file	= csv_path + filename + '.csv'
write_file	= open(csv_file, 'w')
wr 		= csv.writer(write_file, quoting=csv.QUOTE_ALL)

num_rows 					= worksheet.nrows - 1
num_cells 					= worksheet.ncols - 1
curr_row 					= -1
header_row					= True
headers						= []
footer_row					= False

while curr_row < num_rows:
	curr_row 				+= 1
	if curr_row == 1:
		header_row 			= False
		for each in headers:
			each			= clean(each)
		wr.writerow(headers)
		headers = [ \
			'Gifted - Read 3rd grade 2012-13 % proficient or above', \
			'Gifted - Math 3rd grade 2012-13 % proficient or above', \
			'Gifted - Read 4th Grade 2012-13 % proficient or above', \
			'Gifted - Math 4th Grade 2012-13 % proficient or above', \
			'Gifted - Read 5th grade 2012-13 % proficient or above', \
			'Gifted - Math 5th grade 2012-13 % proficient or above', \
			'Gifted - Science 5th grade 2012-13 % proficient or above', \
			'Gifted - Read 6th Grade 2012-13 % proficient or above', \
			'Gifted - Math 6th Grade 2012-13 % proficient or above', \
			'Gifted - Read 7th Grade 2012-13 % proficient or above', \
			'Gifted - Math 7th Grade 2012-13 % proficient or above', \
			'Gifted - Read 8th Grade 2012-13 % proficient or above', \
			'Gifted - Math 8th Grade 2012-13 % proficient or above', \
			'Gifted - Science 8th grade 2012-13 % proficient or above', \
			'Gifted - Read OGT 2012-13 % proficient or above', \
			'Gifted - Math OGT 2012-13 % proficient or above', \
			'Gifted - Write OGT 2012-13 % proficient or above', \
			'Gifted - Social Studies OGT 2012-13 % proficient or above', \
			'Gifted - Science OGT 2012-13 % proficient or above', \
			'Gifted - Read 11th grade 2012-13 % at or above proficient', \
			'Gifted - Math 11th grade 2012-13 % at or above proficient', \
			'Gifted - Write 11th grade 2012-13 % at or above proficient', \
			'Gifted - Social Studies 11th grade 2012-13 % at or above proficient', \
			'Gifted - Science 11th grade 2012-13 % at or above proficient', \
			'Gifted - Attendance rate 2012-13', \
			'Gifted - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'Gifted - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'Gifted - Enrollment', \
			'Gifted - % of total enrollment', \
			'Nongifted - Read 3rd grade 2012-13 % proficient or above', \
			'Nongifted - Math 3rd grade 2012-13 % proficient or above', \
			'Nongifted - Read 4th Grade 2012-13 % proficient or above', \
			'Nongifted - Math 4th Grade 2012-13 % proficient or above', \
			'Nongifted - Read 5th grade 2012-13 % proficient or above', \
			'Nongifted - Math 5th grade 2012-13 % proficient or above', \
			'Nongifted - Science 5th grade 2012-13 % proficient or above', \
			'Nongifted - Read 6th Grade 2012-13 % proficient or above', \
			'Nongifted - Math 6th Grade 2012-13 % proficient or above', \
			'Nongifted - Read 7th Grade 2012-13 % proficient or above', \
			'Nongifted - Math 7th Grade 2012-13 % proficient or above', \
			'Nongifted - Read 8th Grade 2012-13 % proficient or above', \
			'Nongifted - Math 8th Grade 2012-13 % proficient or above', \
			'Nongifted - Science 8th grade 2012-13 % proficient or above', \
			'Nongifted - Read OGT 2012-13 % proficient or above', \
			'Nongifted - Math OGT 2012-13 % proficient or above', \
			'Nongifted - Write OGT 2012-13 % proficient or above', \
			'Nongifted - Social Studies OGT 2012-13 % proficient or above', \
			'Nongifted - Science OGT 2012-13 % proficient or above', \
			'Nongifted - Read 11th grade 2012-13 % at or above proficient', \
			'Nongifted - Math 11th grade 2012-13 % at or above proficient', \
			'Nongifted - Write 11th grade 2012-13 % at or above proficient', \
			'Nongifted - Social Studies 11th grade 2012-13 % at or above proficient', \
			'Nongifted - Science 11th grade 2012-13 % at or above proficient', \
			'Nongifted - Attendance rate 2012-13', \
			'Nongifted - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'Nongifted - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'Nongifted - Enrollment', \
			'Nongifted - % of total enrollment']
		for each in headers:
			each			= clean(each)
	if header_row:
		curr_cell			= -1
		while curr_cell < num_cells:
			curr_cell 		+= 1
			cell_value 		= str(worksheet.cell_value(curr_row, curr_cell))
			headers.append(cell_value)
	elif not(footer_row):
		row				= worksheet.row_values(curr_row)
		if len(row[0]) < 1:
			footer_row		= True
		else:
			wr.writerow(row)
			school_IRN			= worksheet.cell_value(curr_row, 0)
			if type(school_IRN) is float:
				school_IRN		= str(round(school_IRN)).rstrip('0').rstrip('.')
			school_IRN			= school_IRN.zfill(6)

			curr_cell			= 9
			while curr_cell < num_cells:
				curr_cell 		+= 1
				row_type		= worksheet.cell_value(curr_row, 9)
				cell_value 		= clean(worksheet.cell_value(curr_row, curr_cell))
				if row_type == 'Gifted':
					row_constant	= -10
					enroll_percent	= worksheet.cell_value(curr_row, 38)
					if type(enroll_percent) is float:
						charters[school_IRN]['% gifted'] = '%.1f' % enroll_percent
					else:
						charters[school_IRN]['% gifted'] = enroll_percent

				else:
					row_constant	= 19
				header			= headers[curr_cell + row_constant]
				if school_IRN in charters:
					charters[school_IRN][header]			= cell_value
				else:
					charters[school_IRN]				= {}
					charters[school_IRN][header]			= cell_value

write_file.close()

# District Gifted Data

filename	= 'District Gifted Data'
xls_file	= xls_path + 'RAW' + ' ' + filename + '.xls'
workbook	= xlrd.open_workbook(xls_file)

worksheet 	= workbook.sheet_by_name('DIST_GIFTED_13')

# Two rows per charter

csv_file	= csv_path + filename + '.csv'
write_file	= open(csv_file, 'w')
wr 		= csv.writer(write_file, quoting=csv.QUOTE_ALL)

num_rows 					= worksheet.nrows - 1
num_cells 					= worksheet.ncols - 1
curr_row 					= -1
header_row					= True
headers						= []
footer_row					= False

while curr_row < num_rows:
	curr_row 				+= 1
	if curr_row == 1:
		header_row 			= False
		for each in headers:
			each			= clean(each)
		wr.writerow(headers)
		headers = [ \
			'Gifted - Read 3rd grade 2012-13 % proficient or above', \
			'Gifted - Math 3rd grade 2012-13 % proficient or above', \
			'Gifted - Read 4th Grade 2012-13 % proficient or above', \
			'Gifted - Math 4th Grade 2012-13 % proficient or above', \
			'Gifted - Read 5th grade 2012-13 % proficient or above', \
			'Gifted - Math 5th grade 2012-13 % proficient or above', \
			'Gifted - Science 5th grade 2012-13 % proficient or above', \
			'Gifted - Read 6th Grade 2012-13 % proficient or above', \
			'Gifted - Math 6th Grade 2012-13 % proficient or above', \
			'Gifted - Read 7th Grade 2012-13 % proficient or above', \
			'Gifted - Math 7th Grade 2012-13 % proficient or above', \
			'Gifted - Read 8th Grade 2012-13 % proficient or above', \
			'Gifted - Math 8th Grade 2012-13 % proficient or above', \
			'Gifted - Science 8th grade 2012-13 % proficient or above', \
			'Gifted - Read OGT 2012-13 % proficient or above', \
			'Gifted - Math OGT 2012-13 % proficient or above', \
			'Gifted - Write OGT 2012-13 % proficient or above', \
			'Gifted - Social Studies OGT 2012-13 % proficient or above', \
			'Gifted - Science OGT 2012-13 % proficient or above', \
			'Gifted - Read 11th grade 2012-13 % at or above proficient', \
			'Gifted - Math 11th grade 2012-13 % at or above proficient', \
			'Gifted - Write 11th grade 2012-13 % at or above proficient', \
			'Gifted - Social Studies 11th grade 2012-13 % at or above proficient', \
			'Gifted - Science 11th grade 2012-13 % at or above proficient', \
			'Gifted - Attendance rate 2012-13', \
			'Gifted - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'Gifted - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'Gifted - Enrollment', \
			'Gifted - % of total enrollment', \
			'Nongifted - Read 3rd grade 2012-13 % proficient or above', \
			'Nongifted - Math 3rd grade 2012-13 % proficient or above', \
			'Nongifted - Read 4th Grade 2012-13 % proficient or above', \
			'Nongifted - Math 4th Grade 2012-13 % proficient or above', \
			'Nongifted - Read 5th grade 2012-13 % proficient or above', \
			'Nongifted - Math 5th grade 2012-13 % proficient or above', \
			'Nongifted - Science 5th grade 2012-13 % proficient or above', \
			'Nongifted - Read 6th Grade 2012-13 % proficient or above', \
			'Nongifted - Math 6th Grade 2012-13 % proficient or above', \
			'Nongifted - Read 7th Grade 2012-13 % proficient or above', \
			'Nongifted - Math 7th Grade 2012-13 % proficient or above', \
			'Nongifted - Read 8th Grade 2012-13 % proficient or above', \
			'Nongifted - Math 8th Grade 2012-13 % proficient or above', \
			'Nongifted - Science 8th grade 2012-13 % proficient or above', \
			'Nongifted - Read OGT 2012-13 % proficient or above', \
			'Nongifted - Math OGT 2012-13 % proficient or above', \
			'Nongifted - Write OGT 2012-13 % proficient or above', \
			'Nongifted - Social Studies OGT 2012-13 % proficient or above', \
			'Nongifted - Science OGT 2012-13 % proficient or above', \
			'Nongifted - Read 11th grade 2012-13 % at or above proficient', \
			'Nongifted - Math 11th grade 2012-13 % at or above proficient', \
			'Nongifted - Write 11th grade 2012-13 % at or above proficient', \
			'Nongifted - Social Studies 11th grade 2012-13 % at or above proficient', \
			'Nongifted - Science 11th grade 2012-13 % at or above proficient', \
			'Nongifted - Attendance rate 2012-13', \
			'Nongifted - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'Nongifted - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'Nongifted - Enrollment', \
			'Nongifted - % of total enrollment']
		for each in headers:
			each			= clean(each)
	if header_row:
		curr_cell			= -1
		while curr_cell < num_cells:
			curr_cell 		+= 1
			cell_value 		= str(worksheet.cell_value(curr_row, curr_cell))
			headers.append(cell_value)
	elif not(footer_row):
		row				= worksheet.row_values(curr_row)
		if len(row[0]) < 1:
			footer_row		= True
		else:
			wr.writerow(row)
			district_IRN			= worksheet.cell_value(curr_row, 0)
			if type(district_IRN) is float:
				district_IRN		= str(round(district_IRN)).rstrip('0').rstrip('.')
			district_IRN			= district_IRN.zfill(6)

			curr_cell			= 4
			while curr_cell < num_cells:
				curr_cell 		+= 1
				row_type		= worksheet.cell_value(curr_row, 4)
				cell_value 		= clean(worksheet.cell_value(curr_row, curr_cell))
				if row_type == 'Gifted':
					row_constant	= -5
					enroll_percent	= worksheet.cell_value(curr_row, 33)
					if type(enroll_percent) is float:
						districts[district_IRN]['% gifted'] = '%.1f' % enroll_percent
					else:
						districts[district_IRN]['% gifted'] = enroll_percent
				else:
					row_constant	= 24
				header			= headers[curr_cell + row_constant]
				if district_IRN in districts:
					districts[district_IRN][header]			= cell_value
				else:
					districts[district_IRN]				= {}
					districts[district_IRN][header]			= cell_value

write_file.close()


##################### LEP DATA ########################

# Charter LEP Data

filename	= 'Charter LEP Data'
xls_file	= xls_path + 'RAW' + ' ' + filename + '.xls'
workbook	= xlrd.open_workbook(xls_file)

worksheet 	= workbook.sheet_by_name('BLDG_LEP_13')

# Two rows per charter

csv_file	= csv_path + filename + '.csv'
write_file	= open(csv_file, 'w')
wr 		= csv.writer(write_file, quoting=csv.QUOTE_ALL)

num_rows 					= worksheet.nrows - 1
num_cells 					= worksheet.ncols - 1
curr_row 					= -1
header_row					= True
headers						= []
footer_row					= False

while curr_row < num_rows:
	curr_row 				+= 1
	if curr_row == 1:
		header_row 			= False
		for each in headers:
			each			= clean(each)
		wr.writerow(headers)
		headers = [ \
			'LEP - Read 3rd grade 2012-13 % proficient or above', \
			'LEP - Math 3rd grade 2012-13 % proficient or above', \
			'LEP - Read 4th Grade 2012-13 % proficient or above', \
			'LEP - Math 4th Grade 2012-13 % proficient or above', \
			'LEP - Read 5th grade 2012-13 % proficient or above', \
			'LEP - Math 5th grade 2012-13 % proficient or above', \
			'LEP - Science 5th grade 2012-13 % proficient or above', \
			'LEP - Read 6th Grade 2012-13 % proficient or above', \
			'LEP - Math 6th Grade 2012-13 % proficient or above', \
			'LEP - Read 7th Grade 2012-13 % proficient or above', \
			'LEP - Math 7th Grade 2012-13 % proficient or above', \
			'LEP - Read 8th Grade 2012-13 % proficient or above', \
			'LEP - Math 8th Grade 2012-13 % proficient or above', \
			'LEP - Science 8th grade 2012-13 % proficient or above', \
			'LEP - Read OGT 2012-13 % proficient or above', \
			'LEP - Math OGT 2012-13 % proficient or above', \
			'LEP - Write OGT 2012-13 % proficient or above', \
			'LEP - Social Studies OGT 2012-13 % proficient or above', \
			'LEP - Science OGT 2012-13 % proficient or above', \
			'LEP - Read 11th grade 2012-13 % at or above proficient', \
			'LEP - Math 11th grade 2012-13 % at or above proficient', \
			'LEP - Write 11th grade 2012-13 % at or above proficient', \
			'LEP - Social Studies 11th grade 2012-13 % at or above proficient', \
			'LEP - Science 11th grade 2012-13 % at or above proficient', \
			'LEP - Attendance rate 2012-13', \
			'LEP - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'LEP - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'LEP - Enrollment', \
			'LEP - % of total enrollment', \
			'NonLEP - Read 3rd grade 2012-13 % proficient or above', \
			'NonLEP - Math 3rd grade 2012-13 % proficient or above', \
			'NonLEP - Read 4th Grade 2012-13 % proficient or above', \
			'NonLEP - Math 4th Grade 2012-13 % proficient or above', \
			'NonLEP - Read 5th grade 2012-13 % proficient or above', \
			'NonLEP - Math 5th grade 2012-13 % proficient or above', \
			'NonLEP - Science 5th grade 2012-13 % proficient or above', \
			'NonLEP - Read 6th Grade 2012-13 % proficient or above', \
			'NonLEP - Math 6th Grade 2012-13 % proficient or above', \
			'NonLEP - Read 7th Grade 2012-13 % proficient or above', \
			'NonLEP - Math 7th Grade 2012-13 % proficient or above', \
			'NonLEP - Read 8th Grade 2012-13 % proficient or above', \
			'NonLEP - Math 8th Grade 2012-13 % proficient or above', \
			'NonLEP - Science 8th grade 2012-13 % proficient or above', \
			'NonLEP - Read OGT 2012-13 % proficient or above', \
			'NonLEP - Math OGT 2012-13 % proficient or above', \
			'NonLEP - Write OGT 2012-13 % proficient or above', \
			'NonLEP - Social Studies OGT 2012-13 % proficient or above', \
			'NonLEP - Science OGT 2012-13 % proficient or above', \
			'NonLEP - Read 11th grade 2012-13 % at or above proficient', \
			'NonLEP - Math 11th grade 2012-13 % at or above proficient', \
			'NonLEP - Write 11th grade 2012-13 % at or above proficient', \
			'NonLEP - Social Studies 11th grade 2012-13 % at or above proficient', \
			'NonLEP - Science 11th grade 2012-13 % at or above proficient', \
			'NonLEP - Attendance rate 2012-13', \
			'NonLEP - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'NonLEP - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'NonLEP - Enrollment', \
			'NonLEP - % of total enrollment']
		for each in headers:
			each			= clean(each)
	if header_row:
		curr_cell			= -1
		while curr_cell < num_cells:
			curr_cell 		+= 1
			cell_value 		= str(worksheet.cell_value(curr_row, curr_cell))
			headers.append(cell_value)
	elif not(footer_row):
		row				= worksheet.row_values(curr_row)
		if len(row[0]) < 1:
			footer_row		= True
		else:
			wr.writerow(row)
			school_IRN			= worksheet.cell_value(curr_row, 0)
			if type(school_IRN) is float:
				school_IRN		= str(round(school_IRN)).rstrip('0').rstrip('.')
			school_IRN			= school_IRN.zfill(6)

			curr_cell			= 9
			while curr_cell < num_cells:
				curr_cell 		+= 1
				row_type		= worksheet.cell_value(curr_row, 9)
				cell_value 		= clean(worksheet.cell_value(curr_row, curr_cell))
				if row_type == 'LEP':
					row_constant	= -10
				else:
					row_constant	= 19
				header			= headers[curr_cell + row_constant]
				if school_IRN in charters:
					charters[school_IRN][header]			= cell_value
				else:
					charters[school_IRN]				= {}
					charters[school_IRN][header]			= cell_value

write_file.close()

# District LEP Data

filename	= 'District LEP Data'
xls_file	= xls_path + 'RAW' + ' ' + filename + '.xls'
workbook	= xlrd.open_workbook(xls_file)

worksheet 	= workbook.sheet_by_name('DIST_LEP_13')

# Two rows per charter

csv_file	= csv_path + filename + '.csv'
write_file	= open(csv_file, 'w')
wr 		= csv.writer(write_file, quoting=csv.QUOTE_ALL)

num_rows 					= worksheet.nrows - 1
num_cells 					= worksheet.ncols - 1
curr_row 					= -1
header_row					= True
headers						= []
footer_row					= False

while curr_row < num_rows:
	curr_row 				+= 1
	if curr_row == 1:
		header_row 			= False
		for each in headers:
			each			= clean(each)
		wr.writerow(headers)
		headers = [ \
			'LEP - Read 3rd grade 2012-13 % proficient or above', \
			'LEP - Math 3rd grade 2012-13 % proficient or above', \
			'LEP - Read 4th Grade 2012-13 % proficient or above', \
			'LEP - Math 4th Grade 2012-13 % proficient or above', \
			'LEP - Read 5th grade 2012-13 % proficient or above', \
			'LEP - Math 5th grade 2012-13 % proficient or above', \
			'LEP - Science 5th grade 2012-13 % proficient or above', \
			'LEP - Read 6th Grade 2012-13 % proficient or above', \
			'LEP - Math 6th Grade 2012-13 % proficient or above', \
			'LEP - Read 7th Grade 2012-13 % proficient or above', \
			'LEP - Math 7th Grade 2012-13 % proficient or above', \
			'LEP - Read 8th Grade 2012-13 % proficient or above', \
			'LEP - Math 8th Grade 2012-13 % proficient or above', \
			'LEP - Science 8th grade 2012-13 % proficient or above', \
			'LEP - Read OGT 2012-13 % proficient or above', \
			'LEP - Math OGT 2012-13 % proficient or above', \
			'LEP - Write OGT 2012-13 % proficient or above', \
			'LEP - Social Studies OGT 2012-13 % proficient or above', \
			'LEP - Science OGT 2012-13 % proficient or above', \
			'LEP - Read 11th grade 2012-13 % at or above proficient', \
			'LEP - Math 11th grade 2012-13 % at or above proficient', \
			'LEP - Write 11th grade 2012-13 % at or above proficient', \
			'LEP - Social Studies 11th grade 2012-13 % at or above proficient', \
			'LEP - Science 11th grade 2012-13 % at or above proficient', \
			'LEP - Attendance rate 2012-13', \
			'LEP - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'LEP - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'LEP - Enrollment', \
			'LEP - % of total enrollment', \
			'NonLEP - Read 3rd grade 2012-13 % proficient or above', \
			'NonLEP - Math 3rd grade 2012-13 % proficient or above', \
			'NonLEP - Read 4th Grade 2012-13 % proficient or above', \
			'NonLEP - Math 4th Grade 2012-13 % proficient or above', \
			'NonLEP - Read 5th grade 2012-13 % proficient or above', \
			'NonLEP - Math 5th grade 2012-13 % proficient or above', \
			'NonLEP - Science 5th grade 2012-13 % proficient or above', \
			'NonLEP - Read 6th Grade 2012-13 % proficient or above', \
			'NonLEP - Math 6th Grade 2012-13 % proficient or above', \
			'NonLEP - Read 7th Grade 2012-13 % proficient or above', \
			'NonLEP - Math 7th Grade 2012-13 % proficient or above', \
			'NonLEP - Read 8th Grade 2012-13 % proficient or above', \
			'NonLEP - Math 8th Grade 2012-13 % proficient or above', \
			'NonLEP - Science 8th grade 2012-13 % proficient or above', \
			'NonLEP - Read OGT 2012-13 % proficient or above', \
			'NonLEP - Math OGT 2012-13 % proficient or above', \
			'NonLEP - Write OGT 2012-13 % proficient or above', \
			'NonLEP - Social Studies OGT 2012-13 % proficient or above', \
			'NonLEP - Science OGT 2012-13 % proficient or above', \
			'NonLEP - Read 11th grade 2012-13 % at or above proficient', \
			'NonLEP - Math 11th grade 2012-13 % at or above proficient', \
			'NonLEP - Write 11th grade 2012-13 % at or above proficient', \
			'NonLEP - Social Studies 11th grade 2012-13 % at or above proficient', \
			'NonLEP - Science 11th grade 2012-13 % at or above proficient', \
			'NonLEP - Attendance rate 2012-13', \
			'NonLEP - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'NonLEP - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'NonLEP - Enrollment', \
			'NonLEP - % of total enrollment']
		for each in headers:
			each			= clean(each)
	if header_row:
		curr_cell			= -1
		while curr_cell < num_cells:
			curr_cell 		+= 1
			cell_value 		= str(worksheet.cell_value(curr_row, curr_cell))
			headers.append(cell_value)
	elif not(footer_row):
		row				= worksheet.row_values(curr_row)
		if len(row[0]) < 1:
			footer_row		= True
		else:
			wr.writerow(row)
			district_IRN			= worksheet.cell_value(curr_row, 0)
			if type(district_IRN) is float:
				district_IRN		= str(round(district_IRN)).rstrip('0').rstrip('.')
			district_IRN			= district_IRN.zfill(6)

			curr_cell			= 4
			while curr_cell < num_cells:
				curr_cell 		+= 1
				row_type		= worksheet.cell_value(curr_row, 4)
				cell_value 		= clean(worksheet.cell_value(curr_row, curr_cell))
				if row_type == 'LEP':
					row_constant	= -5
				else:
					row_constant	= 24
				header			= headers[curr_cell + row_constant]
				if district_IRN in districts:
					districts[district_IRN][header]			= cell_value
				else:
					districts[district_IRN]				= {}
					districts[district_IRN][header]			= cell_value

write_file.close()


############ ECONOMICALLY DISADVANTAGED DATA ##########

# Charter Economically Disadvantaged Data

filename	= 'Charter Economically Disadvantaged Data'
xls_file	= xls_path + 'RAW' + ' ' + filename + '.xls'
workbook	= xlrd.open_workbook(xls_file)

worksheet 	= workbook.sheet_by_name('BLDG_ECONOMIC_13')

# Two rows per charter

csv_file	= csv_path + filename + '.csv'
write_file	= open(csv_file, 'w')
wr 		= csv.writer(write_file, quoting=csv.QUOTE_ALL)

num_rows 					= worksheet.nrows - 1
num_cells 					= worksheet.ncols - 1
curr_row 					= -1
header_row					= True
headers						= []
footer_row					= False

while curr_row < num_rows:
	curr_row 				+= 1
	if curr_row == 1:
		header_row 			= False
		for each in headers:
			each			= clean(each)
		wr.writerow(headers)
		headers = [ \
			'Disadvantaged - Read 3rd grade 2012-13 % proficient or above', \
			'Disadvantaged - Math 3rd grade 2012-13 % proficient or above', \
			'Disadvantaged - Read 4th Grade 2012-13 % proficient or above', \
			'Disadvantaged - Math 4th Grade 2012-13 % proficient or above', \
			'Disadvantaged - Read 5th grade 2012-13 % proficient or above', \
			'Disadvantaged - Math 5th grade 2012-13 % proficient or above', \
			'Disadvantaged - Science 5th grade 2012-13 % proficient or above', \
			'Disadvantaged - Read 6th Grade 2012-13 % proficient or above', \
			'Disadvantaged - Math 6th Grade 2012-13 % proficient or above', \
			'Disadvantaged - Read 7th Grade 2012-13 % proficient or above', \
			'Disadvantaged - Math 7th Grade 2012-13 % proficient or above', \
			'Disadvantaged - Read 8th Grade 2012-13 % proficient or above', \
			'Disadvantaged - Math 8th Grade 2012-13 % proficient or above', \
			'Disadvantaged - Science 8th grade 2012-13 % proficient or above', \
			'Disadvantaged - Read OGT 2012-13 % proficient or above', \
			'Disadvantaged - Math OGT 2012-13 % proficient or above', \
			'Disadvantaged - Write OGT 2012-13 % proficient or above', \
			'Disadvantaged - Social Studies OGT 2012-13 % proficient or above', \
			'Disadvantaged - Science OGT 2012-13 % proficient or above', \
			'Disadvantaged - Read 11th grade 2012-13 % at or above proficient', \
			'Disadvantaged - Math 11th grade 2012-13 % at or above proficient', \
			'Disadvantaged - Write 11th grade 2012-13 % at or above proficient', \
			'Disadvantaged - Social Studies 11th grade 2012-13 % at or above proficient', \
			'Disadvantaged - Science 11th grade 2012-13 % at or above proficient', \
			'Disadvantaged - Attendance rate 2012-13', \
			'Disadvantaged - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'Disadvantaged - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'Disadvantaged - Enrollment', \
			'Disadvantaged - % of total enrollment', \
			'Nondisadvantaged - Read 3rd grade 2012-13 % proficient or above', \
			'Nondisadvantaged - Math 3rd grade 2012-13 % proficient or above', \
			'Nondisadvantaged - Read 4th Grade 2012-13 % proficient or above', \
			'Nondisadvantaged - Math 4th Grade 2012-13 % proficient or above', \
			'Nondisadvantaged - Read 5th grade 2012-13 % proficient or above', \
			'Nondisadvantaged - Math 5th grade 2012-13 % proficient or above', \
			'Nondisadvantaged - Science 5th grade 2012-13 % proficient or above', \
			'Nondisadvantaged - Read 6th Grade 2012-13 % proficient or above', \
			'Nondisadvantaged - Math 6th Grade 2012-13 % proficient or above', \
			'Nondisadvantaged - Read 7th Grade 2012-13 % proficient or above', \
			'Nondisadvantaged - Math 7th Grade 2012-13 % proficient or above', \
			'Nondisadvantaged - Read 8th Grade 2012-13 % proficient or above', \
			'Nondisadvantaged - Math 8th Grade 2012-13 % proficient or above', \
			'Nondisadvantaged - Science 8th grade 2012-13 % proficient or above', \
			'Nondisadvantaged - Read OGT 2012-13 % proficient or above', \
			'Nondisadvantaged - Math OGT 2012-13 % proficient or above', \
			'Nondisadvantaged - Write OGT 2012-13 % proficient or above', \
			'Nondisadvantaged - Social Studies OGT 2012-13 % proficient or above', \
			'Nondisadvantaged - Science OGT 2012-13 % proficient or above', \
			'Nondisadvantaged - Read 11th grade 2012-13 % at or above proficient', \
			'Nondisadvantaged - Math 11th grade 2012-13 % at or above proficient', \
			'Nondisadvantaged - Write 11th grade 2012-13 % at or above proficient', \
			'Nondisadvantaged - Social Studies 11th grade 2012-13 % at or above proficient', \
			'Nondisadvantaged - Science 11th grade 2012-13 % at or above proficient', \
			'Nondisadvantaged - Attendance rate 2012-13', \
			'Nondisadvantaged - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'Nondisadvantaged - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'Nondisadvantaged - Enrollment', \
			'Nondisadvantaged - % of total enrollment']
		for each in headers:
			each			= clean(each)
	if header_row:
		curr_cell			= -1
		while curr_cell < num_cells:
			curr_cell 		+= 1
			cell_value 		= str(worksheet.cell_value(curr_row, curr_cell))
			headers.append(cell_value)
	elif not(footer_row):
		row				= worksheet.row_values(curr_row)
		if len(row[0]) < 1:
			footer_row		= True
		else:
			wr.writerow(row)
			school_IRN			= worksheet.cell_value(curr_row, 0)
			school_IRN			= fixIRN(school_IRN)

			curr_cell			= 9
			while curr_cell < num_cells:
				curr_cell 		+= 1
				row_type		= worksheet.cell_value(curr_row, 9)
				cell_value 		= clean(worksheet.cell_value(curr_row, curr_cell))
				if row_type == 'Disadvantaged':
					row_constant	= -10
					enroll_percent	= worksheet.cell_value(curr_row, 38)
					if type(enroll_percent) is float:
						charters[school_IRN]['% of kids in poverty'] = '%.1f' % enroll_percent
					else:
						charters[school_IRN]['% of kids in poverty'] = enroll_percent
				else:
					row_constant	= 19
				header			= headers[curr_cell + row_constant]
				if school_IRN in charters:
					charters[school_IRN][header]			= cell_value
				else:
					charters[school_IRN]				= {}
					charters[school_IRN][header]			= cell_value


write_file.close()

# District Economically Disadvantaged Data

filename	= 'District Economically Disadvantaged Data'
xls_file	= xls_path + 'RAW' + ' ' + filename + '.xls'
workbook	= xlrd.open_workbook(xls_file)

worksheet 	= workbook.sheet_by_name('DIST_ECONOMIC_13')

# Two rows per charter

csv_file	= csv_path + filename + '.csv'
write_file	= open(csv_file, 'w')
wr 		= csv.writer(write_file, quoting=csv.QUOTE_ALL)

num_rows 					= worksheet.nrows - 1
num_cells 					= worksheet.ncols - 1
curr_row 					= -1
header_row					= True
headers						= []
footer_row					= False

while curr_row < num_rows:
	curr_row 				+= 1
	if curr_row == 1:
		header_row 			= False
		for each in headers:
			each			= clean(each)
		wr.writerow(headers)
		headers = [ \
			'Disadvantaged - Read 3rd grade 2012-13 % proficient or above', \
			'Disadvantaged - Math 3rd grade 2012-13 % proficient or above', \
			'Disadvantaged - Read 4th Grade 2012-13 % proficient or above', \
			'Disadvantaged - Math 4th Grade 2012-13 % proficient or above', \
			'Disadvantaged - Read 5th grade 2012-13 % proficient or above', \
			'Disadvantaged - Math 5th grade 2012-13 % proficient or above', \
			'Disadvantaged - Science 5th grade 2012-13 % proficient or above', \
			'Disadvantaged - Read 6th Grade 2012-13 % proficient or above', \
			'Disadvantaged - Math 6th Grade 2012-13 % proficient or above', \
			'Disadvantaged - Read 7th Grade 2012-13 % proficient or above', \
			'Disadvantaged - Math 7th Grade 2012-13 % proficient or above', \
			'Disadvantaged - Read 8th Grade 2012-13 % proficient or above', \
			'Disadvantaged - Math 8th Grade 2012-13 % proficient or above', \
			'Disadvantaged - Science 8th grade 2012-13 % proficient or above', \
			'Disadvantaged - Read OGT 2012-13 % proficient or above', \
			'Disadvantaged - Math OGT 2012-13 % proficient or above', \
			'Disadvantaged - Write OGT 2012-13 % proficient or above', \
			'Disadvantaged - Social Studies OGT 2012-13 % proficient or above', \
			'Disadvantaged - Science OGT 2012-13 % proficient or above', \
			'Disadvantaged - Read 11th grade 2012-13 % at or above proficient', \
			'Disadvantaged - Math 11th grade 2012-13 % at or above proficient', \
			'Disadvantaged - Write 11th grade 2012-13 % at or above proficient', \
			'Disadvantaged - Social Studies 11th grade 2012-13 % at or above proficient', \
			'Disadvantaged - Science 11th grade 2012-13 % at or above proficient', \
			'Disadvantaged - Attendance rate 2012-13', \
			'Disadvantaged - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'Disadvantaged - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'Disadvantaged - Enrollment', \
			'Disadvantaged - % of total enrollment', \
			'Nondisadvantaged - Read 3rd grade 2012-13 % proficient or above', \
			'Nondisadvantaged - Math 3rd grade 2012-13 % proficient or above', \
			'Nondisadvantaged - Read 4th Grade 2012-13 % proficient or above', \
			'Nondisadvantaged - Math 4th Grade 2012-13 % proficient or above', \
			'Nondisadvantaged - Read 5th grade 2012-13 % proficient or above', \
			'Nondisadvantaged - Math 5th grade 2012-13 % proficient or above', \
			'Nondisadvantaged - Science 5th grade 2012-13 % proficient or above', \
			'Nondisadvantaged - Read 6th Grade 2012-13 % proficient or above', \
			'Nondisadvantaged - Math 6th Grade 2012-13 % proficient or above', \
			'Nondisadvantaged - Read 7th Grade 2012-13 % proficient or above', \
			'Nondisadvantaged - Math 7th Grade 2012-13 % proficient or above', \
			'Nondisadvantaged - Read 8th Grade 2012-13 % proficient or above', \
			'Nondisadvantaged - Math 8th Grade 2012-13 % proficient or above', \
			'Nondisadvantaged - Science 8th grade 2012-13 % proficient or above', \
			'Nondisadvantaged - Read OGT 2012-13 % proficient or above', \
			'Nondisadvantaged - Math OGT 2012-13 % proficient or above', \
			'Nondisadvantaged - Write OGT 2012-13 % proficient or above', \
			'Nondisadvantaged - Social Studies OGT 2012-13 % proficient or above', \
			'Nondisadvantaged - Science OGT 2012-13 % proficient or above', \
			'Nondisadvantaged - Read 11th grade 2012-13 % at or above proficient', \
			'Nondisadvantaged - Math 11th grade 2012-13 % at or above proficient', \
			'Nondisadvantaged - Write 11th grade 2012-13 % at or above proficient', \
			'Nondisadvantaged - Social Studies 11th grade 2012-13 % at or above proficient', \
			'Nondisadvantaged - Science 11th grade 2012-13 % at or above proficient', \
			'Nondisadvantaged - Attendance rate 2012-13', \
			'Nondisadvantaged - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'Nondisadvantaged - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'Nondisadvantaged - Enrollment', \
			'Nondisadvantaged - % of total enrollment']
		for each in headers:
			each			= clean(each)
	if header_row:
		curr_cell			= -1
		while curr_cell < num_cells:
			curr_cell 		+= 1
			cell_value 		= str(worksheet.cell_value(curr_row, curr_cell))
			headers.append(cell_value)
	elif not(footer_row):
		row				= worksheet.row_values(curr_row)
		if len(row[0]) < 1:
			footer_row		= True
		else:
			wr.writerow(row)
			district_IRN			= worksheet.cell_value(curr_row, 0)
			if type(district_IRN) is float:
				district_IRN		= str(round(district_IRN)).rstrip('0').rstrip('.')
			district_IRN			= district_IRN.zfill(6)

			curr_cell			= 4
			while curr_cell < num_cells:
				curr_cell 		+= 1
				row_type		= worksheet.cell_value(curr_row, 4)
				cell_value 		= clean(worksheet.cell_value(curr_row, curr_cell))
				if row_type == 'Disadvantaged':
					row_constant	= -5
					if type(enroll_percent) is float:
						districts[district_IRN]['% of kids in poverty'] = '%.1f' % enroll_percent
					else:
						districts[district_IRN]['% of kids in poverty'] = enroll_percent
				else:
					row_constant	= 24
				header			= headers[curr_cell + row_constant]
				if district_IRN in districts:
					districts[district_IRN][header]			= cell_value
				else:
					districts[district_IRN]				= {}
					districts[district_IRN][header]			= cell_value

write_file.close()


##################### MOBILITY DATA ########################

# Charter Mobility Data

filename	= 'Charter Mobility Data'
xls_file	= xls_path + 'RAW' + ' ' + filename + '.xls'
workbook	= xlrd.open_workbook(xls_file)

worksheet 	= workbook.sheet_by_name('BLDG_MOBILE_13')

# Three rows per charter

csv_file	= csv_path + filename + '.csv'
write_file	= open(csv_file, 'w')
wr 		= csv.writer(write_file, quoting=csv.QUOTE_ALL)

num_rows 					= worksheet.nrows - 1
num_cells 					= worksheet.ncols - 1
curr_row 					= -1
header_row					= True
headers						= []
footer_row					= False

while curr_row < num_rows:
	curr_row 				+= 1
	if curr_row == 1:
		header_row 			= False
		for each in headers:
			each			= clean(each)
		wr.writerow(headers)
		headers = [ \
			'Longevity0 - Read 3rd grade 2012-13 % proficient or above', \
			'Longevity0 - Math 3rd grade 2012-13 % proficient or above', \
			'Longevity0 - Read 4th Grade 2012-13 % proficient or above', \
			'Longevity0 - Math 4th Grade 2012-13 % proficient or above', \
			'Longevity0 - Read 5th grade 2012-13 % proficient or above', \
			'Longevity0 - Math 5th grade 2012-13 % proficient or above', \
			'Longevity0 - Science 5th grade 2012-13 % proficient or above', \
			'Longevity0 - Read 6th Grade 2012-13 % proficient or above', \
			'Longevity0 - Math 6th Grade 2012-13 % proficient or above', \
			'Longevity0 - Read 7th Grade 2012-13 % proficient or above', \
			'Longevity0 - Math 7th Grade 2012-13 % proficient or above', \
			'Longevity0 - Read 8th Grade 2012-13 % proficient or above', \
			'Longevity0 - Math 8th Grade 2012-13 % proficient or above', \
			'Longevity0 - Science 8th grade 2012-13 % proficient or above', \
			'Longevity0 - Read OGT 2012-13 % proficient or above', \
			'Longevity0 - Math OGT 2012-13 % proficient or above', \
			'Longevity0 - Write OGT 2012-13 % proficient or above', \
			'Longevity0 - Social Studies OGT 2012-13 % proficient or above', \
			'Longevity0 - Science OGT 2012-13 % proficient or above', \
			'Longevity0 - Read 11th grade 2012-13 % at or above proficient', \
			'Longevity0 - Math 11th grade 2012-13 % at or above proficient', \
			'Longevity0 - Write 11th grade 2012-13 % at or above proficient', \
			'Longevity0 - Social Studies 11th grade 2012-13 % at or above proficient', \
			'Longevity0 - Science 11th grade 2012-13 % at or above proficient', \
			'Longevity0 - Attendance rate 2012-13', \
			'Longevity0 - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'Longevity0 - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'Longevity0 - Enrollment', \
			'Longevity0 - % of total enrollment', \
			'Longevity1to2 - Read 3rd grade 2012-13 % proficient or above', \
			'Longevity1to2 - Math 3rd grade 2012-13 % proficient or above', \
			'Longevity1to2 - Read 4th Grade 2012-13 % proficient or above', \
			'Longevity1to2 - Math 4th Grade 2012-13 % proficient or above', \
			'Longevity1to2 - Read 5th grade 2012-13 % proficient or above', \
			'Longevity1to2 - Math 5th grade 2012-13 % proficient or above', \
			'Longevity1to2 - Science 5th grade 2012-13 % proficient or above', \
			'Longevity1to2 - Read 6th Grade 2012-13 % proficient or above', \
			'Longevity1to2 - Math 6th Grade 2012-13 % proficient or above', \
			'Longevity1to2 - Read 7th Grade 2012-13 % proficient or above', \
			'Longevity1to2 - Math 7th Grade 2012-13 % proficient or above', \
			'Longevity1to2 - Read 8th Grade 2012-13 % proficient or above', \
			'Longevity1to2 - Math 8th Grade 2012-13 % proficient or above', \
			'Longevity1to2 - Science 8th grade 2012-13 % proficient or above', \
			'Longevity1to2 - Read OGT 2012-13 % proficient or above', \
			'Longevity1to2 - Math OGT 2012-13 % proficient or above', \
			'Longevity1to2 - Write OGT 2012-13 % proficient or above', \
			'Longevity1to2 - Social Studies OGT 2012-13 % proficient or above', \
			'Longevity1to2 - Science OGT 2012-13 % proficient or above', \
			'Longevity1to2 - Read 11th grade 2012-13 % at or above proficient', \
			'Longevity1to2 - Math 11th grade 2012-13 % at or above proficient', \
			'Longevity1to2 - Write 11th grade 2012-13 % at or above proficient', \
			'Longevity1to2 - Social Studies 11th grade 2012-13 % at or above proficient', \
			'Longevity1to2 - Science 11th grade 2012-13 % at or above proficient', \
			'Longevity1to2 - Attendance rate 2012-13', \
			'Longevity1to2 - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'Longevity1to2 - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'Longevity1to2 - Enrollment', \
			'Longevity1to2 - % of total enrollment', \
			'Longevity3orMore - Read 3rd grade 2012-13 % proficient or above', \
			'Longevity3orMore - Math 3rd grade 2012-13 % proficient or above', \
			'Longevity3orMore - Read 4th Grade 2012-13 % proficient or above', \
			'Longevity3orMore - Math 4th Grade 2012-13 % proficient or above', \
			'Longevity3orMore - Read 5th grade 2012-13 % proficient or above', \
			'Longevity3orMore - Math 5th grade 2012-13 % proficient or above', \
			'Longevity3orMore - Science 5th grade 2012-13 % proficient or above', \
			'Longevity3orMore - Read 6th Grade 2012-13 % proficient or above', \
			'Longevity3orMore - Math 6th Grade 2012-13 % proficient or above', \
			'Longevity3orMore - Read 7th Grade 2012-13 % proficient or above', \
			'Longevity3orMore - Math 7th Grade 2012-13 % proficient or above', \
			'Longevity3orMore - Read 8th Grade 2012-13 % proficient or above', \
			'Longevity3orMore - Math 8th Grade 2012-13 % proficient or above', \
			'Longevity3orMore - Science 8th grade 2012-13 % proficient or above', \
			'Longevity3orMore - Read OGT 2012-13 % proficient or above', \
			'Longevity3orMore - Math OGT 2012-13 % proficient or above', \
			'Longevity3orMore - Write OGT 2012-13 % proficient or above', \
			'Longevity3orMore - Social Studies OGT 2012-13 % proficient or above', \
			'Longevity3orMore - Science OGT 2012-13 % proficient or above', \
			'Longevity3orMore - Read 11th grade 2012-13 % at or above proficient', \
			'Longevity3orMore - Math 11th grade 2012-13 % at or above proficient', \
			'Longevity3orMore - Write 11th grade 2012-13 % at or above proficient', \
			'Longevity3orMore - Social Studies 11th grade 2012-13 % at or above proficient', \
			'Longevity3orMore - Science 11th grade 2012-13 % at or above proficient', \
			'Longevity3orMore - Attendance rate 2012-13', \
			'Longevity3orMore - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'Longevity3orMore - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'Longevity3orMore - Enrollment', \
			'Longevity3orMore - % of total enrollment']
		for each in headers:
			each			= clean(each)
	if header_row:
		curr_cell			= -1
		while curr_cell < num_cells:
			curr_cell 		+= 1
			cell_value 		= str(worksheet.cell_value(curr_row, curr_cell))
			headers.append(cell_value)
	elif not(footer_row):
		row				= worksheet.row_values(curr_row)
		if len(row[0]) < 1:
			footer_row		= True
		else:
			wr.writerow(row)
			school_IRN			= worksheet.cell_value(curr_row, 0)
			if type(school_IRN) is float:
				school_IRN		= str(round(school_IRN)).rstrip('0').rstrip('.')
			school_IRN			= school_IRN.zfill(6)

			curr_cell			= 9
			while curr_cell < num_cells:
				curr_cell 		+= 1
				row_type		= worksheet.cell_value(curr_row, 9)
				cell_value 		= clean(worksheet.cell_value(curr_row, curr_cell))
				if row_type == 'Longevity0':
					row_constant	= -10
				elif row_type == 'Longevity1to2':
					row_constant	= 19					
				else:
					row_constant	= 48
					enroll_percent	= worksheet.cell_value(curr_row, 38)
					try:
						enroll_percent	= float(enroll_percent)
					except:
						pass
					if type(enroll_percent) is float:
						enroll_percent	= 100 - enroll_percent
						charters[school_IRN]['% enrolled less than 3 years'] = '%.1f' % enroll_percent
						charters[school_IRN]['% of kids in poverty'] = '%.1f' % enroll_percent

				header			= headers[curr_cell + row_constant]
				if school_IRN in charters:
					charters[school_IRN][header]			= cell_value
				else:
					charters[school_IRN]				= {}
					charters[school_IRN][header]			= cell_value

write_file.close()

# District Mobility Data

filename	= 'District Mobility Data'
xls_file	= xls_path + 'RAW' + ' ' + filename + '.xls'
workbook	= xlrd.open_workbook(xls_file)

worksheet 	= workbook.sheet_by_name('DIST_MOBILE_13')

# Three rows per district

csv_file	= csv_path + filename + '.csv'
write_file	= open(csv_file, 'w')
wr 		= csv.writer(write_file, quoting=csv.QUOTE_ALL)

num_rows 					= worksheet.nrows - 1
num_cells 					= worksheet.ncols - 1
curr_row 					= -1
header_row					= True
headers						= []
footer_row					= False

while curr_row < num_rows:
	curr_row 				+= 1
	if curr_row == 1:
		header_row 			= False
		for each in headers:
			each			= clean(each)
		wr.writerow(headers)
		headers = [ \
			'Longevity0 - Read 3rd grade 2012-13 % proficient or above', \
			'Longevity0 - Math 3rd grade 2012-13 % proficient or above', \
			'Longevity0 - Read 4th Grade 2012-13 % proficient or above', \
			'Longevity0 - Math 4th Grade 2012-13 % proficient or above', \
			'Longevity0 - Read 5th grade 2012-13 % proficient or above', \
			'Longevity0 - Math 5th grade 2012-13 % proficient or above', \
			'Longevity0 - Science 5th grade 2012-13 % proficient or above', \
			'Longevity0 - Read 6th Grade 2012-13 % proficient or above', \
			'Longevity0 - Math 6th Grade 2012-13 % proficient or above', \
			'Longevity0 - Read 7th Grade 2012-13 % proficient or above', \
			'Longevity0 - Math 7th Grade 2012-13 % proficient or above', \
			'Longevity0 - Read 8th Grade 2012-13 % proficient or above', \
			'Longevity0 - Math 8th Grade 2012-13 % proficient or above', \
			'Longevity0 - Science 8th grade 2012-13 % proficient or above', \
			'Longevity0 - Read OGT 2012-13 % proficient or above', \
			'Longevity0 - Math OGT 2012-13 % proficient or above', \
			'Longevity0 - Write OGT 2012-13 % proficient or above', \
			'Longevity0 - Social Studies OGT 2012-13 % proficient or above', \
			'Longevity0 - Science OGT 2012-13 % proficient or above', \
			'Longevity0 - Read 11th grade 2012-13 % at or above proficient', \
			'Longevity0 - Math 11th grade 2012-13 % at or above proficient', \
			'Longevity0 - Write 11th grade 2012-13 % at or above proficient', \
			'Longevity0 - Social Studies 11th grade 2012-13 % at or above proficient', \
			'Longevity0 - Science 11th grade 2012-13 % at or above proficient', \
			'Longevity0 - Attendance rate 2012-13', \
			'Longevity0 - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'Longevity0 - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'Longevity0 - Enrollment', \
			'Longevity0 - % of total enrollment', \
			'Longevity1to2 - Read 3rd grade 2012-13 % proficient or above', \
			'Longevity1to2 - Math 3rd grade 2012-13 % proficient or above', \
			'Longevity1to2 - Read 4th Grade 2012-13 % proficient or above', \
			'Longevity1to2 - Math 4th Grade 2012-13 % proficient or above', \
			'Longevity1to2 - Read 5th grade 2012-13 % proficient or above', \
			'Longevity1to2 - Math 5th grade 2012-13 % proficient or above', \
			'Longevity1to2 - Science 5th grade 2012-13 % proficient or above', \
			'Longevity1to2 - Read 6th Grade 2012-13 % proficient or above', \
			'Longevity1to2 - Math 6th Grade 2012-13 % proficient or above', \
			'Longevity1to2 - Read 7th Grade 2012-13 % proficient or above', \
			'Longevity1to2 - Math 7th Grade 2012-13 % proficient or above', \
			'Longevity1to2 - Read 8th Grade 2012-13 % proficient or above', \
			'Longevity1to2 - Math 8th Grade 2012-13 % proficient or above', \
			'Longevity1to2 - Science 8th grade 2012-13 % proficient or above', \
			'Longevity1to2 - Read OGT 2012-13 % proficient or above', \
			'Longevity1to2 - Math OGT 2012-13 % proficient or above', \
			'Longevity1to2 - Write OGT 2012-13 % proficient or above', \
			'Longevity1to2 - Social Studies OGT 2012-13 % proficient or above', \
			'Longevity1to2 - Science OGT 2012-13 % proficient or above', \
			'Longevity1to2 - Read 11th grade 2012-13 % at or above proficient', \
			'Longevity1to2 - Math 11th grade 2012-13 % at or above proficient', \
			'Longevity1to2 - Write 11th grade 2012-13 % at or above proficient', \
			'Longevity1to2 - Social Studies 11th grade 2012-13 % at or above proficient', \
			'Longevity1to2 - Science 11th grade 2012-13 % at or above proficient', \
			'Longevity1to2 - Attendance rate 2012-13', \
			'Longevity1to2 - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'Longevity1to2 - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'Longevity1to2 - Enrollment', \
			'Longevity1to2 - % of total enrollment', \
			'Longevity3orMore - Read 3rd grade 2012-13 % proficient or above', \
			'Longevity3orMore - Math 3rd grade 2012-13 % proficient or above', \
			'Longevity3orMore - Read 4th Grade 2012-13 % proficient or above', \
			'Longevity3orMore - Math 4th Grade 2012-13 % proficient or above', \
			'Longevity3orMore - Read 5th grade 2012-13 % proficient or above', \
			'Longevity3orMore - Math 5th grade 2012-13 % proficient or above', \
			'Longevity3orMore - Science 5th grade 2012-13 % proficient or above', \
			'Longevity3orMore - Read 6th Grade 2012-13 % proficient or above', \
			'Longevity3orMore - Math 6th Grade 2012-13 % proficient or above', \
			'Longevity3orMore - Read 7th Grade 2012-13 % proficient or above', \
			'Longevity3orMore - Math 7th Grade 2012-13 % proficient or above', \
			'Longevity3orMore - Read 8th Grade 2012-13 % proficient or above', \
			'Longevity3orMore - Math 8th Grade 2012-13 % proficient or above', \
			'Longevity3orMore - Science 8th grade 2012-13 % proficient or above', \
			'Longevity3orMore - Read OGT 2012-13 % proficient or above', \
			'Longevity3orMore - Math OGT 2012-13 % proficient or above', \
			'Longevity3orMore - Write OGT 2012-13 % proficient or above', \
			'Longevity3orMore - Social Studies OGT 2012-13 % proficient or above', \
			'Longevity3orMore - Science OGT 2012-13 % proficient or above', \
			'Longevity3orMore - Read 11th grade 2012-13 % at or above proficient', \
			'Longevity3orMore - Math 11th grade 2012-13 % at or above proficient', \
			'Longevity3orMore - Write 11th grade 2012-13 % at or above proficient', \
			'Longevity3orMore - Social Studies 11th grade 2012-13 % at or above proficient', \
			'Longevity3orMore - Science 11th grade 2012-13 % at or above proficient', \
			'Longevity3orMore - Attendance rate 2012-13', \
			'Longevity3orMore - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'Longevity3orMore - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'Longevity3orMore - Enrollment', \
			'Longevity3orMore - % of total enrollment']
		for each in headers:
			each			= clean(each)
	if header_row:
		curr_cell			= -1
		while curr_cell < num_cells:
			curr_cell 		+= 1
			cell_value 		= str(worksheet.cell_value(curr_row, curr_cell))
			headers.append(cell_value)
	elif not(footer_row):
		row				= worksheet.row_values(curr_row)
		if len(row[0]) < 1:
			footer_row		= True
		else:
			wr.writerow(row)
			district_IRN			= worksheet.cell_value(curr_row, 0)
			if type(district_IRN) is float:
				district_IRN		= str(round(district_IRN)).rstrip('0').rstrip('.')
			district_IRN			= district_IRN.zfill(6)

			curr_cell			= 4
			while curr_cell < num_cells:
				curr_cell 		+= 1
				row_type		= worksheet.cell_value(curr_row, 4)
				cell_value 		= clean(worksheet.cell_value(curr_row, curr_cell))
				if row_type == 'Longevity0':
					row_constant	= -5
				elif row_type == 'Longevity1to2':
					row_constant	= 24					
				else:
					row_constant	= 53
					enroll_percent	= worksheet.cell_value(curr_row, 33)
					try:
						enroll_percent	= float(enroll_percent)
					except:
						pass
					if type(enroll_percent) is float:
						enroll_percent	= 100 - enroll_percent
						districts[district_IRN]['% enrolled less than 3 years'] = '%.1f' % enroll_percent

				header			= headers[curr_cell + row_constant]
				if district_IRN in districts:
					districts[district_IRN][header]			= cell_value
				else:
					districts[district_IRN]				= {}
					districts[district_IRN][header]			= cell_value

write_file.close()


######################### RACIAL DATA ##########################

# Charter Racial Data

filename	= 'Charter Racial Data'
xls_file	= xls_path + 'RAW' + ' ' + filename + '.xls'
workbook	= xlrd.open_workbook(xls_file)

worksheet 	= workbook.sheet_by_name('BLDG_ETHNIC_13')

# Six rows per charter

csv_file	= csv_path + filename + '.csv'
write_file	= open(csv_file, 'w')
wr 		= csv.writer(write_file, quoting=csv.QUOTE_ALL)

num_rows 					= worksheet.nrows - 1
num_cells 					= worksheet.ncols - 1
curr_row 					= -1
header_row					= True
headers						= []
footer_row					= False

while curr_row < num_rows:
	curr_row 				+= 1
	if curr_row == 1:
		header_row 			= False
		for each in headers:
			each			= clean(each)
		wr.writerow(headers)
		headers = [ \
			'American Indian or Alaskan Native - Read 3rd grade 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Math 3rd grade 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Read 4th Grade 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Math 4th Grade 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Read 5th grade 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Math 5th grade 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Science 5th grade 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Read 6th Grade 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Math 6th Grade 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Read 7th Grade 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Math 7th Grade 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Read 8th Grade 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Math 8th Grade 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Science 8th grade 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Read OGT 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Math OGT 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Write OGT 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Social Studies OGT 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Science OGT 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Read 11th grade 2012-13 % at or above proficient', \
			'American Indian or Alaskan Native - Math 11th grade 2012-13 % at or above proficient', \
			'American Indian or Alaskan Native - Write 11th grade 2012-13 % at or above proficient', \
			'American Indian or Alaskan Native - Social Studies 11th grade 2012-13 % at or above proficient', \
			'American Indian or Alaskan Native - Science 11th grade 2012-13 % at or above proficient', \
			'American Indian or Alaskan Native - Attendance rate 2012-13', \
			'American Indian or Alaskan Native - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'American Indian or Alaskan Native - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'American Indian or Alaskan Native - Enrollment', \
			'American Indian or Alaskan Native - % of total enrollment', \
			'Asian or Pacific Islander - Read 3rd grade 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Math 3rd grade 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Read 4th Grade 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Math 4th Grade 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Read 5th grade 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Math 5th grade 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Science 5th grade 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Read 6th Grade 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Math 6th Grade 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Read 7th Grade 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Math 7th Grade 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Read 8th Grade 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Math 8th Grade 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Science 8th grade 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Read OGT 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Math OGT 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Write OGT 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Social Studies OGT 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Science OGT 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Read 11th grade 2012-13 % at or above proficient', \
			'Asian or Pacific Islander - Math 11th grade 2012-13 % at or above proficient', \
			'Asian or Pacific Islander - Write 11th grade 2012-13 % at or above proficient', \
			'Asian or Pacific Islander - Social Studies 11th grade 2012-13 % at or above proficient', \
			'Asian or Pacific Islander - Science 11th grade 2012-13 % at or above proficient', \
			'Asian or Pacific Islander - Attendance rate 2012-13', \
			'Asian or Pacific Islander - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'Asian or Pacific Islander - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'Asian or Pacific Islander - Enrollment', \
			'Asian or Pacific Islander - % of total enrollment', \
			'Black - Read 3rd grade 2012-13 % proficient or above', \
			'Black - Math 3rd grade 2012-13 % proficient or above', \
			'Black - Read 4th Grade 2012-13 % proficient or above', \
			'Black - Math 4th Grade 2012-13 % proficient or above', \
			'Black - Read 5th grade 2012-13 % proficient or above', \
			'Black - Math 5th grade 2012-13 % proficient or above', \
			'Black - Science 5th grade 2012-13 % proficient or above', \
			'Black - Read 6th Grade 2012-13 % proficient or above', \
			'Black - Math 6th Grade 2012-13 % proficient or above', \
			'Black - Read 7th Grade 2012-13 % proficient or above', \
			'Black - Math 7th Grade 2012-13 % proficient or above', \
			'Black - Read 8th Grade 2012-13 % proficient or above', \
			'Black - Math 8th Grade 2012-13 % proficient or above', \
			'Black - Science 8th grade 2012-13 % proficient or above', \
			'Black - Read OGT 2012-13 % proficient or above', \
			'Black - Math OGT 2012-13 % proficient or above', \
			'Black - Write OGT 2012-13 % proficient or above', \
			'Black - Social Studies OGT 2012-13 % proficient or above', \
			'Black - Science OGT 2012-13 % proficient or above', \
			'Black - Read 11th grade 2012-13 % at or above proficient', \
			'Black - Math 11th grade 2012-13 % at or above proficient', \
			'Black - Write 11th grade 2012-13 % at or above proficient', \
			'Black - Social Studies 11th grade 2012-13 % at or above proficient', \
			'Black - Science 11th grade 2012-13 % at or above proficient', \
			'Black - Attendance rate 2012-13', \
			'Black - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'Black - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'Black - Enrollment', \
			'Black - % of total enrollment', \
			'Hispanic - Read 3rd grade 2012-13 % proficient or above', \
			'Hispanic - Math 3rd grade 2012-13 % proficient or above', \
			'Hispanic - Read 4th Grade 2012-13 % proficient or above', \
			'Hispanic - Math 4th Grade 2012-13 % proficient or above', \
			'Hispanic - Read 5th grade 2012-13 % proficient or above', \
			'Hispanic - Math 5th grade 2012-13 % proficient or above', \
			'Hispanic - Science 5th grade 2012-13 % proficient or above', \
			'Hispanic - Read 6th Grade 2012-13 % proficient or above', \
			'Hispanic - Math 6th Grade 2012-13 % proficient or above', \
			'Hispanic - Read 7th Grade 2012-13 % proficient or above', \
			'Hispanic - Math 7th Grade 2012-13 % proficient or above', \
			'Hispanic - Read 8th Grade 2012-13 % proficient or above', \
			'Hispanic - Math 8th Grade 2012-13 % proficient or above', \
			'Hispanic - Science 8th grade 2012-13 % proficient or above', \
			'Hispanic - Read OGT 2012-13 % proficient or above', \
			'Hispanic - Math OGT 2012-13 % proficient or above', \
			'Hispanic - Write OGT 2012-13 % proficient or above', \
			'Hispanic - Social Studies OGT 2012-13 % proficient or above', \
			'Hispanic - Science OGT 2012-13 % proficient or above', \
			'Hispanic - Read 11th grade 2012-13 % at or above proficient', \
			'Hispanic - Math 11th grade 2012-13 % at or above proficient', \
			'Hispanic - Write 11th grade 2012-13 % at or above proficient', \
			'Hispanic - Social Studies 11th grade 2012-13 % at or above proficient', \
			'Hispanic - Science 11th grade 2012-13 % at or above proficient', \
			'Hispanic - Attendance rate 2012-13', \
			'Hispanic - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'Hispanic - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'Hispanic - Enrollment', \
			'Hispanic - % of total enrollment', \
			'Multiracial - Read 3rd grade 2012-13 % proficient or above', \
			'Multiracial - Math 3rd grade 2012-13 % proficient or above', \
			'Multiracial - Read 4th Grade 2012-13 % proficient or above', \
			'Multiracial - Math 4th Grade 2012-13 % proficient or above', \
			'Multiracial - Read 5th grade 2012-13 % proficient or above', \
			'Multiracial - Math 5th grade 2012-13 % proficient or above', \
			'Multiracial - Science 5th grade 2012-13 % proficient or above', \
			'Multiracial - Read 6th Grade 2012-13 % proficient or above', \
			'Multiracial - Math 6th Grade 2012-13 % proficient or above', \
			'Multiracial - Read 7th Grade 2012-13 % proficient or above', \
			'Multiracial - Math 7th Grade 2012-13 % proficient or above', \
			'Multiracial - Read 8th Grade 2012-13 % proficient or above', \
			'Multiracial - Math 8th Grade 2012-13 % proficient or above', \
			'Multiracial - Science 8th grade 2012-13 % proficient or above', \
			'Multiracial - Read OGT 2012-13 % proficient or above', \
			'Multiracial - Math OGT 2012-13 % proficient or above', \
			'Multiracial - Write OGT 2012-13 % proficient or above', \
			'Multiracial - Social Studies OGT 2012-13 % proficient or above', \
			'Multiracial - Science OGT 2012-13 % proficient or above', \
			'Multiracial - Read 11th grade 2012-13 % at or above proficient', \
			'Multiracial - Math 11th grade 2012-13 % at or above proficient', \
			'Multiracial - Write 11th grade 2012-13 % at or above proficient', \
			'Multiracial - Social Studies 11th grade 2012-13 % at or above proficient', \
			'Multiracial - Science 11th grade 2012-13 % at or above proficient', \
			'Multiracial - Attendance rate 2012-13', \
			'Multiracial - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'Multiracial - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'Multiracial - Enrollment', \
			'Multiracial - % of total enrollment', \
			'White - Read 3rd grade 2012-13 % proficient or above', \
			'White - Math 3rd grade 2012-13 % proficient or above', \
			'White - Read 4th Grade 2012-13 % proficient or above', \
			'White - Math 4th Grade 2012-13 % proficient or above', \
			'White - Read 5th grade 2012-13 % proficient or above', \
			'White - Math 5th grade 2012-13 % proficient or above', \
			'White - Science 5th grade 2012-13 % proficient or above', \
			'White - Read 6th Grade 2012-13 % proficient or above', \
			'White - Math 6th Grade 2012-13 % proficient or above', \
			'White - Read 7th Grade 2012-13 % proficient or above', \
			'White - Math 7th Grade 2012-13 % proficient or above', \
			'White - Read 8th Grade 2012-13 % proficient or above', \
			'White - Math 8th Grade 2012-13 % proficient or above', \
			'White - Science 8th grade 2012-13 % proficient or above', \
			'White - Read OGT 2012-13 % proficient or above', \
			'White - Math OGT 2012-13 % proficient or above', \
			'White - Write OGT 2012-13 % proficient or above', \
			'White - Social Studies OGT 2012-13 % proficient or above', \
			'White - Science OGT 2012-13 % proficient or above', \
			'White - Read 11th grade 2012-13 % at or above proficient', \
			'White - Math 11th grade 2012-13 % at or above proficient', \
			'White - Write 11th grade 2012-13 % at or above proficient', \
			'White - Social Studies 11th grade 2012-13 % at or above proficient', \
			'White - Science 11th grade 2012-13 % at or above proficient', \
			'White - Attendance rate 2012-13', \
			'White - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'White - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'White - Enrollment', \
			'White - % of total enrollment']
		for each in headers:
			each			= clean(each)
	if header_row:
		curr_cell			= -1
		while curr_cell < num_cells:
			curr_cell 		+= 1
			cell_value 		= str(worksheet.cell_value(curr_row, curr_cell))
			headers.append(cell_value)
	elif not(footer_row):
		row				= worksheet.row_values(curr_row)
		if len(row[0]) < 1:
			footer_row		= True
		else:
			wr.writerow(row)
			school_IRN			= worksheet.cell_value(curr_row, 0)
			school_IRN			= fixIRN(school_IRN)

			if school_IRN not in charters:
				charters[school_IRN][header]	= {}

			curr_cell			= 9
			while curr_cell < num_cells:
				curr_cell 		+= 1
				row_type		= worksheet.cell_value(curr_row, 9)
				cell_value 		= clean(worksheet.cell_value(curr_row, curr_cell))
				if row_type == 'American Indian or Alaskan Native':
					row_constant	= -10
				elif row_type == 'Asian or Pacific Islander':
					row_constant	= 19					
				elif row_type == 'Black':
					row_constant	= 48
				elif row_type == 'Hispanic':
					row_constant	= 77
				elif row_type == 'Multiracial':
					row_constant	= 106
				else:
					row_constant	= 135
					enroll_percent	= row[38]
					try:
						enroll_percent	= float(enroll_percent)
					except:
						pass
					if type(enroll_percent) is float:
						charters[school_IRN]['% white'] = '%.1f' % enroll_percent
						enroll_percent	= 100 - enroll_percent
						charters[school_IRN]['% non-white'] = '%.1f' % enroll_percent
					else:
						charters[school_IRN]['% white'] = enroll_percent
					if enroll_percent == '>95.0':
						charters[school_IRN]['% non-white'] = '<5.0'

				header			= headers[curr_cell + row_constant]
				charters[school_IRN][header]			= cell_value



write_file.close()

# District Racial Data

filename	= 'District Racial Data'
xls_file	= xls_path + 'RAW' + ' ' + filename + '.xls'
workbook	= xlrd.open_workbook(xls_file)

worksheet 	= workbook.sheet_by_name('DIST_ETHNIC_13')

# Six rows per charter

csv_file	= csv_path + filename + '.csv'
write_file	= open(csv_file, 'w')
wr 		= csv.writer(write_file, quoting=csv.QUOTE_ALL)

num_rows 					= worksheet.nrows - 1
num_cells 					= worksheet.ncols - 1
curr_row 					= -1
header_row					= True
headers						= []
footer_row					= False

while curr_row < num_rows:
	curr_row 				+= 1
	if curr_row == 1:
		header_row 			= False
		for each in headers:
			each			= clean(each)
		wr.writerow(headers)
		headers = [ \
			'American Indian or Alaskan Native - Read 3rd grade 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Math 3rd grade 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Read 4th Grade 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Math 4th Grade 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Read 5th grade 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Math 5th grade 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Science 5th grade 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Read 6th Grade 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Math 6th Grade 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Read 7th Grade 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Math 7th Grade 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Read 8th Grade 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Math 8th Grade 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Science 8th grade 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Read OGT 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Math OGT 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Write OGT 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Social Studies OGT 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Science OGT 2012-13 % proficient or above', \
			'American Indian or Alaskan Native - Read 11th grade 2012-13 % at or above proficient', \
			'American Indian or Alaskan Native - Math 11th grade 2012-13 % at or above proficient', \
			'American Indian or Alaskan Native - Write 11th grade 2012-13 % at or above proficient', \
			'American Indian or Alaskan Native - Social Studies 11th grade 2012-13 % at or above proficient', \
			'American Indian or Alaskan Native - Science 11th grade 2012-13 % at or above proficient', \
			'American Indian or Alaskan Native - Attendance rate 2012-13', \
			'American Indian or Alaskan Native - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'American Indian or Alaskan Native - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'American Indian or Alaskan Native - Enrollment', \
			'American Indian or Alaskan Native - % of total enrollment', \
			'Asian or Pacific Islander - Read 3rd grade 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Math 3rd grade 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Read 4th Grade 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Math 4th Grade 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Read 5th grade 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Math 5th grade 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Science 5th grade 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Read 6th Grade 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Math 6th Grade 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Read 7th Grade 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Math 7th Grade 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Read 8th Grade 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Math 8th Grade 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Science 8th grade 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Read OGT 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Math OGT 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Write OGT 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Social Studies OGT 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Science OGT 2012-13 % proficient or above', \
			'Asian or Pacific Islander - Read 11th grade 2012-13 % at or above proficient', \
			'Asian or Pacific Islander - Math 11th grade 2012-13 % at or above proficient', \
			'Asian or Pacific Islander - Write 11th grade 2012-13 % at or above proficient', \
			'Asian or Pacific Islander - Social Studies 11th grade 2012-13 % at or above proficient', \
			'Asian or Pacific Islander - Science 11th grade 2012-13 % at or above proficient', \
			'Asian or Pacific Islander - Attendance rate 2012-13', \
			'Asian or Pacific Islander - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'Asian or Pacific Islander - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'Asian or Pacific Islander - Enrollment', \
			'Asian or Pacific Islander - % of total enrollment', \
			'Black - Read 3rd grade 2012-13 % proficient or above', \
			'Black - Math 3rd grade 2012-13 % proficient or above', \
			'Black - Read 4th Grade 2012-13 % proficient or above', \
			'Black - Math 4th Grade 2012-13 % proficient or above', \
			'Black - Read 5th grade 2012-13 % proficient or above', \
			'Black - Math 5th grade 2012-13 % proficient or above', \
			'Black - Science 5th grade 2012-13 % proficient or above', \
			'Black - Read 6th Grade 2012-13 % proficient or above', \
			'Black - Math 6th Grade 2012-13 % proficient or above', \
			'Black - Read 7th Grade 2012-13 % proficient or above', \
			'Black - Math 7th Grade 2012-13 % proficient or above', \
			'Black - Read 8th Grade 2012-13 % proficient or above', \
			'Black - Math 8th Grade 2012-13 % proficient or above', \
			'Black - Science 8th grade 2012-13 % proficient or above', \
			'Black - Read OGT 2012-13 % proficient or above', \
			'Black - Math OGT 2012-13 % proficient or above', \
			'Black - Write OGT 2012-13 % proficient or above', \
			'Black - Social Studies OGT 2012-13 % proficient or above', \
			'Black - Science OGT 2012-13 % proficient or above', \
			'Black - Read 11th grade 2012-13 % at or above proficient', \
			'Black - Math 11th grade 2012-13 % at or above proficient', \
			'Black - Write 11th grade 2012-13 % at or above proficient', \
			'Black - Social Studies 11th grade 2012-13 % at or above proficient', \
			'Black - Science 11th grade 2012-13 % at or above proficient', \
			'Black - Attendance rate 2012-13', \
			'Black - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'Black - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'Black - Enrollment', \
			'Black - % of total enrollment', \
			'Hispanic - Read 3rd grade 2012-13 % proficient or above', \
			'Hispanic - Math 3rd grade 2012-13 % proficient or above', \
			'Hispanic - Read 4th Grade 2012-13 % proficient or above', \
			'Hispanic - Math 4th Grade 2012-13 % proficient or above', \
			'Hispanic - Read 5th grade 2012-13 % proficient or above', \
			'Hispanic - Math 5th grade 2012-13 % proficient or above', \
			'Hispanic - Science 5th grade 2012-13 % proficient or above', \
			'Hispanic - Read 6th Grade 2012-13 % proficient or above', \
			'Hispanic - Math 6th Grade 2012-13 % proficient or above', \
			'Hispanic - Read 7th Grade 2012-13 % proficient or above', \
			'Hispanic - Math 7th Grade 2012-13 % proficient or above', \
			'Hispanic - Read 8th Grade 2012-13 % proficient or above', \
			'Hispanic - Math 8th Grade 2012-13 % proficient or above', \
			'Hispanic - Science 8th grade 2012-13 % proficient or above', \
			'Hispanic - Read OGT 2012-13 % proficient or above', \
			'Hispanic - Math OGT 2012-13 % proficient or above', \
			'Hispanic - Write OGT 2012-13 % proficient or above', \
			'Hispanic - Social Studies OGT 2012-13 % proficient or above', \
			'Hispanic - Science OGT 2012-13 % proficient or above', \
			'Hispanic - Read 11th grade 2012-13 % at or above proficient', \
			'Hispanic - Math 11th grade 2012-13 % at or above proficient', \
			'Hispanic - Write 11th grade 2012-13 % at or above proficient', \
			'Hispanic - Social Studies 11th grade 2012-13 % at or above proficient', \
			'Hispanic - Science 11th grade 2012-13 % at or above proficient', \
			'Hispanic - Attendance rate 2012-13', \
			'Hispanic - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'Hispanic - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'Hispanic - Enrollment', \
			'Hispanic - % of total enrollment', \
			'Multiracial - Read 3rd grade 2012-13 % proficient or above', \
			'Multiracial - Math 3rd grade 2012-13 % proficient or above', \
			'Multiracial - Read 4th Grade 2012-13 % proficient or above', \
			'Multiracial - Math 4th Grade 2012-13 % proficient or above', \
			'Multiracial - Read 5th grade 2012-13 % proficient or above', \
			'Multiracial - Math 5th grade 2012-13 % proficient or above', \
			'Multiracial - Science 5th grade 2012-13 % proficient or above', \
			'Multiracial - Read 6th Grade 2012-13 % proficient or above', \
			'Multiracial - Math 6th Grade 2012-13 % proficient or above', \
			'Multiracial - Read 7th Grade 2012-13 % proficient or above', \
			'Multiracial - Math 7th Grade 2012-13 % proficient or above', \
			'Multiracial - Read 8th Grade 2012-13 % proficient or above', \
			'Multiracial - Math 8th Grade 2012-13 % proficient or above', \
			'Multiracial - Science 8th grade 2012-13 % proficient or above', \
			'Multiracial - Read OGT 2012-13 % proficient or above', \
			'Multiracial - Math OGT 2012-13 % proficient or above', \
			'Multiracial - Write OGT 2012-13 % proficient or above', \
			'Multiracial - Social Studies OGT 2012-13 % proficient or above', \
			'Multiracial - Science OGT 2012-13 % proficient or above', \
			'Multiracial - Read 11th grade 2012-13 % at or above proficient', \
			'Multiracial - Math 11th grade 2012-13 % at or above proficient', \
			'Multiracial - Write 11th grade 2012-13 % at or above proficient', \
			'Multiracial - Social Studies 11th grade 2012-13 % at or above proficient', \
			'Multiracial - Science 11th grade 2012-13 % at or above proficient', \
			'Multiracial - Attendance rate 2012-13', \
			'Multiracial - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'Multiracial - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'Multiracial - Enrollment', \
			'Multiracial - % of total enrollment', \
			'White - Read 3rd grade 2012-13 % proficient or above', \
			'White - Math 3rd grade 2012-13 % proficient or above', \
			'White - Read 4th Grade 2012-13 % proficient or above', \
			'White - Math 4th Grade 2012-13 % proficient or above', \
			'White - Read 5th grade 2012-13 % proficient or above', \
			'White - Math 5th grade 2012-13 % proficient or above', \
			'White - Science 5th grade 2012-13 % proficient or above', \
			'White - Read 6th Grade 2012-13 % proficient or above', \
			'White - Math 6th Grade 2012-13 % proficient or above', \
			'White - Read 7th Grade 2012-13 % proficient or above', \
			'White - Math 7th Grade 2012-13 % proficient or above', \
			'White - Read 8th Grade 2012-13 % proficient or above', \
			'White - Math 8th Grade 2012-13 % proficient or above', \
			'White - Science 8th grade 2012-13 % proficient or above', \
			'White - Read OGT 2012-13 % proficient or above', \
			'White - Math OGT 2012-13 % proficient or above', \
			'White - Write OGT 2012-13 % proficient or above', \
			'White - Social Studies OGT 2012-13 % proficient or above', \
			'White - Science OGT 2012-13 % proficient or above', \
			'White - Read 11th grade 2012-13 % at or above proficient', \
			'White - Math 11th grade 2012-13 % at or above proficient', \
			'White - Write 11th grade 2012-13 % at or above proficient', \
			'White - Social Studies 11th grade 2012-13 % at or above proficient', \
			'White - Science 11th grade 2012-13 % at or above proficient', \
			'White - Attendance rate 2012-13', \
			'White - 2012 4-Year Longitudinal Graduation Rate - Class of 2012', \
			'White - 2012 5-Year Longitudinal Graduation Rate - Class of 2011', \
			'White - Enrollment', \
			'White - % of total enrollment']
		for each in headers:
			each			= clean(each)
	if header_row:
		curr_cell			= -1
		while curr_cell < num_cells:
			curr_cell 		+= 1
			cell_value 		= str(worksheet.cell_value(curr_row, curr_cell))
			headers.append(cell_value)
	elif not(footer_row):
		row				= worksheet.row_values(curr_row)
		if len(row[0]) < 1:
			footer_row		= True
		else:
			wr.writerow(row)
			district_IRN			= worksheet.cell_value(curr_row, 0)
			if type(district_IRN) is float:
				district_IRN		= str(round(district_IRN)).rstrip('0').rstrip('.')
			district_IRN			= district_IRN.zfill(6)

			curr_cell			= 4
			while curr_cell < num_cells:
				curr_cell 		+= 1
				row_type		= worksheet.cell_value(curr_row, 4)
				cell_value 		= clean(worksheet.cell_value(curr_row, curr_cell))
				if row_type == 'American Indian or Alaskan Native':
					row_constant	= -5
				elif row_type == 'Asian or Pacific Islander':
					row_constant	= 24					
				elif row_type == 'Black':
					row_constant	= 53
				elif row_type == 'Hispanic':
					row_constant	= 82
				elif row_type == 'Multiracial':
					row_constant	= 111
				else:
					row_constant	= 140
					enroll_percent	= row[33]
					try:
						enroll_percent	= float(enroll_percent)
					except:
						pass
					if type(enroll_percent) is float:
						districts[district_IRN]['% white'] = '%.1f' % enroll_percent
						enroll_percent	= 100 - enroll_percent
						districts[district_IRN]['% non-white'] = '%.1f' % enroll_percent
					else:
						districts[district_IRN]['% white'] = enroll_percent
					if enroll_percent == '>95.0':
						districts[district_IRN]['% non-white'] = '<5.0'

				header			= headers[curr_cell + row_constant]
				if district_IRN in districts:
					districts[district_IRN][header]			= cell_value
				else:
					districts[district_IRN]				= {}
					districts[district_IRN][header]			= cell_value

write_file.close()


######################## TEACHER DATA #########################

# Charter Teacher Data

filename	= 'Charter Teacher Data'
xls_file	= xls_path + 'RAW' + ' ' + filename + '.xls'
workbook	= xlrd.open_workbook(xls_file)

worksheet 	= workbook.sheet_by_name('TEACHER')

# One row per charter

csv_file	= csv_path + filename + '.csv'
write_file	= open(csv_file, 'w')
wr 		= csv.writer(write_file, quoting=csv.QUOTE_ALL)

num_rows 					= worksheet.nrows - 1
num_cells 					= worksheet.ncols - 1
curr_row 					= -1
header_row					= True
headers						= []
footer_row					= False

while curr_row < num_rows:
	curr_row 				+= 1
	if curr_row == 1:
		header_row 			= False
		for each in headers:
			each 			= clean(each)
		wr.writerow(headers)
		new_headers			= []
		for each in headers:
			each			= filename + ' - ' + each
			each 			= clean(each)
			new_headers.append(each)
		headers				= new_headers	
	if header_row:
		curr_cell			= -1
		while curr_cell < num_cells:
			curr_cell 		+= 1
			cell_value 		= str(worksheet.cell_value(curr_row, curr_cell))
			headers.append(cell_value)
	elif not(footer_row):
		row				= worksheet.row_values(curr_row)
		if len(row[0]) < 1:
			footer_row		= True
		else:
			wr.writerow(row)
			school_IRN			= worksheet.cell_value(curr_row, 0)
			school_IRN			= fixIRN(school_IRN)

			school_teach_attend			= worksheet.cell_value(curr_row, 7)
			school_teach_exp			= worksheet.cell_value(curr_row, 8)
			school_no_teachers			= worksheet.cell_value(curr_row, 9)
			school_per_masters			= worksheet.cell_value(curr_row, 15)

			charters[school_IRN]['Teacher attendance %'] = school_teach_attend
			charters[school_IRN]['Avg Teacher Exp']	= school_teach_exp
			charters[school_IRN]['# of FT teachers'] = school_no_teachers
			charters[school_IRN]['% of teachers with masters degrees'] = school_per_masters


			curr_cell			= -1
			while curr_cell < num_cells:
				curr_cell 		+= 1
				cell_value 		= clean(worksheet.cell_value(curr_row, curr_cell))
				if school_IRN in charters:
					charters[school_IRN][headers[curr_cell]]	= cell_value
				else:
					charters[school_IRN]				= {}
					charters[school_IRN][headers[curr_cell]]	= cell_value

write_file.close()

# District Teacher Data

filename	= 'District Teacher Data'
xls_file	= xls_path + 'RAW' + ' ' + filename + '.xls'
workbook	= xlrd.open_workbook(xls_file)

worksheet 	= workbook.sheet_by_name('TEACHER')

# One row per district

csv_file	= csv_path + filename + '.csv'
write_file	= open(csv_file, 'w')
wr 		= csv.writer(write_file, quoting=csv.QUOTE_ALL)

num_rows 					= worksheet.nrows - 1
num_cells 					= worksheet.ncols - 1
curr_row 					= -1
header_row					= True
headers						= []
footer_row					= False

while curr_row < num_rows:
	curr_row 				+= 1
	if curr_row == 1:
		header_row 			= False
		for each in headers:
			each 			= clean(each)
		wr.writerow(headers)
		new_headers			= []
		for each in headers:
			each			= filename + ' - ' + each
			each 			= clean(each)
			new_headers.append(each)
		headers				= new_headers	
	if header_row:
		curr_cell			= -1
		while curr_cell < num_cells:
			curr_cell 		+= 1
			cell_value 		= str(worksheet.cell_value(curr_row, curr_cell))
			headers.append(cell_value)
	elif not(footer_row):
		row				= worksheet.row_values(curr_row)
		if len(row[0]) < 1:
			footer_row		= True
		else:
			wr.writerow(row)
			district_IRN			= worksheet.cell_value(curr_row, 0)
			district_IRN			= fixIRN(district_IRN)

			dist_teach_exp				= worksheet.cell_value(curr_row, 5)
			dist_teach_attend			= worksheet.cell_value(curr_row, 4)
			dist_no_teachers			= worksheet.cell_value(curr_row, 6)
			dist_per_masters			= worksheet.cell_value(curr_row, 12)

			districts[district_IRN]['Teacher attendance %'] = dist_teach_attend
			districts[district_IRN]['Avg Teacher Exp']	= dist_teach_exp
			districts[district_IRN]['# of FT teachers'] 	= dist_no_teachers
			districts[district_IRN]['% of teachers with masters degrees'] = dist_per_masters

			curr_cell			= -1
			while curr_cell < num_cells:
				curr_cell 		+= 1
				cell_value 		= clean(worksheet.cell_value(curr_row, curr_cell))
				if district_IRN in districts:
					districts[district_IRN][headers[curr_cell]]	= cell_value
				else:
					districts[district_IRN]				= {}
					districts[district_IRN][headers[curr_cell]]	= cell_value

write_file.close()


################## CHARTER SPECIFIC DATA #####################

# Charter Operator Data

filename	= 'Charter Operator Data'
xls_file	= xls_path + 'RAW' + ' ' + filename + '.xlsx'
workbook	= xlrd.open_workbook(xls_file)

worksheet 	= workbook.sheet_by_name('Sheet1')

# One row per charter

csv_file	= csv_path + filename + '.csv'
write_file	= open(csv_file, 'w')
wr 		= csv.writer(write_file, quoting=csv.QUOTE_ALL)

num_rows 					= worksheet.nrows - 1
num_cells 					= worksheet.ncols - 1
curr_row 					= -1
header_row					= True
headers						= []
footer_row					= False

while curr_row < num_rows:
	curr_row 				+= 1
	if curr_row == 1:
		header_row 			= False
		for each in headers:
			each 			= clean(each)
		wr.writerow(headers)
		new_headers			= []
		for each in headers:
			each			= filename + ' - ' + each
			each 			= clean(each)
			new_headers.append(each)
		headers				= new_headers	
	if header_row:
		curr_cell			= -1
		while curr_cell < num_cells:
			curr_cell 		+= 1
			cell_value 		= str(worksheet.cell_value(curr_row, curr_cell))
			headers.append(cell_value)
	elif not(footer_row):
		row				= worksheet.row_values(curr_row)
		if len(str(row[0])) < 1:
			footer_row		= True
		else:
			wr.writerow(row)
			school_IRN			= worksheet.cell_value(curr_row, 0)
			school_IRN			= fixIRN(school_IRN)
			if school_IRN not in charters:
					charters[school_IRN]	= {}

			school_operator			= worksheet.cell_value(curr_row, 2)
			school_org_status		= worksheet.cell_value(curr_row, 3)
		
	# Basic School Information
		# Operator
			charters[school_IRN]['Operator']	= school_operator
			charters[school_IRN]['Organization Status'] = clean(school_org_status)

			curr_cell			= -1
			while curr_cell < num_cells:
				curr_cell 		+= 1
				cell_value 		= clean(worksheet.cell_value(curr_row, curr_cell))
				charters[school_IRN][headers[curr_cell]]	= cell_value

write_file.close()

# Dropout Recovery Report Card

filename	= 'Dropout Recovery Report Card'
xls_file	= xls_path + 'RAW' + ' ' + filename + '.xls'
workbook	= xlrd.open_workbook(xls_file)

worksheet 	= workbook.sheet_by_name('DORP_SCHL_13')

# One row per charter

csv_file	= csv_path + filename + '.csv'
write_file	= open(csv_file, 'w')
wr 		= csv.writer(write_file, quoting=csv.QUOTE_ALL)

num_rows 					= worksheet.nrows - 1
num_cells 					= worksheet.ncols - 1
curr_row 					= -1
header_row					= True
headers						= []
footer_row					= False

while curr_row < num_rows:
	curr_row 				+= 1
	if curr_row == 1:
		header_row 			= False
		for each in headers:
			each 			= clean(each)
		wr.writerow(headers)
		new_headers			= []
		for each in headers:
			each			= filename + ' - ' + each
			each 			= clean(each)
			new_headers.append(each)
		headers				= new_headers	
	if header_row:
		curr_cell			= -1
		while curr_cell < num_cells:
			curr_cell 		+= 1
			cell_value 		= str(worksheet.cell_value(curr_row, curr_cell))
			headers.append(cell_value)
	elif not(footer_row):
		row				= worksheet.row_values(curr_row)
		if len(row[0]) < 1:
			footer_row		= True
		else:
			wr.writerow(row)

			school_IRN			= worksheet.cell_value(curr_row, 0)
			school_IRN			= fixIRN(school_IRN)
			school_name			= worksheet.cell_value(curr_row, 1)
			school_address			= worksheet.cell_value(curr_row, 6)

			school_district_IRN		= worksheet.cell_value(curr_row, 2)
			school_district_IRN		= fixIRN(school_district_IRN)
			school_district_name		= worksheet.cell_value(curr_row, 3)

			school_county			= worksheet.cell_value(curr_row, 4)
			school_gradespan		= worksheet.cell_value(curr_row, 10)
			school_open			= worksheet.cell_value(curr_row, 11)

			city_state_zip				= worksheet.cell_value(curr_row, 7)
			group					= city_state_zip.split(",")
			school_city				= group[0]
			school_group				= group[1].split(" ")
			school_state				= school_group[1]
			school_postal_code			= school_group[-1]

			# Basic School Information
				# School Name
			charters[school_IRN]['Name']		= school_name
				# Address
			charters[school_IRN]['Address']		= school_address
			charters[school_IRN]['City']		= school_city
			charters[school_IRN]['State']		= school_state
			charters[school_IRN]['Postal Code']	= school_postal_code
				# County
			charters[school_IRN]['County']		= school_county
				# District
			charters[school_IRN]['District IRN']	= school_district_IRN
			charters[school_IRN]['District Name']	= school_district_name
				# Grades served
			charters[school_IRN]['Grades Served']	= school_gradespan
				# Open Status
			charters[school_IRN]['Open Status']	= school_open

			if school_IRN not in charters:
				charters[school_IRN]	= {}

			curr_cell			= -1
			while curr_cell < num_cells:
				curr_cell 		+= 1
				cell_value 		= clean(worksheet.cell_value(curr_row, curr_cell))
				charters[school_IRN][headers[curr_cell]]	= cell_value

write_file.close()

################## DISTRICT SPECIFIC DATA #####################

# District Profile Report Data

filename	= 'District Profile Report Data'
xls_file	= xls_path + 'RAW' + ' ' + filename + '.xlsx'
workbook	= xlrd.open_workbook(xls_file)

worksheet 	= workbook.sheet_by_name('District Data')

# One row per district

csv_file	= csv_path + filename + '.csv'
write_file	= open(csv_file, 'w')
wr 		= csv.writer(write_file, quoting=csv.QUOTE_ALL)

num_rows 					= worksheet.nrows - 1
num_cells 					= worksheet.ncols - 1
curr_row 					= -1
header_row					= True
headers						= []
footer_row					= False

while curr_row < num_rows:
	curr_row 				+= 1
	if curr_row == 1:
		curr_row			+= 1
		header_row 			= False
		for each in headers:
			each 			= clean(each)
		wr.writerow(headers)
		new_headers			= []
		for each in headers:
			each 			= clean(each)
	if header_row:
		curr_cell			= -1
		while curr_cell < num_cells:
			curr_cell 		+= 1
			cell_value 		= str(worksheet.cell_value(curr_row, curr_cell))
			headers.append(cell_value)
	elif not(footer_row):
		row				= worksheet.row_values(curr_row)
		if len(row[0]):
			footer_row		= True
		else:
			wr.writerow(row)
			district_IRN			= worksheet.cell_value(curr_row, 1)
			if type(district_IRN) is float:
				district_IRN		= str(round(district_IRN)).rstrip('0').rstrip('.')
			district_IRN			= district_IRN.zfill(6)

			curr_cell			= -1
			while curr_cell < num_cells:
				curr_cell 		+= 1
				cell_value 		= clean(worksheet.cell_value(curr_row, curr_cell))
				if district_IRN in districts:
					districts[district_IRN][headers[curr_cell]]	= cell_value
				else:
					districts[district_IRN]				= {}
					districts[district_IRN][headers[curr_cell]]	= cell_value

write_file.close()

worksheet 	= workbook.sheet_by_name('Similar District Data')

# One row per district

csv_file	= csv_path + filename + '.csv'
write_file	= open(csv_file, 'w')
wr 		= csv.writer(write_file, quoting=csv.QUOTE_ALL)

num_rows 					= worksheet.nrows - 1
num_cells 					= worksheet.ncols - 1
curr_row 					= -1
header_row					= True
headers						= []
footer_row					= False

while curr_row < num_rows:
	curr_row 				+= 1
	if curr_row == 1:
		header_row 			= False
		for each in headers:
			each 			= clean(each)
		wr.writerow(headers)
		new_headers			= []
		for each in headers:
			each 			= clean(each)
	if header_row:
		curr_cell			= -1
		while curr_cell < num_cells:
			curr_cell 		+= 1
			cell_value 		= str(worksheet.cell_value(curr_row, curr_cell))
			headers.append(cell_value)
	elif not(footer_row):
		row				= worksheet.row_values(curr_row)
		if len(row[0]):
			footer_row		= True
		else:
			wr.writerow(row)
			district_IRN			= worksheet.cell_value(curr_row, 1)
			if type(district_IRN) is float:
				district_IRN		= str(round(district_IRN)).rstrip('0').rstrip('.')
			district_IRN			= district_IRN.zfill(6)

			curr_cell			= -1
			while curr_cell < num_cells:
				curr_cell 		+= 1
				cell_value 		= clean(worksheet.cell_value(curr_row, curr_cell))
				if district_IRN in districts:
					districts[district_IRN][headers[curr_cell]]	= cell_value
				else:
					districts[district_IRN]				= {}
					districts[district_IRN][headers[curr_cell]]	= cell_value

write_file.close()

# District Profile Report Data

filename	= 'June Funding Report'
xls_file	= xls_path + 'RAW' + ' ' + filename + '.xlsx'
workbook	= xlrd.open_workbook(xls_file)

worksheet 	= workbook.sheet_by_name('FY14_SFPR_JUN_2')

# One row per district

csv_file	= csv_path + filename + '.csv'
write_file	= open(csv_file, 'w')
wr 		= csv.writer(write_file, quoting=csv.QUOTE_ALL)

num_rows 					= worksheet.nrows - 1
num_cells 					= worksheet.ncols - 1
curr_row 					= 8
header_row					= True
headers						= ['IRN',\
						'DISTRICT',\
						'COUNTY',\
						'COUNTY NUMBER',\
						'DISTRICT TYPE',\
						'CALCULATED OPPORTUNITY GRANT',\
						'CAPPED OPPORTUNITY GRANT',\
						'CALCULATED TARGETED ASSISTANCE',\
						'CAPPED TARGETED ASSISTANCE',\
						'CALCULATED K-3 LITERACY FUNDING',\
						'CAPPED K-3 LITERACY FUNDING',\
						'CALCULATED ECONOMIC DISADVANTAGED FUNDING',\
						'CAPPED ECONOMIC DISADVANTAGED FUNDING',\
						'CALCULATED LIMITED ENGLISH PROFICIENCY FUNDING',\
						'CAPPED LIMITED ENGLISH PROFICIENCY FUNDING',\
						'CALCULATED GIFTED EDUCATION FUNDING',\
						'CAPPED GIFTED EDUCATION FUNDING',\
						'CALCULATED TRANSPORTATION FUNDING',\
						'CAPPED TRANSPORTATION FUNDING',\
						'CALCULATED SPECIAL EDUCATION ADDITIONAL FUNDING',\
						'CAPPED SPECIAL EDUCATION ADDITIONAL FUNDING',\
						'CALCULATED CAREER TECH EDUCATION FUNDING',\
						'CAPPED CAREER TECH EDUCATION FUNDING',\
						'CALCULATED FUNDING BEFORE GUARANTEE',\
						'CAPPED FUNDING BEFORE GUARANTEE',\
						'TRANSITIONAL GUARANTEE BASE',\
						'TRANSITIONAL GUARANTEE',\
						'TOTAL CALCULATED STATE FUNDING',\
						'PRESCHOOL SPECIAL EDUCATION FUNDING',\
						'SPECIAL EDUCATION TRANSPORTATION FUNDING',\
						'TOTAL ADDITIONAL AID ITEMS',\
						'EDUCATION SERVICE CENTER TRANSFER',\
						'OPEN ENROLLMENT ADJUSTMENT',\
						'COMMUNITY SCHOOL TRANSFER',\
						'STEM SCHOOL TRANSFER',\
						'SCHOLARSHIP TRANSFER',\
						'OTHER ADJUSTMENTS',\
						'TOTAL TRANSFERS & ADJUSTMENTS',\
						'NET STATE FOUNDATION FUNDING',\
						'STATEWIDE TOTAL ADM',\
						'STATEWIDE FORMULA ADM',\
						'STATEWIDE ECONOMIC DISADVANTAGED RATIO',\
						'STATEWIDE MEDIAN INCOME',\
						'STATEWIDE 3 YEAR AVERAGE VALUATION',\
						'STATEWIDE 3 YEAR AVERAGE ADJUSTED VALUATION',\
						'STATEWIDE 3 YEAR FEDERAL GROSS INCOME',\
						'ADJUSTED TOTAL ADM',\
						'TOTAL ADM',\
						'TUITION KINDERGARTEN ADM',\
						'JOINTURE JVS ADM',\
						'FORMULA ADM',\
						'CATEGORY 1 SPECIAL EDUCATION ADM',\
						'CATEGORY 2 SPECIAL EDUCATION ADM',\
						'CATEGORY 3 SPECIAL EDUCATION ADM',\
						'CATEGORY 4 SPECIAL EDUCATION ADM',\
						'CATEGORY 5 SPECIAL EDUCATION ADM',\
						'CATEGORY 6 SPECIAL EDUCATION ADM',\
						'CATEGORY 1 CAREER TECH FTE',\
						'CATEGORY 2 CAREER TECH FTE',\
						'CATEGORY 3 CAREER TECH FTE',\
						'CATEGORY 4 CAREER TECH FTE',\
						'CATEGORY 5 CAREER TECH FTE',\
						'CATEGORY 1 LEP ADM',\
						'CATEGORY 2 LEP ADM',\
						'CATEGORY 3 LEP ADM',\
						'K-3 FORMULA ADM',\
						'K-3 E-SCHOOL FORMULA ADM',\
						'PRESCHOOL AUTISM SCHOLARSHIP ADM',\
						'BRICK & MORTAR & STEM SCHOOL ADM',\
						'E-SCHOOL FORMULA ADM',\
						'NET FORMULA ADM',\
						'JON PETERSON SCHOLARSHIP ADM',\
						'AUTISM SCHOLARSHIP ADM',\
						'EDCHOICE SCHOLARSHIP ADM',\
						'ECONOMIC DISADVANTAGED ADM',\
						'ECONOMIC DISADVANTAGED RATIO',\
						'E-SCHOOL ECONOMIC DISADVANTAGED ADM',\
						'3 YEAR AVERAGE FEDERAL GROSS INCOME',\
						'3 YEAR AVERAGE TOTAL REAL VALUATION',\
						'3 YEAR AVERAGE AGRICULTURAL REAL VALUATION',\
						'3 YEAR AVERAGE ADJSUTED TOTAL VALUATION',\
						'3 YEAR AVERAGE TOTAL VALUATION',\
						'EXEMPT PROPERTY VALUATION',\
						'POTENTIAL PROPERTY VALUATION',\
						'MEDIAN INCOME TY11',\
						'STATE SHARE INDEX',\
						'ECONIMC DISADVANTAGED INDEX',\
						'INCOMING OPEN ENROLLMENT ADM',\
						'OUTGOING OPEN ENROLLMENT ADM',\
						'RESIDENT COMMUNITY SCHOOL ADM',\
						'RESIDENT SPECIAL ED PRESCHOOL CATEGORY 1 ADM',\
						'RESIDENT SPECIAL ED PRESCHOOL CATEGORY 2 ADM',\
						'RESIDENT SPECIAL ED PRESCHOOL CATEGORY 3 ADM',\
						'RESIDENT SPECIAL ED PRESCHOOL CATEGORY 4 ADM',\
						'RESIDENT SPECIAL ED PRESCHOOL CATEGORY 5 ADM',\
						'RESIDENT SPECIAL ED PRESCHOOL CATEGORY 6 ADM']
wr.writerow(headers)

footer_row					= False
district_count					= 0
new_district					= 0

while curr_row < num_rows:
	curr_row 				+= 1
	if not(footer_row):
		row				= worksheet.row_values(curr_row)
		if len(str(row[0])) > 0:
			district_count			+= 1
			wr.writerow(row)
			district_IRN			= int(row[0])
			district_IRN			= fixIRN(district_IRN)

			if district_IRN not in districts:
				districts[district_IRN]	= {}
				new_district		+= 1

			totalADM			= row[47]
			charterADM			= row[89]
			statefunding			= row[27]
			adjustedADM			= totalADM - charterADM
			communitySchoolTrans		= float(row[33]) * -1.0
			try:
				costPerStudent		= communitySchoolTrans / float(adjustedADM)
			except:
				pass
			try:
				costPerClassroom	= communitySchoolTrans / float(districts[district_IRN]['# of FT teachers'])
			except:
				pass

			districts[district_IRN]['Total ADM']				= totalADM
			districts[district_IRN]['In District Charter ADM']		= charterADM
			districts[district_IRN]['State Funding']			= '%.2f' % statefunding
			districts[district_IRN]['Charter Adjusted District ADM']	= adjustedADM
			try:
				districts[district_IRN]['Charter cost per student']	= '%.2f' % costPerStudent
			except:
				pass
			if type(costPerClassroom) is float:
				districts[district_IRN]['Charter cost per classroom']	= '%.2f' % costPerClassroom
			else:
				pass
			
			curr_cell			= -1
			while curr_cell < num_cells:
				curr_cell 		+= 1
				cell_value 		= clean(worksheet.cell_value(curr_row, curr_cell))
				districts[district_IRN][headers[curr_cell]]	= cell_value

write_file.close()

###### DATA PROCESSING #######

#sys.exit()

for charter in charters:
	try:
		if 'Virtual' not in charters[charter]:
			charters[charter]['Virtual'] = 'Site Based'
		stateFund		= float(charters[charter]['Public Funding'])
		ADM			= float(charters[charter]['# of students'])
		stateFundADM		= stateFund / ADM
		charters[charter]['State Funding per Student'] = '%.2F' % stateFundADM
	except:
		pass

for district in districts:
	breakpoint			= 'stateFunding'
	try:
		stateFunding		= float(districts[district]['State Funding'])
		breakpoint		= 'charterTrans'
		charterTrans		= float(districts[district]['Charter Transfer'])
		breakpoint		= 'adjADM'
		adjADM			= float(districts[district]['Charter Adjusted District ADM'])
		breakpoint		= 'adjStateFunding'
		adjStateFunding		= stateFunding - charterTrans
		breakpoint		= 'stateFundADM'
		stateFundADM		= adjStateFunding / adjADM
		breakpoint		= 'Dictionary Assign'
		districts[district]['State Funding per Student'] = '%.2F' % stateFundADM
	except:
		pass

############ OUTPUT COMPLETE CHARTER AND DISTRICT TABLES #########

csv_file				= csv_path + 'Combined Charters.csv'
write_file				= open(csv_file, 'w')
wr 					= csv.writer(write_file, quoting=csv.QUOTE_ALL)

headers					= []
headers.append('School IRN')
for school in charters:
	if len(headers) < 2:
		for header in charters[school].keys():
			headers.append(header)
		wr.writerow(headers)
	row				= []
	row.append(school)
	for col in headers:
		try:
			data 		= charters[school][col]
		except:
			data		= ''
		if type(data) is unicode:
			data		= str(data)
		if type(data) is str:
			data		= clean(data)
		elif type(data) is float:
			data		= '%.2f' % data
		row.append(data)

	wr.writerow(row)

write_file.close()

csv_file				= csv_path + 'Combined Districts.csv'
write_file				= open(csv_file, 'w')
wr 					= csv.writer(write_file, quoting=csv.QUOTE_ALL)

headers					= []
headers.append('District IRN')
for district in districts:
	if len(headers) < 2:
		for header in districts[district].keys():
			headers.append(header)
		wr.writerow(headers)
	row				= []
	row.append(district)
	for col in headers:
		try:
			data 		= districts[district][col]
		except:
			data		= ''
		if type(data) is unicode:
			data		= str(data)
		if type(data) is str:
			data		= clean(data)
		elif type(data) is float:
			data		= '%.2f' % data
		row.append(data)
	wr.writerow(row)

write_file.close()

############ OUTPUT COMPARE YOUR CHARTERS TABLES ############

#### ZIP TABLES ####

csv_file				= web_path + 'Zip Search - Charters.csv'
write_file				= open(csv_file, 'w')
wr 					= csv.writer(write_file, quoting=csv.QUOTE_ALL)

headers					= [\
						'School IRN', \
						'School Name', 
						'Street Address', \
						'City', \
						'State', \
						'Postal Code', \
						'Virtual', \
						'Open Status', \
						'Avg Grade', \
						'Letter grade performance index',\
						'Public Funding', \
						'% Spent in Classroom', \
						'Avg Teacher Experience']

wr.writerow(headers)

for school in charters:
	row 			= []
	row.append(school)
	row.append(pull(charters[school], 'Name'))
	row.append(pull(charters[school], 'Address'))
	row.append(pull(charters[school], 'City'))
	row.append(pull(charters[school], 'State'))
	row.append(pull(charters[school], 'Postal Code'))
	row.append(pull(charters[school], 'Virtual'))
	row.append(pull(charters[school], 'Open Status'))
	row.append(pull(charters[school], 'Avg Grade'))
	row.append(pull(charters[school], 'Letter grade performance index'))
	row.append(pull(charters[school], 'Public Funding'))
	row.append(pull(charters[school], '% Spent in Classroom'))
	row.append(pull(charters[school], 'Avg Teacher Exp'))
	if ('Name' in charters[school]) and ('Public Funding' in charters[school]) and ('# of students' in charters[school]):
		wr.writerow(row)

write_file.close()

csv_file				= web_path + 'Zip Search - Districts.csv'
write_file				= open(csv_file, 'w')
wr 					= csv.writer(write_file, quoting=csv.QUOTE_ALL)

headers					= [\
						'District IRN', \
						'District Name', 
						'Street Address', \
						'City', \
						'State', \
						'Postal Code', \
						'Avg Grade', \
						'Letter grade performance index',\
						'Charter Transfer', \
						'% Spent in Classroom', \
						'Avg Teacher Experience']

wr.writerow(headers)

for district in districts:
	try:
		row 			= []
		row.append(district)
		row.append(pull(districts[district], 'Name'))
		row.append(pull(districts[district], 'Address'))
		row.append(pull(districts[district], 'City'))
		row.append(pull(districts[district], 'State'))
		row.append(pull(districts[district], 'Postal Code'))
		row.append(pull(districts[district], 'Avg Grade'))
		row.append(pull(districts[district], 'Letter grade performance index'))
		row.append(pull(districts[district], 'Charter Transfer'))
		row.append(pull(districts[district], '% Spent in Classroom'))
		row.append(pull(districts[district], 'Avg Teacher Exp'))
		if 'Name' in districts[district]:
			wr.writerow(row)
	except:
		pass

write_file.close()

#### Detail Files ####

csv_file				= web_path + 'Detail - Charters.csv'
write_file				= open(csv_file, 'w')
wr 					= csv.writer(write_file, quoting=csv.QUOTE_ALL)

headers					= [\
						'School IRN', \
						'Name', \
						'Address', \
						'City', \
						'State', \
						'Postal Code', \
						'Virtual', \
						'Open Status', \
						'County', \
						'Sponsor', \
						'Operator', \
						'Organization Status', \
						'Years in operation', \
						'Grades Served', \
						'Specialization', \
						'Avg Teacher Exp', \
						'% of teachers with masters degrees', \
						'Teacher attendance %',\
						\
						'# of students',\
						'# of FT teachers',\
						'Student-teacher ratio',\
						'% of kids in poverty',\
						'% of kids with special needs',\
						'% gifted',\
						'% white',\
						'% non-white',\
						'% enrolled less than 3 years',\
						\
						'Letter grade standards met',\
						'Letter grade performance index',\
						'Performance index score',\
						'Letter grade overall value-add',\
						'Letter grade gifted value-add',\
						'Letter grade disabled value-add',\
						'Letter grade lowest 20% value-add',\
						'Letter grade of AMO',\
						'Attendance rate',\
						'Graduation rate',\
						\
						'State Funding per Student',\
						'% Spent in Classroom',\
						'% Spent on Administration']

wr.writerow(headers)

for school in charters:
	try:
		enrollment		= float(charters[school]['# of students'])
		teachers		= float(charters[school]['# of FT teachers'])
		student_teacher		= '%.1f' % (enrollment/teachers)
		charters[school]['Student-teacher ratio'] = student_teacher
	except:
		pass
		
	row 			= []
	row.append(school)
	
	for i in range(1,len(headers)):
		row.append(pull(charters[school], headers[i]))
		
	if ('Name' in charters[school]) and ('Public Funding' in charters[school]) and ('# of students' in charters[school]):
		wr.writerow(row)

write_file.close()

csv_file				= web_path + 'Detail - Districts.csv'
write_file				= open(csv_file, 'w')
wr 					= csv.writer(write_file, quoting=csv.QUOTE_ALL)

headers					= [\
						'District IRN', \
						'Name', \
						'Address', \
						'City', \
						'State', \
						'Postal Code', \
						'Avg Teacher Exp', \
						'% of teachers with masters degrees', \
						'Teacher attendance %',\
						\
						'# of students',\
						'# of FT teachers',\
						'Student-teacher ratio',\
						'% of kids in poverty',\
						'% of kids with special needs',\
						'% gifted',\
						'% white',\
						'% non-white',\
						'% enrolled less than 3 years',\
						\
						'Letter grade standards met',\
						'Letter grade performance index',\
						'Performance index score',\
						'Letter grade overall value-add',\
						'Letter grade gifted value-add',\
						'Letter grade disabled value-add',\
						'Letter grade lowest 20% value-add',\
						'Letter grade of AMO',\
						'Attendance rate',\
						'Graduation rate',\
						\
						'State Funding per Student',\
						'Charter cost per student', \
						'Charter cost per classroom', \
						'% Spent in Classroom',\
						'% Spent on Administration']

wr.writerow(headers)

for district in districts:
	try:
		enrollment		= float(districts[district]['# of students'])
		teachers		= float(districts[district]['# of FT teachers'])
		student_teacher		= '%.1f' % (enrollment/teachers)
		districts[district]['Student-teacher ratio'] = student_teacher
	except:
		pass
		
	row 			= []
	row.append(district)
	
	for i in range(1,len(headers)):
		row.append(pull(districts[district], headers[i]))
		
	if 'Name' in districts[district]:
		wr.writerow(row)

write_file.close()
