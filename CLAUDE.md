# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv sync

# Run the system
uv run python main.py --course "课程名称"
uv run python main.py --course "课程名称" --requirements "额外要求"

# Alternative install with pip
pip install -e .
```

No test suite or linter is configured.

## Architecture

Multi-agent academic paper writing system (多智能体课程论文写作系统) built on **CrewAI + ZhipuAI GLM**.

### 5-Stage Pipeline

`flow.py` orchestrates the full workflow sequentially:
1. **Topic Advisor** — generates 3-5 topic suggestions, pauses for user selection
2. **Researcher** — web search via Tavily API, produces structured literature notes
3. **Outliner** — generates paper outline, pauses for user confirmation (with revision loop)
4. **Writer** — writes full 3000-5000 word draft, saves intermediate file
5. **Reviewer** — polishes and outputs final version to `output/`

### Code Organization Pattern

Each pipeline stage follows the same two-file pattern:
- **`agents/<stage>.py`** — defines `create_<agent>()` (returns a CrewAI Agent with role/goal/backstory/LLM/tools) and `create_<task>()` (returns a CrewAI Task with description/expected_output)
- **`crews/<stage>_crew.py`** — defines `run_<stage>_crew()` which instantiates agent + task, creates a Crew, calls `crew.kickoff()`, returns the result string

### LLM Configuration

`config/llm.py` provides `get_llm()` which returns a CrewAI `LLM` instance connecting to ZhipuAI GLM-4-Flash via OpenAI-compatible API (`open.bigmodel.cn/api/paas/v4`). Model prefix is `openai/` for LiteLLM compatibility.

### Tools

- `tools/search_tool.py` — wraps Tavily search API with graceful fallback (returns manual search instructions if API unavailable)
- `tools/file_tool.py` — file I/O for saving intermediate and final outputs

### Environment

API keys live in `.env`:
- `ZHIPUAI_API_KEY` — required (ZhipuAI GLM)
- `TAVILY_API_KEY` — optional (Tavily for web search)
