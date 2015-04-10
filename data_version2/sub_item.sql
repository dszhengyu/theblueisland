select item_id, item_category from _sub_item
into outfile 'z:\\theblueisland\\subItem.csv' 
fields terminated by ','
lines terminated by '\n'; 