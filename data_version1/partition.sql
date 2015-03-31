delete from train_feature_item;
delete from train_feature_ui;
delete from train_feature_user;

delete from train_label_item;
delete from train_label_ui;
delete from train_label_user;

delete from predict_feature_item;
delete from predict_feature_ui;
delete from predict_feature_user;

delete from predict_label_item;
delete from predict_label_ui;
delete from predict_label_user;

set @TP1 = str_to_date('2014-11-18 00', '%Y-%m-%d %H');
set @TP2 = str_to_date('2014-12-8 23', '%Y-%m-%d %H');
set @TP3 = str_to_date('2014-12-18 23', '%Y-%m-%d %H');
set @FL1 = str_to_date('2014-12-7 23', '%Y-%m-%d %H');
set @FL2 = str_to_date('2014-12-17 23', '%Y-%m-%d %H');

insert into train_feature_item
	select *
	from _train_user
	where time > @TP1 and time < @FL1
	order by item_id, user_id;
    
insert into train_feature_ui
	select *
	from _train_user
	where time > @TP1 and time < @FL1
	order by user_id, item_id;
    
insert into train_label_item
	select distinct item_id
	from _train_user
	where time > @FL1 and time < @TP2 and behavior_type = 4
    order by item_id;

insert into train_label_ui
	select distinct user_id, item_id 
	from _train_user
	where time > @FL1 and time < @TP2 and behavior_type = 4
    order by user_id, item_id;



insert into predict_feature_item
	select *
	from _train_user
	where time > @TP2 and time < @FL2
	order by item_id, user_id;
    
insert into predict_feature_ui
	select *
	from _train_user
	where time > @TP2 and time < @FL2
	order by user_id, item_id;    
    
insert into predict_label_item
	select distinct item_id
	from _train_user
	where time > @FL2 and time < @TP3 and behavior_type = 4
    order by item_id;

insert into predict_label_ui
	select distinct user_id, item_id 
	from _train_user
	where time > @FL2 and time < @TP3 and behavior_type = 4
    order by user_id, item_id;


select * from train_feature_item 
into outfile 'z:\\theblueisland\\train_feature_item.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; 

select * from train_feature_ui
into outfile 'z:\\theblueisland\\train_feature_ui.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; 

select * from train_label_item
into outfile 'z:\\theblueisland\\train_label_item.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; 

select * from train_label_ui
into outfile 'z:\\theblueisland\\train_label_ui.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; 


select * from predict_feature_item 
into outfile 'z:\\theblueisland\\predict_feature_item.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; 

select * from predict_feature_ui
into outfile 'z:\\theblueisland\\predict_feature_ui.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; 

select * from predict_label_item
into outfile 'z:\\theblueisland\\predict_label_item.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; 

select * from predict_label_ui
into outfile 'z:\\theblueisland\\predict_label_ui.csv' 
fields terminated by ',' optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'; 