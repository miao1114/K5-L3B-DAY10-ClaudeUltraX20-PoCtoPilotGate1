# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): ClaudeUltraX20
- Lớp: `L3B`
- Repo của bàn: `K5-L3B-DAY10-ClaudeUltraX20-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): S5

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; bàn 3 người thì để trống dòng 4. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên            | MSSV        | Vai                    | Trưởng nhóm |
| --: | -------------------- | ----------- | ---------------------- | :---------: |
|   1 | Phan Trần Mạnh Cường | 2A202603810 | Sản phẩm và kinh doanh | Thành viên  |
|   2 | Nguyễn Đức Minh      | 2A202603765 | Kỹ sư cổng             | Trưởng nhóm |
|   3 | Nguyễn Trọng Nghĩa   | 2A202603835 | Kỹ sư cổng             | Thành viên  |
|   4 | Nguyễn Văn Cường     | 2A202603750 | Vận hành và pháp lý    | Thành viên  |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## PhanTranManhCuong-2A202603810

### Phần việc phụ trách

Sản phẩm và kinh doanh: tiêu chí, Phiếu B mục B3, B7.4, B8; business trong config/operating_gates.json. Đây là phân công; cá nhân cần xác nhận việc thực tế đã làm.

### Đóng góp cụ thể

### Bằng chứng

### Exit ticket

Chờ cá nhân tự viết một điều học được và một điều còn chưa chắc sau demo.

## NguyenDucMinh-2A202603765

### Phần việc phụ trách

Kỹ sư cổng: phân công đọc trace, soát cổng và test công khai ở CP3; cá nhân xác nhận phần thực tế.

### Đóng góp cụ thể

### Bằng chứng

### Exit ticket

Chờ cá nhân tự viết sau demo.

## NguyenTrongNghia-2A202603835

### Phần việc phụ trách

Kỹ sư cổng. Khối 1: điền và ký Bản tiêu chí (`config/acceptance_criteria.json`, người ký `signed_by`), Phiếu A mục A5.
Khối 2A: chạy baseline, trace `T-002@55`, nháp Phiếu B mục B0–B6 cho bàn soát lại. Vòng 2 (thẻ S5): sửa cổng trong
`lab10/guards.py`, `business.pilot_scope` trong `config/operating_gates.json`, thêm chỉ số trong `lab10/monitors.py`,
điền Phiếu C (C0–C12) và `submission/submission.json`.

### Đóng góp cụ thể

- Chép ngưỡng đã chốt ở Phiếu A (A4) sang `acceptance_criteria.json`; viết `stop_condition` và bốn dòng `decision_rule`; ký và push.
- Chạy baseline bộ nền, xếp lỗi `T-002@55` (tin số ngày khách khai thay vì tracking; payload gửi hãng có `customer_note`) ở B2.
- Phát hiện lỗi CRLF trên Windows làm kiểm tra integrity báo sai; sửa bằng `core.autocrlf=false` và lấy lại file từ git.
- Vòng 2, thẻ S5, mỗi lần đổi một thứ:
  1. `write_gate` / `issue_refund`: chỉ hoàn phần còn thiếu = quyền lợi − mọi khoản đã có trong sổ cái (S5-21: hoàn 12.000đ thay vì chặn hẳn).
  2. `pre_guard`: bỏ phần dán kèm và cắt 1.000 ký tự trước khi model đọc (chi phí 6.491đ → 5.611đ).
  3. `pilot_scope`: chỉ 4 kho đơn lẻ, kho sỉ HCM-B2B làm tay (chi phí 2.307đ, ROI 3,33, hết vượt trần).
  4. `monitors.py`: `worst_warehouse_cost_per_ticket_vnd`, `escalated_after_llm_read_rate`.
  5. `send_reply`: câu trả lời khớp sổ cái khi đơn đã được hoàn trước.
- Viết Phiếu C và đề xuất quyết định v2 là Thu hẹp, khớp dòng "Thu hẹp" của `decision_rule` đã ký.

### Bằng chứng
- Commit ký tiêu chí `5bcde5d` (hash `6f94e36c`), Phiếu A mục A5.
- Baseline `R-base-before-20261119-165518-bde05c` (Phiếu B mục B0–B2).
- Các lần chạy vòng 2: `R-S5-after-20261119-173229-076895`, `…173252-f6f6f2`, `…173305-70b696`, `…173335-17d121`,
  `…173408-67290b`; không regression `R-base-after-20261119-173418-67290b`; grade `R-S5-grade-20261119-173431-67290b`
  (PASS-VISIBLE, 6 ô). Chi tiết ở Phiếu C mục C0, C7.

### Dùng AI
Dùng Claude (Claude Code) để: đọc code của lab, chạy các lệnh eval/trace/grade, gợi ý cách viết các cổng trong `guards.py`
và chỉ số trong `monitors.py`, và soạn nháp Phiếu B (B0–B6), Phiếu C, `submission.json`.

### Exit ticket

Chờ cá nhân tự viết sau demo.

## NguyenVanCuong-2A202603750

### Phần việc phụ trách

Vận hành và pháp lý: phân công HAZOP, checklist, runbook, operations và legal trong config; cá nhân xác nhận phần thực tế.

### Đóng góp cụ thể

### Bằng chứng

### Exit ticket

Chờ cá nhân tự viết sau demo.
