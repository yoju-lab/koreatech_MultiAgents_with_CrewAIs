from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from n01_crewai_for_tools import WebScraperTool, CalculatorTool, MyCustomDuckDuckGoTool

load_dotenv()  # .env 파일에서 API 키 등 환경변수 로드

# 도구 인스턴스 생성
search_tool = MyCustomDuckDuckGoTool()
scrape_tool = WebScraperTool()
calculator_tool = CalculatorTool()

# 뉴스 분석 Agent 정의
news_agent = Agent(
    role="뉴스 분석가",
    goal="최신 여행 관련 뉴스를 검색하고 요약 제공",
    backstory="뉴스 분석 전문 AI 기자",
    tools=[search_tool, scrape_tool],      # 웹 검색 및 스크래핑 도구 사용
    llm="gpt-4o-mini",
    verbose=True
)

# 여행 계획 Agent 정의
travel_agent = Agent(
    role="여행 전문가",
    goal="뉴스 내용을 바탕으로 현실적이고 매력적인 여행 일정 구성",
    backstory="다년간의 여행 플래너 경험 보유",
    tools=[search_tool, scrape_tool, calculator_tool],  # 필요한 경우 계산기 도구도 사용
    llm="gpt-4o-mini",
    verbose=True
)

# 요리 추천 Agent 정의
recipe_agent = Agent(
    role="요리 전문가",
    goal="여행지에서 즐길 수 있는 적절한 현지 요리 레시피 추천",
    backstory="글로벌 요리 전문가 AI 셰프",
    tools=[search_tool, scrape_tool],      # 웹 검색 및 스크래핑 도구 사용
    llm="gpt-4o-mini",
    verbose=True
)

# Task 정의: 각 에이전트에게 할 일 할당
news_task = Task(
    description="최근 일주일 내 국내 여행과 관련된 중요한 뉴스 1건을 한국어로 요약해줘.",
    expected_output="한국어로 작성된 여행 관련 뉴스 1건의 제목, 요약, 링크",
    agent=news_agent
)

travel_task = Task(
    description="위에서 제공된 최신 여행 뉴스를 참고하여 3일 동안의 여행 일정을 한국어로 작성해줘.",
    expected_output="한국어로 작성된 상세한 3일 여행 일정",
    agent=travel_agent
)

recipe_task = Task(
    description="여행 일정에 포함된 지역에서 추천할 만한 현지 음식 레시피 1개를 한국어로 제공해줘.",
    expected_output="한국어로 작성된 현지 음식 이름, 재료 목록, 상세한 조리법",
    agent=recipe_agent
)

# Crew 생성 및 실행 (순차적 프로세스 지정)
crew = Crew(
    # agents=[news_agent, travel_agent, recipe_agent],
    agents=[travel_agent, news_agent, recipe_agent],
    # tasks=[news_task, travel_task, recipe_task],
    tasks=[travel_task, recipe_task, news_task, ],
    process=Process.sequential,  # 순차적으로 Task들을 처리
    verbose=True
)

def run_sequential_scenario():
    result = crew.kickoff()  # 순차적 프로세스 시작
    print("[순차적 시나리오 최종 결과]\n", result)

if __name__ == "__main__":
    run_sequential_scenario()