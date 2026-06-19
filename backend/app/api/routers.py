from fastapi import APIRouter

from app.api.v1.auth.router import router as auth_router
from app.api.v1.consultants.router import router as consultant_router
from app.api.v1.admin.router import router as admin_router
from app.api.v1.admin.refunds_router import router as admin_refunds_router
from app.api.v1.experties.router import router as experties_router
from app.api.v1.availability.router import router as availability_router
from app.api.v1.consultations.router import router as consultation_router
from app.api.v1.transactions.router import router as transaction_router
from app.api.v1.wallet.router import router as wallet_router
from app.api.v1.refunds.router import router as refund_router
from app.api.v1.reviews.router import router as review_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(consultant_router)
api_router.include_router(admin_router)
api_router.include_router(admin_refunds_router)
api_router.include_router(experties_router)
api_router.include_router(availability_router)
api_router.include_router(consultation_router)
api_router.include_router(transaction_router)
api_router.include_router(wallet_router)
api_router.include_router(refund_router)
api_router.include_router(review_router)
