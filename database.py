# import contextlib # DI를 위한 import, FastAPI의 Depend 키워드를 사용하면 이건 필요없음

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///./myapi.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}  
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind = engine)

Base = declarative_base()

# yield 키워드가 있으면 generator, 제너레이터
# with get_db() as db: , db세션 객체를 사용함, with 문을 벗어나는 순간 get_db 함수의 finally에 작성한 db.close() 함수가 자동으로 실행.

def get_db():
    db = SessionLocal()
    try:
        yield db # yield db 코드는, 일단 get_db함수가 이 부분을 만나면 db를 return 해주고 일시정지한다(return 이후 get_db의 scope가 닫힌게 아니다. 여전히 살아있다).
                 # question_router.py의 with get_db() as db에서 이처럼 get_db를 호출할 텐데, get_db를 종료하지 않고 살려둔 뒤 with scope가 닫히면 그때 get_db scope에서
                 # 함수 실행시 무조건 실행되는 finally: 가 돌게된다. 그럼 db.close()의 실행이 보장됨.
                 # 세션 open -> (세션 생존 scope 내) with문에서 db받고 쿼리문 실행 -> (세션 생존 scope 내) 쿼리문 종료 후 with문 종료 -> (세션 생존 scope 내) yield 존재 line 코드 실행 끝 ->
                 # (세션 생존 scope 내) finally 코드 실행 -> (세션 생존 scope 내) db.close()실행 -> get_db 종료 (세션 생존 scope 끝)
                 # 근데 with문 말고 FastAPI의 Depends 사용하면 더 편하대... 백엔드 프레임워크엔 당연하게도 DI 설정하는게 있겠지... 그렇지...
    finally:
        db.close()

