from risk_command_center.internal.riskRule.riskRule_provider import RiskRuleProvider
from risk_command_center.common.huemul_response_to_bloc import HuemulResponseToBloc

class RiskRuleBloc():
    #
    # start riskRuleCreate
    # @param TiskRuleModel riskRuleModel
    # @return HuemulResponseBloc[riskRuleResponseModel]
    #
    def riskRuleCreate(self, riskRuleModel, connectObject):
        continueInLoop = True
        attempt = 0
        result = HuemulResponseToBloc(connectObject=connectObject)

        while (continueInLoop):
            result = RiskRuleProvider(connectObject=connectObject).riskRuleCreate(
                    riskRuleModel=riskRuleModel
            )
            attempt +=1
            continueInLoop = result.analyzeErrors(attempt)
        
        return result