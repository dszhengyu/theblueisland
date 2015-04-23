set @d1 = str_to_date('2014-12-9 00', '%Y-%m-%d %H');
set @d2 = str_to_date('2014-12-19 00', '%Y-%m-%d %H');

CREATE TABLE `u_target` (
  `user_id` varchar(20) NOT NULL,
  `item_id` varchar(20) NOT NULL,
  `behavior_type` varchar(1) NOT NULL,
  `user_geohash` varchar(20) DEFAULT NULL,
  `item_category` varchar(20) NOT NULL,
  `time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `i_target` (
  `user_id` varchar(20) NOT NULL,
  `item_id` varchar(20) NOT NULL,
  `behavior_type` varchar(1) NOT NULL,
  `user_geohash` varchar(20) DEFAULT NULL,
  `item_category` varchar(20) NOT NULL,
  `time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert into u_target
	select *
    from _train_user
    where time >= @d1 and time < @d2
    order by user_id, item_id;
 
 insert into i_target
	select *
    from _train_user
    where time >= @d1 and time < @d2
    order by item_id ,user_id;
    
select * from u_target
into outfile 'z:\\theblueisland\\u_target.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; 

select * from i_target
into outfile 'z:\\theblueisland\\i_target.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; 

select distinct item_id, item_category from _train_item
into outfile 'z:\\theblueisland\\subItem.csv' 
fields terminated by ','
lines terminated by '\n'; 