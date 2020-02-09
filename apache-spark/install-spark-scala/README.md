## Setup Apache Spark & Scala
Bạn có thể click vào các [title]() để download.
* Chuẩn bị:
    * [setup cluster hadoop](https://domanhquang.github.io/bigdatacoban/install-hadoop/)
    * [scala](http://downloads.typesafe.com/scala/2.11.7/scala-2.11.7.tgz)
    * [apache spark](http://mirror.downloadvn.com/apache/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz)

Nào sau khi chuẩn bị xong chúng ta bắt đầu cài đặt nhé!

Bước 1: Giải nén spark & scala
```text
    tar -xvf spark-2.4.4-bin-hadoop2.7
    tar -xvf scala-2.11.7.tgz
```
Bước 2: Cấu hình scala
```text
    sudo mv scala-2.11.7 /usr/lib
    sudo ln -s /usr/lib/scala-2.11.7 /usr/lib/scala
    vim .bashrc
----------file .bashrc-----------
# set scala

export PATH=$PATH:/usr/lib/scala/bin
---------------------------------
    
    source .bashrc
    scala -version
-------------output--------------
Scala code runner version 2.11.7 -- Copyright 2002-2013, LAMP/EPFL
---------------------------------
```
Bước 3: Cấu hình apache spark
```text
    vim .bashrc
----------file .bashrc-----------
# set spark

export SPARK_HOME=$HOME/spark-2.4.4-bin-hadoop2.7
export PATH=$PATH:$SPARK_HOME/bin
---------------------------------
    
    source .bashrc
    spark-shell
-------------output--------------
....
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 2.4.4
      /_/
         
Using Scala version 2.11.12 (Java HotSpot(TM) 64-Bit Server VM, Java 1.8.0_241)
Type in expressions to have them evaluated.
Type :help for more information.
....
---------------------------------
```
