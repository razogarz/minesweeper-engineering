include "globals.mzn";


int: size;
array[int, int] of -1..9: fields;


var int: x;
var int: y; 


constraint x >= 0 /\ x < size;
constraint y >= 0 /\ y < size;

constraint fields[x,y] == -1;


solve satisfy;

output
["click suggested: [", show(x), ",", show(y), "] - ", show(fields[x,y])]