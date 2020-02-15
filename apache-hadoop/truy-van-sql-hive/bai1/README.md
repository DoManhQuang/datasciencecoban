## Truy vấn dữ liệu cơ bản trên apache hive

#### Click vào để xem cấu hình [Apache Hive]()

Run Hive:
```text
    hive
------------------------
[sherlock@master ~]$ hive
which: no hbase in (/home/sherlock/jdk1.8.0_241/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/sherlock/hadoop-2.7.7/bin:/usr/lib/scala/bin:/home/sherlock/spark-2.4.4-bin-hadoop2.7/bin:/home/sherlock/apache-hive-2.1.0-bin/bin:/home/sherlock/sqoop-1.4.7.bin__hadoop-2.6.0/bin:/home/sherlock/.local/bin:/home/sherlock/bin)
SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: Found binding in [jar:file:/home/sherlock/apache-hive-2.1.0-bin/lib/log4j-slf4j-impl-2.4.1.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/home/sherlock/hadoop-2.7.7/share/hadoop/common/lib/slf4j-log4j12-1.7.10.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J: Actual binding is of type [org.apache.logging.slf4j.Log4jLoggerFactory]

Logging initialized using configuration in jar:file:/home/sherlock/apache-hive-2.1.0-bin/lib/hive-common-2.1.0.jar!/hive-log4j2.properties Async: true
Hive-on-MR is deprecated in Hive 2 and may not be available in the future versions. Consider using a different execution engine (i.e. spark, tez) or using Hive 1.X releases.
hive>
------------------------
```

Cú pháp truy vấn cơ bản:

```text
hive> show databases;
OK
default
Time taken: 1.472 seconds, Fetched: 1 row(s)
hive> create database quanghaui;
OK
Time taken: 0.712 seconds
hive> use quanghaui;
OK
Time taken: 0.021 seconds
hive> create table sinhvien(masv int, tensv string, lop string);
OK
Time taken: 0.903 seconds
hive> show create table sinhvien;
OK
CREATE TABLE `sinhvien`(
  `masv` int, 
  `tensv` string, 
  `lop` string)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  'hdfs://master:9000/user/hive/warehouse/quanghaui.db/sinhvien'
TBLPROPERTIES (
  'COLUMN_STATS_ACCURATE'='{\"BASIC_STATS\":\"true\"}', 
  'numFiles'='0', 
  'numRows'='0', 
  'rawDataSize'='0', 
  'totalSize'='0', 
  'transient_lastDdlTime'='1581317621')
Time taken: 0.708 seconds, Fetched: 19 row(s)
```

Insert Data:
```text
hive> insert into sinhvien(masv, tensv, lop) values ('1', 'manhquang', 'httt1'), ('2', 'ngoc hung', 'httt1'), ('3', 'thuy huong', 'httt1');
WARNING: Hive-on-MR is deprecated in Hive 2 and may not be available in the future versions. Consider using a different execution engine (i.e. spark, tez) or using Hive 1.X releases.
Query ID = sherlock_20200210140114_565ce279-1049-40c6-9313-549092b7854a
Total jobs = 3
Launching Job 1 out of 3
Number of reduce tasks is set to 0 since there's no reduce operator
Starting Job = job_1581309943515_0001, Tracking URL = http://master:8088/proxy/application_1581309943515_0001/
Kill Command = /home/sherlock/hadoop-2.7.7/bin/hadoop job  -kill job_1581309943515_0001
Hadoop job information for Stage-1: number of mappers: 1; number of reducers: 0
2020-02-10 14:01:58,394 Stage-1 map = 0%,  reduce = 0%
2020-02-10 14:02:11,304 Stage-1 map = 100%,  reduce = 0%, Cumulative CPU 2.51 sec
MapReduce Total cumulative CPU time: 2 seconds 510 msec
Ended Job = job_1581309943515_0001
Stage-4 is selected by condition resolver.
Stage-3 is filtered out by condition resolver.
Stage-5 is filtered out by condition resolver.
Moving data to directory hdfs://master:9000/user/hive/warehouse/quanghaui.db/sinhvien/.hive-staging_hive_2020-02-10_14-01-14_008_207370989929231550-1/-ext-10000
Loading data to table quanghaui.sinhvien
MapReduce Jobs Launched: 
Stage-Stage-1: Map: 1   Cumulative CPU: 2.51 sec   HDFS Read: 4370 HDFS Write: 129 SUCCESS
Total MapReduce CPU Time Spent: 2 seconds 510 msec
OK
Time taken: 61.733 seconds
```

Query Data :

```text
hive> select * from sinhvien;
OK
1	manhquang	httt1
2	ngoc hung	httt1
3	thuy huong	httt1
Time taken: 0.375 seconds, Fetched: 3 row(s)
hive> select * from sinhvien where masv = 1;
OK
1	manhquang	httt1
Time taken: 0.923 seconds, Fetched: 1 row(s)
hive> select COUNT(*) from sinhvien;
WARNING: Hive-on-MR is deprecated in Hive 2 and may not be available in the future versions. Consider using a different execution engine (i.e. spark, tez) or using Hive 1.X releases.
Query ID = sherlock_20200210140557_26fe21aa-f299-4f74-9b76-8cddedd5c805
Total jobs = 1
Launching Job 1 out of 1
Number of reduce tasks determined at compile time: 1
In order to change the average load for a reducer (in bytes):
  set hive.exec.reducers.bytes.per.reducer=<number>
In order to limit the maximum number of reducers:
  set hive.exec.reducers.max=<number>
In order to set a constant number of reducers:
  set mapreduce.job.reduces=<number>
Starting Job = job_1581309943515_0002, Tracking URL = http://master:8088/proxy/application_1581309943515_0002/
Kill Command = /home/sherlock/hadoop-2.7.7/bin/hadoop job  -kill job_1581309943515_0002
Hadoop job information for Stage-1: number of mappers: 1; number of reducers: 1
2020-02-10 14:06:10,337 Stage-1 map = 0%,  reduce = 0%
2020-02-10 14:06:22,932 Stage-1 map = 100%,  reduce = 0%, Cumulative CPU 2.01 sec
2020-02-10 14:06:37,436 Stage-1 map = 100%,  reduce = 100%, Cumulative CPU 3.88 sec
MapReduce Total cumulative CPU time: 3 seconds 880 msec
Ended Job = job_1581309943515_0002
MapReduce Jobs Launched: 
Stage-Stage-1: Map: 1  Reduce: 1   Cumulative CPU: 4.14 sec   HDFS Read: 7800 HDFS Write: 101 SUCCESS
Total MapReduce CPU Time Spent: 4 seconds 140 msec
OK
3
Time taken: 45.698 seconds, Fetched: 1 row(s)
```

Exit hive:
```text
hive> exit;
```