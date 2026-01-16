from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from app.core.game_engine import GameEngine
from app.models.schemas import WorldState, Player

# 게임 엔진 인스턴스 (전역 관리)
game_engine = GameEngine()

router = APIRouter()


# Request/Response 모델 정의
class ActionRequest(BaseModel):
    """플레이어 행동 요청 모델"""
    action: str


class ActionResponse(BaseModel):
    """플레이어 행동 처리 응답 모델"""
    dialogue: str
    action_description: str
    npc_name: str
    updated_emotion: str
    updated_relationship_score: int


class GameStateResponse(BaseModel):
    """게임 상태 응답 모델"""
    player: Player
    world_state: WorldState


class ResetResponse(BaseModel):
    """게임 리셋 응답 모델"""
    message: str
    state: GameStateResponse


@router.post("/action", response_model=ActionResponse)
async def process_action(request: ActionRequest) -> ActionResponse:
    """
    플레이어의 행동을 처리하고 NPC 반응을 반환합니다.
    
    Args:
        request: 플레이어 행동 요청
        
    Returns:
        NPC 반응 정보
    """
    try:
        result = game_engine.process_player_action(request.action)
        return ActionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"행동 처리 중 오류 발생: {str(e)}")


@router.get("/state", response_model=GameStateResponse)
async def get_state() -> GameStateResponse:
    """
    현재 게임 상태를 반환합니다 (프론트엔드 디버깅용).
    
    Returns:
        현재 게임 상태 (플레이어 + 월드 상태)
    """
    try:
        state = game_engine.get_current_state()
        return GameStateResponse(**state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"상태 조회 중 오류 발생: {str(e)}")


@router.post("/reset", response_model=ResetResponse)
async def reset_game() -> ResetResponse:
    """
    게임 상태를 초기화합니다.
    
    Returns:
        리셋 완료 메시지와 초기화된 게임 상태
    """
    try:
        # 게임 엔진 재초기화
        global game_engine
        game_engine = GameEngine()
        
        # 초기화된 상태 반환
        state = game_engine.get_current_state()
        return ResetResponse(
            message="게임이 초기화되었습니다.",
            state=GameStateResponse(**state)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"게임 리셋 중 오류 발생: {str(e)}")
