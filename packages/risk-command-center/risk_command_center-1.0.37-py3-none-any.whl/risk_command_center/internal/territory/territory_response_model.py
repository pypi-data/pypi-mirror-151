#
# territoryId: String,
#
class TerritoryResponseModel:
    def __init__(self, territoryId, **args):
        self.territoryId = territoryId
        self.args = args