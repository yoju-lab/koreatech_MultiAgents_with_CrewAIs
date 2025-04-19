from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from crewai import Agent, Task, Crew, Process

# .env 파일 로드하여 OPENAI_API_KEY 등 환경변수 설정
load_dotenv()

# LLM 초기화 (OpenAI GPT-4o-mini 모델 사용)
openai_model = os.getenv('OPENAI_MODEL')
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# 여행 기획자 에이전트 정의
travel_agent = Agent(
    role="여행 기획자",
    goal="사용자의 요청에 따라 {place} 여행 일정을 계획하고 제안합니다.",
    backstory="여행사에서 10년 경력의 전문 여행 플래너로, 다양한 국내 여행 코스를 알고 있습니다.",
    llm=llm,
    verbose=True
)

# {place} 3일 여행 일정 작성 Task 정의
# itinerary_task = Task(
#     description=(
#         "{place}에서 3일간 여행 일정을 계획해 주세요.\n"
#         "여행 일정에는 부산의 주요 관광지와 현지 맛집 추천을 포함하고, 교통 수단 정보나 팁이 있으면 함께 제공하세요."
#     ),
#     agent=travel_agent,
#     expected_output="Day 1, Day 2, Day 3으로 구분된 상세 일정 제안"
# )

itinerary_task = Task(
    description=(
        "{place}에서 {days}일간 여행 일정을 계획해 주세요.\n"
        "{days}일별로 나누고, 1일차, 2일차와 같이 나누어 각 일별마다 아침/점심/저녁에 할 활동을 상세히 제안하세요.\n"
        "여행 일정에는 부산의 주요 관광지와 현지 맛집 추천을 포함하고, 교통 수단 정보나 팁이 있으면 함께 제공하세요."
    ),
    agent=travel_agent,
    expected_output="Day 1, Day 2, Day 3와 같이 구분된 상세 일정 제안"
)
# Crew 생성 및 실행 (순차 실행 - Task가 하나뿐이므로 순차 처리)
crew_single = Crew(
    agents=[travel_agent],
    tasks=[itinerary_task],
    process=Process.sequential,
    verbose=True
)
print("=== [단일 에이전트] 부산 3일 일정 생성 시작 ===")
inputs = {
    'place' : "부산",
    'days' : "5"
}
result_single = crew_single.kickoff(inputs=inputs)
print("=== [단일 에이전트] 생성된 부산 3일 일정 ===")
print(result_single)