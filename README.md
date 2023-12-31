# 叮当猫智能身份证补全工具

![](https://img.shields.io/github/stars/pandao/editor.md.svg) ![](https://img.shields.io/github/forks/pandao/editor.md.svg) ![](https://img.shields.io/github/tag/pandao/editor.md.svg) ![](https://img.shields.io/github/release/pandao/editor.md.svg) ![](https://img.shields.io/github/issues/pandao/editor.md.svg) ![](https://img.shields.io/bower/v/editor.md.svg)

## 简介
叮当猫智能身份证补全工具是一个基于Python的脚本，用于自动补全部分身份证信息。它使用特定的API来处理输入数据，并返回补全的身份证信息。该工具旨在帮助需要大量身份证信息处理的用户快速、高效地完成任务。

![运行截图](https://raw.githubusercontent.com/dingdangcats/CompleteIDCardsBatches/main/2023-12-20_01-37-49.png)

## 功能
- 从文本文件读取身份证信息
- 使用API自动补全信息
- 输出处理结果到文本文件
- 提供友好的用户界面和错误提示

## 安装
1. 克隆仓库到本地
```
git clone https://github.com/dingdangcats/CompleteIDCardsBatches.git
```
2. 安装所需依赖
```
pip install -r requirements.txt
```

## 使用方法
1. 将需要处理的数据以文本形式放入`input.txt`文件中，格式为`姓名, 身份证号码`。
2. 运行脚本:
```
python start.py
```
3. 根据提示输入您的`auth_secret`（API密钥）。
4. 查看输出文件中的结果。

## 注意事项
- 请确保input.txt格式正确
```
姓名, 模糊身份证
```
- 正常情况下，程序会生成三个文件
`1）去重版补齐(txt)`
`2）未去重版补齐(txt)`
`2）去重版excel表格(xlsx)`

- 确保您的API密钥有效且未过期。
- 确保您的ip在系统白名单内。
- 本工具仅用于学习和研究目的，不应用于非法活动。

## 贡献
欢迎任何形式的贡献，包括新功能建议、代码优化、文档改进等。

## 许可
[MIT](https://opensource.org/licenses/MIT)





