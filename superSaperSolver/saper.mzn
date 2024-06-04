include "globals.mzn";

% INPUT
% EXPLAINATION:
% -1 indicates unchecked field
% 0..8 indicates number of mines around
% 9 indicates bomb

int: size;
int: mines_count;
array[int, int] of -1..8: fields;

% CLICK VARIABLES
var int: x;
var int: y; 

% CLICK POSSIBLE
array[1..size, 1..size] of var 0..9: potential_board;
array[1..size, 1..size] of var 0..9: potential_board_neg;


array[1..size, 1..size] of var bool: potential_mines;
array[1..size, 1..size] of var bool: potential_mines_neg;

%CLICK ON BOARD
constraint x >= 0 /\ x < size;
constraint y >= 0 /\ y < size;

% CLICK ON UNTOUCHED
constraint fields[x,y] == -1;

% NO MINE ON CLICK
constraint potential_mines[x,y] == false;
constraint potential_mines_neg[x,y] == true;

% NO MINE ON KNOWN FIELDS
constraint forall (i,j in 1..size) (
  if 
    fields[i,j] != -1
  then
    potential_mines[i,j] == false /\
    potential_mines_neg[i,j] == false
  endif
);

% THERE ARE ENOUGH MINES
constraint mines_count = sum(i, j in 1..size) (bool2int(potential_mines[i,j]));
constraint mines_count = sum(i, j in 1..size) (bool2int(potential_mines_neg[i,j]));

% CHECK IF MINES POSITIONS MATCH CURRENT BOARD STATE
constraint forall (i, j in 1..size) (
  potential_board[i,j] = if potential_mines[i,j] 
  then 9 
  else
    sum([bool2int(potential_mines[i+di,j+dj]) | di, dj in -1..1 where
     (di != 0 \/ dj != 0) /\
     i+di >= 1 /\ 
     i+di <= size /\ 
     j+dj >= 1 /\ 
     j+dj <= size
     ])
  endif
);

% CHECK IF FIELD DOES NOT MATCH (MEANS THERE CANT BE BOMB)
constraint forall (i, j in 1..size) (
  potential_board_neg[i,j] = if potential_mines_neg[i,j] 
  then 9 
  else
    sum([bool2int(potential_mines_neg[i+di,j+dj]) | di, dj in -1..1 where
     (di != 0 \/ dj != 0) /\
     i+di >= 1 /\ 
     i+di <= size /\ 
     j+dj >= 1 /\ 
     j+dj <= size
     ])
  endif
);



% MATCH FIELDS TO KNOWN BOARD STATE
constraint forall (i, j in 1..size) (
  if fields[i,j] != -1 then
    potential_board[i,j] == fields[i,j]
  endif
);

% SUM OF DIFFERENT FIELDS MORE THAN 0
constraint 0 < sum(
  [bool2int(potential_board_neg[i,j] == fields[i,j]) | i, j in 1..size]
);

% CLICK HAS UNCOVERED FIELD AROUND
% constraint 0 < sum(
%   [bool2int(fields[x-i,y-j] != -1) | i, j in -1..1 
%     where (i != 0 \/ j != 0) /\ 
%            (x-i >= 1 /\ x-i <= size) /\
%            (y-j >= 1 /\ y-j <= size)
%     ]
% );


solve satisfy;

output
["click suggested: [", show(x-1), ",", show(y-1), "] - ", show(fields[x,y])]