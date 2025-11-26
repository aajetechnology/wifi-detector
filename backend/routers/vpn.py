from fastapi import APIRouter
# Cloudflare WARP VPN
router = APIRouter(prefix="/api", tags=["vpn"])

@router.get("/vpn/activate")
def activate_vpn():
    return {
        "success": True,
        "message": "Guardian VPN Activated!",
        "url": "https://1.1.1.1"
    }
