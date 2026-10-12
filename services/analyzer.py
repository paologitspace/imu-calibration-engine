from typing import List
from models.schemas import IMUSample

def calculate_calibration_offsets(samples: List[IMUSample]) -> dict:
    sum_ax = sum_ay = sum_az = 0.0
    sum_gx = sum_gy = sum_gz = 0.0
    
    count = len(samples)
    
    for s in samples:
        sum_ax += s.ax
        sum_ay += s.ay
        sum_az += s.az
        sum_gx += s.gx
        sum_gy += s.gy
        sum_gz += s.gz
        
    return {
        "offset_ax": sum_ax / count,
        "offset_ay": sum_ay / count,
        "offset_az": sum_az / count,
        "offset_gx": sum_gx / count,
        "offset_gy": sum_gy / count,
        "offset_gz": sum_gz / count,
    }
