from pydantic import BaseModel, validator

from .base import CommonAttrs


class QuizCreate(BaseModel):
    to_pass: float

    @validator("to_pass")
    def to_pass_must_be_between_0_and_1(cls, to_pass):
        if not 0 <= to_pass <= 1:
            raise ValueError("to_pass must be between 0 and 1")
        return to_pass


class QuizUpdate(BaseModel):
    to_pass: float

    @validator("to_pass")
    def to_pass_must_be_between_0_and_1(cls, to_pass):
        if not 0 <= to_pass <= 1:
            raise ValueError("to_pass must be between 0 and 1")
        return to_pass


class QuestionCreate(BaseModel):
    class AnswerCreate(BaseModel):
        content: str
        is_correct: bool
    content: str
    answers: list[AnswerCreate]

    @validator("answers")
    def validate_answers(cls, answers):
        if len(answers) < 2:
            raise ValueError("At least 2 answers are required")
        if not any(answer.is_correct for answer in answers):
            raise ValueError("At least one answer must be correct")
        return answers


class Quiz(CommonAttrs):
    class Question(CommonAttrs):
        class Answer(CommonAttrs):
            content: str
            is_correct: bool | None
        content: str
        answers: list[Answer]
        has_more_than_one_correct_answer: bool
    to_pass: float
    questions: list[Question]


class QuizSubmit(BaseModel):
    class QuestionSubmit(BaseModel):
        id: str
        answer_ids: list[str]
    questions: list[QuestionSubmit]


class QuizResult(BaseModel):
    class QuestionResult(BaseModel):
        class AnswerResult(BaseModel):
            id: str
            is_correct: bool
        id: str
        is_correct: bool
        answers: list[AnswerResult]
    correct_count: int
    total_count: int
    to_pass: float
    is_passed: bool
    questions: list[QuestionResult]
