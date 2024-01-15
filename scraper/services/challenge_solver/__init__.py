from speech_recognition import Recognizer

from scraper.services.challenge_solver.interfaces.challenge_solver import ChallengeSolver
from scraper.services.challenge_solver.recaptcha_solver import ReCaptchaSolver


async def get_solver() -> ChallengeSolver:
    recognizer = Recognizer()
    return ReCaptchaSolver(recognizer)
