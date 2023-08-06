from risk_command_center.internal.riskType.riskType_provider import RiskTypeProvider
from risk_command_center.common.huemul_response_to_bloc import HuemulResponseToBloc

class RiskTypeBloc():
    #
    # start riskTypeCreate
    # @param riskTypeModel RiskTypeModel
    # @return HuemulResponseBloc[RiskTypeResponseModel]
    #
    def riskTypeCreate(self, riskTypeModel, connectObject):
        continueInLoop = True
        attempt = 0
        result = HuemulResponseToBloc(connectObject=connectObject)

        while (continueInLoop):
            result = RiskTypeProvider(connectObject=connectObject).riskTypeCreate(
                    riskTypeModel=riskTypeModel
            )
            attempt +=1
            continueInLoop = result.analyzeErrors(attempt)
        
        return result