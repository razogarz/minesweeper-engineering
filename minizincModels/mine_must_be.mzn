include "globals.mzn";

% INPUT
% EXPLAINATION:
% -1 indicates unchecked field
% 0..8 indicates number of mines around
% 9 indicates bomb

int: size;
int: mines_count;
array[1..size, 1..size] of -1..8: fields;
array[1..size, 1..size] of 0..1: not_mines;
1..size: x;
1..size: y;

% BOARD AND MINES ALONE
array[1..size, 1..size] of var -1..9: potential_board;
array[1..size, 1..size] of var bool: potential_mines;

% FIELD IS UNKNOWN
constraint fields[x,y] == -1;

% NO MINE ON CLICK
constraint potential_mines[x,y] == true;

% NO MINE ON KNOWN FIELDS
constraint forall (i,j in 1..size) (
  if
    fields[i,j] != -1
  then
    potential_mines[i,j] == false /\
    potential_board[i,j] == fields[i,j]
  endif
);

% ALL MINES ON THE FIELD PRESENT
constraint mines_count = sum(i, j in 1..size) (bool2int(potential_mines[i,j]));

% NO MINE WHERE I KNOW THERE IS NOT ONE
constraint forall (i,j in 1..size) (
  if
    not_mines[i,j] == 1
  then
    potential_mines[i,j] == false
  endif
);

% CHECK IF MINES POSITIONS MATCH CURRENT BOARD STATE
constraint forall (i, j in 1..size) (
  potential_board[i,j] = if potential_mines[i,j]
  then 9
  else
  max(
    sum([bool2int(potential_mines[i+di,j+dj]) 
    | di, dj in -1..1 where
     (di != 0 \/ dj != 0) /\
     i+di >= 1 /\
     i+di <= size /\
     j+dj >= 1 /\
     j+dj <= size
     ]),0)
  endif
);

solve satisfy;

output["x = ", show(x), " y = ", show(y)];