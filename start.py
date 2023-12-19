import requests
import datetime
import json
from colorama import init, Fore, Style
import pandas as pd

# 初始化Colorama
init(autoreset=True)

# 欢迎提示
print(Fore.CYAN + Style.BRIGHT + r'''
  _____  _____   _____  _____  _____ _  __
 |  __ \|  __ \ / ____|/ ____|/ ____| |/ /
 | |  | | |  | | |    | (___ | |  __| ' / 
 | |  | | |  | | |     \___ \| | |_ |  <  
 | |__| | |__| | |____ ____) | |__| | . \ 
 |_____/|_____/ \_____|_____/ \_____|_|\_\   v3.0.1
                                          
''' + Fore.RESET + r'''Welcome to 叮当猫智能身份证补全!''')
print() 

import requests
import datetime
import json
from colorama import init, Fore, Style
import pandas as pd

# 初始化Colorama
init(autoreset=True)

def remove_duplicates_from_line(line):
    parts = line.split(',')
    name = parts[0].strip()  # 提取姓名
    unique_ids = set()  # 用于存储唯一的身份证号
    for id_part in parts[1:]:
        unique_id = id_part.strip()
        if unique_id not in unique_ids:
            unique_ids.add(unique_id)
    return name + ',' + ', '.join(unique_ids)

def process_file(input_file, output_file):
    with open(input_file + '.txt', 'r', encoding='UTF-8') as file:
        lines = file.readlines()

    with open(output_file + '.txt', 'w', encoding='UTF-8') as file:
        for line in lines:
            new_line = remove_duplicates_from_line(line)
            file.write(new_line + '\n')

def create_combined_list(input_list, output_list):
    combined_list = []
    for input_line, output_line in zip(input_list, output_list):
        try:
            name_input, wildcard_id = input_line.split(', ')
            name_output, *id_cards = output_line.split(',')
            id_cards_str = ', '.join(id_cards).strip()
            combined_list.append((name_input, wildcard_id, id_cards_str))
        except ValueError as e:
            print(Fore.RED + f"格式错误: 输入行'{input_line}' 或 输出行'{output_line}' - {str(e)}")
            continue  # 跳过格式错误的行
    return combined_list

def save_to_excel(data, output_file):
    df = pd.DataFrame(data, columns=['Name', 'WildcardIDCard', 'DedupedIDCards'])
    df.to_excel(output_file, index=False)

# 获取用户输入的auth_secret
auth_secret = input("\n请输入您的安全密钥 (auth_secret):" + f"{Fore.GREEN} ")

output_lines = []

# 执行API查询和处理逻辑
try:
    with open('input.txt', 'r', encoding='UTF-8') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue

        try:
            name, wildcardIDCard = line.split(', ')
            if not name or not wildcardIDCard:
                raise ValueError("无效的姓名或身份证号码")
        except ValueError as e:
            print(Fore.RED + f"格式错误: '{line}' - {str(e)}")
            continue

        data = {"auth_secret": auth_secret, "name": name, "wildcardIDCard": wildcardIDCard}
        start_time = datetime.datetime.now()
        url = "https://api.ae6a859f07d19413.com/api/v1/09B219F8177F9B68.php"
        response = requests.post(url, data=data)
        if 'text/html' in response.headers.get('Content-Type', ''):
            print(Fore.RED + "错误: 您的请求被阻止。")
            continue

        response_data = json.loads(response.text)
        elapsed_time = datetime.datetime.now() - start_time

        if response_data["code"] == 200:
            if response_data.get("message") == "Not Found Result":
                print(Fore.LIGHTYELLOW_EX + "空结果")
                output_lines.append(f"{name}, 空结果, {elapsed_time.total_seconds():.6f}s")
                continue

            id_cards = [result["id_card"] for result in response_data.get("data", {}).get("result", [])]
            id_cards_str = ', '.join(id_cards)
            process_info = f"{name},{id_cards_str},{elapsed_time.total_seconds():.6f}s"
            output_lines.append(process_info)
            print(f"{Fore.RESET}[成功] {Fore.LIGHTRED_EX}{name}, {Fore.YELLOW}{id_cards_str}, {Fore.LIGHTCYAN_EX}{elapsed_time.total_seconds():.6f}s")
        elif response_data["code"] == 500 and "Invalid API Key Limit" in response_data["message"]:
            print(Fore.RED + "错误: 无效的API密钥。")
            break
        else:
            print(Fore.RED + f"错误: {response_data.get('message', '未知错误')}")
            continue
except Exception as e:
    print(Fore.RED + f"发生未知错误: {e}")

# 生成带有时间戳的文件名
current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
output_file_name = f"output_{current_time}"

# 保存已处理的数据到文件
with open(output_file_name + '.txt', 'w', encoding='UTF-8') as file:
    for line in output_lines:
        name, id_cards_str, _ = line.rsplit(',', 2)
        file.write(f"{name}, {id_cards_str}\n")

# 调用去重函数
process_file(output_file_name, output_file_name + "_deduped")

# 将去重后的结果和input.txt文件合并到Excel
input_list = [line.strip() for line in open('input.txt', 'r', encoding='UTF-8') if line.strip()]
output_list = [line.strip() for line in open(output_file_name + '_deduped.txt', 'r', encoding='UTF-8') if line.strip()]

# 检查两个列表的长度是否匹配
if len(input_list) != len(output_list):
    print(Fore.RED + "错误: input.txt 和去重后的结果文件行数不匹配。")
else:
    combined_data = create_combined_list(input_list, output_list)
    save_to_excel(combined_data, output_file_name + '_final_output.xlsx')
    print(Fore.RESET + f"\nExcel文件已生成: {Fore.YELLOW}{output_file_name}_final_output.xlsx{Fore.RESET}")
