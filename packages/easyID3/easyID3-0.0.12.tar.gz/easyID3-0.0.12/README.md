
Utilizes pandas, math and numpy.\
Easy textual print of categorical-only ID3 decision tree adjusted for any number of answers.\
will clean data of perfectly unique columns (such as an index column).\
\
example code:\
\n
tree = ID3(df, "Purchased?")\
print(tree)\
\
As of now there are four rotating colors for middle nodes (cyan magenta blue yellow) and two (red and green) for the final nodes. \ future release will include functions for controlling the print color scheme.