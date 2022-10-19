# from sqlalchemy import Column, ForeignKey, String, select

# from .base import Base, Crud


# class QuizDetailCrud(Crud, Base):
#     __tablename__ = "QuizDetails"

#     quiz_id = Column(String, ForeignKey("Quizzes.id"), primary_key=True)
#     answer_id = Column(String, ForeignKey("Answers.id"), primary_key=True)


# class QuizCrud(Crud, Base):
#     __tablename__ = "Quizzes"

#     user_id = Column(String(36), ForeignKey("Users.id"), nullable=False)
#     lesson_id = Column(String(36), ForeignKey("Lessons.id"), nullable=False)

