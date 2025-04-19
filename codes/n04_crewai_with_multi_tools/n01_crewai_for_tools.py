from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from crewai import Agent, Task, Crew, Process

from crewai.tools import BaseTool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.document_loaders import WebBaseLoader

class MyCustomDuckDuckGoTool(BaseTool):
    # DuckDuckGo 검색 도구를 래핑하는 클래스, BaseTool을 상속받아 구현(필요사항 : name, description, _run 메소드)
    name: str = "DuckDuckGo Search Tool"
    description: str = "웹에서 최신 정보를 검색할 수 있는 도구입니다."

    def _run(self, query: str) -> str:
        duckduckgo_tool = DuckDuckGoSearchRun()
        response = duckduckgo_tool.invoke(query)
        return response

# .env 파일 로드하여 OPENAI_API_KEY 등 환경변수 설정
load_dotenv()

# LLM 초기화 (OpenAI GPT-4o-mini 모델 사용)
openai_model = os.getenv('OPENAI_MODEL')
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

class WebScraperTool(BaseTool):
    name: str = "웹 스크래퍼"
    description: str = "웹페이지 내용을 추출합니다."

    def _run(self, url: str) -> str:
        loader = WebBaseLoader(url)
        docs = loader.load()
        return docs[0].page_content if docs else "내용을 찾을 수 없습니다."
    
class CalculatorTool(BaseTool):
    name: str = "계산기"
    description: str = "수학 계산을 수행합니다."

    def _run(self, expression: str) -> str:
        try:
            return str(eval(expression))
        except Exception as e:
            return f"계산 오류: {e}"    