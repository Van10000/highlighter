var i: integer;
begin
// С помощью for
  For i := 1 to 5 do
    write(i,' ');
  writeln;
 
  For i := 5 downto 1 do
    write(i,' ');
  writeln;
  writeln;
 
// С помощью while
  i := 1;
  while i<=5 do
  begin
    write(i,' ');
    i := i + 1;
  end;
  writeln;
 
  i := 5;
  while i>=1 do
  BEGIN
    write(i,' ');
    i := i - 1;
  END;
  writeln;
  writeln;
 
// С помощью repeat
  i := 1;
  repeat
    write(i,' ');
    i := i + 1;
  until i>5;
  writeln;
 
  i := 5;
  repeat
    write(i,' ');
    i := i - 1;
  until i<1;
  writeln;
end.