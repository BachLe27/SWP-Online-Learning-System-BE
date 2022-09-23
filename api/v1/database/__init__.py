from .answer import AnswerCrud
from .base import Base, engine
from .chapter import ChapterCrud
from .course import CourseCrud
from .lession import LessionCrud
from .price_package import PricePackageCrud
from .purchase import PurchaseCrud
from .question import QuestionCrud
from .quiz import QuizCrud
from .user import UserCrud
from .user_answer import UserAnswerCrud
from .user_course import UserCourseCrud

Base.metadata.drop_all(engine)

Base.metadata.create_all(engine)
