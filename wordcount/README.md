## Hadoop Example WordCount
Main java:
```java
import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class WordCount {

    public static class TokenizerMapper
            extends Mapper<Object, Text, Text, IntWritable>{

        private final static IntWritable one = new IntWritable(1);
        private Text word = new Text();

        public void map(Object key, Text value, Context context
        ) throws IOException, InterruptedException {
            StringTokenizer itr = new StringTokenizer(value.toString());
            while (itr.hasMoreTokens()) {
                word.set(itr.nextToken());
                context.write(word, one);
            }
        }
    }

    public static class IntSumReducer
            extends Reducer<Text,IntWritable,Text,IntWritable> {
        private IntWritable result = new IntWritable();

        public void reduce(Text key, Iterable<IntWritable> values,
                           Context context
        ) throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            result.set(sum);
            context.write(key, result);
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "word count");
        job.setJarByClass(WordCount.class);
        job.setMapperClass(TokenizerMapper.class);
        job.setCombinerClass(IntSumReducer.class);
        job.setReducerClass(IntSumReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
```
build file.jar:
```text
    Lifecycle clean
    Plugins jar:jar
    Lifecycle install
```
input:
```text
[sherlock@master ~]$ hdfs dfs -ls /example/wordcount/input
Found 4 items
-rw-r--r--   2 sherlock supergroup       4096 2020-01-29 18:23 /example/wordcount/input/.data1.txt.swp
-rw-r--r--   2 sherlock supergroup         29 2020-01-29 18:23 /example/wordcount/input/data1.txt
-rw-r--r--   2 sherlock supergroup         31 2020-01-29 18:23 /example/wordcount/input/data2.txt
-rw-r--r--   2 sherlock supergroup         15 2020-01-29 18:23 /example/wordcount/input/data3.txt
```
run:
```text
[sherlock@master ~]$ hadoop jar wordcount-1.0-SNAPSHOT.jar WordCount /example/wordcount/input /example/wordcount/output
```
view:
```text
....
20/01/29 18:42:00 INFO mapreduce.Job: Running job: job_1580293409881_0001
20/01/29 18:43:08 INFO mapreduce.Job: Job job_1580293409881_0001 running in uber mode : false
20/01/29 18:43:08 INFO mapreduce.Job:  map 0% reduce 0%
20/01/29 18:44:15 INFO mapreduce.Job:  map 67% reduce 0%
20/01/29 18:44:22 INFO mapreduce.Job:  map 100% reduce 0%
20/01/29 18:44:47 INFO mapreduce.Job:  map 100% reduce 100%
20/01/29 18:44:50 INFO mapreduce.Job: Job job_1580293409881_0001 completed successfully
20/01/29 18:44:54 INFO mapreduce.Job: Counters: 49
....
```
output:
```text
[sherlock@master ~]$ hdfs dfs -ls /example/wordcount/
Found 2 items
drwxr-xr-x   - sherlock supergroup          0 2020-01-29 18:23 /example/wordcount/input
drwxr-xr-x   - sherlock supergroup          0 2020-01-29 18:44 /example/wordcount/output
[sherlock@master ~]$ hdfs dfs -ls /example/wordcount/output
Found 2 items
-rw-r--r--   2 sherlock supergroup          0 2020-01-29 18:44 /example/wordcount/output/_SUCCESS
-rw-r--r--   2 sherlock supergroup         22 2020-01-29 18:44 /example/wordcount/output/part-r-00000
[sherlock@master ~]$ hdfs dfs -cat /example/wordcount/output/part-r-00000
haui	6
manh	4
quang	4
```
Follow me [github](https://github.com/DoManhQuang) and [facebook](https://www.facebook.com/manhquang.rnd)