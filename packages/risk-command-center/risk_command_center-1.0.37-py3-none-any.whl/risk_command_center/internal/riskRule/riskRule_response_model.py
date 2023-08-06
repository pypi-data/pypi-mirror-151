#
# ritId: String,
#
class RiskRuleResponseModel:
    def __init__(self, ruleId, **args):
        self.ruleId = ruleId
        self.args = args