include "globals.mzn";

% INPUT
% EXPLAINATION:
% -1 indicates unchecked field
% 0..8 indicates number of mines around
% 9 indicates bomb

int: rows;
int: cols;
int: mines_count;
array[1..rows, 1..cols] of -1..8: fields;
constraint assert(fields[x,y] == -1, "Field already known");

array[1..rows, 1..cols] of 0..1: not_mines;
1..rows: x;
1..cols: y;

% BOARD AND MINES ALONE
array[1..rows, 1..cols] of var -1..9: potential_board;
array[1..rows, 1..cols] of var bool: potential_mines;

% NO MINE ON CLICK
% we want unsat, so if its unsat with false on this, there has to be mine
constraint potential_mines[x,y] == false;

% NO MINE ON KNOWN FIELDS
constraint forall (i in 1..rows, j in 1..cols) (
  if
    fields[i,j] != -1
  then
    potential_mines[i,j] == false /\
    potential_board[i,j] == fields[i,j]
  endif
);

% ALL MINES ON THE FIELD PRESENT
constraint mines_count == sum(i in 1..rows, j in 1..cols) (bool2int(potential_mines[i,j]));

% NO MINE WHERE I KNOW THERE IS NOT ONE
constraint forall (i in 1..rows, j in 1..cols) (
  if
    not_mines[i,j] == 1 /\ i != x /\ j != y
  then
    potential_mines[i,j] == false
  endif
);

% CHECK IF MINES POSITIONS MATCH CURRENT BOARD STATE
constraint forall (i in 1..rows, j in 1..cols) (
  potential_board[i,j] = if potential_mines[i,j]
  then 9
  else
  max(
    sum([bool2int(potential_mines[i+di,j+dj])
    | di, dj in -1..1 where
     (di != 0 \/ dj != 0) /\
     i+di >= 1 /\
     i+di <= rows /\
     j+dj >= 1 /\
     j+dj <= cols
     ]),0)
  endif
);

solve satisfy;

output["x = ", show(x), " y = ", show(y)];