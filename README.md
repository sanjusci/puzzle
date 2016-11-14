# puzzle

A large group of friends from the town of Nocillis visit the vineyards of Apan to taste wines. 
The vineyards produce many  fine wines and the friends decide to buy as many as 3 bottles of wine each 
if they are available to purchase. Unfortunately,  the vineyards of Apan have a peculiar restriction that 
they can not sell more than one bottle of the same wine. So the vineyards  come up with the following scheme: 
They ask each person to write down a list of up to 10 wines that they enjoyed and would be happy buying. 
With this information, please help the vineyards maximize the number of wines that they can sell to the group of friends.

Input: 

A two-column TSV file with the first column containing the ID (just a string) of a person and the second column 
the ID of the wine  that they like: https://s3.amazonaws.com/br-user/puzzles/person_wine_3.txt

Output: 

First line contains the number of wine bottles sold in aggregate with your solution. Each subsequent line should be 
two columns, tab separated. The first column is an ID of a person and the second column should be the ID of the wine 
that they will buy.

Please check your work. Note that the IDs of the output second column should be unique since a single bottle of wine 
can not be sold to two people and an ID on the first column can appear at most three times since each person can only 
buy up to 3 bottles of wine.

#Run Using command line

python puzzle.py filename
