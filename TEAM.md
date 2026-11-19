# Team

## Thông tin nhóm

- Tên nhóm: ClaudeUltraX20
- Lớp: L3B
- Repo: `K5-L3B-DAY10-ClaudeUltraX20-PoCtoPilotGate1`
- Thẻ sự cố: S5

## Thành viên

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
|---:|---|---|---|:---:|
| 1 | Phan Trần Mạnh Cường | 2A202603810 | Sản phẩm và kinh doanh | Thành viên |
| 2 | Nguyễn Đức Minh | 2A202603765 | Kỹ sư cổng | Trưởng nhóm |
| 3 | Nguyễn Trọng Nghĩa | 2A202603835 | Kỹ sư cổng | Thành viên |
| 4 | Nguyễn Văn Cường | 2A202603750 | Vận hành và pháp lý | Thành viên |

## Cách ghi nhận đóng góp

Các thành viên cùng thực hiện trên một repo. Phần đóng góp dưới đây được tổng hợp theo vai, với bốn đầu việc cho mỗi người.

## PhanTranManhCuong-2A202603810

### Phần việc phụ trách

Sản phẩm và kinh doanh: cùng nhóm xây tiêu chí, đọc dòng tiền, chọn phạm vi và đối chiếu quyết định Gate 1 với bằng chứng.

### Đóng góp cụ thể

1. Cùng nhóm đối chiếu ngưỡng chất lượng và kinh doanh trong Phiếu A với chi phí làm tay 10.000đ/ticket; tổng hợp lý do cho trần chi phí 6.000đ, ROI tối thiểu 0,5 và trần hoàn tự động 1.600.000đ/ngày.
2. Tổng hợp theo vai kinh doanh bản đồ dữ liệu và pre-mortem: nguồn sự thật về quyền lợi, khác biệt giữa ledger và cờ đối soát, rủi ro pilot không tiết kiệm so với làm tay.
3. Cùng nhóm phân tích S5 theo kho: prepared tốn 6.488đ/ticket, kho sỉ HCM-B2B tốn 10.382đ; đối chiếu phương án giữ 4 kho đơn lẻ, chuyển kho sỉ sang quy trình thủ công.
4. Tổng hợp bằng chứng cho quyết định v2 Thu hẹp: after tốn 2.307đ/ticket, ROI 3,33, độ phủ 60% trên S5; nêu điều kiện đánh giá lại ngày 30/11/2026.

### Bằng chứng

- Phiếu A: A2–A4; `config/acceptance_criteria.json` và commit ký `5bcde5d`.
- Phiếu B: B3, B6, B7.4, B8; commit vòng 1 `e0fedea`.
- Phiếu C: C3.5, C8, C10, C12; `config/operating_gates.json` mục business.
- Tái kiểm chứng: `R-S5-grade-20261119-184708-c54eb0`; báo cáo gom tại `submission/runs/grade-report.md`.

### Công cụ hỗ trợ

Sử dụng trợ lý AI để gợi ý và rà soát tiêu chí, phân tích chi phí và diễn đạt quyết định; nhóm chịu trách nhiệm về ngưỡng và kết luận.

### Exit ticket

- Điều học được: pass_rate cao chưa đủ để mở pilot; phải tách chi phí theo kho và tính cả tiền máy, công người, tiền mất. Thu hẹp từ 100% xuống 60% ticket S5 giúp chi phí giảm từ 6.488đ xuống 2.307đ trong mô phỏng.
- Điều còn chưa chắc: cơ cấu đơn và chi phí thực tế của 4 kho có giữ ROI tối thiểu 0,5 trong hai tuần pilot hay không; cần đo lại tiền LLM và thời gian người duyệt thật.

## NguyenDucMinh-2A202603765

### Phần việc phụ trách

Kỹ sư cổng, trưởng nhóm: cùng nhóm rà luồng agent, tính đúng của lệnh ghi, kiểm hồi quy và tính tái lập của gói nộp.

### Đóng góp cụ thể

1. Cùng nhóm đọc baseline và trace T-002@55: xác định model dùng số khách khai 5 ngày thay tracking 2 ngày, gây hoàn sai 20.000đ và một lỗi hãng oan.
2. Tổng hợp theo vai kỹ sư thiết kế kiểm tra trước khi ghi: policy theo ngày hiệu lực, quyền lợi theo tracking, approval đúng đối tượng, lỗi hãng đúng kiện và payload theo danh sách trường cho phép.
3. Cùng nhóm kiểm chứng không làm hỏng ca đúng: 13 test công khai qua, bộ nền after đạt 110/110 lượt chạy; đối chiếu hai ticket hiểm ở B7.3 và các trace S5 ở C12.
4. Rà tính tái lập: đối chiếu hash tiêu chí/bản chốt, lỗi CRLF và mã chạy; kiểm tra gói gom có code/config, báo cáo ba mốc, nhật ký và manifest khớp nhau.

### Bằng chứng

- Phiếu B: B0–B2, B7.1–B7.3; `lab10/guards_round1.py`; hash vòng 1 `d083b7ff`.
- Phiếu C: C0, C7, C12; code hiện tại `lab10/guards.py`.
- Bộ nền cuối: `R-base-after-20261119-184736-c54eb0`.
- Báo cáo grade: `R-S5-grade-20261119-184708-c54eb0`, integrity/regression đạt; `submission/manifest.json` do lệnh gom sinh.

### Công cụ hỗ trợ

Sử dụng trợ lý AI để đọc code, gợi ý cổng, chạy và đối chiếu kết quả kiểm tra; nhóm kiểm chứng bằng trace, test và hash.

### Exit ticket

- Điều học được: cổng phải kiểm nguồn sự thật ở thời điểm ghi, bên ngoài model; 13 test công khai và kiểm hồi quy giúp xác nhận sửa một lỗi không làm hỏng ca trước đó đúng.
- Điều còn chưa chắc: kiểm ledger rồi ghi tuần tự có còn chống lặp khi hai worker cùng xử lý một đơn hay không; cần giao dịch nguyên tử hoặc idempotency key và thử tải đồng thời trước khi mở rộng.

## NguyenTrongNghia-2A202603835

### Phần việc phụ trách

Kỹ sư cổng: cùng nhóm xử lý sự cố S5, phân tích sổ cái, tối ưu phần chữ model đọc và theo dõi chi phí không dùng nhãn. Tên người ký trong tiêu chí là Nguyễn Trọng Nghĩa.

### Đóng góp cụ thể

1. Cùng nhóm hoàn thiện bản tiêu chí và quy tắc quyết định; ghi nhận người ký, thời điểm ký và commit trước lần đánh giá đầu tiên, giữ nguyên ngưỡng đã niêm phong.
2. Tổng hợp theo vai kỹ sư cách sửa hoàn một phần: quyền lợi trừ mọi khoản đã ghi trong ledger; S5-21 còn được hưởng 12.000đ; chỉnh câu trả lời cho ticket lặp để khớp số đã hoàn.
3. Cùng nhóm phân tích tiền đọc theo độ dài và áp dụng pre_guard giới hạn 1.000 ký tự, bỏ phần dán kèm; giữ ticket gốc cho người duyệt, ghi nhận rủi ro mất thông tin ở phần bị cắt.
4. Tổng hợp hai monitor và cách đọc: worst_warehouse_cost_per_ticket_vnd, escalated_after_llm_read_rate; nối từng sửa đổi với fault tree trước/sau và kết quả kiểm chứng.

### Bằng chứng

- Commit ký `5bcde5d`, hash tiêu chí `6f94e36c`; Phiếu A A5.
- Commit vòng 2 `9bc5358`; `lab10/guards.py`, `lab10/monitors.py`; Phiếu C C5–C9.
- Trace S5-21@11 after: modify amount_vnd=12000, kết quả ĐẠT; S5-02@11 after: không ghi khoản mới.
- Grade `R-S5-grade-20261119-184708-c54eb0`: monitor đạt; S5 after pass_rate=1, pass^k=1, hoàn sai/thiếu bằng 0.

### Công cụ hỗ trợ

Sử dụng trợ lý AI để gợi ý sửa cổng hoàn tiền, giới hạn chữ đọc, monitor và rà soát Phiếu C; nhóm kiểm chứng bằng dữ liệu và báo cáo S5.

### Exit ticket

- Điều học được: “ledger có dòng” không đồng nghĩa “đã hoàn đủ”; phải trừ tổng đã trả khỏi quyền lợi để vừa tránh hoàn lặp vừa không chặn phần khách còn được hưởng.
- Điều còn chưa chắc: thông tin quan trọng ở sau ký tự 1.000 hoặc sau dòng phân cách có thể làm thay đổi ý định người dùng; cần người duyệt kiểm mẫu ticket bị cắt trong pilot thật.

## NguyenVanCuong-2A202603750

### Phần việc phụ trách

Vận hành và pháp lý: cùng nhóm phân tích bên chịu ảnh hưởng, năng lực người duyệt, điều kiện dừng, runbook và bài nộp.

### Đóng góp cụ thể

1. Cùng nhóm xây HAZOP và checklist 9 nhóm việc, gồm các nhánh ngoài kỹ thuật: ngân sách, năng lực người duyệt, quyền riêng tư và tác hại cho hãng/người nhận.
2. Tổng hợp theo vai vận hành cấu hình PIC NV-TUNG, người duyệt NV-HANH, 1 người × 6 ca/giờ, SLA 60 phút; ngưỡng cảnh báo, dừng và quy trình liên lạc trong runbook.
3. Cùng nhóm cập nhật sau S5: CSKH phải ghi sổ ngay khi hoàn tay; kho sỉ giữ thủ công; ghi risk register về chi phí kho mới và khoản hoàn ngoài sổ; đối chiếu cổng legal và payload gửi hãng.
4. Rà thành phần nộp: 4 thành viên/MSSV, incident S5, v1/v2 và ba dòng bắt buộc khớp C12; tổng hợp kịch bản demo, phản biện và các bước mỗi người tự nộp LMS.

### Bằng chứng

- Phiếu B: B4–B5, B7.5–B7.6; `config/operating_gates.json` mục operations/legal.
- Phiếu C: C4, C10–C12; runbook phần 4–5 và kịch bản demo.
- `submission/submission.json`: đủ 4 thành viên, S5, v1 Cải tiến thêm, v2 Thu hẹp, ba dòng bắt buộc.
- Báo cáo `R-S5-grade-20261119-184708-c54eb0`: queue_stuck=0; lỗi hãng oan/PII=0 trên bản after.

### Công cụ hỗ trợ

Sử dụng trợ lý AI để rà HAZOP, runbook, cấu hình vận hành và thành phần bài nộp; nhóm chịu trách nhiệm về quy trình và phân công.

### Exit ticket

- Điều học được: an toàn vận hành cần cả cổng code, con số và người chịu trách nhiệm; 1 người chỉ có năng lực 6 ca/giờ, nên tăng số người phải cập nhật cả công suất cam kết và đo lại chi phí.
- Điều còn chưa chắc: nhân sự thật có ghi sổ kịp thời và phản ứng đúng ngưỡng trong ca đông hay không; cần diễn tập hàng chờ, gián đoạn LLM và khiếu nại bên thứ ba trước khi mở rộng.
