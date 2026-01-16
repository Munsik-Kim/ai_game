from typing import List
from pydantic import BaseModel, ConfigDict


class CharacterProfile(BaseModel):
    """캐릭터 프로필 모델"""
    name: str
    job: str
    traits: List[str]  # 성격 키워드 리스트
    lore: str  # 배경 스토리

    model_config = ConfigDict(from_attributes=True)


class CharacterStats(BaseModel):
    """캐릭터 스탯 모델"""
    hp: int
    mp: int
    gold: int
    location_id: str  # 현재 위치

    model_config = ConfigDict(from_attributes=True)


class NPC(BaseModel):
    """NPC 모델"""
    id: str
    profile: CharacterProfile
    stats: CharacterStats
    current_emotion: str
    relationship_score: int  # 플레이어와의 관계 점수
    short_term_memory: List[str]

    model_config = ConfigDict(from_attributes=True)


class Player(BaseModel):
    """플레이어 모델"""
    profile: CharacterProfile
    stats: CharacterStats
    inventory: List[str]

    model_config = ConfigDict(from_attributes=True)


class WorldState(BaseModel):
    """월드 상태 모델"""
    time_of_day: str  # 현재 시간
    weather: str  # 날씨
    npcs: List[NPC]  # 현재 지역에 있는 NPC들

    model_config = ConfigDict(from_attributes=True)
