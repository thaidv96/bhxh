Code demo bài toán Bảo Hiểm Xã Hội

- File create_fake_data.py: tạo 2048 bản ghi dữ liệu sai lệch tương ứng với mỗi bản ghi trong 1000 bản ghi dữ liệu đã có.
- File split_data.py: cắt lấy ra các trường có trong 1000 bản ghi.
- File search.py: chạy tìm kiếm so khớp trong tập 2,048,000 bản ghi sử dụng 4 độ đo khác nhau.
- File search_vec.py: chạy tìm kiếm so khớp sử dụng vectorize của numpy, tốc độ nhanh gấp 2 lần search.py.
- File search_mp_vec.py: chạy tìm kiếm so khớp bằng xử lý song song trên 32 CPUs với sử dụng vectorize của numpy, tốc độ nhanh hơn 100 lần so với search.py.
