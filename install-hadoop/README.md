## Hướng dẫn cài đặt cụm master-slave hadoop

* Chuẩn bị 
    * master: 192.168.10.100
    * slave1: 192.168.10.101
    * slave2: 192.168.10.102
    * [apache-hadoop-2.7.7](http://mirror.downloadvn.com/apache/hadoop/common/hadoop-2.7.7/hadoop-2.7.7.tar.gz)
    * [java-jdk8](https://download.oracle.com/otn/java/jdk/8u241-b07/1f5b5a70bf22433b84d0e960903adac8/jdk-8u241-linux-x64.tar.gz)
    
 * Bước 1: Giải nén hadoop & jdk8
 ```text
    tar -xvf hadoop-2.7.7.tar.gz
    tar -xvf jdk-8u241-linux-x64.tar.gz
``` 
* Bước 2: Cấu hình file .bashrc trên cụm master-slave hadoop
```text
    cd ~
    vi .bashrc
--------------------------------
    # Thêm cấu hình vào file .bashrc
    #set hadoop
    
    export HADOOP_HOME=$HOME/hadoop-2.7.7
    export HADOOP_CONF_DIR=$HOME/hadoop-2.7.7/etc/hadoop
    export HADOOP_MAPRED_HOME=$HOME/hadoop-2.7.7
    export HADOOP_COMMON_HOME=$HOME/hadoop-2.7.7
    export HADOOP_HDFS_HOME=$HOME/hadoop-2.7.7
    export YARN_HOME=$HOME/hadoop-2.7.7
    export PATH=$PATH:$HOME/hadoop-2.7.7/bin
                 
    #set java
    
    export JAVA_HOME=$HOME/jdk1.8.0_241
    export PATH=$HOME/jdk1.8.0_241/bin:$PATH
--------------------------------
    source .bashrc
    java -version
    hadoop version
```
* Bước 3: Tạo file master và chỉnh sửa file slave trên máy server master
```text
    cd hadoop-2.7.7/etc/hadoop/
    cp slaves masters
    vi masters
# chỉnh sửa file master, xóa cấu hình cũ và thêm cấu hình mới:
------------------------------
master
------------------------------
    
    vi slaves
# chỉnh sửa file slave, xóa cấu hình cũ và thêm cấu hình mới:
------------------------------
master
slave1
slave2
------------------------------
``` 
* Bước 4: Chỉnh sửa file slave trên máy server slave1&2
```text
    cd hadoop-2.7.7/etc/hadoop/
    vi slaves

# máy slave 1
------------------------------
slave1
------------------------------

# máy slave 2
------------------------------
slave2
------------------------------    
```
Bước 5: Cấu hình file core-site.xml trên cụm máy master và slaves
```text
    cd hadoop-2.7.7/etc/hadoop/
    vi core-site.xml
-----------------------------
<configuration>
        <property>
                <name>fs.default.name</name>
                <value>hdfs://master:9000</value>
        </property>
</configuration>
-----------------------------
```
Bước 6: Cấu hình file hdfs-site.xml trên máy server master
```text
    cd hadoop-2.7.7/etc/hadoop/
    vi hdfs-site.xml
-----------------------------
<configuration>
        <property>
                <name>dfs.replication</name>
                <value>2</value>
        </property> 
        <property>
                <name>dfs.permission</name> 
                <value>false</value>
        </property>
        <property>
                <name>dfs.namenode.name.dir</name> 
                <value>$HOME/hadoop-2.7.7/namenode</value>
        </property> 
        <property>
                <name>dfs.datanode.data.dir</name>
                <value>$HOME/hadoop-2.7.7/datanode</value>
        </property>
</configuration>
-----------------------------
```
Bước 7: Cấu hình file hdfs-site.xml trên máy server slave1&2
```text
    cd hadoop-2.7.7/etc/hadoop/
    vi hdfs-site.xml
-----------------------------
<configuration>
        <property>
                <name>dfs.replication</name>
                <value>2</value>
        </property>
        <property>
                <name>dfs.permission</name> 
                <value>false</value>
        </property>
        <property>
                <name>dfs.datanode.data.dir</name> 
                <value>$HOME/hadoop-2.7.7/datanode</value>
        </property> 
</configuration>
-----------------------------
```
Bước 8: Cấu hình file mapred-site.xml trên cụm master-slaves
```text
    cd hadoop-2.7.7/etc/hadoop/
    cp mapred-site.xml.template mapred-site.xml
    vi mapred-site.xml
------------------------------
<configuration>
        <property>
                <name>mapreduce.framework.name</name>
                <value>yarn</value>
        </property>
</configuration>
------------------------------
```
Bước 9: Cấu hình file yarn-site.xml trên cụm master-slaves
```text
    cd hadoop-2.7.7/etc/hadoop/
    vi yarn-site.xml
------------------------------
<configuration>
        <property>
                <name>yarn.nodemanager.aux-services</name>
                <value>mapreduce_shuffle</value>
        </property>
        <property>
                <name>yarn.nodemanager.auxservices.mapreduce.shuffle.class</name>
                <value>org.apache.hadoop.mapred.ShuffleHandler</value>
        </property>
</configuration>
------------------------------
```
Bước 10: format namenode trên máy server master
```text
    cd hadoop-2.7.7/bin/
    hadoop namenode -format
```
Bước 11: start hadoop trên máy server master
```text
    cd hadoop-2.7.7/sbin
    hadoop-daemon.sh start namenode
    hadoop-daemon.sh start datanode
    yarn-daemon.sh start resourcemanager
    yarn-daemon.sh start nodemanager
    jps
--------------------------------
7153 NameNode
7603 NodeManager
9096 Jps
7355 ResourceManager
7245 DataNode
--------------------------------
```
Bước 12: start hadoop trên máy server slave
```text
    cd hadoop-2.7.7/sbin
    hadoop-daemon.sh start datanode
    yarn-daemon.sh start nodemanager
    jps
--------------------------------
7609 NodeManager
7243 DataNode
--------------------------------
```
Bước 13: Xem kết quả giao diện hadoop
```text
    http://192.168.10.100:50070/
```
![img2](https://domanhquang.github.io/bigdatacoban/install-hadoop/img/view-hadoop.png)

![img1](https://domanhquang.github.io/bigdatacoban/install-hadoop/img/view-hadoop-datanode.png)

