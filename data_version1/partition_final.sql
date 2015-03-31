insert into _set2predict
	select *
    from _train_user
    where item_id in (select item_id from _train_item);

CREATE TABLE `final_feature_item` (
  `user_id` varchar(45) DEFAULT NULL,
  `item_id` varchar(45) DEFAULT NULL,
  `behavior_type` varchar(45) DEFAULT NULL,
  `user_geohash` varchar(45) DEFAULT NULL,
  `item_category` varchar(45) DEFAULT NULL,
  `time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `final_feature_ui` (
  `user_id` varchar(45) DEFAULT NULL,
  `item_id` varchar(45) DEFAULT NULL,
  `behavior_type` varchar(45) DEFAULT NULL,
  `user_geohash` varchar(45) DEFAULT NULL,
  `item_category` varchar(45) DEFAULT NULL,
  `time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

delete from final_feature_item;
delete from final_feature_ui;

insert into final_feature_item
	select * from _set2predict
    order by item_id, user_id;

insert into final_feature_ui
	select * from _set2predict
    order by user_id, item_id;
    
select * from final_feature_item
into outfile 'z:\\theblueisland\\final_feature_item.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; 

select * from final_feature_ui
into outfile 'z:\\theblueisland\\final_feature_ui.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; 

