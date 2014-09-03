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
| Avg Grade              | Charter Report Card                                             | COMMSCHL                  | Letter grade of performance index    | 20 | No           |
| Public Funding         | District to Charter Transfer by Performance Data                | Sheet1                    | FY13 Total Funding Transfer          | 59 | Yes          |
| % Spent in Classroom   | Charter-District Expenditure Data                               | EFM_Data                  | *                                    | *  | Yes          |
| Avg Teacher Experience | Charter Teacher Data                                            | TEACHER                   | Average Years of teacher experience  | 9  | No           |

#### Transformations

* **City**, **State**, and **Postal Code** are seperated out from a single text field.
* All charters without data for **Virtual** are assumed to be *Site Based*.
* **Public Funding** is the total of this column where the *School IRN matches that of the charter*.
* **% Spent in Classroom** is computed in the following manner:

	1. total expenses are computed by totaling columns 4 through 9
	2. classroom expenditure is computed by subtracting column 8 (administrative) from total expenses
	3. classroom percentage is then computed by dividing classroom expenditure by total expenses
	4. classroom percentage is then rounded to three significant digits
	
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
| Avg Grade              | District Report Card                                            | DISTRICT                  | Letter grade of performance index    | 15 | No           |
| Charter Transfer       | District to Charter Transfer by Performance Data                | Sheet1                    | FY13 Total Funding Transfer          | 59 | Yes          |
| % Spent in Classroom   | Charter-District Expenditure Data                               | EFM_Data                  | *                                    | *  | Yes          |
| Avg Teacher Experience | District Teacher Data                                           | TEACHER                   | Average Years of teacher experience  | 6  | No           |

#### Transformations

* **City**, **State**, and **Postal Code** are seperated out from a single text field.
* **Charter Transfer** is the total of this column where the *District IRN matches that of the District*.
* **% Spent in Classroom** is computed in the following manner:

	1. total expenses are computed by totaling columns 4 through 9
	2. classroom expenditure is computed by subtracting column 8 (administrative) from total expenses
	3. classroom percentage is then computed by dividing classroom expenditure by total expenses
	4. classroom percentage is then rounded to three significant digits

### Detail - Charters.csv

### Detail - Districts.csv

### Transfer Data.csv

