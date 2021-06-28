# 使用说明

```bash

# 进入项目文件夹
cd 5nd音乐网爬虫

# 安装依赖库
pip install -r requirements.txt

# 运行程序, 并等待程序运行
# 程序运行期间会生成 items.jl 和 runtime.log
# item.jl 存放爬取下来的数据, 格式为 jsonlines
# runtime.log 用于保存程序运行日志，用于排查 bug
python crawl.py

```