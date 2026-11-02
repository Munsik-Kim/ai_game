# 🎮 AI Text Game - Living World Core

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128.0-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.53.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**AI 기반 동적 텍스트 RPG 게임 엔진**

NPC들이 AI를 통해 실시간으로 반응하며, 플레이어와의 상호작용에 따라 감정과 관계가 변화하는 생동감 넘치는 게임 세계를 경험하세요.

[🚀 빠른 시작](#-빠른-시작) • [📖 문서](#-문서) • [🎯 기능](#-주요-기능) • [🛠️ 설치](#-설치-및-설정)

</div>

---

## 📋 목차

- [프로젝트 소개](#-프로젝트-소개)
- [주요 기능](#-주요-기능)
- [기술 스택](#-기술-스택)
- [프로젝트 구조](#-프로젝트-구조)
- [빠른 시작](#-빠른-시작)
- [설치 및 설정](#-설치-및-설정)
- [사용 방법](#-사용-방법)
- [API 문서](#-api-문서)
- [아키텍처](#-아키텍처)
- [개발 가이드](#-개발-가이드)
- [문제 해결](#-문제-해결)
- [기여하기](#-기여하기)
- [라이선스](#-라이선스)

---

## 🎯 프로젝트 소개

**Living World Core**는 Google Gemini API를 활용한 AI 기반 텍스트 RPG 게임 엔진입니다. 

이 프로젝트의 핵심 아이디어는 **"State vs. Narrative Separation"**입니다:
- 🤖 **AI (LLM)**: NPC의 대사, 감정, 행동 지문 등 **내러티브** 생성
- 💻 **Python 로직**: 게임 상태(HP, 관계 점수, 인벤토리 등) **엄격한 관리**

현재 구현은 NPC 대화와 제한된 상태 갱신을 연결하는 프로토타입입니다. [게임 엔진](app/core/game_engine.py)은 감정·관계 점수와 최근 기억을 갱신하고, [API](app/api/endpoints.py)는 행동·상태 조회·초기화를 제공합니다.

**구현 범위와 남은 확장:** HP·인벤토리·시간·날씨 필드는 있지만, 일반 전투·퀘스트·아이템 거래·자동 세계 진행 로직이 완성된 것은 아닙니다. 상태는 프로세스 메모리에 있으며 사용자별 영속 저장도 별도 구현이 필요합니다. 이 구분은 코드 확인 결과이며 새 Gemini API 요청을 실행한 검증은 아닙니다.

### ✨ 특징

- 🧠 **AI 기반 NPC**: Google Gemini를 활용한 동적 NPC 반응
- 🎭 **감정 시스템**: NPC의 감정이 실시간으로 변화
- 💝 **관계 시스템**: 플레이어와의 관계 점수 추적 (-100 ~ 100)
- 📝 **대화 기록**: NPC의 단기 기억 시스템
- 🎨 **직관적 UI**: Streamlit 기반 웹 인터페이스
- 🔌 **RESTful API**: FastAPI 기반 확장 가능한 API

---

## 🚀 주요 기능

### 1. AI 기반 NPC 상호작용
- 플레이어의 행동에 따라 NPC가 동적으로 반응
- NPC의 성격, 배경, 현재 감정을 고려한 자연스러운 대화
- JSON 출력을 요청하고 파싱하며, 파싱·API 오류에는 기본 응답을 반환합니다. 모든 응답의 정확성을 보장하지 않습니다.

### 2. 게임 상태 관리
- **플레이어**: HP, MP, Gold, 인벤토리의 초기값과 상태 조회
- **NPC**: 같은 위치의 첫 NPC를 선택해 감정·관계 점수·최근 대화 기억 갱신
- **월드**: 시간·날씨·위치 초기값을 대화 문맥으로 제공

### 3. Streamlit 웹 UI
- 실시간 게임 상태 표시
- 대화형 인터페이스
- 대화 기록 관리
- 빠른 행동 버튼

### 4. RESTful API
- FastAPI 기반 확장 가능한 API
- Swagger UI 자동 문서화
- Pydantic 모델 기반 타입 검증

---

## 🛠️ 기술 스택

| 카테고리 | 기술 |
|---------|------|
| **언어** | Python 3.11+ |
| **웹 프레임워크** | FastAPI 0.128.0 |
| **UI 프레임워크** | Streamlit 1.53.0 |
| **AI 서비스** | Google Gemini API (gemini-2.5-flash) |
| **데이터 검증** | Pydantic V2 |
| **서버** | Uvicorn |
| **환경 변수** | python-dotenv |

---

## 📁 프로젝트 구조

```
AI_Text_Game/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 앱 진입점
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py        # API 엔드포인트 정의
│   ├── core/
│   │   ├── __init__.py
│   │   └── game_engine.py     # 게임 엔진 로직
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py         # Pydantic 모델 정의
│   └── services/
│       ├── __init__.py
│       └── ai_service.py      # Gemini API 서비스
├── streamlit_app.py            # Streamlit 웹 UI
├── requirements.txt            # 의존성 패키지
├── .env                        # 환경 변수 (gitignore)
├── .gitignore                  # Git 무시 파일
└── README.md                   # 프로젝트 문서
```

---

## 🚀 빠른 시작

### 1. 저장소 클론

```bash
git clone https://github.com/Munsik-Kim/ai_game.git
cd ai_game
```

### 2. 환경 설정

```bash
# Conda 환경 생성 및 활성화
conda create -n ai_game python=3.11
conda activate ai_game

# 의존성 설치
pip install -r requirements.txt
```

### 3. 환경 변수 설정

`.env` 파일을 생성하고 Google API 키를 설정하세요:

```bash
GOOGLE_API_KEY=your_google_api_key_here
```

> 🔑 Google API 키는 [Google AI Studio](https://makersuite.google.com/app/apikey)에서 발급받을 수 있습니다.

### 4. 서버 실행

**터미널 1 - FastAPI 서버:**
```bash
conda activate ai_game
python app/main.py
```

**터미널 2 - Streamlit UI:**
```bash
conda activate ai_game
python -m streamlit run streamlit_app.py
```

브라우저에서 http://localhost:8501 접속하여 게임을 시작하세요! 🎮

---

## 📖 설치 및 설정

### 필수 요구사항

- Python 3.11 이상
- Conda (권장) 또는 pip
- Google Gemini API 키

### 상세 설치 가이드

#### 방법 1: Conda 사용 (권장)

```bash
# 1. Conda 환경 생성
conda create -n ai_game python=3.11

# 2. 환경 활성화
conda activate ai_game

# 3. 의존성 설치
pip install -r requirements.txt
```

#### 방법 2: pip 사용

```bash
# 가상환경 생성 (선택사항)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 환경 변수 설정

프로젝트 루트에 `.env` 파일을 생성:

```bash
GOOGLE_API_KEY=your_actual_api_key_here
```

> ⚠️ `.env` 파일은 `.gitignore`에 포함되어 있어 Git에 커밋되지 않습니다.

---

## 🎮 사용 방법

### Streamlit UI 사용 (권장)

가장 쉬운 방법입니다. 브라우저에서 직관적인 인터페이스를 사용할 수 있습니다.

1. **FastAPI 서버 실행** (터미널 1)
   ```bash
   python app/main.py
   ```

2. **Streamlit 앱 실행** (터미널 2)
   ```bash
   python -m streamlit run streamlit_app.py
   ```

3. **브라우저에서 게임 플레이**
   - http://localhost:8501 접속
   - 행동을 입력하고 NPC와 대화 시작!

### API 직접 사용

FastAPI 서버만 실행하여 REST API로 게임을 제어할 수 있습니다:

```bash
python app/main.py
```

서버가 실행되면:
- **API 서버**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📚 API 문서

### 엔드포인트 목록

#### 1. 플레이어 행동 처리

**POST** `/api/action`

플레이어의 행동을 처리하고 NPC의 반응을 반환합니다.

**Request:**
```bash
curl -X POST "http://localhost:8000/api/action" \
  -H "Content-Type: application/json" \
  -d '{"action": "안녕하세요! 상점에 무엇이 있나요?"}'
```

**Response:**
```json
{
  "dialogue": "어서오세요! 오늘은 좋은 물건들이 많이 들어왔어요.",
  "action_description": "그레고르가 미소를 지으며 손을 흔든다.",
  "npc_name": "그레고르",
  "updated_emotion": "happy",
  "updated_relationship_score": 2
}
```

#### 2. 게임 상태 조회

**GET** `/api/state`

현재 게임 상태를 반환합니다.

```bash
curl -X GET "http://localhost:8000/api/state"
```

**Response:**
```json
{
  "player": {
    "profile": {
      "name": "모험가",
      "job": "모험가",
      "traits": ["용감함", "호기심", "친절함"],
      "lore": "평범한 마을에서 시작한 모험가..."
    },
    "stats": {
      "hp": 100,
      "mp": 50,
      "gold": 100,
      "location_id": "marketplace"
    },
    "inventory": ["낡은 검", "가죽 갑옷", "빵 3개"]
  },
  "world_state": {
    "time_of_day": "오후",
    "weather": "맑음",
    "npcs": [...]
  }
}
```

#### 3. 게임 리셋

**POST** `/api/reset`

게임 상태를 초기화합니다.

```bash
curl -X POST "http://localhost:8000/api/reset"
```

### 전체 플로우 예제

```bash
# 1. 게임 상태 확인
curl -X GET "http://localhost:8000/api/state"

# 2. 플레이어 행동 실행
curl -X POST "http://localhost:8000/api/action" \
  -H "Content-Type: application/json" \
  -d '{"action": "안녕하세요!"}'

# 3. 상태 변화 확인
curl -X GET "http://localhost:8000/api/state"

# 4. 게임 리셋
curl -X POST "http://localhost:8000/api/reset"
```

---

## 🏗️ 아키텍처

### 핵심 설계 원칙

#### 1. State vs. Narrative Separation

```
플레이어 행동
    ↓
현재 NPC·월드 상태를 프롬프트로 구성
    ↓
Gemini 요청 1회 (대사·감정·관계 변화 JSON)
    ↓
Python 로직 (감정·관계 점수·최근 기억 업데이트)
    ↓
응답 반환
```

**핵심**: LLM은 게임 상태를 직접 변경하지 않고, JSON 형식의 "제안"만 반환합니다.

#### 2. Structured Output

AI 서비스는 JSON을 파싱하고 관계 변화량을 -5~5로 제한합니다. Pydantic은 상태와 API 요청·응답의 형식을 정의합니다. 모든 LLM 필드를 별도의 Pydantic 모델로 검증하는 경로는 아닙니다:

```python
{
  "dialogue": str,              # NPC 대사
  "emotion_change": str,        # 감정 변화
  "relationship_change": int,   # 관계 변화 (-5 ~ 5)
  "action_description": str     # 행동 지문
}
```

#### 3. Type Safety

모든 함수에 타입 힌트를 적용하여 안정성을 확보합니다.

### 데이터 흐름

```
┌─────────────┐
│  Streamlit  │  ← 사용자 인터페이스
└──────┬──────┘
       │ HTTP
       ↓
┌─────────────┐
│   FastAPI   │  ← REST API 서버
└──────┬──────┘
       │
       ↓
┌─────────────┐
│ GameEngine  │  ← 게임 상태 관리
└──────┬──────┘
       │
       ↓
┌─────────────┐
│GeminiService│  ← AI 서비스
└──────┬──────┘
       │
       ↓
┌─────────────┐
│ Gemini API  │  ← Google Gemini
└─────────────┘
```

---

## 💻 개발 가이드

### 코드 구조

| 파일 | 설명 |
|------|------|
| `app/models/schemas.py` | Pydantic 모델 정의 (CharacterProfile, NPC, Player, WorldState) |
| `app/services/ai_service.py` | Google Gemini API 래퍼 클래스 |
| `app/core/game_engine.py` | 게임 상태 관리 및 AI 서비스 호출 |
| `app/api/endpoints.py` | FastAPI 엔드포인트 정의 |
| `streamlit_app.py` | Streamlit 웹 UI |

### 개발 환경 설정

```bash
# 1. 저장소 클론
git clone https://github.com/Munsik-Kim/ai_game.git
cd ai_game

# 2. Conda 환경 생성
conda create -n ai_game python=3.11
conda activate ai_game

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 개발 모드로 서버 실행 (자동 재시작)
uvicorn app.main:app --reload
```

### 코드 스타일

- **타입 힌트**: 모든 함수에 타입 힌트 필수
- **문서화**: 모든 클래스와 함수에 docstring 작성
- **에러 처리**: try-except로 AI 호출 실패 시 기본값 반환

---

## 🐛 문제 해결

### 일반적인 문제

#### 1. `GOOGLE_API_KEY` 오류

**증상**: `ValueError: GOOGLE_API_KEY가 설정되지 않았습니다`

**해결**:
- `.env` 파일이 프로젝트 루트에 있는지 확인
- API 키가 올바르게 설정되었는지 확인
- `.env` 파일 형식: `GOOGLE_API_KEY=your_key_here` (공백 없음)

#### 2. Python 버전 오류

**증상**: `ModuleNotFoundError` 또는 패키지 설치 실패

**해결**:
```bash
# Python 버전 확인
python --version  # 3.11 이상이어야 함

# Conda 환경 확인
conda activate ai_game
which python  # conda 환경의 python을 사용하는지 확인
```

#### 3. Streamlit 버전 오류

**증상**: `AttributeError: module 'streamlit' has no attribute 'rerun'`

**해결**:
```bash
# 올바른 방법으로 실행
python -m streamlit run streamlit_app.py

# 또는 conda 환경의 streamlit 직접 사용
conda activate ai_game
/Users/munsikkim/opt/anaconda3/envs/ai_game/bin/streamlit run streamlit_app.py
```

#### 4. 포트 충돌

**증상**: `Address already in use`

**해결**:
```bash
# 다른 포트 사용
uvicorn app.main:app --port 8001
streamlit run streamlit_app.py --server.port 8502
```

#### 5. API 서버 연결 실패

**증상**: Streamlit에서 "API 서버에 연결할 수 없습니다"

**해결**:
- FastAPI 서버가 실행 중인지 확인
- `streamlit_app.py`의 `API_BASE_URL`이 올바른지 확인
- 방화벽 설정 확인

---

## 🤝 기여하기

기여를 환영합니다! 다음 단계를 따라주세요:

1. **Fork** 저장소
2. **Feature 브랜치** 생성 (`git checkout -b feature/AmazingFeature`)
3. **변경사항 커밋** (`git commit -m 'Add some AmazingFeature'`)
4. **브랜치에 Push** (`git push origin feature/AmazingFeature`)
5. **Pull Request** 생성

### 기여 가이드라인

- 코드 스타일을 유지해주세요
- 새로운 기능은 테스트를 포함해주세요
- 문서를 업데이트해주세요
- 커밋 메시지는 명확하게 작성해주세요

---

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

---

## 🙏 감사의 말

- [Google Gemini API](https://ai.google.dev/) - AI 서비스 제공
- [FastAPI](https://fastapi.tiangolo.com/) - 웹 프레임워크
- [Streamlit](https://streamlit.io/) - 웹 UI 프레임워크

---

## 📞 문의

문제가 발생하거나 제안사항이 있으시면 [Issues](https://github.com/Munsik-Kim/ai_game/issues)에 등록해주세요.

---

<div align="center">

**⭐ 이 프로젝트가 도움이 되었다면 Star를 눌러주세요! ⭐**

Made with ❤️ by [Your Name]

</div>
