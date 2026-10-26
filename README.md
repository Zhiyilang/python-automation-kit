# python-automation-kit

[![CI](https://github.com/Zhiyilang/python-automation-kit/actions/workflows/test.yml/badge.svg)](https://github.com/Zhiyilang/python-automation-kit/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

零依赖（纯 Python 标准库）的日常自动化小工具集。拿来即用，不需要 `pip install` 任何东西，Windows / macOS / Linux 通用。

每一个脚本都**默认安全**：查重只报告不删、重命名默认 dry-run，避免误操作系统文件。

## 工具一览

| 脚本 | 用途 | 默认安全 |
|------|------|----------|
| `file_dedup.py` | 按内容 SHA-256 找出重复文件，报告可释放空间 | ✅ 只报告；`--delete` 才移到备份夹 |
| `batch_rename.py` | 用正则批量重命名文件夹里的文件 | ✅ 默认 dry-run；`--apply` 才真改 |
| `folder_tree.py` | 打印 / 导出目录树（带文件大小） | ✅ 只读 |
| `csv_merge.py` | 合并多个同表头 CSV 成一个 | ✅ 只读源文件 |

## 快速开始

```bash
# 找出 Downloads 里的重复文件（只看不改）
python file_dedup.py "C:/Users/你/Downloads"

# 预览把 IMG_2024_xxx.jpg 改名成 photo_2024_xxx.jpg
python batch_rename.py "C:/Photos" --pattern "IMG_(\d+_\w+)" --repl "photo_\1"

# 导出项目目录树
python folder_tree.py D:/project --out tree.txt

# 合并 data 目录下所有 CSV
python csv_merge.py "data/*.csv" -o all.csv
```

每条命令都带 `--help`，参数随时可查。

## 为什么是它

- **零依赖**：只用 Python 自带库，拷到任何装了 Python 3.8+ 的机器就能跑。
- **可审计**：脚本都很短，一眼能看懂在干什么，不用担心偷偷删你文件。
- **好改造**：这是给 RPA / 办公自动化场景打底的模板，影刀、UiBot 里也能照着改写逻辑。

## 许可证

MIT —— 随便用、随便改、随便拿去上架组件市场。
