# 필요한 라이브러리 임포트
from crewai import Agent, Task, Crew, Process  # CrewAI 핵심 클래스들
from dotenv import load_dotenv
import os

# 0. 환경 변수 로드 (.env에서 OPENAI_API_KEY 불러오기)
load_dotenv()  # .env 파일에 정의된 환경변수를 로드합니다.
# OPENAI_API_KEY가 환경변수로 설정되었다면, openai 패키지가 이를 자동으로 사용합니다.

# 1. Agent 생성(LLM 모델): role, goal, backstory 설정
agent = Agent(
    role="AI 어시스턴트",            # 에이전트의 역할
    goal="사용자에게 간단한 환영 인사를 제공",  # 에이전트가 달성할 목표
    backstory="당신은 친절한 AI 비서로, 언제나 정중하고 도움이 되는 인사를 건넵니다."  # 에이전트의 성격/배경
)

# 2. Task 생성(User): description, expected_output, agent 지정
task = Task(
    description="사용자에게 환영 인사 한 마디를 작성하세요.",   # 에이전트가 수행할 작업 내용
    expected_output="한 줄의 따뜻한 환영 메시지",            # 기대하는 출력 결과물 (Output Indictor)
    agent=agent                                    # 이 태스크를 수행할 에이전트
)

# 3. Crew 생성: 에이전트와 태스크를 크루로 구성 (순차 프로세스 설정)
crew = Crew(
    agents=[agent],               # 크루에 속한 에이전트 목록 (여기서는 1개)
    tasks=[task],                 # 크루가 수행할 태스크 목록 (여기서는 1개)
    process=Process.sequential,   # 순차적 진행 방식으로 태스크 실행
    verbose=True                  # 실행 중 상세한 로그 출력 여부
)

# 4. Crew 실행: kickoff() 메서드로 태스크 수행 시작
result = crew.kickoff()

# 5. 실행 결과 출력
print("최종 결과:", result)