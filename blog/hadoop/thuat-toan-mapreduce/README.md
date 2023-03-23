## Thuật Toán MapReduce
Hi, các bạn! hôm nay chúng ta sẽ cùng tìm hiểu về thuật toán MapReduce trong xử lý dữ liệu lớn nhé.

#### Giới thiệu
<i>Có thể bạn chưa biết ?</i>

 * <b>Sáng lập</b>: Các kỹ sư Google
 * <b>Một chút khái niệm</b>: MapReduce là một mô hình lập trình và triển khai các vấn để xử lý trong Bigdata. Sử dụng thuật toán xử lý phân tán, song song trên một cụm các máy tính.
 * <b>Chương trình MapReduce bao gồm 2 phần chính</b> : ```Map procedure``` & ```Reduce```.
 * <b>Hệ thống MapReduce</b> (còn gọi là Cơ sở hạ tầng MapReduce) phối hợp xử lý bằng cách sắp xếp các máy chủ phân tán, chạy song song các tác vụ khác nhau, quản lý tất cả các giao tiếp và truyền dữ liệu giữa các phần khác nhau của hệ thống và hỗ trợ đề phòng sự cố và khả năng chịu lỗi.
 * Một số dự án phát triển : [Apache Hadoop](https://en.wikipedia.org/wiki/Apache_Hadoop) (open source), Apache Mahout ([ASF](https://en.wikipedia.org/wiki/Apache_Mahout)) 

#### Đào sâu một chút
* Chương trình MapReduce(Programming model):
    * ```input data``` tương ứng với key<sub>i</sub> / value<sub>i</sub> & ```output data``` tương ứng với key<sub>o</sub> / value<sub>o</sub>.
    * <b>function</b> ```map (in_key, in_value) -> list(out_key, intermediate_value)```:
        * Xử lý cặp key<sub>i</sub> / value<sub>i</sub>.
        * Đưa ra tập hợp các cặp trung gian.
    * <b>function</b> ```reduce (out_key, list(intermediate_value)) -> list(out_value)```:
        * Kết hợp tất cả các giá trị trung gian cho một <b>key<b> cụ thể.
        * Tạo ra một tập hợp các key<sub>o</sub> / value<sub>o</sub> được hợp nhất (thường chỉ là một)

![img4](https://domanhquang.github.io/datasciencecoban/image/img-mapreduce/44.png)
* Hệ thống MapReduce (MapReduce System):
    * ```Map```: Mỗi node(máy tính) worker áp dụng hàm ```Map()``` cho dữ liệu cục bộ và ghi đầu ra vào bộ lưu trữ tạm thời. Node master đảm bảo rằng chỉ một bản sao của dữ liệu <b>input</b> được xử lý.
    * ```Shuffle``` : các node worker phân phối lại dữ liệu dựa trên các <b>key output</b> (được tạo bởi hàm ```Map()```), sao cho tất cả dữ liệu thuộc về một <b>key</b> được đặt trên cùng một node worker.
    * ```Reduce``` : các node worker thực hiện xử lý song song từng nhóm dữ liệu <b>output</b> trên mỗi <b>key</b>.

![img1](https://domanhquang.github.io/datasciencecoban/image/img-mapreduce/11.png)
#### Ví dụ kinh điển
Nào chúng ta cùng đến với ví dụ kinh điển trong bài toán xử lý phân tán, song song đó là <b>WordCount</b>.

* Ý tưởng thực hiện :
    * Chia file cần xử lý thành các phần nhỏ để xử lý.
    * Xử lý các phần nhỏ được lưu phân tán độc lập trên các node và song song trên một cụm. 
    * Tổng hợp các kết quả thu được để đưa ra kết quả cuối cùng.

* Tổng quan :

![img6](https://domanhquang.github.io/datasciencecoban/image/img-mapreduce/6.png)

* Mã giải:

```text
function map(String input_key, String input_value):
    // input_key: document name
    // input_value: document contents
    for each word w in input_value:
      EmitIntermediate(w, "1");


function reduce(String output_key, Iterator intermediate_values):
    // output_key: a word
    // output_values: a list of counts
    int result = 0;
    for each v in intermediate_values:
      result += ParseInt(v);
    Emit(AsString(result));
```

* Luồng xử lý:

![image7](https://domanhquang.github.io/datasciencecoban/image/img-mapreduce/7.png)

* Luồng xử lý song song:

![img3](https://domanhquang.github.io/datasciencecoban/image/img-mapreduce/33.png)

Bạn có thể tham khảo [Hadoop WordCount Example](https://domanhquang.github.io/datasciencecoban/source/word-count)

#### Tài liệu tham khảo
* [wiki_mapreduce](https://en.wikipedia.org/wiki/MapReduce)
* [MapReduce: Simplified Data Processing on Large Clusters by Jeff Dean, Sanjay Ghemawat Google, Inc.](http://research.google.com/archive/mapreduce-osdi04-slides/index.html)
* [Mapreduce Algorithms Optimizes the Potential of Big Data by Lalit Malik, Sunita Sangwan](https://github.com/DoManhQuang/ebook)
