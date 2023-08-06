#
# riskTypeId: String,
#
class RiskTypeResponseModel:
    def __init__(self, riskTypeId, **args):
        self.riskTypeId = riskTypeId
        self.args = args