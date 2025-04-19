from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from crewai import Agent, Task, Crew, Process
from langchain_community.document_loaders import WebBaseLoader
from n01_crewai_for_tools import WebScraperTool, CalculatorTool, MyCustomDuckDuckGoTool

# .env 파일 로드하여 OPENAI_API_KEY 등 환경변수 설정
load_dotenv()  # .env 파일에서 API 키 등 환경변수 로드

# 도구 인스턴스 생성
search_tool = MyCustomDuckDuckGoTool()
scrape_tool = WebScraperTool()
calculator_tool = CalculatorTool()

# 총괄 여행 플래너 (관리자 Agent)
planner_agent = Agent(
    role="총괄 여행 플래너",
    goal="최적의 서울 근교 1박 2일 여행 일정과 추천 음식을 종합하여 최종 여행 계획서를 작성",
    backstory="10년 경력의 베테랑 여행 컨설턴트로 다양한 분야의 의견을 취합하여 여행 계획을 완성합니다.",
    allow_delegation=True,   # 다른 에이전트에게 업무 위임을 허용
    llm="gpt-4o-mini",
    verbose=True
)

# 여행 전문가 Agent (여행 일정 추천 담당)
travel_agent = Agent(
    role="여행 전문가",
    goal="최신 여행 트렌드를 조사하여 서울 근교의 인기 있는 여행지와 일정을 제안",
    backstory="국내 여행지에 대해 잘 알고 있는 전문가로, 최근의 여행 트렌드를 바탕으로 관광지를 추천합니다.",
    tools=[search_tool],
    llm="gpt-4o-mini",
    verbose=True
)

# 요리 전문가 Agent (음식 추천 담당)
culinary_agent = Agent(
    role="요리 전문가",
    goal="추천된 여행지와 잘 어울리는 현지 음식 및 레시피를 추천",
    backstory="국내 각 지역의 음식 문화와 레시피에 능통한 전문가로, 여행지에 어울리는 음식을 추천합니다.",
    tools=[search_tool],
    llm="gpt-4o-mini",
    verbose=True
)

# Task 정의 (총괄 플래너에게 최종 여행 계획서 작성 지시)
planner_task = Task(
    description=(
        "국내 최신 여행 트렌드가 반영된 서울 근교의 1박 2일 여행 일정을 작성하고, "
        "각 여행지와 잘 어울리는 현지 음식과 레시피를 포함하여 여행 계획서를 한국어로 작성해주세요."
    ),
    expected_output=(
        "최신 여행 트렌드를 반영한 서울 근교 1박 2일 여행 일정과 "
        "각 여행지의 현지 음식 및 간단한 레시피를 포함한 한국어 여행 계획서"
    ),
    agent=planner_agent
)

# 여행 전문가를 위한 태스크
travel_task = Task(
    description=(
        "서울 근교의 1박 2일 여행지로 적합한 장소를 조사하고, "
        "교통 수단, 숙박 정보, 관광 명소 등을 포함한 여행 일정을 제안해주세요."
    ),
    expected_output="서울 근교 1박 2일 여행 일정 제안서",
    agent=travel_agent
)

# 요리 전문가를 위한 태스크
culinary_task = Task(
    description=(
        "제안된 여행지에서 맛볼 수 있는 현지 음식과 특산물을 조사하고, "
        "간단한 레시피나 추천 식당 정보를 제공해주세요."
    ),
    expected_output="여행지별 음식 추천 및 레시피 가이드",
    agent=culinary_agent
)

# Crew 구성 (계층적 프로세스 사용)
crew = Crew(
    agents=[travel_agent, culinary_agent],   # 하위 실행에 참여할 에이전트들 (관리자 제외)
    tasks=[planner_task],
    process=Process.hierarchical,
    manager_agent=planner_agent,   # 총괄 여행 플래너를 매니저로 지정
    verbose=True
)

# Crew 실행
if __name__ == "__main__":
    result = crew.kickoff()
    print("\n\n📗 최종 여행 계획서:\n")
    print(result)