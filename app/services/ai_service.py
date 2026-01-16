import os
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import google.generativeai as genai

# .env 파일에서 환경 변수 로드
load_dotenv()


class GeminiService:
    """Google Gemini API를 사용하는 AI 서비스 클래스"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        GeminiService 초기화
        
        Args:
            api_key: Google API 키. None이면 환경 변수에서 로드
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # 시스템 프롬프트
        self.system_prompt = "너는 생동감 넘치는 판타지 세계의 NPC 연기자다."
    
    def generate_npc_reaction(
        self,
        player_action: str,
        npc_data: Dict[str, Any],
        world_context: str
    ) -> Dict[str, Any]:
        """
        플레이어의 행동에 대한 NPC의 반응을 생성합니다.
        
        Args:
            player_action: 플레이어의 행동 설명
            npc_data: NPC 데이터 (dict)
            world_context: 세계 맥락 정보
            
        Returns:
            JSON 형식의 NPC 반응:
            {
                "dialogue": "NPC의 대사",
                "emotion_change": "감정 변화 (예: happy, angry)",
                "relationship_change": -5 ~ 5 사이의 정수,
                "action_description": "행동 지문 (예: 칼을 뽑아든다)"
            }
        """
        # 프롬프트 구성
        prompt = f"""{self.system_prompt}

플레이어의 행동: {player_action}

NPC 정보:
- 이름: {npc_data.get('name', '알 수 없음')}
- 직업: {npc_data.get('job', '알 수 없음')}
- 성격: {', '.join(npc_data.get('traits', []))}
- 현재 감정: {npc_data.get('current_emotion', 'neutral')}
- 관계 점수: {npc_data.get('relationship_score', 0)}
- 최근 기억: {', '.join(npc_data.get('short_term_memory', []))}

세계 맥락: {world_context}

위 정보를 바탕으로 NPC의 반응을 생성해주세요. 반드시 아래 JSON 형식으로 응답해야 합니다:
{{
    "dialogue": "NPC의 대사 (직접 인용 형식)",
    "emotion_change": "감정 변화 (happy, sad, angry, surprised, neutral, fearful, disgusted 중 하나)",
    "relationship_change": -5 ~ 5 사이의 정수 (플레이어와의 관계 변화),
    "action_description": "NPC의 행동 지문 (예: 칼을 뽑아든다, 미소를 지으며 고개를 끄덕인다)"
}}
"""
        
        try:
            # JSON 형식으로 응답 요청
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    response_mime_type='application/json',
                    temperature=0.8,
                )
            )
            
            # JSON 파싱
            result = json.loads(response.text)
            
            # 관계 변화 값 검증 (-5 ~ 5 사이)
            if 'relationship_change' in result:
                result['relationship_change'] = max(-5, min(5, int(result['relationship_change'])))
            
            return result
            
        except json.JSONDecodeError as e:
            # JSON 파싱 실패 시 기본값 반환
            return {
                "dialogue": "NPC가 당황한 표정을 짓는다.",
                "emotion_change": "surprised",
                "relationship_change": 0,
                "action_description": "뭔가 이상한 기분을 느낀다."
            }
        except Exception as e:
            # 기타 오류 발생 시 기본값 반환
            print(f"Gemini API 호출 중 오류 발생: {e}")
            return {
                "dialogue": "NPC가 혼란스러워 보인다.",
                "emotion_change": "neutral",
                "relationship_change": 0,
                "action_description": "아무 말도 하지 않는다."
            }
