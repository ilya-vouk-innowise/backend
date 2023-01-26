from fastapi import APIRouter

router = APIRouter()


@router.get(path='')
async def get_health_check_status() -> dict:
    """Get health check status"""
    return {'status': 'ok'}
