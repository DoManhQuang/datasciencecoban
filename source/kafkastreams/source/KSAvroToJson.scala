package vn.ghtk

import java.nio.file.{Files, Paths}

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.avro.from_avro
import org.apache.spark.sql.functions.col
import org.apache.spark.sql.streaming.Trigger

object KSAvroToJson {
  def main(args: Array[String]): Unit = {

    //System.setProperty("hadoop.home.dir", "C:\\winutil\\")
    val spark: SparkSession = SparkSession.builder()
      .master("local[*]")
      .config("", "")
      .appName("KSAvroToJson")
      .getOrCreate()

    // Subscribe to 1 topic
    val df = spark
      .readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", "192.168.2.115:9092,192.168.2.113:9092,192.168.2.114:9092")
      .option("subscribe", "quang_avro_topic")
      .load()

    df.printSchema()

    val jsonFormatSchema = new String(
      Files.readAllBytes(Paths.get("/home/manhquang/stream/resources/shemadata.avsc")))

    val dataTable = df.select(from_avro(col("value"), jsonFormatSchema).as("person"))
      .select("person.*")

    dataTable.printSchema()

    dataTable.writeStream
      .format("json")
      .outputMode("append")
      .option("checkpointLocation", "/tmp/KSAvroToJson-checkpoint")
      .option("path", "/quangdm/stream/json")
      .trigger(Trigger.ProcessingTime("5 seconds"))
      .start()
      .awaitTermination()
  }
}
