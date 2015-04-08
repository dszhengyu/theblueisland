set @d1 = str_to_date('2014-12-6 00', '%Y-%m-%d %H');
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
lines terminated by '\n'; 