"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


# V2 (S5) · công một ca qua người duyệt, lấy từ data/world.json → ops_facts.review_cost_per_ticket_vnd (10.000đ)
REVIEW_COST_VND = 10000


def _warehouse_costs(trials):
    """Chi phí mỗi ticket theo kho = (tiền máy + công người duyệt) / số ticket của kho. Không dùng nhãn."""
    groups = {}
    for t in trials:
        g = groups.setdefault(t.get("warehouse") or "?", [0, 0])
        g[0] += (t.get("cost_vnd") or 0) + (REVIEW_COST_VND if t.get("review_kind") else 0)
        g[1] += 1
    return {wh: c / n for wh, (c, n) in groups.items() if n}


def worst_warehouse_cost_per_ticket_vnd(trials):
    """Chi phí mỗi ticket (đ) của kho đắt nhất. Báo động khi ≥ 10.000đ (bằng làm tay): kho đó tự động hoá chỉ thêm tiền máy."""
    costs = _warehouse_costs(trials)
    return round(max(costs.values()), 1) if costs else 0.0


def escalated_after_llm_read_rate(trials):
    """Tỉ lệ ticket đã tốn tiền model đọc (cost_vnd vượt phí nền 200đ) mà vẫn chuyển người: trả cả hai lần tiền."""
    paid_twice = sum(1 for t in trials if t.get("status") == "escalated" and (t.get("cost_vnd") or 0) > 200)
    return paid_twice / max(1, len(trials))


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "worst_warehouse_cost_per_ticket_vnd": worst_warehouse_cost_per_ticket_vnd,   # V2 (S5), metric chính
    "escalated_after_llm_read_rate": escalated_after_llm_read_rate,               # V2 (S5), metric phụ
}
STARTER_MONITORS = ("escalation_rate",)
