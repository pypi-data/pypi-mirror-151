
class EvaluationWrapper(object):
    evaluation = {}

    def __init__(self, evaluation):
        self.evaluation = evaluation

    def __str__(self):
        return str(self.evaluation)
