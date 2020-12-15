//package vn.ghtk
//
//import java.nio.file.{Files, Paths}
//
//import com.fasterxml.jackson.databind.ObjectMapper
//import org.apache.spark.sql.SparkSession
//import org.apache.spark.sql.avro.from_avro
//import org.apache.spark.sql.functions.col
//import org.apache.spark.sql.streaming.Trigger
//import org.mortbay.util.ajax.JSON
//import scalaj.http.{Http, HttpResponse}
//
//import scala.io.Source
//
//object KSAvroToParquet {
//  def main(args: Array[String]): Unit = {
//
//    System.setProperty("hadoop.home.dir", "C:\\winutil\\")
//    val spark: SparkSession = SparkSession.builder()
//      .master("local[*]")
//      .config("","")
//      .appName("KSAvroToParquet")
//      .getOrCreate()
//
//    // Subscribe to 1 topic
//    val df = spark
//      .readStream
//      .format("kafka")
//      .option("kafka.bootstrap.servers", "192.168.2.115:9092,192.168.2.113:9092,192.168.2.114:9092")
//      .option("subscribe", "quang_avro_topic")
//      .load()
//
//    df.printSchema()
////    val resourcesPath = getClass.getResource("/shemadata.avsc")
////    println(resourcesPath.getFile)
//
//
//
////    val jsonFormatSchema = new String(
////      Files.readAllBytes(Paths.get("./src/main/resources/shemadata.avsc")))
//
//
////    val jsonFormatSchema = new String(
////      Files.readAllBytes(Paths.get("/home/manhquang/stream/resources/shemadata.avsc")))
//
//    val response: HttpResponse[String] = Http("http://192.168.2.113:8081/schemas/ids/27").asString
//    val body = response.body
//    val objectMapper = new ObjectMapper()
//    val jsonNode = objectMapper.readTree(body.toString)
//    val jsonFormatSchema = jsonNode.get("schema").asText
//	println(jsonFormatSchema)
//
//    val dataTable = df.select(from_avro(col("value"), jsonFormatSchema).as("person"))
//      .select("person.*")
//
//    dataTable.printSchema()
//
//    dataTable.writeStream
//      .format("parquet")
//      .outputMode("append")
//      .option("checkpointLocation", "/tmp/KSAvroToParquet-checkpoint")
//      .option("path", "/quangdm/stream/output/parquet")
//      .trigger(Trigger.ProcessingTime("5 seconds"))
//      .start()
//      .awaitTermination()
//  }
//}
