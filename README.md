# Synopsis

This is a python package to digest a library of excel workbooks concerning Ohio education, and prepare a set of csv files as the backend for the Choose Your Charters website. The following csv files are created:

1. Zip Search - Charters.csv
2. Zip Search - Districts.csv
3. Detail - Charters.csv
4. Detail - Districts.csv
5. Transfer Data.csv

The information between sheets is connected using the IRN.

### Zip Search - Charters.csv

| CSV Column             | Origin Workbook                                                 | Worksheet                 | Col Name                             | #  | Transformed? |
|------------------------|-----------------------------------------------------------------|---------------------------|--------------------------------------|----|--------------|
| School IRN             | District to Charter Transfer by Performance Data                | Sheet1                    | Community School IRN                 | 23 | No           |
|                        | Charter Report Card                                             | COMMSCHL                  | Building IRN                         | 1  | No           |
| School Name            | District to Charter Transfer by Performance Data                | Sheet1                    | Community School                     | 24 | No           |
|                        | Charter Report Card                                             | COMMSCHL                  | Building Name                        | 2  | No           |
| Street Address         | Charter Report Card                                             | COMMSCHL                  | Street address                       | 7  | No           |
| City                   | Charter Report Card                                             | COMMSCHL                  | City and Zip code                    | 8  | Yes          |
| State                  | Charter Report Card                                             | COMMSCHL                  | City and Zip code                    | 8  | Yes          |
| Postal Code            | Charter Report Card                                             | COMMSCHL                  | City and Zip code                    | 8  | Yes          |
| Virtual                | Charter Annual Report Academic Performance and Demographic Data | TABLE 1A_Trad Demo & Acad | School Type 2                        | 8  | Yes          |
| Open Status            | Charter Report Card                                             | COMMSCHL                  | Open/Closed Status (as of 8/20/2013) | 12 | No           |
| Avg Grade              | Charter Report Card                                             | COMMSCHL                  | *                                    | *  | Yes          |
| Letter grade performance index     | Charter Report Card                                             | COMMSCHL                  | Letter grade of performance index         | 20  | No           |
| Public Funding         | District to Charter Transfer by Performance Data                | Sheet1                    | FY13 Total Funding Transfer          | 59 | Yes          |
| % Spent in Classroom   | Charter-District Expenditure Data                               | EFM_Data                  | *                                    | *  | Yes          |
| Avg Teacher Experience | Charter Teacher Data                                            | TEACHER                   | Average Years of teacher experience  | 9  | No           |

#### Transformations

* **City**, **State**, and **Postal Code** are seperated out from a single text field.
* All charters without data for **Virtual** are assumed to be *Site Based*.
* **Avg Grade** is computed in the following manner:

	1. all columns in the Charter Report Card which recieved a letter grade are collected
	2. these letters are translated to point equivalent (4.0 - 0.0)
	3. these points are averaged
	4. the average is translated back into a letter grade

* **Public Funding** is the total of this column where the *School IRN matches that of the charter*.
* **% Spent in Classroom** is computed in the following manner:

	1. total expenses are computed by totaling columns 4 through 9
	2. classroom expenditure is computed by subtracting column 8 (administrative) from total expenses
	3. classroom percentage is then computed by dividing classroom expenditure by total expenses
	4. classroom percentage is then rounded to three significant digits

* All **Dropout Recovery Schools** which have an entry in the *Dropout Recovery Report Card* will first take available data from that sheet. If there is no entry in *Charter Report Card* it will leave the grade metrics blank as they do not appear in the *Dropout Recovery Report Card*.
	
### Zip Search - Districts.csv

| CSV Column             | Origin Workbook                                                 | Worksheet                 | Col Name                             | #  | Transformed? |
|------------------------|-----------------------------------------------------------------|---------------------------|--------------------------------------|----|--------------|
| District IRN           | District to Charter Transfer by Performance Data                | Sheet1                    | IRN of District of Residence         | 1  | No           |
|                        | District Report Card                                            | DISTRICT                  | District IRN                         | 1  | No           |
| District Name          | District to Charter Transfer by Performance Data                | Sheet1                    | District                             | 2  | No           |
|                        | District Report Card                                            | DISTRICT                  | District Name                        | 2  | No           |
| Street Address         | District Report Card                                            | DISTRICT                  | Street address                       | 5  | No           |
| City                   | District Report Card                                            | DISTRICT                  | City and Zip code                    | 6  | Yes          |
| State                  | District Report Card                                            | DISTRICT                  | City and Zip code                    | 6  | Yes          |
| Postal Code            | District Report Card                                            | DISTRICT                  | City and Zip code                    | 6  | Yes          |
| Avg Grade              | District Report Card                                            | DISTRICT                  | *                                    | *  | Yes          |
| Letter grade performance index     | District Report Card                                | DISTRICT                  | Letter grade of performance index         | 15  | No           |
| Charter Transfer       | District to Charter Transfer by Performance Data                | Sheet1                    | FY13 Total Funding Transfer          | 59 | Yes          |
| % Spent in Classroom   | Charter-District Expenditure Data                               | EFM_Data                  | *                                    | *  | Yes          |
| Avg Teacher Experience | District Teacher Data                                           | TEACHER                   | Average Years of teacher experience  | 6  | No           |

#### Transformations

* **City**, **State**, and **Postal Code** are seperated out from a single text field.
* **Avg Grade** is computed in the following manner:

	1. all columns in the District Report Card which recieved a letter grade are collected
	2. these letters are translated to point equivalent (4.0 - 0.0)
	3. these points are averaged
	4. the average is translated back into a letter grade

* **Charter Transfer** is the total of this column where the *District IRN matches that of the District*.
* **% Spent in Classroom** is computed in the following manner:


	1. total expenses are computed by totaling columns 4 through 9
	2. classroom expenditure is computed by subtracting column 8 (administrative) from total expenses
	3. classroom percentage is then computed by dividing classroom expenditure by total expenses
	4. classroom percentage is then rounded to three significant digits

### Detail - Charters.csv

| CSV Column                         | Origin Workbook                                                 | Worksheet                 | Col Name                                  | #   | Transformed? |
|------------------------------------|-----------------------------------------------------------------|---------------------------|-------------------------------------------|-----|--------------|
| School IRN                         | District to Charter Transfer by Performance Data                | Sheet1                    | Community School IRN                      | 23  | No           |
|                                    | Charter Report Card                                             | COMMSCHL                  | Building IRN                              | 1   | No           |
| Name                               | District to Charter Transfer by Performance Data                | Sheet1                    | Community School                          | 24  | No           |
|                                    | Charter Report Card                                             | COMMSCHL                  | Building Name                             | 2   | No           |
| Address                            | Charter Report Card                                             | COMMSCHL                  | Street address                            | 7   | No           |
| City                               | Charter Report Card                                             | COMMSCHL                  | City and Zip code                         | 8   | Yes          |
| State                              | Charter Report Card                                             | COMMSCHL                  | City and Zip code                         | 8   | Yes          |
| Postal Code                        | Charter Report Card                                             | COMMSCHL                  | City and Zip code                         | 8   | Yes          |
| Virtual                            | Charter Annual Report Academic Performance and Demographic Data | TABLE 1A_Trad Demo & Acad | School Type 2                             | 8   | Yes          |
| Open Status                        | Charter Report Card                                             | COMMSCHL                  | Open/Closed Status (as of 8/20/2013)      | 12  | No           |
| County                             | Charter Report Card                                             | COMMSCHL                  | County                                    | 5   | No           |
| Sponsor                            | Charter Annual Report Academic Performance and Demographic Data | TABLE 1A_Trad Demo & Acad | Sponsor Name                              | 2   | No           |
| Operator                | Charter Operator Data | Sheet1 | Charter Operator                        | 3  | No          |
| Organizational Status                | Charter Operator Data | Sheet1 | Organization Status                        | 4  | No          |
| Years in operation                 | Charter Annual Report Academic Performance and Demographic Data | TABLE 1A_Trad Demo & Acad | First Year of Operation                   | 5   | Yes          |
| Grades Served                      | Charter Report Card                                             | COMMSCHL                  | Grade Span                                | 11  | No
| Specialization                     | Charter Annual Report Academic Performance and Demographic Data | TABLE 1A_Trad Demo & Acad | School Type 3                             | 9   | No           |
| Avg Teacher Exp                    | Charter Teacher Data                                            | TEACHER                   | Average Years of teacher experience       | 9   | No           |
| % of teachers with masters degrees | Charter Teacher Data                                            | TEACHER                   | % of Teachers who have at least a masters | 16  | No           |
| Teacher attendance %               | Charter Teacher Data                                            | TEACHER                   | Teachers attendance rate 2012-13          | 8   | No           |
| # of students                      | *                                             | *                  | *                                | *  | Yes           |
| # of FT teachers                   | Charter Teacher Data                                            | TEACHER                   | Number of Full Time teachers              | 10  | No           |
| Student-teacher ratio              | *                                                               | *                         | *                                         | *   | Yes          |       
| % of kids in poverty               | Charter Economically Disadvantaged Data                         | BLDG_ECONOMIC_13          | % of total enrollment                     | 39  | No           |
| % of kids with special needs       | Charter Disability Data                                         | BLDG_DISABILITY_13        | % of total enrollment                     | 39  | No           |
| % gifted                           | Charter Gifted Data                                             | BLDG_GIFTED_13            | % of total enrollment                     | 39  | No           |
| % white                            | Charter Racial Data                                             | BLDG_ETHNIC_13            | % of total enrollment                     | 39  | No           |
| % non-white                        | Charter Racial Data                                             | BLDG_ETHNIC_13            | % of total enrollment                     | 39  | Yes          |     
| % enrolled less than 3 years       | Charter Mobility Data                                           | BLDG_ETHNIC_13            | % of total enrollment                     | 39  | Yes          |   
| Letter grade standards met         | Charter Report Card                                             | COMMSCHL                  | Letter grade of standards met             | 17  | No           |
| Letter grade performance index     | Charter Report Card                                             | COMMSCHL                  | Letter grade of performance index         | 20  | No           |
| Performance index score            | Charter Report Card                                             | COMMSCHL                  | Performance Index Score 2012-13           | 18  | No           |
| Letter grade overall value-add     | Charter Report Card                                             | COMMSCHL                  | Letter grade of Overall Value-Added       | 21  | No           |
| Letter grade gifted value-add      | Charter Report Card                                             | COMMSCHL                  | Letter grade of Gifted Value-Added        | 22  | No           |
| Letter grade disabled value-add    | Charter Report Card                                             | COMMSCHL                  | Letter grade of Disabled Value-Added      | 23  | No           |
| Letter grade lowest 20% value-add  | Charter Report Card                                             | COMMSCHL                  | Letter grade of Lowest 20% Value-Added    | 24  | No           |
| Letter grade of AMO                | Charter Report Card                                             | COMMSCHL                  | Letter grade of AMO                       | 25  | No           |
| Attendance rate                    | Charter Report Card                                             | COMMSCHL                  | Attendance 2012-13                        | 103 | No           |
| Graduation rate                    | Charter Report Card                                             | COMMSCHL                  | Multiple Columns                          | *   | Yes          |
| State Funding per Student          | *                                                               | *                         | *                                         | *   | Yes          |       
| % Spent in Classroom               | Charter-District Expenditure Data                               | EFM_Data                  | Multiple Columns                          | *   | Yes          |
| % Spent on Administration          | *                                                               | *                         | *                                         | *   | Yes          |       

#### Transformations

* **City**, **State**, and **Postal Code** are seperated out from a single text field.
* All charters without data for **Virtual** are assumed to be *Site Based*.
* **Years in Operation** is computed by subtracting the first year in service from 14. If the result is zero, the value 'First' is returned.
* **# of students** is first computed by rounding the most recent figure from the *Charter Annual Report Enrollment History Data*. If this is not available, it will instead be set to the *Enrollment* column of the *Charter Report Card*.
* **Student-teacher ratio** is computed by dividing the **# of students** by **# of FT teachers** and rounding to one decimal place.
* **% non-white** is computed by subtracting **% white** from 1.
* **% enrolled less than 3 years** is computed by subtracting *% of total enrollment* for *Longevity3orMore* from 1.
* **Graduation rate** is computed in the following manner:

	1. Four-Year Graduation Rate Numerator 2012 is divided by Four-Year Graduation Rate Denominator 2012. 
	2. Graduation rate is then rounded to three significant digits

* **State Funding per Student** is computed by taking the **Public Funding** (see Zip Search - Charters.csv) and dividing by **# of students**, then rounding to two decimal places.
* **% Spent in Classroom** is computed in the following manner:

	1. total expenses are computed by totaling columns 4 through 9
	2. classroom expenditure is computed by subtracting column 8 (administrative) from total expenses
	3. classroom percentage is then computed by dividing classroom expenditure by total expenses
	4. classroom percentage is then rounded to three significant digits
	
* **% Spent on Administration** is computed by subtracting **% Spent in Classroom** from 1.

* All **Dropout Recovery Schools** which have an entry in the *Dropout Recovery Report Card* will first take available data from that sheet. If there is no entry in *Charter Report Card* it will leave the grade metrics blank as they do not appear in the *Dropout Recovery Report Card*.

### Detail - Districts.csv

| CSV Column                         | Origin Workbook                                  | Worksheet                 | Col Name                                  | #   | Transformed? |
|------------------------------------|--------------------------------------------------|---------------------------|-------------------------------------------|-----|--------------|
| District IRN                       | District to Charter Transfer by Performance Data | Sheet1                    | IRN of District of Residence              | 1   | No           |
|                                    | District Report Card                             | DISTRICT                  | District IRN                              | 1   | No           |
| District Name                      | District to Charter Transfer by Performance Data | Sheet1                    | District                                  | 2   | No           |
|                                    | District Report Card                             | DISTRICT                  | District Name                             | 2   | No           |
| Street Address                     | District Report Card                             | DISTRICT                  | Street address                            | 5   | No           |
| City                               | District Report Card                             | DISTRICT                  | City and Zip code                         | 6   | Yes          |
| State                              | District Report Card                             | DISTRICT                  | City and Zip code                         | 6   | Yes          |
| Postal Code                        | District Report Card                             | DISTRICT                  | City and Zip code                         | 6   | Yes          |
| Avg Teacher Exp                    | District Teacher Data                            | TEACHER                   | Average Years of teacher experience       | 6   | No           |
| % of teachers with masters degrees | District Teacher Data                            | TEACHER                   | % of Teachers who have at least a masters | 13  | No           |
| Teacher attendance %               | District Teacher Data                            | TEACHER                   | Teachers attendance rate 2012-13          | 5   | No           |
| # of students                      | District Report Card                             | DISTRICT                  | Enrollment                                | 25  | No           |
| # of FT teachers                   | District Teacher Data                            | TEACHER                   | Number of Full Time teachers              | 7   | No           |
| Student-teacher ratio              | *                                                | *                         | *                                         | *   | Yes          |       
| % of kids in poverty               | District Economically Disadvantaged Data         | DIST_ECONOMIC_13          | % of total enrollment                     | 34  | No           |
| % of kids with special needs       | District Disability Data                         | DIST_DISABILITY_13        | % of total enrollment                     | 34  | No           |
| % gifted                           | District Gifted Data                             | DIST_GIFTED_13            | % of total enrollment                     | 34  | No           |
| % white                            | District Racial Data                             | DIST_ETHNIC_13            | % of total enrollment                     | 34  | No           |
| % non-white                        | District Racial Data                             | DIST_ETHNIC_13            | % of total enrollment                     | 34  | Yes          |     
| % enrolled less than 3 years       | District Mobility Data                           | DIST_ETHNIC_13            | % of total enrollment                     | 34  | Yes          |   
| Letter grade standards met         | District Report Card                             | DISTRICT                  | Letter grade of standards met             | 12  | No           |
| Letter grade performance index     | District Report Card                             | DISTRICT                  | Letter grade of performance index         | 15  | No           |
| Performance index score            | District Report Card                             | DISTRICT                  | Performance Index Score 2012-13           | 13  | No           |
| Letter grade overall value-add     | District Report Card                             | DISTRICT                  | Letter grade of Overall Value-Added       | 16  | No           |
| Letter grade gifted value-add      | District Report Card                             | DISTRICT                  | Letter grade of Gifted Value-Added        | 17  | No           |
| Letter grade disabled value-add    | District Report Card                             | DISTRICT                  | Letter grade of Disabled Value-Added      | 18  | No           |
| Letter grade lowest 20% value-add  | District Report Card                             | DISTRICT                  | Letter grade of Lowest 20% Value-Added    | 19  | No           |
| Letter grade of AMO                | District Report Card                             | DISTRICT                  | Letter grade of AMO                       | 20  | No           |
| Attendance rate                    | District Report Card                             | DISTRICT                  | Attendance 2012-13                        | 98  | No           |
| Graduation rate                    | Charter Annual Report Academic Performance and Demographic Data              | *                  | 2012 4 Year Graduation Rate                    | *   | No          |
| State Funding per Student          | June Funding Report                              | FY14_SFPR_JUN_2           | Multiple Columns                          | *   | Yes          |       
| Charter cost per student           | June Funding Report                              | FY14_SFPR_JUN_2           | Community School Transfer                 | 34  | Yes          |       
| Charter cost per classroom         | June Funding Report                              | FY14_SFPR_JUN_2           | Community School Transfer                 | 34  | Yes          |       
| % Spent in Classroom               | Charter-District Expenditure Data                | EFM_Data                  | Multiple Columns                          | *   | Yes          |
| % Spent on Administration          | *                                                | *                         | *                                         | *   | Yes          |       

#### Transformations

* **City**, **State**, and **Postal Code** are seperated out from a single text field.
* **Student-teacher ratio** is computed by dividing the **# of students** by **# of FT teachers** and rounding to one decimal place.
* **% non-white** is computed by subtracting **% white** from 1.
* **% enrolled less than 3 years** is computed by subtracting *% of total enrollment* for *Longevity3orMore* from 1.
* **State Funding per Student** is computed in the following manner:


	1. Compute *State Funding* by taking *Charter Transfer* (see Zip Search - District.csv) and subtracting *Total Calculated State Funding* from the *June Funding Report*.
	2. Compute *Adjusted ADM* by subtracting *Resident Community School ADM* from *Adjusted Total ADM* (both from the *June Funding Report*).
	3. Divide *State Funding* by the *Adjusted ADM* and round to two decimal points.

* **Charter cost per student** is computed by taking the *Community School Transfer* column and dividing by the *Adjusted ADM*.
* **Charter cost per classroom** is computed by taking the *Community School Transfer* column and dividing by the *# of FT teachers* (this assumes approximately one classroom / FT teacher.

* **% Spent in Classroom** is computed in the following manner:


	1. total expenses are computed by totaling columns 4 through 9
	2. classroom expenditure is computed by subtracting column 8 (administrative) from total expenses
	3. classroom percentage is then computed by dividing classroom expenditure by total expenses
	4. classroom percentage is then rounded to three significant digits
	
* **% Spent on Administration** is subtracting **% Spent in Classroom** from 1.

### Transfer Data.csv

| CSV Column             | Origin Workbook                                                 | Worksheet                 | Col Name                             | #  | Transformed? |
|------------------------|-----------------------------------------------------------------|---------------------------|--------------------------------------|----|--------------|
| District IRN           | District to Charter Transfer by Performance Data                | Sheet1                    | IRN of District of Residence         | 1  | No           |
| District Name          | District to Charter Transfer by Performance Data                | Sheet1                    | District                             | 2  | No           |
| School IRN             | District to Charter Transfer by Performance Data                | Sheet1                    | Community School IRN                 | 23 | No           |
| School Name            | District to Charter Transfer by Performance Data                | Sheet1                    | Community School                     | 24 | No           |
| Transfer               | District to Charter Transfer by Performance Data                | Sheet1                    | FY13 Total Funding Transfer          | 59 | No           |

