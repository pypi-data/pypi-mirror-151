#
# riskTypeId: String,
# riskTypeName: String,
# orgId: String,

class RiskTypeModel:
    def __init__(self, riskTypeId, riskTypeName, orgId):
        self.riskTypeId = riskTypeId
        self.riskTypeName = riskTypeName
        self.orgId = orgId