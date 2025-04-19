from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from crewai import Agent, Task, Crew, Process

from crewai.tools import BaseTool
from langchain_community.tools import DuckDuckGoSearchRun

class MyCustomDuckDuckGoTool(BaseTool):
    # DuckDuckGo 검색 도구를 래핑하는 클래스, BaseTool을 상속받아 구현(필요사항 : name, description, _run 메소드)
    name: str = "DuckDuckGo Search Tool"
    description: str = "웹에서 최신 정보를 검색할 수 있는 도구입니다."

    def _run(self, query: str) -> str:
        duckduckgo_tool = DuckDuckGoSearchRun()
        response = duckduckgo_tool.invoke(query)
        return response

# DuckDuckGo 검색 도구 인스턴스 생성
search_tool = MyCustomDuckDuckGoTool()

# .env 파일 로드하여 OPENAI_API_KEY 등 환경변수 설정
load_dotenv()

# LLM 초기화 (OpenAI GPT-4o-mini 모델 사용)
openai_model = os.getenv('OPENAI_MODEL')
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# 정보 조사 에이전트 정의
research_agent = Agent(
    role="정보 조사자",
    goal="여행에 필요한 최신 정보를 조사하여 제공합니다.",
    backstory="온라인 정보 검색에 능통한 여행 정보 전문가입니다.",
    llm=llm,
    tools=[search_tool],    # 웹 검색 도구 장착
    verbose=True,
    max_iter=5  # 최대 반복 횟수 설정
)

# 일정 작성 에이전트 정의
planner_agent = Agent(
    role="여행 일정 기획자",
    goal="제공된 정보를 활용해 완성도 높은 여행 일정을 작성합니다.",
    backstory="국내 여행 일정을 여러 차례 기획한 경험이 풍부한 전문가입니다.",
    llm=llm,
    verbose=True,
    max_iter=3  # 최대 반복 횟수 설정
)

# 정보 조사 Task 정의
research_task = Task(
    description=(
        "{place} 여행을 위해 알아야 할 핵심 정보를 조사하세요.\n"
        "{place}의 인기 관광지 목록, 지역별 맛집 추천, 이동 시 유용한 교통 정보 등을 최신 자료를 기반으로 정리해 주세요."
        "검색 주제와 링크를 꼭 포함해 주세요.\n"
    ),
    agent=research_agent,
    expected_output="{place} 여행에 대한 요약 정보 목록"
)

# 개선된 일정 작성 Task 정의 (예산 및 교통 고려 추가)
improved_planning_task = Task(
    description=(
        "위의 조사 결과를 참고하여 {place}에서 {days}일 동안 머무는 여행 일정을 작성해 주세요.\n"
        "각 날짜별로 오전/오후/저녁 계획을 세우고, 조사된 관광지와 맛집 정보를 일정에 반영하세요.\n"
        "가능하면 **예산은 하루 {budget_per_day}만원 내외로 맞추고, 이동은 모두 대중교통**을 이용하는 것으로 고려하세요.\n"
        "버스정류장 및 지하철역을 포함한 대중교통 경로를 제안해 주세요.\n"
        "버스 및 지하철을 이용할 때의 소요 시간도 포함해 주세요.\n"
        "일정에는 방문지에 대한 간단한 설명이나 여행 팁도 포함해 주세요. 결과는 한국어로 작성해 주세요.\n"
        "참조한 검색 정보 출처 링크를 꼭 포함해 주세요.\n"
    ),
    agent=planner_agent,
    context=[research_task],
    expected_output="예산과 교통을 고려한 {days}일간의 여행 일정"
)

crew_multi_improved = Crew(
    agents=[research_agent, planner_agent],
    tasks=[research_task, improved_planning_task],
    process=Process.sequential,
    verbose=True
)

# 여행지와 예산 설정
inputs = {
    "place": "목표", "days": 2, "budget_per_day": 15
}

print("\n=== [협업 에이전트] 개선된 프롬프트로 일정 생성 ===")
result_multi_improved = crew_multi_improved.kickoff(inputs=inputs)
print("=== [협업 에이전트] 개선된 일정 결과 ===")
print(result_multi_improved)