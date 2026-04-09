from crewai import LLM
import os


def get_llm(model_name: str = "GLM-4.7") -> LLM:
    """获取智谱AI GLM模型"""
    return LLM(
        model=f"openai/{model_name}",
        base_url="https://open.bigmodel.cn/api/coding/paas/v4",
        api_key=os.getenv("ZHIPUAI_API_KEY"),
        temperature=0.7,
    )
