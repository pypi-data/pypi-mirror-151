#
# riskId: string
# ruleIdLocal: string
# ruleType: string
# processId: string
# elementId: string
# ruleName: string
# ruleFormula: string
# ruleEnabled: boolean
# orgId: string

class RiskRuleModel:
    def __init__(self, riskId, ruleIdLocal, ruleType, processId, elementId, ruleName, ruleFormula, ruleEnabled, orgId):
        self.riskId = riskId
        self.ruleIdLocal = ruleIdLocal
        self.ruleType = ruleType
        self.processId = processId
        self.elementId = elementId
        self.ruleName = ruleName
        self.ruleFormula = ruleFormula
        self.ruleEnabled = ruleEnabled
        self.orgId = orgId
        self.ruleId = ""