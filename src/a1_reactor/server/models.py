from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, List, Tuple

class JobCreate(BaseModel):
    prompt: str = Field(..., min_length=1)
    seconds: float = Field(2.0, ge=0.5, le=30.0)
    fps: int = Field(24, ge=12, le=60)
    seed: int = Field(0, ge=0)
    width: int = Field(768, ge=256, le=1920)
    height: int = Field(768, ge=256, le=1920)
    style_preset: Optional[str] = None
    regen_windows: Optional[List[Tuple[float, float]]] = None
    provider: str = Field("mock", description="mock|http")
    http_endpoint: Optional[str] = None

class JobStatus(BaseModel):
    id: str
    status: str
    artifact_path: Optional[str] = None
    message: Optional[str] = None
