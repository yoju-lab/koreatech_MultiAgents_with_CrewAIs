from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from crewai import Agent, Task, Crew, Process
from langchain_community.document_loaders import WebBaseLoader
# Import the tools from the file with dot in name
from n01_crewai_for_tools import MyCustomDuckDuckGoTool, WebScraperTool, CalculatorTool

# .env 파일 로드하여 OPENAI_API_KEY 등 환경변수 설정
load_dotenv()

# LLM 초기화 (OpenAI GPT-4o-mini 모델 사용)
openai_model = os.getenv('OPENAI_MODEL')
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# 도구 인스턴스 생성
search_tool = MyCustomDuckDuckGoTool()
scrape_tool = WebScraperTool()
calculator_tool = CalculatorTool()

news_agent = Agent(
    role="뉴스 분석가",
    goal="최신 뉴스를 검색하여 요약",
    backstory="뉴스 분석 전문 AI 기자",
    tools=[search_tool, scrape_tool],
    llm="gpt-4o-mini",
    verbose=True
)
news_task = Task(
    description="최근 인공지능 관련 뉴스 3건을 요약하고 링크 제공",
    expected_output="한국어로 작성된 뉴스 3건의 요약 및 링크",
    agent=news_agent
)
crew = Crew(
    agents=[news_agent], 
    tasks=[news_task], 
    process=Process.sequential,
    verbose=True
)

result_multi = crew.kickoff()
