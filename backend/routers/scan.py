from fastapi import APIRouter
from models.schemas import ScanRequest, ScanResult
from database.db import get_db_connection
from core.ai import analyze_network

router = APIRouter(prefix="/api", tags=["scan"])

@router.post("/scan", response_model=list[ScanResult])
async def scan_networks(request: ScanRequest):
    results = []
    conn = get_db_connection()
    
    for net in request.networks:
        row = conn.execute("SELECT risk FROM rogue_aps WHERE bssid = ? OR ssid = ?", (net.bssid or "", net.ssid)).fetchone()
        is_rogue = row is not None
        
        ai = await analyze_network(net.dict())
        risk = "dangerous" if is_rogue else ai.get("risk", "risky")
        reason = "Known rogue!" if is_rogue else ai.get("reason", "AI analysis")
        vpn_needed = is_rogue or net.security == "Open" or ai.get("vpn_needed", True)
        
        results.append(ScanResult(**net.dict(), risk=risk, reason=reason, vpn_needed=vpn_needed))
    
    conn.close()
    return results
