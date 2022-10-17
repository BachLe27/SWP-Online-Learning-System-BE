from pydantic import BaseModel

from .base import CommonAttrs
from .lesson import Lesson


class AnswerCreate(BaseModel):
    content: str
    is_correct: bool


class Answer(BaseModel):
    content: str


class QuestionCreate(BaseModel):
    content: str
    answers : list[AnswerCreate]


class Question(CommonAttrs):
    content: str
    answers : list[Answer]


class LessonQuestion(Lesson):
    questions: list[Question]
