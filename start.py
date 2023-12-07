import requests
import datetime
import json
from colorama import init, Fore, Style

# 初始化Colorama
init(autoreset=True)

# 欢迎提示
print(Fore.CYAN + Style.BRIGHT + r'''
  _____  _____   _____  _____  _____ _  __
 |  __ \|  __ \ / ____|/ ____|/ ____| |/ /
 | |  | | |  | | |    | (___ | |  __| ' / 
 | |  | | |  | | |     \___ \| | |_ |  <  
 | |__| | |__| | |____ ____) | |__| | . \ 
 |_____/|_____/ \_____|_____/ \_____|_|\_\
                                          
''' + Fore.RESET + r'''Welcome to 叮当猫智能身份证补全!''')
print() 

# 获取用户的auth_secret
auth_secret = input("\n请输入您的安全密钥 (auth_secret):" + f"{Fore.GREEN}")

with open('input.txt', 'r', encoding='UTF-8') as file:
    lines = file.readlines()

output_lines = []

# 遍历文件
for line in lines:
    # ...（之前的格式检查代码）

    # 尝试分割字符串并定义 data 变量
    try:
        name, wildcardIDCard = line.split(', ')
        if not name or not wildcardIDCard:
            raise ValueError("无效的姓名或身份证号码")

        # 准备请求数据
        data = {
            "auth_secret": auth_secret,
            "name": name,
            "wildcardIDCard": wildcardIDCard,
        }
    except ValueError as e:
        print(Fore.RED + f"格式错误: '{line}' - {str(e)}")
        continue  # 如果格式不正确，跳过当前迭代

    # 记录开始时间
    start_time = datetime.datetime.now()

    # 发送POST请求
    url = "https://api.ae6a859f07d19413.com/api/v1/09B219F8177F9B68.php"
    response = requests.post(url, data=data)

    # 检查响应内容类型
    if 'text/html' in response.headers.get('Content-Type', ''):
        print(Fore.RED + "错误: 您的请求被阻止。请确保您的IP地址在系统的白名单内。")
        continue  # 如果请求被阻止，跳过当前迭代

    response_data = json.loads(response.text)

    # 检查API错误
    if response_data["code"] == 500 and "Invalid API Key Limit" in response_data["message"]:
        print(Fore.RED + "错误: 无效的API密钥。请检查您的API密钥。")
        break  # 如果API密钥无效，停止循环

    # 计算花费的时间
    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time

    # 判断补全是否成功
    result = "成功" if response_data["code"] == 200 and response_data.get("data") and "total" in response_data["data"] and response_data["data"]["total"] > 0 else "失败"
    id_card = response_data["data"]["result"][0]["id_card"] if result == "成功" else wildcardIDCard

    # 打印过程信息
    process_info = f"{name},{id_card},{result},{elapsed_time.total_seconds():.6f}s"
    print(f"{Fore.LIGHTRED_EX}{name},{Fore.YELLOW}{id_card},{Fore.RESET}{result},{Fore.LIGHTCYAN_EX}{elapsed_time.total_seconds():.6f}s")

    output_lines.append(process_info)
    
    # 打印过程信息
    process_info = f"{name},{id_card},{result},{elapsed_time.total_seconds():.6f}s"
    print(f"{Fore.LIGHTRED_EX}{name},{Fore.YELLOW}{id_card},{Fore.RESET}{result},{Fore.LIGHTCYAN_EX}{elapsed_time.total_seconds():.6f}s")

    output_lines.append(process_info)

# 仅当API密钥有效时才继续
if api_key_valid:
    # 生成带有时间戳的文件名
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_file_name = f"output_{current_time}.txt"

    # 询问用户是否过滤失败的条目
    filter_failed = input("\n是否过滤处理结果为失败的条目(Y/N): " + f"{Fore.GREEN}")
    if filter_failed.upper() == "Y":
        # 过滤失败的条目并保存到文件
        with open(output_file_name, 'w', encoding='UTF-8') as file:
            for line in output_lines:
                if "成功" in line:
                    file.write(line.split(',')[0] + ', ' + line.split(',')[1] + '\n')
        print(Fore.RESET + f"\n过滤后的结果已保存到 " + Fore.YELLOW + f"{output_file_name}" + Fore.RESET + " 文件中。")
    else:
        # 将所有结果保存到文件
        with open(output_file_name, 'w', encoding='UTF-8') as file:
            for line in output_lines:
                file.write(line.split(',')[0] + ', ' + line.split(',')[1] + '\n')
        print(Fore.RESET + f"\n所有结果已全部保存到 " + Fore.YELLOW + f"{output_file_name}" + Fore.RESET + " 文件中。")
