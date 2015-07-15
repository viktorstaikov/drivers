drop table if exists drivers;
create table drivers (
  id integer primary key autoincrement,
  name text not null unique,
  email text not null unique,
  status integer 
);