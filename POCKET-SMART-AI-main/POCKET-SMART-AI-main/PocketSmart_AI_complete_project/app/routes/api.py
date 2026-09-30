import json
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy import desc
from sqlalchemy.orm import Session
from ..auth import create_access_token, hash_password, verify_password
from ..config import get_settings
from ..database import get_db
from ..dependencies import get_current_user
from ..models import RecommendationHistory, User
from ..schemas import *
from ..services.recommendation_service import generate_home, generate_party, generate_jewelry
router=APIRouter(); settings=get_settings()

def auth_response(u): return AuthResponse(access_token=create_access_token(str(u.id)),user_id=u.id,email=u.email,full_name=u.full_name)
@router.post("/register",response_model=AuthResponse)
def register(p:UserRegister,db:Session=Depends(get_db)):
    email=p.email.strip().lower()
    if db.query(User).filter(User.email==email).first(): raise HTTPException(409,"Email is already registered")
    u=User(email=email,full_name=p.full_name.strip(),password_hash=hash_password(p.password)); db.add(u); db.commit(); db.refresh(u); return auth_response(u)
@router.post("/login",response_model=AuthResponse)
def login(p:UserLogin,db:Session=Depends(get_db)):
    u=db.query(User).filter(User.email==p.email.strip().lower()).first()
    if not u or not verify_password(p.password,u.password_hash): raise HTTPException(401,"Invalid email or password")
    return auth_response(u)
@router.post("/logout")
def logout():
    r=JSONResponse({"message":"Logged out"}); r.delete_cookie("access_token"); return r
@router.post("/token",response_model=AuthResponse)
def token(p:UserLogin,db:Session=Depends(get_db)): return login(p,db)
@router.get("/session-info",response_model=SessionInfo)
def session_info(u=Depends(get_current_user)): return SessionInfo(authenticated=True,user_id=u.id,email=u.email,full_name=u.full_name)
@router.get("/session-data")
def session_data(u=Depends(get_current_user),db:Session=Depends(get_db)):
    return {"user":{"id":u.id,"email":u.email,"full_name":u.full_name},"recommendation_count":db.query(RecommendationHistory).filter(RecommendationHistory.user_id==u.id).count()}

def save(db,u,kind,payload,result):
    row=RecommendationHistory(user_id=u.id,planner_type=kind,request_json=json.dumps(payload,ensure_ascii=False),response_json=result.model_dump_json(),source=result.source); db.add(row); db.commit(); db.refresh(row); return row
@router.post("/generate-home")
def generate_home_route(p:HomeRequest,u=Depends(get_current_user),db:Session=Depends(get_db)):
    result=generate_home(p); row=save(db,u,"home",p.model_dump(),result); return {"id":row.id,**result.model_dump()}
@router.post("/generate-party")
def generate_party_route(p:PartyRequest,u=Depends(get_current_user),db:Session=Depends(get_db)):
    result=generate_party(p); row=save(db,u,"party",p.model_dump(),result); return {"id":row.id,**result.model_dump()}
@router.post("/generate-jewelry")
async def generate_jewelry_route(budget:float=Form(...),currency:str=Form("INR"),occasion:str=Form(...),style:str=Form(""),outfit_description:str=Form(""),outfit_image:UploadFile|None=File(None),u=Depends(get_current_user),db:Session=Depends(get_db)):
    image_bytes=image_mime=None
    if outfit_image and outfit_image.filename:
        if outfit_image.content_type not in {"image/jpeg","image/png","image/webp"}: raise HTTPException(415,"Only JPG, PNG and WEBP images are supported")
        image_bytes=await outfit_image.read()
        if len(image_bytes)>settings.max_upload_mb*1024*1024: raise HTTPException(413,f"Image must be <= {settings.max_upload_mb} MB")
        image_mime=outfit_image.content_type
    p=JewelryRequest(budget=budget,currency=currency,occasion=occasion,style=style,outfit_description=outfit_description); result=generate_jewelry(p,image_bytes,image_mime); row=save(db,u,"jewelry",p.model_dump(),result); return {"id":row.id,**result.model_dump()}
@router.get("/history")
def history(u=Depends(get_current_user),db:Session=Depends(get_db)):
    rows=db.query(RecommendationHistory).filter(RecommendationHistory.user_id==u.id).order_by(desc(RecommendationHistory.created_at)).limit(50).all()
    return [{"id":x.id,"planner_type":x.planner_type,"source":x.source,"created_at":x.created_at.isoformat()} for x in rows]
@router.get("/recommendations-details/{recommendation_id}")
def details(recommendation_id:int,u=Depends(get_current_user),db:Session=Depends(get_db)):
    x=db.query(RecommendationHistory).filter(RecommendationHistory.id==recommendation_id,RecommendationHistory.user_id==u.id).first()
    if not x: raise HTTPException(404,"Recommendation not found")
    return {"id":x.id,"planner_type":x.planner_type,"source":x.source,"created_at":x.created_at.isoformat(),"request":json.loads(x.request_json),"result":json.loads(x.response_json)}
@router.get("/startup")
def startup(): return {"status":"ready","app":settings.app_name}
@router.get("/health")
def health(): return {"status":"ok"}
