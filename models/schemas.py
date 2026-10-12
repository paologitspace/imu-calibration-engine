from pydantic import BaseModel, Field
from typing import List

class IMUSample(BaseModel):
    timestamp: int
    ax: float
    ay: float
    az: float
    gx: float
    gy: float
    gz: float

class IMUBatch(BaseModel):
    # Il vincolo architetturale: imponiamo esattamente 100 elementi
    samples: List[IMUSample] = Field(
        ..., 
        min_length=100, 
        max_length=100, 
        description="Il batch deve contenere esattamente 100 letture IMU."
    )
