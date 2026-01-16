import streamlit as st
import requests
from typing import Dict, Any, Optional
import json
from datetime import datetime

# Streamlit 버전 호환성 처리
def safe_rerun():
    """Streamlit 버전에 따라 적절한 rerun 함수 사용"""
    if hasattr(st, 'rerun'):
        st.rerun()  # Streamlit >= 1.18.0
    elif hasattr(st, 'experimental_rerun'):
        st.experimental_rerun()  # Streamlit < 1.18.0
    else:
        # 최후의 수단: 페이지 새로고침
        st.experimental_rerun()

# 페이지 설정 (반드시 최상단)
st.set_page_config(
    page_title="AI Text Game",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API 서버 URL
API_BASE_URL = "http://localhost:8000/api"

# 세션 상태 초기화
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "game_state" not in st.session_state:
    st.session_state.game_state = None
if "last_update" not in st.session_state:
    st.session_state.last_update = None
if "selected_action" not in st.session_state:
    st.session_state.selected_action = ""


def get_game_state() -> Optional[Dict[str, Any]]:
    """게임 상태를 API에서 가져옵니다."""
    try:
        response = requests.get(f"{API_BASE_URL}/state", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"상태 조회 실패: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"API 서버에 연결할 수 없습니다: {e}")
        st.info("FastAPI 서버가 실행 중인지 확인하세요: `python app/main.py`")
        return None


def send_action(action: str) -> Optional[Dict[str, Any]]:
    """플레이어 행동을 API로 전송합니다."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/action",
            json={"action": action},
            timeout=30  # AI 응답을 기다리므로 타임아웃을 길게 설정
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"행동 처리 실패: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"API 서버에 연결할 수 없습니다: {e}")
        return None


def reset_game() -> bool:
    """게임을 리셋합니다."""
    try:
        response = requests.post(f"{API_BASE_URL}/reset", timeout=5)
        if response.status_code == 200:
            return True
        else:
            st.error(f"리셋 실패: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        st.error(f"API 서버에 연결할 수 없습니다: {e}")
        return False


def get_emotion_emoji(emotion: str) -> str:
    """감정에 따른 이모지 반환"""
    emotion_map = {
        "happy": "😊",
        "sad": "😢",
        "angry": "😠",
        "surprised": "😲",
        "neutral": "😐",
        "fearful": "😨",
        "disgusted": "🤢",
    }
    return emotion_map.get(emotion.lower(), "😐")


def get_relationship_color(score: int) -> str:
    """관계 점수에 따른 색상 반환"""
    if score >= 50:
        return "🟢"  # 매우 좋음
    elif score >= 20:
        return "🟡"  # 좋음
    elif score >= -20:
        return "⚪"  # 중립
    elif score >= -50:
        return "🟠"  # 나쁨
    else:
        return "🔴"  # 매우 나쁨


# 콜백 함수들
def refresh_state():
    """게임 상태를 새로고침합니다."""
    st.session_state.game_state = get_game_state()
    st.session_state.last_update = datetime.now()


def handle_reset():
    """게임을 리셋합니다."""
    if reset_game():
        st.session_state.conversation_history = []
        st.session_state.game_state = get_game_state()
        st.session_state.last_update = datetime.now()
        st.success("게임이 리셋되었습니다!")
        safe_rerun()


def clear_conversation():
    """대화 기록을 지웁니다."""
    st.session_state.conversation_history = []
    safe_rerun()


def handle_quick_action(action: str):
    """빠른 행동 버튼 클릭 처리"""
    st.session_state.selected_action = action
    safe_rerun()


def handle_send_action():
    """행동 전송 처리"""
    action_input = st.session_state.get("action_input", "")
    if not action_input:
        st.warning("행동을 입력해주세요.")
        return
    
    with st.spinner("NPC가 반응을 생성하는 중..."):
        # 플레이어 행동 기록
        st.session_state.conversation_history.append({
            "type": "player",
            "content": action_input,
            "timestamp": datetime.now().isoformat()
        })
        
        # API 호출
        response = send_action(action_input)
        
        if response:
            # NPC 응답 기록
            st.session_state.conversation_history.append({
                "type": "npc",
                "npc_name": response.get("npc_name", "NPC"),
                "dialogue": response.get("dialogue", ""),
                "action_description": response.get("action_description", ""),
                "emotion": response.get("updated_emotion", "neutral"),
                "relationship": response.get("updated_relationship_score", 0),
                "timestamp": datetime.now().isoformat()
            })
            
            # 게임 상태 새로고침
            st.session_state.game_state = get_game_state()
            st.session_state.last_update = datetime.now()
            
            # 입력 필드 초기화
            st.session_state.action_input = ""
            st.session_state.selected_action = ""
            
            st.success("행동이 처리되었습니다!")
            safe_rerun()
        else:
            st.error("행동 처리에 실패했습니다.")


def retry_get_state():
    """게임 상태 다시 시도"""
    st.session_state.game_state = get_game_state()
    safe_rerun()


# 메인 타이틀
st.title("🎮 AI Text Game - Living World Core")
st.markdown("---")

# 사이드바
with st.sidebar:
    st.header("⚙️ 게임 설정")
    
    # API 서버 상태 확인
    st.button("🔄 상태 새로고침", on_click=refresh_state, use_container_width=True)
    
    # 게임 리셋 버튼
    st.button("🔄 게임 리셋", on_click=handle_reset, type="primary", use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 📖 사용 방법")
    st.markdown("""
    1. FastAPI 서버 실행:
       ```bash
       python app/main.py
       ```
    2. 행동을 입력하고 전송
    3. NPC의 반응을 확인
    4. 관계와 감정 변화 관찰
    """)
    
    st.markdown("---")
    st.markdown("### 🔗 API 문서")
    st.markdown("[Swagger UI](http://localhost:8000/docs)")

# 게임 상태 표시
if st.session_state.game_state is None:
    st.session_state.game_state = get_game_state()

if st.session_state.game_state:
    game_state = st.session_state.game_state
    player = game_state.get("player", {})
    world_state = game_state.get("world_state", {})
    
    # 상단 정보 표시
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 👤 플레이어")
        player_profile = player.get("profile", {})
        player_stats = player.get("stats", {})
        st.markdown(f"**이름**: {player_profile.get('name', 'N/A')}")
        st.markdown(f"**직업**: {player_profile.get('job', 'N/A')}")
        st.markdown(f"**HP**: {player_stats.get('hp', 0)}")
        st.markdown(f"**MP**: {player_stats.get('mp', 0)}")
        st.markdown(f"**Gold**: {player_stats.get('gold', 0)} 💰")
    
    with col2:
        st.markdown("### 🌍 월드 상태")
        st.markdown(f"**시간**: {world_state.get('time_of_day', 'N/A')}")
        st.markdown(f"**날씨**: {world_state.get('weather', 'N/A')}")
        st.markdown(f"**위치**: {player_stats.get('location_id', 'N/A')}")
    
    with col3:
        st.markdown("### 📦 인벤토리")
        inventory = player.get("inventory", [])
        if inventory:
            for item in inventory:
                st.markdown(f"- {item}")
        else:
            st.markdown("*비어있음*")
    
    st.markdown("---")
    
    # NPC 정보 표시
    npcs = world_state.get("npcs", [])
    if npcs:
        st.markdown("### 👥 NPC 정보")
        npc_cols = st.columns(len(npcs))
        
        for idx, npc in enumerate(npcs):
            with npc_cols[idx]:
                npc_profile = npc.get("profile", {})
                npc_stats = npc.get("stats", {})
                emotion = npc.get("current_emotion", "neutral")
                relationship = npc.get("relationship_score", 0)
                
                st.markdown(f"#### {npc_profile.get('name', 'N/A')} {get_emotion_emoji(emotion)}")
                st.markdown(f"**직업**: {npc_profile.get('job', 'N/A')}")
                st.markdown(f"**감정**: {emotion}")
                st.markdown(f"**관계**: {get_relationship_color(relationship)} {relationship}")
                
                traits = npc_profile.get("traits", [])
                if traits:
                    st.markdown(f"**성격**: {', '.join(traits)}")
    
    st.markdown("---")
    
    # 대화 영역
    st.markdown("### 💬 대화")
    
    # 대화 기록 표시
    if st.session_state.conversation_history:
        chat_container = st.container()
        with chat_container:
            for entry in st.session_state.conversation_history:
                if entry["type"] == "player":
                    st.markdown(f"**👤 플레이어**: {entry['content']}")
                elif entry["type"] == "npc":
                    st.markdown(f"**{entry.get('npc_name', 'NPC')} {get_emotion_emoji(entry.get('emotion', 'neutral'))}**: {entry['dialogue']}")
                    if entry.get("action_description"):
                        st.caption(f"*{entry['action_description']}*")
                st.markdown("---")
    else:
        st.info("대화 기록이 없습니다. 행동을 입력하여 NPC와 대화를 시작하세요.")
    
    st.markdown("---")
    
    # 행동 입력
    st.markdown("### 🎯 행동 입력")
    
    # 빠른 행동 버튼
    st.markdown("**빠른 행동:**")
    quick_actions = [
        "안녕하세요!",
        "상점에 무엇이 있나요?",
        "물건을 구매하고 싶습니다",
        "고마워요!",
        "잘 가요!"
    ]
    
    quick_cols = st.columns(len(quick_actions))
    
    # 선택된 행동이 있으면 텍스트 입력에 반영
    default_value = st.session_state.selected_action if st.session_state.selected_action else ""
    
    # 빠른 행동 버튼
    for idx, action in enumerate(quick_actions):
        with quick_cols[idx]:
            st.button(
                action,
                key=f"quick_{idx}",
                on_click=handle_quick_action,
                args=(action,),
                use_container_width=True
            )
    
    # 텍스트 입력
    action_input = st.text_input(
        "행동을 입력하세요:",
        value=default_value,
        key="action_input",
        placeholder="예: 안녕하세요! 상점에 무엇이 있나요?"
    )
    
    # 선택된 행동 사용 후 초기화
    if st.session_state.selected_action and action_input == st.session_state.selected_action:
        st.session_state.selected_action = ""
    
    col_send, col_clear = st.columns([1, 1])
    
    with col_send:
        st.button("📤 전송", on_click=handle_send_action, type="primary", use_container_width=True)
    
    with col_clear:
        st.button("🗑️ 대화 기록 지우기", on_click=clear_conversation, use_container_width=True)
    
    # 하단 정보
    if st.session_state.last_update:
        st.caption(f"마지막 업데이트: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}")
    
else:
    st.warning("⚠️ 게임 상태를 불러올 수 없습니다.")
    st.info("FastAPI 서버가 실행 중인지 확인하세요.")
    
    st.button("🔄 다시 시도", on_click=retry_get_state, use_container_width=True)

# 푸터
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "AI Text Game - Living World Core | Powered by Google Gemini API"
    "</div>",
    unsafe_allow_html=True
)
