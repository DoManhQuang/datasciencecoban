## Thuật Toán Raft Consensus

#### Lịch sử
Thuật toán Raft Cosensus được phát triển bởi Diego dự trên Thuật toán Paxos thông qua bài báo [In Search of an Understandable Consensus Algorithm](https://raft.github.io/raft.pdf).

#### Mục đích
* Do thuật toán Paxos quá khó hiểu và khó phát triển :D (Trích: Diego viết trong bài báo)
* Raft là giao thức để thực hiện sự đồng thuận phân tán
* Giải quyết vấn đề bầu cử leader server
* Giải quyết vấn đề Sao lưu dữ liệu

#### Vấn đề bầu cử (lựa chọn) Leader server
Sẽ chả có vấn đề gì nếu như chúng ta sử dụng hệ thống Client - Server. Khi đó chỉ có 01 server chịu trách nhiệm tương tác với client.

![img0](https://domanhquang.github.io/bigdatacoban/image/raft/1.PNG)

Vấn đề chỉ xảy ra khi chúng ta sử dụng 01 cụm server.

Sự đồng thuận (Consensus) : Đồng thuận có nghĩa là nhiều máy chủ đồng ý về cùng một thông tin, một điều bắt buộc để thiết kế các hệ thống phân tán chịu lỗi.

Giao thức đồng thuận có thể giải quyết được nhiều sự cố nhưng phải tuân theo các <b>quy ước</b> sau :
* <b>Hiệu lực (Validity)</b> : Nếu 1 xử lý đọc/ghị giá trị thì nó phải được sự đề xuất (đồng thuận) từ xác tiến trình xử lý đúng khác trong hệ thống.
* <b>Hiệp ước (Agreement)</b> : Mọi tiến trình đúng phải chấp nhấp nhận giá trị.
* <b>Chấm dứt (Termination)</b> : Mỗi tiến trình đúng phải được kết thúc sau một số bước hữu hạn (không được vô hạn).
* <b>Toàn vẹn (Integrity)</b> : Nếu tất cả các tiến trình quyết định xử lý giá trị thì bất kỳ tiến trình nào cũng đều phải có giá trị nói trên.

Có một số ý tưởng khá hay về hệ thống có nhiều máy chủ sau đây là 2 ý tưởng :
* <b>Hệ thống đối xứng (Symmetric)</b> : Tất cả các server có thể trả lời client và tất cả server khác phải đồng bộ hóa dữ liệu mà server đã trả lời client.
* <b>Hệ thống không đối xứng (Asymmetric)</b> : Chỉ có một server được bầu chọn có thể trả lời client và tất cả các server khác phải đồng bộ dữ liệu trả lời của con server được chọn.

Ở bài viết này chúng ta sẽ cùng tìm hiểu về <b>Hệ thống không đối xứng (Asymmetric)</b>. Vì giải pháp này được khá nhiều các hệ thống lựa chọn.

![img1](https://domanhquang.github.io/bigdatacoban/image/raft/2.PNG)

Một số thuật ngữ trong Hệ thống không đối xứng (Asymmetric) :

* <b>Leader</b> : 1 máy server được bầu làm leader có thể tương tác với client. Tất cả các server khác phải đồng bộ dữ liệu tương tác với client của server leader. Ở bất kỳ thời gian nào, có thể có 0 hoặc 1 server leader.

* <b>Follower</b> : Máy server theo dõi sẽ copy dữ liệu của Leader server sau khoảng thời gian nhất định. Khi máy Leader server gặp sự cố thì Follower server có thể trở thành leader server nếu được bầu chọn.

* <b>Candidate(ứng viên)</b> : Trong khoảng thời gian lựa chọn máy leader server thì các server sẽ yêu cầu các server khác lựa chọn. Khi đó server được gọi là Candidate. Ở thời điểm đầu tiên tất cả các server đều là Candidate.

![img2](https://domanhquang.github.io/bigdatacoban/image/raft/3.PNG)

<i>Hệ thống này sẽ tuân theo định lý CAP (CAP theorem) :</i>

* <b>Tính nhất quán(Consistency)</b> : Hệ thống phải được đồng bộ hóa dữ liệu. Tất cả các dữ liệu ở server nodes phải được đồng nhất kể cả leader và follower.

* <b>Tính khả dụng(Availability)</b> : Mọi yêu cầu được gửi đi đều nhận về (success hoặc failure). Nó đòi hỏi hệ thống phải hoạt động 100% thời gian khi server yêu cầu.

* <b>Phân vùng dung sai(Partition Tolerance)</b> : Hệ thống sẽ liên tục trả lời kể cả khi server nodes fail. Có nghĩa là hệ thống sẽ luôn duy trì tất cả yêu cầu hoặc trả lời bằng một function nào đó.

#### Giao thức Raft là gì ?
Raft là một thuật toán đồng thuận được thiết kế để dễ hiểu. Nó tương đương với Paxos về khả năng chịu lỗi và hiệu suất. Sự khác biệt là nó bị phân rã thành các bài toán con tương đối độc lập và nó giải quyết rõ ràng tất cả các phần chính cần thiết cho các hệ thống thực tế. Chúng tôi hy vọng Raft sẽ cung cấp sự đồng thuận cho nhiều đối tượng hơn và đối tượng rộng hơn này sẽ có thể phát triển nhiều hệ thống dựa trên sự đồng thuận chất lượng cao hơn so với hiện nay.

#### Quy trình lựa chọn leader server (Sơ đồ thuật toán)

![img3](https://domanhquang.github.io/bigdatacoban/image/raft/4.PNG)

<b>Term number</b> là thời gian duy trì để truyền tải các thông tin giữa các server nodes. Trong khoảng thời gian đó các server sẽ vote ra leader server thông qua các đường truyền tin. Mỗi server chỉ được vote 1 lần trong thời gian bỏ phiếu. Nếu xảy ra tình huống có 2 server cùng số lượng vote thì nhiệm kỳ sẽ được gọi là split vote (Bỏ phiếu chia). Nhiệm kỳ sẽ kết thúc mà không có leader server nào được tạo. Và sẽ chạy lại nhiệm kỳ. Vì thế mỗi nhiệm kỳ chỉ có nhiều mất 01 leader server.
 
Mục đích sử dụng <b>Term number</b> :

* Các server sẽ cập nhập term number được khởi tạo để tăng thời gian duy trì kỳ hạn.

* Khi kỳ hạn hết thúc ở bất kể thời điểm nào server có thứ hạng term number cao sẽ được trở thành leader.

* Các node server được phân thứ hạng các node có thứ hạng cao sẽ không nghe lời node có thứ hạng thấp.
 
 
#### Thuật toán Raft sử dụng 2 thủ tục được gọi từ xa (RPCs) :

* RequestVotes được gửi bởi các ứng viên để thu thập phiếu vote trong cuộc bầu cử.

* AppendEntries được sử dụng như 1 cơ chế theo theo dõi xem máy chủ còn hoạt động không. Nếu có sự phản hồi đồng nghĩa là máy chủ hoạt động và ngược lại.

<b>Leader election</b> : Để duy trì cuộc bầu cử thì leader server phải gửi request đến các follower server để thông báo được gọi là RequestVotes. Một cuộc bầu cử diễn ra khi Follower server hết thời gian chờ RequestVotes. Tại thời điểm đó Follower server sẽ tự ứng cử trở thành Candidate (ứng viên). Chính Cadidate sẽ cố gắng gửi RPC RequestVotes để trở thành Leader server.

#### Cuộc bầu cử sẽ diễn ra dưới 3 hình thức sau :

* Candidate trở thành Leader khi nhận được đa số phiếu bầu. Leader mới sẽ cập nhập trạng thái và gửi RequestVotes đến các Follower để thông báo có leader mới.

* Candidate trở về Follower khi không nhận được đa số phiếu bầu.

* Candidate gửi request đến các Cadidate node khác trong cụm mà AppendEntries bị từ chối thì các Cadidate được giữ nguyên trạng thái. Tạo lại cuộc bầu cử.

![img4](https://domanhquang.github.io/bigdatacoban/image/raft/5.PNG)

#### Vấn đề sao lưu dữ liệu giữa các server

<b>Log replication (bản sao nhật ký)</b> : Khi leader server tương tác với client thì sẽ lưu lại dữ liệu gửi đi vào 1 thư mục mới và sử dụng AppendEmtries song song được kết nối với các máy chủ khác để sao lưu một cách an toàn. 
Việc bảo đảm log được lưu đúng chỉ mục trên tất cả các server node là điều tương đối khó khăn . Nếu như máy leader gặp sự cố có thể các nhật ký sẽ trở nên không được nhất quán chính vì vậy raft phát triển thuật toán lưu trữ dựa trên các server với nhau.

![img5](https://domanhquang.github.io/bigdatacoban/image/raft/6.PNG)

Giải thích quá trình sao lưu:

* Trong(a) S1 là người lãnh đạo và sao chép một phần mục nhập nhật ký tại chỉ mục 2.

* Trong (b) S1 sự cố S5 được bầu làm lãnh đạo cho nhiệm kỳ 3 với số phiếu từ S3, S4 và chính nó, và chấp nhận một mục khác trong nhật ký chỉ số 2.

* Trong (c) S5 sự cố, S1 khởi động lại, được bầu làm lãnh đạo, và tiếp tục nhân rộng.Tại thời điểm này, mục nhật ký từ học kỳ 2 đã được sao chép trên phần lớn các máy chủ, nhưng nó không phải là cam kết.

* Nếu S1 gặp sự cố như trong (d), S5 có thể được bầu làm lãnh đạo (có phiếu bầu từ S2, S3 và S4) và ghi đè mục nhập bằng mục nhập riêng của nó từ term 3. Tuy nhiên, nếu S1 sao chép một mục từ term hiện tại của nó trên phần lớn các máy chủ trước đó nên không được phép ghi đè log .

* Trong (e), sau đó mục này được cam kết (không thể có S5 giành chiến thắng trong một cuộc bầu cử).

Sơ đồ thuật toán :

![img6](https://domanhquang.github.io/bigdatacoban/image/raft/7.PNG)

<i>Các quy tắc về an toàn trong giao thức Raft</i> đảm bảo sự an toàn sau đây chống lại sự cố đồng thuận nhờ thiết kế của nó:

* Leader election safety (An toàn bầu cử lãnh đạo) - Nhiều nhất một nhà lãnh đạo mỗi nhiệm kỳ

* Log Matching safety (An toàn đối sánh) nhật ký (Nếu nhiều nhật ký có một mục nhập có cùng chỉ mục và thời hạn, thì các nhật ký đó được đảm bảo giống hệt nhau trong tất cả các mục nhập cho đến chỉ mục đã cho.

* Leader completeness (Tính đầy đủ của nhà lãnh đạo) - Các mục nhật ký được cam kết trong một thuật ngữ nhất định sẽ luôn xuất hiện trong nhật ký của các nhà lãnh đạo theo thời hạn đã nêu)

* State Machine safety (An toàn máy trạng thái) - Nếu một máy chủ đã áp dụng một mục nhật ký cụ thể cho máy trạng thái của nó, thì không có máy chủ nào khác trong cụm máy chủ có thể áp dụng một lệnh khác cho cùng một nhật ký.

* Leader is Append-only (Thêm 1 leader) - Nút lãnh đạo (máy chủ) chỉ có thể chắp thêm (không có hoạt động nào khác như ghi đè, xóa, cập nhật được phép) các lệnh mới vào nhật ký của nó.

* Follower node crash (Sự cố node follower) - Khi follower gặp sự cố, tất cả các yêu cầu được gửi đến nút bị lỗi sẽ bị bỏ qua. Hơn nữa, nút bị sập không thể tham gia cuộc bầu cử lãnh đạo vì những lý do rõ ràng. Khi nút khởi động lại, nó sẽ đồng bộ hóa nhật ký của nó với leader.

<b>Thời gian và tính sẵn sàng</b>:

* Thời gian là rất quan trọng trong Raft để bầu và duy trì một nhà lãnh đạo ổn định theo thời gian, để có một sự sẵn có hoàn hảo của cụm của bạn. Tính ổn định được đảm bảo bằng cách tôn trọng yêu cầu về thời gian của thuật toán:
        
```text
                BroadcastTime << electionTimeout << MTBF
```
        
* <i>BroadcastTime</i> là thời gian trung bình để một máy chủ gửi yêu cầu đến mọi máy chủ trong cụm và nhận phản hồi. Nó liên quan đến cơ sở hạ tầng bạn đang sử dụng.

* <i>MTBF</i> (Thời gian trung bình giữa các lần thất bại) là thời gian trung bình giữa các lần thất bại cho máy chủ. Nó cũng liên quan đến cơ sở hạ tầng của bạn.

* <i>ElectionTimeout</i> giống như được mô tả trong phần Bầu cử Lãnh đạo. Đó là điều bạn phải chọn.

Số điển hình cho các giá trị này có thể là 0,5ms đến 20ms cho <b>BroadcastTime</b>, điều này ngụ ý rằng bạn đặt thời gian bầu cử ở đâu đó trong khoảng từ 10ms đến 500ms. Có thể mất vài tuần hoặc vài tháng giữa các lần hỏng máy chủ, điều đó có nghĩa là các giá trị đều ổn để một cụm ổn định hoạt động.

#### Tài liệu tham khảo
[Raft Consensus Algorithm](https://www.geeksforgeeks.org/raft-consensus-algorithm/)

[raft-paper](https://raft.github.io/raft.pdf)

[Dự án về raft](https://raft.github.io/)
