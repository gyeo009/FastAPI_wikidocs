import datetime

from pydantic import BaseModel, validator

class AnswerCreate(BaseModel):
    content: str

    # HTTP 프로토콜의 URL에 포함된 입력 값(URL Parameter)은 매개변수로 읽는다(Path Parameter or Query Parameter)
    # HTTP 프로토콜의 Body에 포함된 입력 값(payload)은 Pydantic 스키마로 읽는다(Request Body)
    # content 값이 저장될 때 실행되는 not_empty 함수
    @validator('content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v
    


class Answer(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime

    class Config:
        orm_mode = True