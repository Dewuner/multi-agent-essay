#!/usr/bin/env python3
"""课程论文多智能体写作系统 — CLI 入口"""

import argparse
import os
import sys

from dotenv import load_dotenv


def main():
    load_dotenv()

    if not os.getenv("ZHIPUAI_API_KEY") or os.getenv("ZHIPUAI_API_KEY") == "your_api_key_here":
        print("错误：请先在 .env 文件中设置 ZHIPUAI_API_KEY")
        print("获取 API Key: https://open.bigmodel.cn")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="课程论文多智能体写作系统")
    parser.add_argument(
        "--course", "-c",
        required=True,
        help="课程名称，例如 '创业者故事赏析' 或 '公共安全与应急技术'",
    )
    parser.add_argument(
        "--requirements", "-r",
        default="",
        help="额外的论文要求（可选）",
    )
    args = parser.parse_args()

    # 避免循环导入，延迟导入 flow
    from flow import run_full_flow

    run_full_flow(args.course, args.requirements)


if __name__ == "__main__":
    main()
