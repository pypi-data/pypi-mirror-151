
Utilizes pandas, math and numpy.\n
Easy textual print of categorical-only ID3 decision tree adjusted for any number of answers.\n
will clean data of perfectly unique columns (such as an index column).\n
\n
example code:\n
\n
tree = ID3(df, "Purchased?")\n
print(tree)\n
\n
As of now there are four rotating colors for middle nodes (cyan magenta blue yellow) and two (red and green) for the final nodes. \n future release will include functions for controlling the print color scheme.