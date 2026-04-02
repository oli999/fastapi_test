from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, text  # text 함수가 핵심입니다!
from sqlalchemy.orm import sessionmaker, Session

# 1. DB 연결 설정 (동일)
DB_URL = "postgresql://kimgura:1234@localhost/kimgura_db"
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. DB 세션 관리 (동일)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    
    # 3. Raw SQL 실행 
    query = text("""
        SELECT num, writer, title, content, 
               TO_CHAR(created_at, 'YY.MM.DD TMDY TMAM HH:MI') as created_at 
        FROM post 
        ORDER BY num DESC
    """)
    
    # 실행 결과 가져오기
    result = db.execute(query)
    posts = result.fetchall() # 전체 행(Row)을 리스트로 변환
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "fortuneToday": "동쪽으로 가면 귀인을 만나요zzz",
        "posts": posts
    })