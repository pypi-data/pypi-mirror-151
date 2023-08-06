from risk_command_center.internal.risk.risk_provider import RiskProvider
from risk_command_center.common.huemul_response_to_bloc import HuemulResponseToBloc

class RiskBloc():
    #
    # start riskCreate
    # @param RiskModel RiskModel
    # @return HuemulResponseBloc[RiskResponseModel]
    #
    def riskCreate(self, RiskModel, connectObject):
        continueInLoop = True
        attempt = 0
        result = HuemulResponseToBloc(connectObject=connectObject)

        while (continueInLoop):
            result = RiskProvider(connectObject=connectObject).riskCreate(
                    riskModel=RiskModel
            )
            attempt +=1
            continueInLoop = result.analyzeErrors(attempt)
        
        return result