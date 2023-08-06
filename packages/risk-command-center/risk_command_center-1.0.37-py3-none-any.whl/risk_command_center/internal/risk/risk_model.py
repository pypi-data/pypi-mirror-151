#
# riskId: String,
# departmentId: String,
# riskTypeId: String,
# userEmail: String,
# riskName: String,
# riskSource: String,
# riskEffect: String,
# riskTrigger: String,
# riskCrossArea: Bool,
# orgId: String,
# riskDate: Date

class RiskModel:
    def __init__(self, riskId, departmentId, riskTypeId, userEmail, riskName, riskSource, riskEffect, riskTrigger, riskCrossArea, orgId, riskDate):
        self.riskId = riskId
        self.departmentId = departmentId
        self.riskTypeId = riskTypeId
        self.userEmail = userEmail
        self.riskName = riskName
        self.riskSource = riskSource
        self.riskEffect = riskEffect 
        self.riskTrigger = riskTrigger
        self.riskCrossArea = riskCrossArea
        self.orgId = orgId
        self.riskDate = riskDate