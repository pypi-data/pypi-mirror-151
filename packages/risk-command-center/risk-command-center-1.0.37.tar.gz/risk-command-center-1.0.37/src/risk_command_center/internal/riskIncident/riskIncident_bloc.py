from risk_command_center.internal.riskIncident.riskIncident_provider import RiskIncidentProvider
from risk_command_center.common.huemul_response_to_bloc import HuemulResponseToBloc

class RiskIncidentBloc():
    #
    # start riskIncidentCreate
    # @param TiskIncidentModel riskIncidentModel
    # @return HuemulResponseBloc[riskIncidentResponseModel]
    #
    def riskIncidentCreate(self, riskIncidentModel, connectObject):
        continueInLoop = True
        attempt = 0
        result = HuemulResponseToBloc(connectObject=connectObject)

        while (continueInLoop):
            result = RiskIncidentProvider(connectObject=connectObject).riskIncidentCreate(
                    riskIncidentModel=riskIncidentModel
            )
            attempt +=1
            continueInLoop = result.analyzeErrors(attempt)
        
        return result