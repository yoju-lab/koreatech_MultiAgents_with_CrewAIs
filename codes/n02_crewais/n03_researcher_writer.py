# 필요한 라이브러리 임포트
from crewai import Agent, Task, Crew, Process  # CrewAI 핵심 클래스들
from dotenv import load_dotenv
import os

# 0. 환경 변수 로드 (.env에서 OPENAI_API_KEY 불러오기)
load_dotenv()  # .env 파일에 정의된 환경변수를 로드합니다.
# OPENAI_API_KEY가 환경변수로 설정되었다면, openai 패키지가 이를 자동으로 사용합니다.

# 2. 에이전트 정의 (연구원, 작가)
researcher = Agent(
    role="AI Researcher",
    goal="멀티 에이전트 시스템의 주요 장점을 3가지 조사하여 설명합니다.",
    backstory="다년간 AI 트렌드를 연구해온 전문가입니다."
)
writer = Agent(
    role="Technical Writer",
    goal="연구 결과를 바탕으로 간략한 결론을 작성합니다.",
    backstory="복잡한 정보를 쉽게 요약하는 작문 전문가입니다."
)

# 3. 태스크 정의 (조사 태스크, 작성 태스크)
research_task = Task(
    description="멀티 에이전트 시스템의 주요 장점 3가지를 조사하고 각 장점을 간략히 설명하세요.",
    expected_output="3가지 장점에 대한 간단한 설명 (bullet point 목록)",    # 3가지 까지 반복
    agent=researcher
)
write_task = Task(
    description="위 조사 결과를 참고하여, 멀티 에이전트 시스템의 장점에 대한 짧은 결론을 작성하세요.",
    expected_output="3~4문장으로 구성된 결론 단락",     # 확실한 표현 권장 ex.4문장으로 구성된 결론 단락
    agent=writer,
    context=[research_task]  # 이전 태스크의 결과를 활용
)

# 4. 크루 생성 (순차적 프로세스 설정)
crew = Crew(
    # agents=[researcher, writer],
    agents=[writer, researcher],
    tasks=[research_task, write_task],      # 일 순서가 중요
    process=Process.sequential,
    verbose=True
)

# 5. 크루 실행 및 결과 출력
crew_output = crew.kickoff()

# 6. 각 태스크의 결과를 순차적으로 출력
for idx, task_output in enumerate(crew_output.tasks_output, start=1):
    print(f"\n[Task {idx} Output]\n{task_output}\n")