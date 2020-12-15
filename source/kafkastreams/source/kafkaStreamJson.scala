package vn.ghtk

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions.{col, from_json}
import org.apache.spark.sql.streaming.Trigger
import org.apache.spark.sql.types.{IntegerType, StringType, StructType}

object kafkaStreamJson {
  def main(args: Array[String]): Unit = {

    //System.setProperty("hadoop.home.dir", "C:\\winutil\\")
    val spark: SparkSession = SparkSession.builder()
      .master("local[*]")
      .config("","")
      .appName("kafkaStreamJson")
      .getOrCreate()

    // Subscribe to 1 topic
    val df = spark
      .readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", "192.168.2.115:9092,192.168.2.113:9092,192.168.2.114:9092")
      .option("subscribe", "dataJson")
      .load()

    df.printSchema()


    val schema = new StructType()
      .add("firstname",StringType)
      .add("middlename",StringType)
      .add("lastname",StringType)
      .add("dob",StringType)
      .add("gender",StringType)
      .add("salary",IntegerType)

    val dataTable = df.selectExpr("CAST(value AS STRING) as value").select(from_json(col("value")
      .cast("string"), schema)
      .as("data"))
      .select("data.*")
//
//    dataTable.show(false)
//
//    dataTable.writeStream
//      .format("console")
//      .outputMode("append")
//      .option("checkpointLocation", "D:/tmp/kafkaStreamJson")
//      .trigger(Trigger.ProcessingTime("5 seconds"))
//      .start()
//      .awaitTermination()

    dataTable.writeStream
      .format("json")
      .outputMode("append")
      .option("checkpointLocation", "/tmp/kafkaStreamJson")
      .option("path", "/quangdm/stream/json")
      .trigger(Trigger.ProcessingTime("5 seconds"))
      .start()
      .awaitTermination()



  }
}
