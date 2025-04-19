# MultiAgents_with_CrewAIs
AI Multi Agents to develop Service with_CrewAIs

## 코드 구조 및 실행 방법

### 환경 설정
- `/codes/01_env_config`: 개발 환경 설정 및 API 키 관리
  - OpenAI API 키를 `.env` 파일에 설정하여 사용
  - 실행: `python 01_env_config_test.py`

### CrewAI 기본 사용법
- `/codes/n02_crewais`: CrewAI의 기본 개념과 간단한 실행 예제
  - `n01_hellow_crewais.py`: Agent, Task, Crew의 기본 사용법
  - `n02_crewais_with_topic.py`: 주제 기반 CrewAI 사용
  - `n03_researcher_writer.py`: 연구자와 작가 역할의 에이전트 협업
  - 실행: `python n02_crewais/n01_hellow_crewais.py`

### 다중 에이전트 작업
- `/codes/n03_crewai_with_agents`: 여러 에이전트의 협업 작업
  - 여행 계획 작성 예제: 입력값 활용, 도구 사용, 프롬프트 개선 단계별 구현
  - 실행: `python n03_crewai_with_agents/n01.travel_planner_wih_inputs.py`

### 다양한 도구 통합
- `/codes/n04_crewai_with_multi_tools`: 외부 도구를 활용한 CrewAI
  - 뉴스 수집, 레시피 작성, 여행 계획 등 다양한 시나리오 구현
  - 실행: `python n04_crewai_with_multi_tools/n01_crewai_for_tools.py`

### 프로세스 실행 방식
- `/codes/n05_crewai_with_anyprocesses`: 다양한 실행 방식 구현
  - 순차적 실행(Sequential) 및 계층적 실행(Hierarchical) 방식 비교
  - 실행: `python n05_crewai_with_anyprocesses/n02_process_with_sequential.py`
