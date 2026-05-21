from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field


Classification = Literal[
    "Coherent",
    "Stable with watch items",
    "Degraded but usable",
    "High entropy",
    "Misaligned",
]


class EntropyMetrics(BaseModel):
    contradiction_density: float = Field(ge=0, le=1, default=0)
    uncertainty_variance: float = Field(ge=0, le=1, default=0)
    memory_fragmentation: float = Field(ge=0, le=1, default=0)
    recursion_instability: float = Field(ge=0, le=1, default=0)
    context_decay: float = Field(ge=0, le=1, default=0)


class FlowQualityMetrics(BaseModel):
    task_completion_consistency: float = Field(ge=0, le=1, default=0)
    reasoning_continuity: float = Field(ge=0, le=1, default=0)
    semantic_coherence: float = Field(ge=0, le=1, default=0)
    verification_success_rate: float = Field(ge=0, le=1, default=0)


class EFGMInput(BaseModel):
    task_id: str
    T: float = Field(ge=0, le=1)
    E: float = Field(ge=0, le=1)
    entropy: EntropyMetrics
    flow_quality: FlowQualityMetrics
    notes: list[str] = Field(default_factory=list)


class EFGMResult(BaseModel):
    task_id: str
    T: float
    E: float
    Fq: float
    e: float
    F: float
    classification: Classification
    recommended_action: str
    entropy_drivers: list[str]
