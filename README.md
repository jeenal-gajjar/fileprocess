# ETL sales Module

### Database ###
Install MYSQL Database
Table name must be the same as Model name : product
You can also use the table schema as mentioned in file /etl/Common/tables_schema.sql
$ mysql -u username -p database_name < ../etl/Common/tables_schema.sql

Else You can create table by using below mentioned Query:
CREATE TABLE product(id int NOT NULL AUTO_INCREMENT, product_name varchar(250) DEFAULT NULL, product_category varchar(250) DEFAULT NULL, short_description varchar(250) DEFAULT NULL, room_id INT DEFAULT NULL, location_id varchar(250) DEFAULT NULL, PRIMARY KEY (id));

##### Timezone configuration #####

```buildoutcfg
[mysqld]  
default_time_zone='+00:00'
```

### Quick Setup ###
 * Create python3.6 virtual environment.
   virtualenv venv --python==python3.6
 * Install packages from requirements.txt.
   pip install -r requirements.txt
 
#### Initial configuration
Required Details in configuration File.
---------------------------------------
Please go to in /etl/sales directory  and open sales.conf file.

1.Database Settings: 
------------------------------
Go line no 46 - db section

Set Database Name
Set username
Set password
Set host


2.All Directory path 
--------------------------------
Go line no 8,9,10 - Main Section

Set local_directory
Set working_directory
Set destination_directory

3.Email Settings
---------------------------------
Go line no 61 - email Section

Set sender_email
Set receiver_email
Set subject 
Set password

4.SFTP Settings
--------------------------------
Go line no 26 - sftp_server

Set sftp_host
Set sftp_username
Set sftp_password
Set remote_data_directory


#### How to run?

Cron Job Setup
Need to create CRONTAB by using command crontab -e
Add in file :
* * * * * sh (location of etl.sh file) >> /home/jeenal/etl.log
eg. 0 0 * * * sh /home/jeenal/etl.sh >> /home/jeenal/etl.log
```sh
/,etl.sh
```

