import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext, ttk
import requests
import datetime
import json

def process_data():
    auth_secret = entry_auth_secret.get()
    if not auth_secret:
        messagebox.showerror("错误", "请输入您的安全密钥")
        return

    file_path = filedialog.askopenfilename(title="选择输入文件", filetypes=[("Text files", "*.txt")])
    if not file_path:
        return

    with open(file_path, 'r', encoding='UTF-8') as file:
        lines = file.readlines()

    output_lines = []
    has_error = False

    for line in lines:
        name, wildcardIDCard = line.strip().split(', ')
        data = {
            "auth_secret": auth_secret,
            "name": name,
            "wildcardIDCard": wildcardIDCard,
        }

        start_time = datetime.datetime.now()
        url = "https://api.ae6a859f07d19413.com/api/v1/09B219F8177F9B68.php"
        response = requests.post(url, data=data)
        response_data = json.loads(response.text)
        end_time = datetime.datetime.now()
        elapsed_time = end_time - start_time

        if response_data["code"] == 500 and "Invalid API Key Limit" in response_data["message"]:
            process_info = f"错误: 无效的API密钥。处理 {name} 时失败。"
            text_process.insert(tk.END, process_info + '\n')
            has_error = True
            continue

        if response_data["code"] == 200 and response_data.get("data") and "total" in response_data["data"] and response_data["data"]["total"] > 0:
            result = "成功"
            id_card = response_data["data"]["result"][0]["id_card"]
            name = response_data["data"]["result"][0]["name"]
            process_info = f"{name},{id_card},{result},{elapsed_time.total_seconds():.6f}s"
        else:
            result = "失败"
            id_card = wildcardIDCard
            process_info = f"{name},{id_card},{result},{elapsed_time.total_seconds():.6f}s"

        text_process.insert(tk.END, process_info + '\n')
        output_lines.append(process_info)

    if not has_error:
        output_file_name = f"output_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
        with open(output_file_name, 'w', encoding='UTF-8') as file:
            for line in output_lines:
                file.write(line + '\n')
        messagebox.showinfo("完成", f"所有结果已全部保存到 {output_file_name}")
    else:
        messagebox.showwarning("警告", "处理过程中遇到错误，请检查输出文件和日志。")

root = tk.Tk()
root.title("叮当猫智能身份证补全")
root.geometry("800x500")  # 设置窗口大小

style = ttk.Style()
style.theme_use('clam')

frame = ttk.Frame(root, padding="10")
frame.pack(fill='both', expand=True)

label_auth_secret = ttk.Label(frame, text="请输入您的安全密钥 (auth_secret):", font=("Helvetica", 12))
label_auth_secret.pack(fill='x', expand=True)

entry_auth_secret = ttk.Entry(frame, font=("Helvetica", 12), show='*')
entry_auth_secret.pack(fill='x', expand=True, pady=5)

button_process = ttk.Button(frame, text="处理数据", command=process_data)
button_process.pack(fill='x', expand=True, pady=10)

text_process = scrolledtext.ScrolledText(frame, font=("Helvetica", 10), height=15)
text_process.pack(fill='both', expand=True, pady=5)

root.mainloop()
