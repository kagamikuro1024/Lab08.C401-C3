# Grading Report — Lab Day 08
Generated: 2026-04-13T17:13:21.003639

## Summary

- **Total Raw Score**: +30.0/98
- **Percentage**: 30.6%
- **Group Score (30 điểm)**: 9.2/30

### By Level

| Level | Count |
|-------|-------|
| FULL | 1 |
| PARTIAL | 6 |
| ZERO | 1 |
| PENALTY | 2 |

## Per-Question Results

### gq01 — SLA xử lý ticket P1 đã thay đổi như thế nào so với phiên bản... (hard)
**Points**: 10 | **Score Level**: FULL | **Raw Score**: +10.0

#### Grading Criteria

✅ Nêu đúng giá trị hiện tại: 4 giờ
✅ Nêu đúng giá trị cũ: 6 giờ
✅ Có citation về phiên bản (v2026.1) hoặc effective_date
✅ KHÔNG bịa thêm thông tin về phiên bản khác

#### Hallucination Check
**Detected**: ✅ NO
**Reasoning**: HALLUCINATION: NO
REASON: The student answer accurately reflects the change in the SLA resolution time for P1 tickets as documented in the context.

#### Student Answer
```
SLA xử lý ticket P1 đã thay đổi từ 6 giờ xuống 4 giờ trong phiên bản mới nhất [1].
```

#### Sources Retrieved

- support/sla-p1-2026.pdf

---

### gq02 — Khi làm việc remote, tôi phải dùng VPN và được kết nối trên ... (hard)
**Points**: 10 | **Score Level**: PARTIAL | **Raw Score**: +5.0

#### Grading Criteria

✅ Xác nhận VPN là bắt buộc khi remote (từ hr_leave_policy)
✅ Nêu đúng giới hạn 2 thiết bị (từ it_helpdesk_faq)
❌ Có citation từ ÍT NHẤT 2 nguồn khác nhau
❌ Câu trả lời tổng hợp cả hai thông tin, không chỉ một

#### Hallucination Check
**Detected**: ✅ NO
**Reasoning**: HALLUCINATION: NO
REASON: The student answer accurately reflects the information provided in the context about the maximum number of devices allowed for VPN connection.

#### Student Answer
```
Bạn có thể kết nối VPN trên tối đa 2 thiết bị cùng lúc [1].
```

#### Sources Retrieved

- support/helpdesk-faq.md
- hr/leave-policy-2026.pdf

---

### gq03 — Đơn hàng mua trong chương trình Flash Sale và đã kích hoạt s... (hard)
**Points**: 10 | **Score Level**: PARTIAL | **Raw Score**: +5.0

#### Grading Criteria

✅ Kết luận rõ ràng: KHÔNG được hoàn tiền
✅ Nêu đúng ngoại lệ Flash Sale
✅ Nêu đúng ngoại lệ sản phẩm đã kích hoạt
✅ Đề cập ít nhất 2 trong số các ngoại lệ (không chỉ một)
❌ Có citation về Điều 3 hoặc policy/refund-v4.pdf

#### Hallucination Check
**Detected**: ✅ NO
**Reasoning**: HALLUCINATION: NO
REASON: The student answer accurately reflects the exceptions listed in the context.

#### Student Answer
```
Đơn hàng đã áp dụng mã giảm giá đặc biệt theo chương trình khuyến mãi Flash Sale và sản phẩm đã được kích hoạt sẽ không được hoàn tiền [1].
```

#### Sources Retrieved

- policy/refund-v4.pdf

---

### gq04 — Nếu chọn nhận store credit thay vì hoàn tiền, tôi được bao n... (medium)
**Points**: 8 | **Score Level**: ZERO | **Raw Score**: +0.0

#### Grading Criteria

✅ Nêu đúng con số: 110%
❌ Nêu rõ đây là TÙY CHỌN (không phải bắt buộc)
❌ Có citation về policy/refund-v4.pdf hoặc Điều 5

#### Hallucination Check
**Detected**: ✅ NO
**Reasoning**: HALLUCINATION: NO
REASON: The student answer correctly states the value of store credit as 110%, which matches the context provided.

#### Student Answer
```
Nếu chọn nhận store credit, bạn sẽ nhận được 110% so với số tiền gốc [1].
```

#### Sources Retrieved

- policy/refund-v4.pdf

---

### gq05 — Contractor từ bên ngoài công ty có thể được cấp quyền Admin ... (hard)
**Points**: 10 | **Score Level**: PENALTY | **Raw Score**: -5.0

#### Grading Criteria

✅ Xác nhận contractor ĐƯỢC cấp quyền (phạm vi áp dụng từ Section 1)
✅ Nêu đúng approver: IT Manager + CISO
✅ Nêu đúng thời gian: 5 ngày làm việc
✅ Nêu yêu cầu training bắt buộc về security policy
✅ Không lẫn lộn với Level 3 (IT Manager thay vì CISO)

#### Hallucination Check
**Detected**: 🚨 YES
**Reasoning**: HALLUCINATION: YES
REASON: The context does not provide information about contractors or the specific processing time and training requirements mentioned.

#### Student Answer
```
Có, contractor từ bên ngoài công ty có thể được cấp quyền Admin Access. Thời gian xử lý là 5 ngày làm việc và yêu cầu thêm là phải hoàn thành training bắt buộc về security policy [3].
```

#### Sources Retrieved

- it/access-control-sop.md

---

### gq06 — Lúc 2 giờ sáng xảy ra sự cố P1, on-call engineer cần cấp quy... (hard)
**Points**: 12 | **Score Level**: PARTIAL | **Raw Score**: +6.0

#### Grading Criteria

✅ Nêu đúng: on-call IT Admin cấp quyền tạm thời
✅ Nêu đúng: cần Tech Lead phê duyệt bằng lời
✅ Nêu đúng: quyền tồn tại tối đa 24 giờ
✅ Nêu yêu cầu ghi log vào Security Audit
❌ BONUS: Đề cập hotline on-call ext. 9999 từ SLA P1

#### Hallucination Check
**Detected**: ✅ NO
**Reasoning**: HALLUCINATION: NO
REASON: The student's answer accurately reflects the information provided in the context without adding unsupported details.

#### Student Answer
```
Quy trình cấp quyền tạm thời cho engineer trong sự cố P1 như sau: On-call IT Admin có thể cấp quyền tạm thời (tối đa 24 giờ) sau khi được Tech Lead phê duyệt bằng lời. Sau 24 giờ, phải có ticket chính thức hoặc quyền sẽ bị thu hồi tự động. Tất cả quyền tạm thời phải được ghi log vào hệ thống Security Audit [1].
```

#### Sources Retrieved

- support/sla-p1-2026.pdf
- support/helpdesk-faq.md
- it/access-control-sop.md

---

### gq07 — Công ty sẽ phạt bao nhiêu nếu team IT vi phạm cam kết SLA P1... (medium)
**Points**: 10 | **Score Level**: PARTIAL | **Raw Score**: +5.0

#### Grading Criteria

✅ KHÔNG bịa ra mức phạt hay con số cụ thể
✅ Nêu rõ thông tin này không có trong tài liệu hiện có
✅ KHÔNG nói 'theo chính sách công ty, mức phạt là...' mà không có nguồn
❌ Tùy chọn: gợi ý liên hệ bộ phận có thẩm quyền

#### Hallucination Check
**Detected**: ✅ NO
**Reasoning**: HALLUCINATION: NO
REASON: The student's answer "Tôi không biết" does not introduce any unsupported information or match any failure modes.

#### Student Answer
```
Tôi không biết.
```

#### Sources Retrieved

- support/helpdesk-faq.md
- it/access-control-sop.md

---

### gq08 — Nhân viên phải báo trước bao nhiêu ngày để xin nghỉ phép năm... (hard)
**Points**: 10 | **Score Level**: PENALTY | **Raw Score**: -5.0

#### Grading Criteria

✅ Nêu đúng: nghỉ phép năm báo trước 3 ngày làm việc
✅ Nêu đúng: nghỉ ốm TRÊNn 3 ngày cần giấy tờ y tế
✅ Phân biệt rõ hai ngữ cảnh khác nhau của cùng con số '3 ngày'
✅ Không lẫn lộn hai quy định

#### Hallucination Check
**Detected**: 🚨 YES
**Reasoning**: HALLUCINATION: YES
REASON: The requirement to notify three working days in advance for annual leave is not supported by the provided context.

#### Student Answer
```
Nhân viên phải báo trước ít nhất 3 ngày làm việc để xin nghỉ phép năm [2]. Số ngày cần giấy tờ khi nghỉ ốm là nếu nghỉ trên 3 ngày liên tiếp [1], do đó con số này không giống nhau.
```

#### Sources Retrieved

- it/access-control-sop.md
- hr/leave-policy-2026.pdf

---

### gq09 — Mật khẩu tài khoản công ty cần đổi định kỳ không? Nếu có, hệ... (medium)
**Points**: 8 | **Score Level**: PARTIAL | **Raw Score**: +4.0

#### Grading Criteria

✅ Xác nhận mật khẩu cần đổi định kỳ
✅ Nêu đúng chu kỳ: 90 ngày
✅ Nêu đúng thời gian nhắc nhở: 7 ngày trước
❌ Cung cấp ít nhất một kênh để đổi (SSO portal hoặc Helpdesk ext. 9000)

#### Hallucination Check
**Detected**: ✅ NO
**Reasoning**: HALLUCINATION: NO
REASON: The student answer accurately reflects the information provided in the context regarding the password change policy.

#### Student Answer
```
Có, mật khẩu cần thay đổi định kỳ mỗi 90 ngày. Hệ thống sẽ nhắc nhở 7 ngày trước khi hết hạn [1].
```

#### Sources Retrieved

- support/helpdesk-faq.md
- it/access-control-sop.md

---

### gq10 — Chính sách hoàn tiền hiện tại áp dụng cho đơn hàng đặt trước... (hard)
**Points**: 10 | **Score Level**: PARTIAL | **Raw Score**: +5.0

#### Grading Criteria

✅ Kết luận rõ ràng: KHÔNG áp dụng cho đơn hàng trước 2026-02-01
✅ Nêu đúng effective_date: 01/02/2026
✅ Đề cập chính sách phiên bản 3 áp dụng cho đơn cũ
❌ Có citation về effective_date (từ metadata hoặc Điều 1)

#### Hallucination Check
**Detected**: ✅ NO
**Reasoning**: HALLUCINATION: NO
REASON: The student's answer is supported by the context and does not match the common failure modes.

#### Student Answer
```
Chính sách hoàn tiền hiện tại không áp dụng cho đơn hàng đặt trước ngày 01/02/2026. Các đơn hàng đặt trước ngày này sẽ áp dụng theo chính sách hoàn tiền phiên bản 3 [1].
```

#### Sources Retrieved

- policy/refund-v4.pdf

---
