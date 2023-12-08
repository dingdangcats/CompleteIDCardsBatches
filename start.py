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

# 获取用户输入的auth_secret
auth_secret = input("\n请输入您的安全密钥 (auth_secret):" + f"{Fore.GREEN} ")

# 初始化api_key_valid变量
api_key_valid = True

output_lines = []

try:
    # 打开用于读取的文本文件，使用UTF-8编码
    with open('input.txt', 'r', encoding='UTF-8') as file:
        lines = file.readlines()

    # 遍历文件中的每一行
    for line in lines:
        # 去除空白字符并判断是否为空行
        line = line.strip()
        if not line:
            continue  # 跳过空行

        # 尝试分割字符串并定义 data 变量
        try:
            name, wildcardIDCard = line.split(', ')
            if not name or not wildcardIDCard:
                raise ValueError("无效的姓名或身份证号码")
        except ValueError as e:
            print(Fore.RED + f"格式错误: '{line}' - {str(e)}")
            continue  # 跳过格式错误的行

        # 准备请求数据
        data = {
            "auth_secret": auth_secret,
            "name": name,
            "wildcardIDCard": wildcardIDCard,
        }

        # 记录开始时间
        start_time = datetime.datetime.now()

        # 发送POST请求
        url = "https://api.ae6a859f07d19413.com/api/v1/09B219F8177F9B68.php"
        response = requests.post(url, data=data)

        # 检查响应内容类型
        if 'text/html' in response.headers.get('Content-Type', ''):
            print(Fore.RED + "错误: 您的请求被阻止。请确保您的IP地址在系统的白名单内。")
            continue  # 跳过当前迭代

        response_data = json.loads(response.text)

        # 检查API错误
        if response_data["code"] == 500 and "Invalid API Key Limit" in response_data["message"]:
            print(Fore.RED + "错误: 无效的API密钥。请检查您的API密钥。")
            break

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

except Exception as e:
    print(Fore.RED + f"发生未知错误,请检查input.txt格式: {e}")

finally:
    # 不管是否发生异常，都执行以下代码
    # 生成带有时间戳的文件名
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_file_name = f"output_{current_time}.txt"

    # 保存已处理的数据到文件
    with open(output_file_name, 'w', encoding='UTF-8') as file:
        for line in output_lines:
            file.write(line.split(',')[0] + ', ' + line.split(',')[1] + '\n')
    print(Fore.RESET + f"\n已处理的结果已保存到 " + Fore.YELLOW + f"{output_file_name}" + Fore.RESET + " 文件中。")
