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

recipe_agent = Agent(
    role="요리 분석가",
    goal="요리 레시피 추천 및 안내",
    backstory="글로벌 요리 전문가 AI 셰프",
    tools=[search_tool, scrape_tool],
    llm="gpt-4o-mini",
    verbose=True
)
recipe_task = Task(
    description="채식 파스타 레시피 추천, 재료 및 조리법 안내",
    expected_output="한국어로 작성된 채식 파스타 레시피(재료 및 조리법)",
    agent=recipe_agent
)
crew = Crew(
    agents=[recipe_agent], 
    tasks=[recipe_task], 
    process=Process.sequential,
    verbose=True
)

result_multi = crew.kickoff()
