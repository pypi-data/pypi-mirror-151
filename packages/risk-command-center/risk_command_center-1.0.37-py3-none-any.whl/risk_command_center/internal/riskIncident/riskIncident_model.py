#
# riskId: string,
# territoryId: string,
# riskControlId: string,
# riskAssetId: string,
# riskIncidentName: string,
# riskIncidentDescription: string,
# riskIncidentPeriod: Date,
# riskIncidentDate: Date,
# riskIncidentMode: string,
# riskIncidentExternalId: string,
# riskIncidentInfo: string,
# riskIncidentIp: string,
# riskIncidentMoney: number,
# riskIncidentValue: number,
# ritId: string,
# orgId: string

class RiskIncidentModel:
    def __init__(self, riskId, territoryId, riskControlId, riskAssetId, riskIncidentName, riskIncidentDescription, riskIncidentPeriod, riskIncidentDate, riskIncidentMode, riskIncidentExternalId, riskIncidentInfo, riskIncidentIp, riskIncidentMoney, riskIncidentValue, ritId, ritIdUser, orgId):
        self.riskId = riskId
        self.riskIncidentId = ""
        self.riskTerritoryId = ""
        self.territoryId = territoryId
        self.riskControlId = riskControlId
        self.riskAssetId = riskAssetId
        self.riskIncidentName = riskIncidentName
        self.riskIncidentDescription = riskIncidentDescription
        self.riskIncidentPeriod = riskIncidentPeriod
        self.riskIncidentDate = riskIncidentDate
        self.riskIncidentMode = riskIncidentMode
        self.riskIncidentExternalId = riskIncidentExternalId
        self.riskIncidentInfo = riskIncidentInfo
        self.riskIncidentIp = riskIncidentIp
        self.riskIncidentMoney = riskIncidentMoney
        self.riskIncidentValue = riskIncidentValue
        self.ritId = ritId
        self.ritIdUser = ritIdUser
        self.orgId = orgId