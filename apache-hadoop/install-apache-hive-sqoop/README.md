## Cài đặt Apache Hive & Apache Sqoop

Bạn click vào [title]() để download!

* Chuẩn bị:
    * Cấu hình [Hadoop Cluster](https://domanhquang.github.io/bigdatacoban/install-hadoop/) xem ở bài trước.
    * [apache-hive-2.1.0](http://archive.apache.org/dist/hive/hive-2.1.0/apache-hive-2.1.0-bin.tar.gz)
    * [apache-sqoop-1.4.7](http://mirror.downloadvn.com/apache/sqoop/1.4.7/sqoop-1.4.7.bin__hadoop-2.6.0.tar.gz)
    * [mysql-connector-java-8](https://cdn.mysql.com//archives/mysql-connector-java-8.0/mysql-connector-java-8.0.15.tar.gz)
 
#### Apache Hive

Bước 1: Giải nén Hive.

 ```text
    tar -xvf apache-hive-2.1.0-bin
```

Bước 2: cấu hình file .bashrc

```text
    cd ~
    vim .bashrc
------------------------
# set hive
            
export HIVE_HOME=$HOME/apache-hive-2.1.0-bin
export PATH=$PATH:$HOME/apache-hive-2.1.0-bin/bin
------------------------
    source .bashrc
```
 
Bước 3: Kiểm tra hive version

```text
    hive --version
-------------------------
...
Hive 2.1.0
Subversion git://jcamachguezrMBP/Users/jcamachorodriguez/src/workspaces/hive/HIVE-release2/hive -r 9265bc24d75ac945bde9ce1a0999fddd8f2aae29
Compiled by jcamachorodriguez on Fri Jun 17 01:03:25 BST 2016
...
-------------------------
```

Bước 4: Khởi tạo thư mục lưu trữ dữ liệu của Hive trên HDFS

```text
# tạo thư mục trên HDFS
    hdfs dfs -mkdir -p /user/hive/warehouse
    hdfs dfs -mkdir /tmp
# set quyền read/write
    hdfs dfs -chmod g+w /user/hive/warehouse
    hdfs dfs -chmod g+w /tmp
```

Bước 5: Cấu hình file hive-env.sh

```text
    cd $HOME/apache-hive-2.1.0-bin/conf
    vim hive-env.sh
---------------------------
export HADOOP_HEAPSIZE=1024
export HADOOP_HOME=/home/sherlock/hadoop-2.7.7
export HIVE_CONF_DIR=/home/sherlock/apache-hive-2.1.0-bin/conf
---------------------------
```

Bước 6: Cấu hình file hive-site.xml

```text
    cd $HOME/apache-hive-2.1.0-bin/conf
    vim hive-site.xml
---------------------------------
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>

	<property>
		<name>javax.jdo.option.ConnectionURL</name>
		<value>jdbc:derby:;databaseName=//home/sherlock/apache-hive-2.1.0-bin/metastore_db;create=true</value>
		<description>
		JDBC connect string for a JDBC metastore.
		To use SSL to encrypt/authenticate the connection, provide database-specific SSL flag in the connection URL.
		For example, jdbc:postgresql://myhost/db?ssl=true for postgres database.
		</description>
	</property>
	<property>
		<name>hive.metastore.warehouse.dir</name>
		<value>/user/hive/warehouse</value>
		<description>location of default database for the warehouse</description>
	</property>
	<property>
		<name>hive.metastore.uris</name>
		<value/>
		<description>Thrift URI for the remote metastore. Used by metastore client to connect to remote metastore.</description>
	</property>
	<property>
		<name>javax.jdo.option.ConnectionDriverName</name>
		<value>org.apache.derby.jdbc.EmbeddedDriver</value>
		<description>Driver class name for a JDBC metastore</description>
	</property>

	<property>
		<name>javax.jdo.PersistenceManagerFactoryClass</name>
		<value>org.datanucleus.api.jdo.JDOPersistenceManagerFactory</value>
		<description>class implementing the jdo persistence</description>
	</property>

</configuration>
---------------------------------
```

Bước 7: Hive sử dụng Derby database, nên khởi tạo derby

```text
    cd $HOME/apache-hive-2.1.0-bin
    bin/schematool -initSchema -dbType derby

...
Initialization script completed
schemaTool completed
```

Bước 8: Run Hive

```text
    cd ~
    hive
# Hoặc sử dụng
    cd $HOME/apache-hive-2.1.0-bin/bin/
    hive

...
hive>
hive> show databases;
OK
default
Time taken: 1.889 seconds, Fetched: 1 row(s)
hive> 
hive> exit; # thoát khỏi hive
```

#### Apache Sqoop

Bước 1: Giải nén sqoop và mysql

```text
    tar -xvf sqoop-1.4.7.bin__hadoop-2.6.0.tar.gz 
    tar -xvf mysql-connector-java-8.0.15.tar.gz
```

Bước 2: Cấu hình file .bashrc

```text
    cd ~
    vim .bashrc
---------------------------
# set sqoop 
    
export SQOOP_HOME=$HOME/sqoop-1.4.7.bin__hadoop-2.6.0
export PATH=$PATH:$SQOOP_HOME/bin
---------------------------
    source .bashrc
```

Bước 3: Chuyển thư viện mysql-connector-java-8.0.15 vào sqoop-1.4.7/lib

```text
    cd ~
    mv mysql-connector-java-8.0.15/mysql-connector-java-8.0.15.jar sqoop-1.4.7.bin__hadoop-2.6.0/lib
```

Bước 4 : Kiểm tra sqoop version

```text
    cd ~
    sqoop version

...
Sqoop 1.4.7
git commit id 2328971411f57f0cb683dfb79d19d4d19d185dd8
Compiled by maugli on Thu Dec 21 15:59:58 STD 2017
```
Bài tiếp theo chúng ta sẽ làm một số ví dụ về hive và sqoop nhé!