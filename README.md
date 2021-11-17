# Thuật toán ước lượng năng lực thí sinh trong mô hình IRT 3 tham số

Các ràng buộc:
- Trả lời đúng liên tiếp một ngưỡng câu hỏi -> lấy ra câu khó nhất và break
- Theta không thay đổi đáng kể sau một số câu liên tiếp -> lấy ra câu khó nhất và break
- Trả lời sai liên tiếp một ngưỡng câu hỏi -> lấy ra câu dễ nhất chưa trả lời
- Theta được khởi tạo từ lần thi trước của thí sinh