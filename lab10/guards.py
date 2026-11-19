"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


READ_MAX_CHARS = 1000   # V2 (S5): ~400đ tiền đọc; đủ cho yêu cầu của khách, phần dán kèm dài không đổi quyết định


def _core_request(text):
    """V2 (S5): giữ phần khách tự viết, bỏ phần dán kèm (sau dòng phân cách ---) và cắt độ dài tối đa.

    Quyết định tiền dựa trên tracking + chính sách, không dựa trên bảng kê khách dán, nên model không cần đọc phần đó.
    Bản gốc vẫn nằm nguyên trong ticket cho người duyệt xem.
    """
    kept = []
    for line in (text or "").splitlines():
        if len(line.strip()) >= 3 and set(line.strip()) <= {"-", "—", "=", "_"}:
            break
        if line.strip().startswith("---"):
            break
        kept.append(line)
    core = "\n".join(kept).strip() or (text or "")
    return core[:READ_MAX_CHARS]


def pre_guard(ctx):
    # G1: the effective date is authoritative; index_active is only an index.
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if policy is None:
        return Verdict.escalate("không có chính sách còn hiệu lực, cần trưởng ca duyệt")
    # V2 (S5): tiền LLM tăng theo độ dài chữ phải đọc; cắt phần dán kèm trước khi model đọc.
    text = ctx.ticket.get("text") or ""
    core = _core_request(text)
    if core != text:
        ctx.log("guard_trim_text", chars_before=len(text), chars_after=len(core))
        return Verdict.rewrite("chỉ đọc phần yêu cầu của khách, bỏ phần dán kèm dài", core,
                               policy_id=policy["policy_id"])
    return Verdict.allow(policy_id=policy["policy_id"])


def write_gate(ctx, action):
    tool = action.get("tool")
    if tool == "send_reply":
        # V2 (S5): không nói "chưa hoàn khoản nào" khi sổ cái đã có khoản hoàn trước cho đơn (ticket lặp, CSKH hoàn tay).
        order_id = ctx.ticket.get("order_id")
        prior = [r for r in ctx.tools.ledger_rows(order_id=order_id)
                 if r.get("ticket_id") != ctx.ticket.get("ticket_id")] if order_id else []
        if prior and not action.get("amount_vnd"):
            paid = sum(r.get("amount_vnd", 0) for r in prior)
            text = (f"Đơn {order_id} đã được LogiX hoàn {paid:,}đ trước đó; "
                    f"yêu cầu lần này không phát sinh khoản hoàn mới.").replace(",", ".")
            return Verdict.modify("trả lời khớp sổ cái: đơn đã được hoàn trước đó", text=text)
        return Verdict.allow()

    order = ctx.tools.lookup_order(ctx.ticket.get("order_id"))
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if not order or not policy or order["customer_id"] != ctx.ticket["customer_id"]:
        return Verdict.escalate("thiếu nguồn sự thật hoặc người gửi không phải chủ đơn")
    if action.get("order_id", order["order_id"]) != order["order_id"]:
        return Verdict.escalate("lệnh ghi không khớp đơn của ticket")

    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    if ctx.ticket.get("parcel_id") and ctx.ticket["parcel_id"] != parcel["parcel_id"]:
        return Verdict.escalate("không tìm thấy kiện được yêu cầu")
    delay = H.db_delay_days(parcel, ctx.as_of)

    # G1: money, payer, idempotency and approval are checked outside the model.
    if tool == "issue_refund":
        # V2 (S5): the ledger is shared with manual CSKH refunds. Pay only what is still owed for the order:
        # entitlement minus everything already in the ledger (auto or manual), never a second full payment.
        rows = ctx.tools.ledger_rows(order_id=order["order_id"])
        already = sum(r.get("amount_vnd", 0) for r in rows)
        if not rows and order.get("refund_status") == "REFUNDED":
            return Verdict.deny("đơn đã được đánh dấu hoàn đủ; không ghi lần hai")
        if action.get("payer") != "LOGIX" or action.get("basis") != "policy":
            return Verdict.escalate("nguồn chi hoặc căn cứ ngoài chính sách, cần người duyệt")
        entitled = H.entitlement_vnd(policy, order, delay, parcel.get("delay_cause"))
        if entitled <= 0:
            return Verdict.deny("tracking và chính sách hiện hành không cho phép hoàn")
        amount = entitled - already
        if amount <= 0:
            return Verdict.deny("sổ cái đã có đủ khoản hoàn cho đơn; không ghi lần hai")
        if parcel.get("delay_cause") is None:
            return Verdict.escalate("thiếu nguyên nhân trễ trong tracking")
        approval_id = action.get("approval_id")
        if amount > policy["auto_limit_vnd"] or approval_id:
            approvals = ctx.tools.lookup_approvals(approval_id=approval_id) if approval_id else []
            approver = (ctx.gates or {}).get("operations", {}).get("approver_id")
            valid = any(
                a.get("status") == "valid" and a.get("expires_at", "") >= ctx.as_of
                and a.get("ticket_id") == ctx.ticket["ticket_id"]
                and a.get("order_id") == order["order_id"]
                and a.get("customer_id") == order["customer_id"]
                and a.get("approver_id") and (not approver or a["approver_id"] == approver)
                and a.get("max_vnd", 0) >= amount
                and not ctx.tools.ledger_rows(approval_id=approval_id)
                for a in approvals
            )
            if not valid:
                return Verdict.escalate("phê duyệt thiếu, hết hạn, đã dùng hoặc không đúng đối tượng")
        if not approval_id:
            limits = ctx.tools.ops_limits()
            cap = limits.get("max_auto_refund_per_customer_per_day_vnd")
            spent = sum(r["amount_vnd"] for r in ctx.tools.ledger_rows(customer_id=order["customer_id"])
                        if not r.get("approval_id"))
            if cap is not None and spent + amount > cap:
                return Verdict.escalate("vượt trần hoàn tự động của một khách, chuyển trưởng ca")
        if action.get("amount_vnd") != amount:
            return Verdict.modify("tính lại tiền từ tracking và chính sách hiệu lực", amount_vnd=amount)

    # G2: a strike must belong to the actual delayed parcel and recorded cause.
    if tool == "file_carrier_fault":
        if not H.carrier_at_fault(policy, parcel, delay):
            return Verdict.deny("tracking không chứng minh hãng chịu lỗi")
        if ctx.tools.fault_rows(order_id=order["order_id"], parcel_id=parcel["parcel_id"]):
            return Verdict.deny("đã ghi lỗi cho kiện này")
        cap = ctx.tools.ops_limits().get("max_auto_strikes_per_carrier_per_day")
        if cap is not None and len(ctx.tools.fault_rows(carrier_id=parcel["carrier_id"])) >= cap:
            return Verdict.escalate("đạt trần lỗi hãng trong ngày, cần người kiểm tra")
        fields = {"parcel_id": parcel["parcel_id"], "carrier_id": parcel["carrier_id"],
                  "driver_id": parcel.get("driver_id"), "delay_days": delay}
        if any(action.get(k) != v for k, v in fields.items()):
            return Verdict.modify("gắn lỗi đúng kiện, hãng, tài xế và độ trễ DB", **fields)

    # G3: never copy untrusted free text or recipient contacts to a third party.
    if tool == "notify_carrier":
        faults = ctx.tools.fault_rows(ticket_id=ctx.ticket["ticket_id"],
                                     order_id=order["order_id"], parcel_id=parcel["parcel_id"])
        if not faults or action.get("carrier_id") != parcel["carrier_id"]:
            return Verdict.deny("thông báo không có bản ghi lỗi tương ứng")
        facts = {"order_id": order["order_id"], "parcel_id": parcel["parcel_id"],
                 "district": order.get("recipient", {}).get("district"), "delay_days": delay}
        allowed = set(policy.get("carrier_notice_fields", []))
        blocked = set((ctx.gates or {}).get("legal", {}).get("pii_fields_blocked_to_third_party", []))
        payload = {k: v for k, v in facts.items() if k in allowed and k not in blocked}
        if action.get("payload") != payload:
            return Verdict.modify("chỉ gửi dữ kiện DB thuộc danh sách trường cho phép", payload=payload)
    return Verdict.allow()
