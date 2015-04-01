set @d1 = str_to_date('2014-11-22 00', '%Y-%m-%d %H');
set @d2 = str_to_date('2014-12-02 00', '%Y-%m-%d %H');
set @d3 = str_to_date('2014-12-03 00', '%Y-%m-%d %H');

CREATE TABLE `u_11_22` (
  `user_id` varchar(20) NOT NULL,
  `item_id` varchar(20) NOT NULL,
  `behavior_type` varchar(1) NOT NULL,
  `user_geohash` varchar(20) DEFAULT NULL,
  `item_category` varchar(20) NOT NULL,
  `time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `i_11_22` (
  `user_id` varchar(20) NOT NULL,
  `item_id` varchar(20) NOT NULL,
  `behavior_type` varchar(1) NOT NULL,
  `user_geohash` varchar(20) DEFAULT NULL,
  `item_category` varchar(20) NOT NULL,
  `time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `l_11_22` (
  `user_id` varchar(20) NOT NULL,
  `item_id` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert into u_11_22
	select *
    from _train_user
    where time >= @d1 and time < @d2
    order by user_id, item_id;
 
 insert into i_11_22
	select *
    from _train_user
    where time >= @d1 and time < @d2
    order by item_id ,user_id;
    
insert into l_11_22
	select distinct user_id, item_id
    from _train_user
    where time >= @d2 and time < @d3 and behavior_type = 4;
    
select * from u_11_22
into outfile 'z:\\theblueisland\\u_11_22.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; 

select * from i_11_22
into outfile 'z:\\theblueisland\\i_11_22.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; 

select * from l_11_22
into outfile 'z:\\theblueisland\\l_11_22.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; 