package vn.ghtk

import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.streaming.Trigger

import org.apache.spark.sql.types.{IntegerType, StringType, StructField, StructType}

object StreamWriteConsole {
  def main(args: Array[String]): Unit = {
    System.setProperty("hadoop.home.dir", "C:\\winutil\\")
    // Create a local StreamingContext with two working thread and batch interval of 1 second.
    // The master requires 2 cores to prevent from a starvation scenario.

    //    val conf = new SparkConf().setMaster("local[*]").setAppName("StreamExample")
    //    val ssc = new StreamingContext(conf, Seconds(5))

    val spark = SparkSession
      .builder()
      .appName("StreamWriteConsole")
      .master("local[*]")
      .getOrCreate()

    //    val columns = Seq("firstname","middlename","lastname","dob","gender","salary")

    val schema = StructType(
      List(
        StructField("firstname", StringType, true),
        StructField("middlename", StringType, true),
        StructField("lastname", StringType, true),
        StructField("dob", StringType, true),
        StructField("gender", StringType, true),
        StructField("salary", IntegerType, true)
      )
    )

    val df = spark.readStream
      .schema(schema)
      .parquet("D:/tmp/output/KafkaStreamParquet")

    df.writeStream
      .format("console")
      .outputMode("append")
      .option("checkpointLocation", "D:/tmp/KafkaStreamParquet")
      .trigger(Trigger.ProcessingTime("5 seconds"))
      .start()
      .awaitTermination()

//    df.writeStream
//      .format("parquet")
//      .outputMode("append")
//      .option("checkpointLocation", "D:/school/study/maven/test3/hello")
//      .option("path", "D:/school/study/data/output/op1")
//      .trigger(Trigger.ProcessingTime("5 seconds"))
//      .start()
//      .awaitTermination()

  }
}
