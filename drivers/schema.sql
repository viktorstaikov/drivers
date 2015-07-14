drop table if exists drivers;
create table drivers (
  id integer primary key autoincrement,
  name text not null,
  status integer 
);