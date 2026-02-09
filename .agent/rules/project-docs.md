---
trigger: always_on
---

# 프로젝트 요약: AutoDoc-RAG (Middleware AI Assistant)

## 1. 프로젝트 개요
- **목적**: 미들웨어 설계서 및 소스 코드를 학습(RAG)하여 API 문서를 자동 생성하고 질의응답을 제공하는 에이전트 개발.
- **기간**: 3일 (단기 집중 스프린트)
- **대상 데이터**: `docs/` 내 미들웨어 설계서(.md, .pdf) 및 소스 코드.

## 2. 기술 스택 및 환경 (Tech Stack)
- **Hardware**: Mac M3 Pro
- **Language**: Python 3.12 (uv를 이용한 환경 관리)
- **Framework**: LangChain (langchain-ollama, langchain-community)
- **Local LLM**: Ollama (Model: `llama3.1:8b`)
- **Embedding**: `nomic-embed-text` (Ollama 기반)
- **Vector DB**: ChromaDB (로컬 유지형)
- **IDE/Tools**: Google Antigravity (Agent-first IDE), VS Code/Cursor, GitHub CLI (gh)

## 3. 현재 진행 상황 (Day 1 완료)
- [x] **환경 세팅**: `uv`를 통한 Python 3.12 가상환경 구축 및 패키지 설치.
- [x] **연결 테스트**: `test_connection.py`를 통해 LangChain-Ollama(Llama 3.1) 통신 확인 완료.
- [x] **버전 관리**: GitHub 원격 저장소(`raqoon886/AutoDoc-RAG`) 연결 및 첫 커밋 완료.

## 4. 프로젝트 구조
AutoDoc-RAG/
├── .venv/            # uv 가상환경
├── data/
│   └── vector_db/    # ChromaDB 데이터 저장소
├── docs/             # 미들웨어 설계서 및 코드 저장소
├── src/
│   └── test_connection.py  # Ollama 통신 테스트
├── .gitignore
├── pyproject.toml / requirements.txt
└── README.md