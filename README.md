# Các giải thuật liên quan cho bài toán MCP

## Bài toán bè cực đại
Bài toán bè cực đại (Maximum Clique Problem – MCP) là bài toán tìm một tập đỉnh lớn nhất trong đồ thị sao cho mọi cặp đỉnh trong tập đều kề nhau. Đây là một bài toán tối ưu tổ hợp kinh điển, thuộc lớp NP-hard, xuất hiện trong nhiều lĩnh vực như phân tích mạng, sinh học tính toán, thiết kế mạch và khoa học dữ liệu. 

Phần project này nghiên cứu qua về giải thuật di truyền trong bài toán này

## Thuật toán liên quan
Phần project này bao gồm các thuật toán : 
+ Giải thuật chính xác (Exact Search)
+ Giải thuật di truyền (với hàm fitness đơn giản)
+ Giải thuật di truyền + luyện kim

## Các module chính
+ BasicGraph : cung cấp lớp biểu diễn đồ thị bằng ma trận kề 
+ Binary GA : cung cấp các thao tác chung cho giải thuật di truyền (biểu diễn cá thể bằng vector nhị phân)
+ ExactSearchMCP : thuật toán chính xác (Quay lui + Nhánh cận)
+ simpleGA : code cho Giải thuật di truyền (với hàm fitness đơn giản)
+ annealGA : code Giải thuật di truyền + luyện kim
+ testGraph : sinh đồ thị với xác suất cạnh ngẫu nhiên 