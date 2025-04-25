# Giả sử bạn có kết quả email hoặc thông tin cần lưu
email_results = "List of unread emails:\n"

# Thêm vào kết quả bạn muốn lưu
email_results += "Email 1: test@example.com\n"
email_results += "Email 2: another@example.com\n"

# Lưu vào file .txt
with open("email_results.txt", "w") as file:
    file.write(email_results)

print("Results saved to email_results.txt")
