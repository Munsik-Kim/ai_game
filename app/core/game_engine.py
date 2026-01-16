from typing import Dict, Any, Optional
from app.models.schemas import (
    WorldState,
    Player,
    NPC,
    CharacterProfile,
    CharacterStats
)
from app.services.ai_service import GeminiService


class GameEngine:
    """게임 상태를 관리하고 AI 서비스를 호출하는 게임 엔진"""
    
    def __init__(self):
        """게임 엔진 초기화 - 더미 데이터 생성"""
        # AI 서비스 초기화
        self.ai_service = GeminiService()
        
        # 플레이어 초기 데이터 생성
        self.player = Player(
            profile=CharacterProfile(
                name="모험가",
                job="모험가",
                traits=["용감함", "호기심", "친절함"],
                lore="평범한 마을에서 시작한 모험가. 세계를 탐험하며 성장하고 있다."
            ),
            stats=CharacterStats(
                hp=100,
                mp=50,
                gold=100,
                location_id="marketplace"
            ),
            inventory=["낡은 검", "가죽 갑옷", "빵 3개"]
        )
        
        # 테스트용 NPC '상인 그레고르' 생성
        merchant_gregor = NPC(
            id="merchant_gregor_001",
            profile=CharacterProfile(
                name="그레고르",
                job="상인",
                traits=["교활함", "상업적", "수다스러움"],
                lore="시장에서 20년 넘게 장사를 해온 베테랑 상인. 좋은 물건을 싸게 팔아주지만 때로는 교활한 협상가이기도 하다."
            ),
            stats=CharacterStats(
                hp=80,
                mp=30,
                gold=500,
                location_id="marketplace"
            ),
            current_emotion="neutral",
            relationship_score=0,
            short_term_memory=[]
        )
        
        # 월드 상태 초기 데이터 생성
        self.world_state = WorldState(
            time_of_day="오후",
            weather="맑음",
            npcs=[merchant_gregor]
        )
    
    def _npc_to_dict(self, npc: NPC) -> Dict[str, Any]:
        """
        NPC 객체를 AI 서비스에 전달할 dict 형식으로 변환
        
        Args:
            npc: NPC 객체
            
        Returns:
            NPC 데이터를 담은 dict
        """
        return {
            "name": npc.profile.name,
            "job": npc.profile.job,
            "traits": npc.profile.traits,
            "lore": npc.profile.lore,
            "current_emotion": npc.current_emotion,
            "relationship_score": npc.relationship_score,
            "short_term_memory": npc.short_term_memory
        }
    
    def _get_world_context(self) -> str:
        """
        현재 세계 맥락 정보를 문자열로 반환
        
        Returns:
            세계 맥락 정보 문자열
        """
        return (
            f"시간: {self.world_state.time_of_day}, "
            f"날씨: {self.world_state.weather}, "
            f"현재 위치: {self.player.stats.location_id}"
        )
    
    def process_player_action(self, action_text: str) -> Dict[str, Any]:
        """
        플레이어의 행동을 처리하고 NPC 반응을 생성합니다.
        
        Args:
            action_text: 플레이어의 행동 설명
            
        Returns:
            NPC 반응 정보를 담은 dict:
            {
                "dialogue": "NPC의 대사",
                "action_description": "NPC의 행동 지문",
                "npc_name": "NPC 이름",
                "updated_emotion": "업데이트된 감정",
                "updated_relationship_score": "업데이트된 관계 점수"
            }
        """
        # 현재 위치에 있는 NPC 찾기 (첫 번째 NPC로 가정)
        current_location_npcs = [
            npc for npc in self.world_state.npcs
            if npc.stats.location_id == self.player.stats.location_id
        ]
        
        if not current_location_npcs:
            return {
                "dialogue": "",
                "action_description": "주변에 아무도 없습니다.",
                "npc_name": "",
                "updated_emotion": "",
                "updated_relationship_score": 0
            }
        
        # 첫 번째 NPC 선택
        target_npc = current_location_npcs[0]
        
        # NPC 데이터를 dict로 변환
        npc_data = self._npc_to_dict(target_npc)
        
        # 세계 맥락 정보 가져오기
        world_context = self._get_world_context()
        
        # AI 서비스를 통해 NPC 반응 생성
        ai_response = self.ai_service.generate_npc_reaction(
            player_action=action_text,
            npc_data=npc_data,
            world_context=world_context
        )
        
        # AI 응답을 파싱하여 NPC 상태 업데이트 (Python 로직으로 처리)
        # 관계 점수 업데이트
        new_relationship_score = target_npc.relationship_score + ai_response.get("relationship_change", 0)
        # 관계 점수는 일반적으로 -100 ~ 100 범위로 제한 (선택사항)
        target_npc.relationship_score = max(-100, min(100, new_relationship_score))
        
        # 감정 업데이트
        target_npc.current_emotion = ai_response.get("emotion_change", target_npc.current_emotion)
        
        # 단기 기억에 대화 추가 (최근 5개만 유지)
        dialogue = ai_response.get("dialogue", "")
        if dialogue:
            target_npc.short_term_memory.append(f"플레이어: {action_text}")
            target_npc.short_term_memory.append(f"{target_npc.profile.name}: {dialogue}")
            # 최근 10개만 유지
            if len(target_npc.short_term_memory) > 10:
                target_npc.short_term_memory = target_npc.short_term_memory[-10:]
        
        # 결과 반환
        return {
            "dialogue": dialogue,
            "action_description": ai_response.get("action_description", ""),
            "npc_name": target_npc.profile.name,
            "updated_emotion": target_npc.current_emotion,
            "updated_relationship_score": target_npc.relationship_score
        }
    
    def get_current_state(self) -> Dict[str, Any]:
        """
        현재 게임 상태를 반환합니다.
        
        Returns:
            현재 게임 상태 정보
        """
        return {
            "player": self.player.model_dump(),
            "world_state": self.world_state.model_dump()
        }
