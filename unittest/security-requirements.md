# Security Requirements for json_search()

SR1. apiKey chỉ được phép trả về cho role admin.

SR2. managementIpAddress chỉ được phép trả về cho role admin và operator.

SR3. issueSummary được phép trả về cho role admin, operator và viewer.

SR4. Nếu role không nằm trong danh sách được phép truy cập một key trong policy.py, json_search() phải trả về danh sách rỗng.

SR5. Kiểm soát truy cập phải áp dụng cho dữ liệu nằm trong các dict và list lồng nhau.

SR6. Việc bổ sung kiểm soát truy cập không được làm hỏng chức năng tìm kiếm đệ quy hiện có.
