#
# ritIdUser: String,
# ritName: String,
# ritDescription: String,
# riskId: string,
# riskImpactId: string,
# orgId: String,
# ritId: String,

class RiskIncidentTypeModel:
    def __init__(self, ritIdUser, ritName, ritDescription, riskId, riskImpactId, orgId):
        self.ritIdUser = ritIdUser
        self.ritName = ritName
        self.ritDescription = ritDescription
        self.riskId = riskId
        self.riskImpactId = riskImpactId
        self.orgId = orgId