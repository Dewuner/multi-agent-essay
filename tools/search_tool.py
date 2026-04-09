import os

import requests
from crewai.tools import tool as crewai_tool


@crewai_tool("web_search")
def web_search(query: str) -> str:
    """搜索网络获取学术资料和相关信息。

    Args:
        query: 搜索关键词
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return (
            f"未配置 TAVILY_API_KEY，请手动补充关于「{query}」的文献资料。"
            "建议使用 Google Scholar、知网等平台进行检索。"
        )

    try:
        resp = requests.post(
            "https://api.tavily.com/search",
            headers={"Content-Type": "application/json"},
            json={
                "api_key": api_key,
                "query": query,
                "max_results": 8,
                "include_answer": False,
            },
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()

        results = []
        for item in data.get("results", [])[:8]:
            title = item.get("title", "")
            link = item.get("url", "")
            snippet = item.get("content", "")
            results.append(f"- {title}\n  {link}\n  {snippet}")

        if not results:
            return f"未找到关于「{query}」的相关结果。"

        return f"搜索「{query}」的结果：\n\n" + "\n\n".join(results)

    except Exception as e:
        print(f"[search_tool] 搜索失败: {e}")
        return (
            f"搜索工具暂不可用 ({e})，请手动补充关于「{query}」的文献资料。"
            "建议使用 Google Scholar、知网等平台进行检索。"
        )
