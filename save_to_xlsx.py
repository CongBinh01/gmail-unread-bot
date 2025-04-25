from openpyxl import Workbook

# Giả sử bạn có dữ liệu cần lưu vào Excel
email_data = [
    ["Sender", "Subject", "Received Date"],
    ["test@example.com", "Test Subject 1", "2025-04-26"],
    ["another@example.com", "Test Subject 2", "2025-04-25"]
]

# Tạo một workbook mới
wb = Workbook()

# Chọn sheet đầu tiên
ws = wb.active

# Thêm dữ liệu vào sheet
for row in email_data:
    ws.append(row)

# Lưu file Excel
wb.save("email_results.xlsx")

print("Results saved to email_results.xlsx")
