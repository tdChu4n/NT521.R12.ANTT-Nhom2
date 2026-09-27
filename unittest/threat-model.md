# Threat Model for json_search()

## 1. Actors / Roles

### admin
Quản trị viên hệ thống. Có quyền truy cập đầy đủ các thông tin phục vụ quản trị, bao gồm thông tin xác thực và dữ liệu thiết bị.

### operator
Nhân viên vận hành mạng. Có quyền truy cập thông tin vận hành và địa chỉ quản trị nhưng không được đọc thông tin xác thực bí mật.

### viewer
Người dùng chỉ có quyền quan sát. Chỉ được xem thông tin sự cố không nhạy cảm.

## 2. Sensitive Assets

### apiKey
Chứa thông tin xác thực SNMP. Nếu bị lộ có thể cho phép người không có quyền truy cập hoặc khai thác thiết bị mạng.

### managementIpAddress
Địa chỉ IP quản trị của thiết bị. Đây là thông tin về hạ tầng mạng cần hạn chế truy cập.

### issueSummary
Thông tin tóm tắt sự cố. Có độ nhạy thấp hơn và có thể được truy cập bởi admin, operator và viewer.

## 3. Trust Boundary

Trust boundary tồn tại giữa người dùng gọi json_search() và dữ liệu JSON được trả về từ API giám sát hạ tầng mạng.

Nếu json_search() chỉ tìm kiếm key mà không kiểm tra role, dữ liệu nhạy cảm có thể đi qua trust boundary và được trả về cho người dùng không có quyền.

## 4. STRIDE Threats

### Information Disclosure
Người dùng có role viewer hoặc operator có thể tìm kiếm apiKey và nhận được SNMP community string nếu hàm không thực hiện kiểm soát truy cập.

### Elevation of Privilege
Người dùng có quyền thấp có thể truy cập dữ liệu dành cho role có quyền cao hơn bằng cách trực tiếp yêu cầu json_search() tìm key nhạy cảm.

## 5. Mitigations

json_search() phải kiểm tra quyền trong policy.py trước khi trả về dữ liệu.

Khi role không được phép đọc một key, hàm phải trả về danh sách rỗng.

Kiểm soát truy cập phải được áp dụng cả đối với các key nằm sâu trong dict hoặc list lồng nhau.
