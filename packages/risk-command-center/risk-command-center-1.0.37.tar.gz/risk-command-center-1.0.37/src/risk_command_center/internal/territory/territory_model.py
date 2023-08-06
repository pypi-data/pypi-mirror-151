#
# territoryId: String,
# territoryName: String,
# territoryAddress: String,
# orgId: String,

class TerritoryModel:
    def __init__(self, territoryId, territoryName, territoryAddress, orgId):
        self.territoryId = territoryId
        self.territoryName = territoryName
        self.territoryAddress = territoryAddress
        self.orgId = orgId