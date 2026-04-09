# Multi-Agent Essay — 多智能体课程论文写作系统

基于 [CrewAI](https://github.com/crewAIInc/crewAI) + [智谱AI GLM](https://open.bigmodel.cn) 的多智能体协作系统，自动完成课程论文从选题到成稿的全流程。

## 系统架构

```
用户输入课程名称
       │
       ▼
┌──────────────┐
│  1. 选题顾问  │  生成 3-5 个选题建议 → 用户选择
└──────┬───────┘
       ▼
┌──────────────┐
│  2. 文献研究员 │  搜索并整理相关文献
└──────┬───────┘
       ▼
┌──────────────┐
│  3. 大纲规划师 │  生成论文大纲 → 用户确认
└──────┬───────┘
       ▼
┌──────────────┐
│  4. 论文写作者 │  撰写论文全文（3000-5000字）
└──────┬───────┘
       ▼
┌──────────────┐
│  5. 审稿编辑  │  审阅润色 → 输出最终版本
└──────────────┘
```

5 个专业 Agent 各司其职，通过 CrewAI 框架协调，在选题和大纲阶段暂停等待用户确认。

## 项目结构

```
.
├── main.py              # CLI 入口
├── flow.py              # 5 阶段完整流程编排
├── config/
│   └── llm.py           # 智谱AI GLM 模型配置
├── agents/
│   ├── topic_advisor.py # 选题顾问
│   ├── researcher.py    # 文献研究员
│   ├── outliner.py      # 大纲规划师
│   ├── writer.py        # 论文写作者
│   └── reviewer.py      # 审稿编辑
├── crews/
│   ├── topic_crew.py    # 选题阶段
│   ├── research_crew.py # 文献研究阶段
│   ├── outline_crew.py  # 大纲规划阶段
│   ├── writing_crew.py  # 写作阶段
│   └── review_crew.py   # 审阅阶段
├── tools/
│   ├── search_tool.py   # 网络搜索工具（SerperDev）
│   └── file_tool.py     # 文件读写工具
├── output/              # 论文输出目录
├── .env                 # API Key 配置
└── pyproject.toml       # 项目依赖
```

## 快速开始

### 环境要求

- **操作系统**: Windows / Linux / macOS 均可
- Python >= 3.10
- [uv](https://docs.astral.sh/uv/)（推荐）或 pip

### 安装

```bash
# 克隆项目
git clone https://github.com/Dewuner/multi-agent-essay.git
cd multi-agent-essay

# 安装依赖（推荐使用 uv）
uv sync

# 或使用 pip
pip install -e .
```

<details>
<summary>Windows 用户注意事项</summary>

- 推荐使用 **Windows Terminal** 或 **PowerShell** 运行
- 如使用 WSL2，在 WSL 终端中操作即可
- uv 安装命令（PowerShell）：
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
</details>

<details>
<summary>Linux / macOS 用户注意事项</summary>

- uv 安装命令：
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- 如遇到权限问题，可能需要在命令前加 `sudo`
</details>

### 配置 API Key

复制 `.env` 文件并填入你的 API Key：

```bash
# 智谱AI API Key（必填，从 https://open.bigmodel.cn 获取）
ZHIPUAI_API_KEY=your_api_key_here

# Serper API Key（可选，从 https://serper.dev 获取，用于网络搜索）
SERPER_API_KEY=your_serper_key_here
```

### 运行

```bash
# 基本用法
uv run python main.py --course "课程名称"

# 指定额外要求
uv run python main.py --course "课程名称" --requirements "字数不少于4000字，需包含案例分析"
```

运行后系统将：
1. 生成选题建议，等待你选择
2. 自动搜索文献并整理
3. 生成大纲，等待你确认（不满意可提出修改建议）
4. 撰写论文全文
5. 审阅润色，输出最终版本到 `output/` 目录

## 示例

```bash
$ uv run python main.py --course "创业者故事赏析"

============================================================
  课程论文写作系统 — 创业者故事赏析
============================================================

【阶段 1/5】生成选题建议...

选题建议如下：
============================================================
1. 从张一鸣到王兴：互联网创业者的共性特质分析
   ...
```

## 技术栈

- **框架**: [CrewAI](https://github.com/crewAIInc/crewAI) — 多智能体编排
- **LLM**: [智谱AI GLM-4-Flash](https://open.bigmodel.cn) — 通过 OpenAI 兼容接口调用
- **搜索**: [SerperDev](https://serper.dev) — Google 搜索 API
- **包管理**: [uv](https://docs.astral.sh/uv/)

## License

[MIT](LICENSE)
