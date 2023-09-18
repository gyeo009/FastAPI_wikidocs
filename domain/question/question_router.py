from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.question import question_schema, question_crud




# routing : FastAPI가 요청받은 URL을 해석해 그에 맞는 함수를 실행하여 결과를 리턴하는 행위.
# prefix 값은 request URL에 항상 포함되어야 하는 값
# 이 router는 FastAPI 인스턴스에 등록해야 함
router = APIRouter(
    prefix = "/api/question",
)

# /api/question/list 라는 URL 요청이 발생하면, /api/question 이라는 prefix가 등록된 question_router.py 파일의 /list로 등록된 함수 question_list가 실행되는 것이다.

# @router.get("/list")
# def question_list():
    
#     # with 문을 벗어나면 자동적으로 get_db의 finally가 실행; finally: 에 db.close가 있음
#     with get_db() as db:
#         _question_list = db.query(Question).order_by(Question.create_date.desc()).all()


#     # db = SessionLocal() # db connection 생성
#     # _question_list = db.query(Question).order_by(Question.create_date.desc()).all() # 조회 쿼리 날리기
#     # db.close() # db 닫기

#     return _question_list

# with문 안쓰고 라우터에 db 의존성 추가, db: Session의 의미는 db 객체가 Session 타입임을 의미. db 객체에 get_db()의 return value 할당
# 이렇게 fastapi 의존성을 추가하게 되면 get_db 함수에 자동으로 contextmanager가 적용되기 때문에 해당 get_db 함수에서 어노테이션 제거
@router.get("/list", response_model=question_schema.QuestionList)
def question_list(db: Session = Depends(get_db),
                    page: int = 0, size: int = 10):
    total, _question_list = question_crud.get_question_list(
        db, skip=page*size, limit=size)
    return {
        'total': total,
        'question_list': _question_list
    }

@router.get("/detail/{question_id}", response_model= question_schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    question = question_crud.get_question(db, question_id = question_id)
    return question

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def question_create(_question_create: question_schema.QuestionCreate,
                    db:Session = Depends(get_db)):
    question_crud.create_question(db=db, question_create=_question_create)