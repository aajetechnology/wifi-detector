from pydantic import BaseModel
from typing import List, Optional

class Network(BaseModel):
    ssid: str
    bssid: Optional[str] = None
    signal: int
    security: str

class ScanRequest(BaseModel):
    networks: List[Network]

class ScanResult(BaseModel):
    ssid: str
    bssid: Optional[str]
    signal: int
    security: str
    risk: str
    reason: str
    vpn_needed: bool
