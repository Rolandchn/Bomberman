
from data.entity.AI.evaluation import easy
from data.entity.AI.evaluation import medium
from data.entity.AI.evaluation import hard


class DifficultyProfile:
    def __init__(self, name, depth, eval_fn):
        self.name = name
        self.depth = depth
        self.eval_fn = eval_fn

EASY = DifficultyProfile("Easy", 3, easy.eval)
MEDIUM = DifficultyProfile("Medium", 3, medium.eval)
HARD = DifficultyProfile("Hard", 3, hard.eval)
