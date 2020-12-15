package vn.ghtk

import org.apache.spark.sql.SparkSession


object KafkaWriteJsonTopic {

  def main(args: Array[String]): Unit = {
    //System.setProperty("hadoop.home.dir", "C:\\winutil\\")
    val spark: SparkSession = SparkSession.builder()
      .master("local[*]")
      .appName("KafkaWriteJsonTopic")
      .getOrCreate()

    val random = scala.util.Random
    val number = random.nextInt(9999)
    val data = Seq(
      ("quangdm","Anne","Jones","39192","Boy",number),
      ("quangvm","Anne","Jones","39192","Boy",number),
      ("huynhnd","Anne","Jones","39192","Boy",number),
      ("tuanla","Anne","Jones","39192","Boy",number)
    )
    val columns = Seq("firstname","middlename","lastname","dob","gender","salary")
    import spark.sqlContext.implicits._
    val df = data.toDF(columns:_*)

      df.selectExpr("CAST(1 AS STRING)", "to_json(struct(*)) AS value")
      .write
      .format("kafka")
      .option("kafka.bootstrap.servers", "192.168.2.115:9092,192.168.2.113:9092,192.168.2.114:9092")
      .option("topic", "dataJson")
      .option("checkpointLocation", "D:/tmp/KafkaWriteJsonTopic")
      .save()

  }
}
