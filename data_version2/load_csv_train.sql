load data infile 'z:\\theblueisland\\tianchi_mobile_recommend_train_user.csv' 
into table _train_user  
fields terminated by ','  optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'
IGNORE 1 LINES
(user_id, item_id, behavior_type, user_geohash, item_category, @time)
set time = STR_TO_DATE(@time, '%Y-%m-%d %H');


load data infile 'z:\\theblueisland\\train_item.csv' 
into table _train_item  
fields terminated by ','  optionally enclosed by '"' escaped by '"' 
lines terminated by '\n'
IGNORE 1 LINES;

load data infile 'z:\\theblueisland\\train_user.csv' 
into table _test_table  
fields terminated by ','  optionally enclosed by '"' escaped by '"' 
lines terminated by '\r\n'
IGNORE 1 LINES
(user_id, item_id, behavior_type, user_geohash, item_category, @time)
set time = STR_TO_DATE(@time, '%Y-%m-%d %H');
