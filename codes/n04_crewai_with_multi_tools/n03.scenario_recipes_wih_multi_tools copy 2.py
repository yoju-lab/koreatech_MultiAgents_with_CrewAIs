from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from crewai import Agent, Task, Crew, Process
from langchain_community.document_loaders import WebBaseLoader
# Import the tools from the file with dot in name
from n01_crewai_for_tools import MyCustomDuckDuckGoTool, WebScraperTool, CalculatorTool

# .env 파일 로드하여 OPENAI_API_KEY 등 환경변수 설정
load_dotenv()

# 도구 인스턴스 생성
search_tool = MyCustomDuckDuckGoTool()
scrape_tool = WebScraperTool()
calculator_tool = CalculatorTool()

travel_agent = Agent(
    role="여행 전문가",
    goal="최적의 여행 일정과 예산 계획 제공",
    backstory="다년간의 여행 플래너 경험 보유",
    tools=[search_tool, scrape_tool, calculator_tool],
    llm="gpt-4o-mini",
    verbose=True
)
travel_task = Task(
    description="파리 5일 여행 일정(문화, 미식 포함), 예산은 1000달러 (항공 300달러, 숙박 하루 100달러).",
    expected_output="한국어로 작성된 5일간 파리 여행에 대한 상세한 일정과 예산 계산 결과",
    agent=travel_agent
)
crew = Crew(
    agents=[travel_agent], 
    tasks=[travel_task], 
    process=Process.sequential,
    verbose=True
)

result_multi = crew.kickoff()
