# AutoDoc-RAG: Middleware AI Assistant

## 1. 프로젝트 개요 (Project Goal)
**미들웨어 설계서 및 소스 코드를 학습(RAG)하여 API 문서를 자동 생성하고 평가하는 에이전트 시스템**입니다.
단순 코딩 어시스턴트를 넘어, **"공식 문서(Official Docs) 수준"**의 고품질 API 문서를 생성하는 것을 목표로 합니다.

### 핵심 기능
- **RAG 기반 문서 생성**: VectorDB(Chroma)를 활용해 관련 설계서, 스타일 가이드, 아키텍처 문서를 참조하여 문서 생성.
- **다국어 지원**: C, C++, Rust, Go, Python 등 다양한 언어의 소스 코드 분석 지원.
- **자동 평가 시스템 (Dual Evaluation)**:
  - **LLM-as-a-Judge**: 생성된 문서의 정확성, 완결성, 구조 등을 LLM이 10점 만점으로 평가.
  - **BLEU Score**: 공식 문서(Ground Truth)와의 문장 유사도를 정량적으로 측정.

---

## 2. 수집 데이터 (Dataset & Ground Truth)
다양한 언어의 대표적인 오픈소스 프로젝트를 수집하여 **Ground Truth(정답)** 데이터셋을 구축했습니다.

| 언어 | 프로젝트 | 설명 | Ground Truth 출처 |
|---|---|---|---|
| **Python** | **Requests** | HTTP 요청 라이브러리 | Official Docs (readthedocs.io) |
| **C** | **SQLite** | 경량 데이터베이스 | Doxygen generated |
| **C** | **NetworkManager** | 네트워크 설정 데몬 | Official D-Bus API Docs |
| **C++** | **nlohmann/json** | Modern C++ JSON | Doxygen generated |
| **Rust** | **Tokio** | 비동기 런타임 | `cargo doc` output |
| **Go** | **Gin** | 웹 프레임워크 | `gomarkdoc` output |

---

## 3. 실행 방법 (Usage)

### 3.1 환경 설정
```bash
# 가상환경 생성 및 패키지 설치
uv pip install -r requirements.txt
source .venv/bin/activate

# 테스트 데이터 셋업 (리포지토리 클론 및 Ground Truth 생성)
./setup_test_data.sh
```

### 3.2 데이터 수집 (Ingestion)
VectorDB에 문서와 코드를 학습시킵니다.
```bash
# 예: Python 공식 문서 학습
python src/ingest_data.py --source ground_truth/python/
```

### 3.3 문서 생성 (Generation)
소스 코드를 입력받아 API 문서를 생성합니다 (No-RAG vs RAG).
```bash
# No-RAG 모드 (단순 LLM 생성)
python src/generate_docs.py target_file.py --mode no-rag

# RAG 모드 (VectorDB 참조 생성)
python src/generate_docs.py target_file.py --mode rag
```

### 3.4 평가 (Evaluation)
생성된 문서를 Ground Truth와 비교 평가합니다.
```bash
# LLM-as-a-Judge 평가 (정성 평가)
python src/evaluate_docs.py target_file.py

# BLEU Score 평가 (정량 평가)
python src/bleu_eval.py ground_truth_doc.md --no-rag output/no-rag/doc.md --rag output/rag/doc.md
```

---

## 4. 벤치마크 결과 (Benchmark Results)

본 프로젝트는 **BLEU-4 Score** 기준, RAG 모드가 No-RAG 대비 압도적인 성능 향상을 보였습니다.

| 언어 | 대상 파일 | No-RAG | RAG | 성능 향상 |
|---|---|---|---|---|
| **Python** | `requests/api.py` | 1.23% | **23.94%** | **19.5배** 🚀 |
| **C** | `nm-dbus-manager.c` | 0.20% | **0.93%** | **4.7배** 🚀 |

> **Conclusion**: RAG 모드는 공식 문서의 구조와 용어를 정확하게 반영하여, 사람이 작성한 것과 가장 유사한 품질의 문서를 생성합니다.
