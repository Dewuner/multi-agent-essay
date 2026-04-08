from crewai.tools import tool as crewai_tool


@crewai_tool("web_search")
def web_search(query: str) -> str:
    """搜索网络获取学术资料和相关信息。

    Args:
        query: 搜索关键词
    """
    try:
        from crewai_tools import SerperDevTool
        search = SerperDevTool()
        return search.run(search_query=query)
    except Exception:
        return (
            f"搜索工具暂不可用，请手动补充关于「{query}」的文献资料。"
            "建议使用 Google Scholar、知网等平台进行检索。"
        )
