from flask import session
import re
NoneType = type(None)

#Scripts go here

#Count Categories for a given table
def CategoryCount(table,Categories):
    #Grab Headers
    headers = table.iloc[0]
    #Set table to only Categories
    table = table.iloc[:,9]
    
    CategoryLen = len(Categories)
    countArray = [0]*CategoryLen

    for row in table:
        #Regex the numbers out of the Category column and convert them to int
        var = [int(cat) for cat in re.findall(r'\d+', row)]
        #Go through each value in the row
        for Category in var:
            index = Category-1
            countArray[index] += 1

    return countArray