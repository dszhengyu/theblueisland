set @d1 = str_to_date('2014-12-1 00', '%Y-%m-%d %H');
set @d2 = str_to_date('2014-12-11 00', '%Y-%m-%d %H');
set @d3 = str_to_date('2014-12-12 00', '%Y-%m-%d %H');

CREATE TABLE `u_12_1` (
  `user_id` varchar(20) NOT NULL,
  `item_id` varchar(20) NOT NULL,
  `behavior_type` varchar(1) NOT NULL,
  `user_geohash` varchar(20) DEFAULT NULL,
  `item_category` varchar(20) NOT NULL,
  `time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `i_12_1` (
  `user_id` varchar(20) NOT NULL,
  `item_id` varchar(20) NOT NULL,
  `behavior_type` varchar(1) NOT NULL,
  `user_geohash` varchar(20) DEFAULT NULL,
  `item_category` varchar(20) NOT NULL,
  `time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `l_12_1` (
  `user_id` varchar(20) NOT NULL,
  `item_id` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert into u_12_1
	select *
    from _train_user
    where time >= @d1 and time < @d2
    order by user_id, item_id;
 
 insert into i_12_1
	select *
    from _train_user
    where time >= @d1 and time < @d2
    order by item_id ,user_id;
    
insert into l_12_1
	select distinct user_id, item_id
    from _train_user
    where time >= @d2 and time < @d3 and behavior_type = 4;
    
select * from u_12_1
into outfile 'z:\\theblueisland\\u_12_1.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; 

select * from i_12_1
into outfile 'z:\\theblueisland\\i_12_1.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; 

select * from l_12_1
into outfile 'z:\\theblueisland\\l_12_1.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; set @d1 = str_to_date('2014-12-2 00', '%Y-%m-%d %H');
set @d2 = str_to_date('2014-12-12 00', '%Y-%m-%d %H');
set @d3 = str_to_date('2014-12-13 00', '%Y-%m-%d %H');

CREATE TABLE `u_12_2` (
  `user_id` varchar(20) NOT NULL,
  `item_id` varchar(20) NOT NULL,
  `behavior_type` varchar(1) NOT NULL,
  `user_geohash` varchar(20) DEFAULT NULL,
  `item_category` varchar(20) NOT NULL,
  `time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `i_12_2` (
  `user_id` varchar(20) NOT NULL,
  `item_id` varchar(20) NOT NULL,
  `behavior_type` varchar(1) NOT NULL,
  `user_geohash` varchar(20) DEFAULT NULL,
  `item_category` varchar(20) NOT NULL,
  `time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `l_12_2` (
  `user_id` varchar(20) NOT NULL,
  `item_id` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert into u_12_2
	select *
    from _train_user
    where time >= @d1 and time < @d2
    order by user_id, item_id;
 
 insert into i_12_2
	select *
    from _train_user
    where time >= @d1 and time < @d2
    order by item_id ,user_id;
    
insert into l_12_2
	select distinct user_id, item_id
    from _train_user
    where time >= @d2 and time < @d3 and behavior_type = 4;
    
select * from u_12_2
into outfile 'z:\\theblueisland\\u_12_2.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; 

select * from i_12_2
into outfile 'z:\\theblueisland\\i_12_2.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; 

select * from l_12_2
into outfile 'z:\\theblueisland\\l_12_2.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; set @d1 = str_to_date('2014-12-3 00', '%Y-%m-%d %H');
set @d2 = str_to_date('2014-12-13 00', '%Y-%m-%d %H');
set @d3 = str_to_date('2014-12-14 00', '%Y-%m-%d %H');

CREATE TABLE `u_12_3` (
  `user_id` varchar(20) NOT NULL,
  `item_id` varchar(20) NOT NULL,
  `behavior_type` varchar(1) NOT NULL,
  `user_geohash` varchar(20) DEFAULT NULL,
  `item_category` varchar(20) NOT NULL,
  `time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `i_12_3` (
  `user_id` varchar(20) NOT NULL,
  `item_id` varchar(20) NOT NULL,
  `behavior_type` varchar(1) NOT NULL,
  `user_geohash` varchar(20) DEFAULT NULL,
  `item_category` varchar(20) NOT NULL,
  `time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `l_12_3` (
  `user_id` varchar(20) NOT NULL,
  `item_id` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert into u_12_3
	select *
    from _train_user
    where time >= @d1 and time < @d2
    order by user_id, item_id;
 
 insert into i_12_3
	select *
    from _train_user
    where time >= @d1 and time < @d2
    order by item_id ,user_id;
    
insert into l_12_3
	select distinct user_id, item_id
    from _train_user
    where time >= @d2 and time < @d3 and behavior_type = 4;
    
select * from u_12_3
into outfile 'z:\\theblueisland\\u_12_3.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; 

select * from i_12_3
into outfile 'z:\\theblueisland\\i_12_3.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; 

select * from l_12_3
into outfile 'z:\\theblueisland\\l_12_3.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; set @d1 = str_to_date('2014-12-4 00', '%Y-%m-%d %H');
set @d2 = str_to_date('2014-12-14 00', '%Y-%m-%d %H');
set @d3 = str_to_date('2014-12-15 00', '%Y-%m-%d %H');

CREATE TABLE `u_12_4` (
  `user_id` varchar(20) NOT NULL,
  `item_id` varchar(20) NOT NULL,
  `behavior_type` varchar(1) NOT NULL,
  `user_geohash` varchar(20) DEFAULT NULL,
  `item_category` varchar(20) NOT NULL,
  `time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `i_12_4` (
  `user_id` varchar(20) NOT NULL,
  `item_id` varchar(20) NOT NULL,
  `behavior_type` varchar(1) NOT NULL,
  `user_geohash` varchar(20) DEFAULT NULL,
  `item_category` varchar(20) NOT NULL,
  `time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `l_12_4` (
  `user_id` varchar(20) NOT NULL,
  `item_id` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert into u_12_4
	select *
    from _train_user
    where time >= @d1 and time < @d2
    order by user_id, item_id;
 
 insert into i_12_4
	select *
    from _train_user
    where time >= @d1 and time < @d2
    order by item_id ,user_id;
    
insert into l_12_4
	select distinct user_id, item_id
    from _train_user
    where time >= @d2 and time < @d3 and behavior_type = 4;
    
select * from u_12_4
into outfile 'z:\\theblueisland\\u_12_4.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; 

select * from i_12_4
into outfile 'z:\\theblueisland\\i_12_4.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; 

select * from l_12_4
into outfile 'z:\\theblueisland\\l_12_4.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; set @d1 = str_to_date('2014-12-5 00', '%Y-%m-%d %H');
set @d2 = str_to_date('2014-12-15 00', '%Y-%m-%d %H');
set @d3 = str_to_date('2014-12-16 00', '%Y-%m-%d %H');

CREATE TABLE `u_12_5` (
  `user_id` varchar(20) NOT NULL,
  `item_id` varchar(20) NOT NULL,
  `behavior_type` varchar(1) NOT NULL,
  `user_geohash` varchar(20) DEFAULT NULL,
  `item_category` varchar(20) NOT NULL,
  `time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `i_12_5` (
  `user_id` varchar(20) NOT NULL,
  `item_id` varchar(20) NOT NULL,
  `behavior_type` varchar(1) NOT NULL,
  `user_geohash` varchar(20) DEFAULT NULL,
  `item_category` varchar(20) NOT NULL,
  `time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `l_12_5` (
  `user_id` varchar(20) NOT NULL,
  `item_id` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert into u_12_5
	select *
    from _train_user
    where time >= @d1 and time < @d2
    order by user_id, item_id;
 
 insert into i_12_5
	select *
    from _train_user
    where time >= @d1 and time < @d2
    order by item_id ,user_id;
    
insert into l_12_5
	select distinct user_id, item_id
    from _train_user
    where time >= @d2 and time < @d3 and behavior_type = 4;
    
select * from u_12_5
into outfile 'z:\\theblueisland\\u_12_5.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; 

select * from i_12_5
into outfile 'z:\\theblueisland\\i_12_5.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; 

select * from l_12_5
into outfile 'z:\\theblueisland\\l_12_5.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; set @d1 = str_to_date('2014-12-6 00', '%Y-%m-%d %H');
set @d2 = str_to_date('2014-12-16 00', '%Y-%m-%d %H');
set @d3 = str_to_date('2014-12-17 00', '%Y-%m-%d %H');

CREATE TABLE `u_12_6` (
  `user_id` varchar(20) NOT NULL,
  `item_id` varchar(20) NOT NULL,
  `behavior_type` varchar(1) NOT NULL,
  `user_geohash` varchar(20) DEFAULT NULL,
  `item_category` varchar(20) NOT NULL,
  `time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `i_12_6` (
  `user_id` varchar(20) NOT NULL,
  `item_id` varchar(20) NOT NULL,
  `behavior_type` varchar(1) NOT NULL,
  `user_geohash` varchar(20) DEFAULT NULL,
  `item_category` varchar(20) NOT NULL,
  `time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `l_12_6` (
  `user_id` varchar(20) NOT NULL,
  `item_id` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert into u_12_6
	select *
    from _train_user
    where time >= @d1 and time < @d2
    order by user_id, item_id;
 
 insert into i_12_6
	select *
    from _train_user
    where time >= @d1 and time < @d2
    order by item_id ,user_id;
    
insert into l_12_6
	select distinct user_id, item_id
    from _train_user
    where time >= @d2 and time < @d3 and behavior_type = 4;
    
select * from u_12_6
into outfile 'z:\\theblueisland\\u_12_6.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; 

select * from i_12_6
into outfile 'z:\\theblueisland\\i_12_6.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; 

select * from l_12_6
into outfile 'z:\\theblueisland\\l_12_6.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; set @d1 = str_to_date('2014-12-7 00', '%Y-%m-%d %H');
set @d2 = str_to_date('2014-12-17 00', '%Y-%m-%d %H');
set @d3 = str_to_date('2014-12-18 00', '%Y-%m-%d %H');

CREATE TABLE `u_12_7` (
  `user_id` varchar(20) NOT NULL,
  `item_id` varchar(20) NOT NULL,
  `behavior_type` varchar(1) NOT NULL,
  `user_geohash` varchar(20) DEFAULT NULL,
  `item_category` varchar(20) NOT NULL,
  `time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `i_12_7` (
  `user_id` varchar(20) NOT NULL,
  `item_id` varchar(20) NOT NULL,
  `behavior_type` varchar(1) NOT NULL,
  `user_geohash` varchar(20) DEFAULT NULL,
  `item_category` varchar(20) NOT NULL,
  `time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `l_12_7` (
  `user_id` varchar(20) NOT NULL,
  `item_id` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert into u_12_7
	select *
    from _train_user
    where time >= @d1 and time < @d2
    order by user_id, item_id;
 
 insert into i_12_7
	select *
    from _train_user
    where time >= @d1 and time < @d2
    order by item_id ,user_id;
    
insert into l_12_7
	select distinct user_id, item_id
    from _train_user
    where time >= @d2 and time < @d3 and behavior_type = 4;
    
select * from u_12_7
into outfile 'z:\\theblueisland\\u_12_7.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; 

select * from i_12_7
into outfile 'z:\\theblueisland\\i_12_7.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; 

select * from l_12_7
into outfile 'z:\\theblueisland\\l_12_7.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; 