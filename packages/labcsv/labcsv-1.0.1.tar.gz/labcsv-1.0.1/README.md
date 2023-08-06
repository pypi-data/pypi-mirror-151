# labcsv.py
You can easily get the data you need columns from lab.js.csv!

# Installation
`pip install labcsv`


# How to Use
### Read CSV
```python
from labcsv import read_csv,DefaultHeaderName as LHName
rlab = read_csv("tests/test.csv") #<- path
```

### Get columns data
The type of data returned is ndarray.

```python
values = rlab.get_column_values(LHName.SENDER) #n×1 size
# or
values = rlab.get_column_values([LHName.SENDER,LHName.RESPONSE,LHName.DURATION]) # n×3 size
# or
values = rlab.get_column_values("Param1") #custom column name
# or 
values = rlab.get_column_values([LHName.SENDER, "Param1"]) #multiple
```

### nan to empty string

```python
from labcsv import read_csv,DefaultHeaderName as LHName
rlab = read_csv("tests/test.csv")
rlab.pandas_data.fillna('', inplace=True) #<---
print(rlab.get_column_values("Param1"))
```
You can use pandas functions.

### Get meta
None yet.
