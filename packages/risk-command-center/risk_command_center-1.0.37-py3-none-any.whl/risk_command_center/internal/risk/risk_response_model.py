#
# riskId: String,
#
class RiskResponseModel:
    def __init__(self, riskId, **args):
        self.riskId = riskId
        self.args = args