---
name: so-tu-vung-a4
description: Tạo sổ học từ vựng tiếng Anh + tiếng Trung theo phương pháp gấp giấy A4 4 cột (sáng đọc, trưa viết nghĩa, tối viết lại từ, sáng hôm sau kiểm tra, cuối tuần ôn + sổ chép riêng), xuất ra một file HTML chạy offline, miễn phí, không cần tài khoản, có phát âm và bàn phím pinyin. Dùng skill này bất cứ khi nào người dùng muốn học, ôn hoặc luyện từ vựng (Anh, Trung, hoặc cả hai), gửi danh sách từ / file Excel / Google Sheets từ vựng, nhắc tới "giấy A4", "gấp 4 cột", "chép riêng", "unit từ mới", HSK, IELTS, TOEIC, hoặc cần bộ từ vựng cho công việc — kể cả khi họ không nói rõ là cần một công cụ.
---

# Sổ Từ Vựng A4

Skill này biến một danh sách từ vựng thành một **file HTML tự chạy** (mở bằng Chrome/Edge, không cần mạng để học, không cần tài khoản) mô phỏng phương pháp học bằng tờ A4 gấp 4 cột:

| Buổi | Cột | Việc làm |
|---|---|---|
| Sáng | 1 | Đọc từ mới, nghe phát âm, chép từ |
| Trưa | 2 | Nhìn từ → viết nghĩa, chấm ✓/✗, đọc lại từ sai |
| Tối | 3 | Gấp cột 1, nhìn nghĩa → viết lại từ |
| Sáng hôm sau | 4 | Gấp cột 1–2, nhìn từ → viết nghĩa; từ sai vào **Sổ chép riêng** |
| Thứ 7, CN | – | Ôn toàn bộ từ trong tuần + luyện sổ chép riêng |

Ứng dụng có sẵn: nhập Excel/CSV/dán từ Sheets, phát âm Anh/Trung bằng giọng đọc của trình duyệt, bàn phím pinyin (gõ `gongzuo` → 工作, `gong1` → gōng), bảng pinyin có âm thanh, sao lưu/khôi phục `.json`.

## Quy trình

1. **Lấy danh sách từ.** Người dùng có thể dán văn bản, gửi file `.xlsx/.csv`, ảnh chụp danh sách, hoặc chỉ nói chủ đề ("50 từ tiếng Trung văn phòng", "từ vựng IELTS unit 3").
   - Nếu chỉ có chủ đề: tự soạn danh sách phù hợp trình độ họ nói tới.
   - Nếu từ thiếu nghĩa: bổ sung nghĩa **tiếng Việt** ngắn gọn (1–3 nghĩa, ngăn bằng dấu phẩy — máy chấm chấp nhận khớp bất kỳ nghĩa nào, nên nghĩa gọn thì chấm chuẩn hơn).
   - Bổ sung phiên âm: IPA cho tiếng Anh (`/ˈvaɪtl/`), pinyin có dấu cho tiếng Trung (`gōngzuò`). Kiểm tra kỹ pinyin vì người dùng sẽ học theo nó.
   - Ví dụ là tuỳ chọn; chỉ thêm khi người dùng muốn hoặc từ dễ nhầm.
2. **Ghi ra file CSV** (UTF-8) với tiêu đề: `Từ,Nghĩa,Phiên âm,Ngôn ngữ,Ví dụ` (`Ngôn ngữ` là `en` hoặc `zh`). Có thể trộn Anh và Trung trong cùng file — ứng dụng sẽ xếp xen kẽ trong mỗi unit, giúp người học cả hai thứ tiếng cùng lúc.
3. **Đóng gói**:
   ```bash
   python scripts/build_deck.py words.csv "So-tu-vung-<ten-bo>.html" --deck "<Tên bộ>" --unit-size 20
   ```
   Script nhận cả `.csv`, `.xlsx` (cần `openpyxl`) hoặc `.json`. Bộ từ được nhúng vào file và tự nạp ở lần mở đầu tiên. Unit 15–20 từ là vừa cho một ngày; người mới hoặc tiếng Trung khó thì 10–12.
4. **Giao file** cho người dùng (công cụ gửi file nếu có) kèm hướng dẫn ngắn bên dưới. Nếu người dùng chỉ muốn ứng dụng trống để tự nhập, giao thẳng `assets/so-tu-vung-a4-offline.html` và file mẫu `assets/mau-tu-vung.csv`.

## Hướng dẫn gửi kèm (viết bằng tiếng Việt, ngắn)

- Tải file về máy, mở bằng Chrome hoặc Edge. Trên điện thoại: mở bằng Chrome.
- Tab **Hôm nay** cho biết cần làm bước nào; bấm **Bắt đầu học** mỗi sáng.
- Tiến độ lưu trong trình duyệt đó: dùng **Cài đặt → Tải file sao lưu** hàng tuần; chuyển máy thì **Khôi phục từ file**.
- Không nghe được tiếng Trung trên Windows: Settings → Time & language → Speech → thêm giọng Chinese (Simplified).
- Muốn có link dùng trên mọi thiết bị miễn phí: kéo thả file vào https://app.netlify.com/drop hoặc đưa lên GitHub Pages (đổi tên file thành `index.html`).

## Lưu ý

- Việc đọc file Excel trong ứng dụng và tự điền pinyin tải thư viện từ CDN nên cần mạng; học, chấm bài, phát âm và bàn phím pinyin chạy offline. Vì vậy hãy tự điền pinyin trong CSV trước khi đóng gói.
- Khi thêm bộ từ mới cho người đã có sổ: tạo file mới với `--deck` khác tên; khi mở, bộ mới được thêm vào sổ hiện có trong trình duyệt (nếu mở cùng một file trên cùng trình duyệt) — hoặc hướng dẫn họ dùng tab **Nhập từ vựng** với file CSV.
