from pydantic import BaseModel, validator

from .base import CommonAttrs


class QuestionCreate(BaseModel):

    class AnswerCreate(BaseModel):
        content: str
        is_correct: bool

    content: str
    answers : list[AnswerCreate]

    @validator("answers")
    def validate_answers(cls, answers):
        if len(answers) < 2:
            raise ValueError("At least 2 answers are required")
        if not any(answer.is_correct for answer in answers):
            raise ValueError("At least one answer must be correct")
        return answers


class Question(CommonAttrs):

    class Answer(CommonAttrs):
        content: str

    content: str
    answers : list[Answer]
    has_more_than_one_correct_answer: bool
