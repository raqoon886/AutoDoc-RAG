import sys
from langchain_ollama import OllamaLLM

def test_ollama_connection():
    print("--- Ollama Connection Test ---")
    
    # 1. 모델 초기화 (Llama 3.1 사용)
    # 로컬에서 실행 중이므로 base_url은 기본값(http://localhost:11434)을 사용합니다.
    try:
        llm = OllamaLLM(model="llama3.1:8b")
        
        print(f"[1/3] 모델 'llama3.1' 로드 시도 중...")
        
        # 2. 간단한 질문 던지기
        question = "Hello! Tell me one short sentence about why M3 Pro is good for AI."
        print(f"[2/3] 질문 던지는 중: {question}")
        
        response = llm.invoke(question)
        
        # 3. 결과 출력
        print(f"[3/3] Ollama 답변 수신 완료!")
        print("-" * 30)
        print(f"답변: {response}")
        print("-" * 30)
        print("\n✅ 통신 성공! 이제 RAG 개발을 시작해도 좋습니다.")

    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")
        print("\n[체크리스트]")
        print("1. Ollama 앱이 실행 중인가요? (메뉴 바 아이콘 확인)")
        print("2. 터미널에서 'ollama pull llama3.1'을 실행해 모델을 내려받았나요?")
        print("3. uv 환경이 활성화(source .venv/bin/activate) 되었나요?")

if __name__ == "__main__":
    test_ollama_connection()