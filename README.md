# csvcombi.py
Combines data in CSV files according to user-defined parameters.

## Prerequisites
To use csvcombi.py, you will need to have an installation of Python which allows you to run Python files. You will also need a text editor capable of editing Python (.py) files to use csvcombi.py. A basic understanding of Python is recommended, however csvcombi.py is designed to be very accessible to even someone who is inexperienced with Python.

## How to use csvcombi.py
Firstly, place the CSV file that you want to condense in the same directory as csvcombi.py. Open the csvcombi.py file in your chosen text editor. There are three variables which must be changed according to your needs.
### inputName
This corresponds to the file name of your input CSV file, and by default is set to 'input.csv'. You will need to change it to the filename of your input CSV file.
### combineColumn
This corresponds to the index of the column that contains the IDs of the data which will be used to combine the data entries, and by default is set to 0. Note that the first column of data is represented by a value of 0, not by 1. Set this value as appropriate for your data.
### colFunctions
This corresponds to a list of columns of which you wish to combine the data, as well as the method of combining this data. By default, this list is empty. New column functions can be added to this list in the format \[COLUMNNUMBER, METHOD\]. Here, COLUMNNUMBER corresponds to the index of the column, and METHOD corresponds to a string that identifies the method of reducing the column. Note again that a column index of 0 represents the first column, 1 the second, 2 the third, 3 the fourth and so on. This is often forgotten and leads to reading the wrong columns. If adding multiple column functions, remember to separate each entry by a comma, as is standard Python syntax for list entries.

EXAMPLE:
If you wish to reduce the data in the 4th, 5th, and 7th columns, and wish to do so by finding the average value of data in these columns, you would use the following syntax:
```
colFunctions = [
    [3, 'MEAN'],
    [4, 'MEAN'],
    [6, 'MEAN']
    ]
```

#### List of column functions:
- MAX - Stores the maximum value
- MEAN - Stores the mean (average) value of all the values
- MEDIAN - Stores the median value
- MIN - Stores the minimum value
- MODE - Stores the most common value
- STDEV - Stores the standard deviation
- SUM - Stores the sum
- VAR - Stores the variance

### Running the csvcombi.py file
One you have altered the variables as appropriate, open an instance of Command Prompt with the working directory set to the directory of the csvcombi.py file. This can be easily done by navigating to the correct directory in File Explorer, typing 'cmd' in the address bar, and pressing the Enter key. Assuming your Python installation was installed correctly and the PATH variable is correct, you should now be able to run csvcombi.py by entering the command 'python csvcombi.py' into the Command Prompt. Information on the output CSV file will be displayed in Command Prompt, however the output CSV file should always be created in the same directory as the csvcombi.py file. The default output file name is 'output.csv', however this can be changed by the user in the csvcombi.py file. A log file will be created ('log.txt', saved in the same directory as csvcombi.py) containing useful information about the execution of the csvcombi.py script.
