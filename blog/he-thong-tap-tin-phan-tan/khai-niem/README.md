## Hệ thống tập tin phân tán (DFS)

Hệ Thống Tập Tin Phân Tán hay Distributed File System (DFS) là một giải pháp cho phép người quản trị tập trung các dữ liệu nằm rời rạc trên các file server về một thư mục chung và thực hiện các tính năng replicate nhằm đảm bảo dữ liệu luôn sẵn sang khi có sự cố về file server. Bao gồm 2 tính năng : DFS Namespace và DFS Replication.
Cung cấp 3 giải pháp :

* <b>Sharing File Across banch office</b> : người dùng đi ở site nào cũng có thể truy cập các thư mục trên, và họ lưu dữ liệu trên các thư mục này thì dữ liệu sẽ được replicate qua các site khác, nhờ vào DFS Replication

* <b>Data collection</b> : dữ liệu của các file server ở chi nhánh sẽ được replicate tới văn phòng chính hoặc data center, điều này giúp tập trung các dữ liệu về một nơi duy nhất. Sau đó người quản trị ở văn phòng chính sẽ dùng các giải pháp backup để sao lưu toàn bộ dữ liệu.

* <b>Data distribution</b> : kết hợp DFS Namespace và DFS Replication cho các thư mục như Software, Trainning, Document, Project. Người dùng sẽ dễ dàng truy cập và tăng độ sẵn sàng khi có sự cố xảy ra (nhờ vào tính năng DFS Replication), khi người dùng không truy cập được tới DFS Server trong Site của họ, thì hệ thống sẽ tự redirect người dùng qua DFS Server của Site khác. Dữ liệu vẫn đầy đủ.

![img0](https://domanhquang.github.io/bigdatacoban/image/raft/dfs.png)