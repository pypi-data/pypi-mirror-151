from risk_command_center.internal.territory.territory_provider import TerritoryProvider
from risk_command_center.common.huemul_response_to_bloc import HuemulResponseToBloc

class TerritoryBloc():
    #
    # start territoryCreate
    # @param TerritoryModel TerritoryModel
    # @return HuemulResponseBloc[TerritoryResponseModel]
    #
    def territoryCreate(self, territoryModel, connectObject):
        continueInLoop = True
        attempt = 0
        result = HuemulResponseToBloc(connectObject=connectObject)

        while (continueInLoop):
            result = TerritoryProvider(connectObject=connectObject).territoryCreate(
                    territoryModel=territoryModel
            )
            attempt +=1
            continueInLoop = result.analyzeErrors(attempt)
        
        return result