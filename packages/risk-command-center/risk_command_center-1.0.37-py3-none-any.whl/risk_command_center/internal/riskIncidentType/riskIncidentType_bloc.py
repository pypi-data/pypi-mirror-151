from risk_command_center.internal.riskIncidentType.riskIncidentType_provider import RiskIncidentTypeProvider
from risk_command_center.common.huemul_response_to_bloc import HuemulResponseToBloc

class RiskIncidentTypeBloc():
    #
    # start riskIncidentTypeCreate
    # @param TiskIncidentTypeModel riskIncidentTypeModel
    # @return HuemulResponseBloc[riskIncidentTypeResponseModel]
    #
    def riskIncidentTypeCreate(self, riskIncidentTypeModel, connectObject):
        continueInLoop = True
        attempt = 0
        result = HuemulResponseToBloc(connectObject=connectObject)

        while (continueInLoop):
            result = RiskIncidentTypeProvider(connectObject=connectObject).riskIncidentTypeCreate(
                    riskIncidentTypeModel=riskIncidentTypeModel
            )
            attempt +=1
            continueInLoop = result.analyzeErrors(attempt)
        
        return result