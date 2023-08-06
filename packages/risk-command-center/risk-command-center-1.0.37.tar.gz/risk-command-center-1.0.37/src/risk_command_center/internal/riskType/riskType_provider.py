from risk_command_center.common.huemul_response_to_bloc import HuemulResponseToBloc
from risk_command_center.common.huemul_response_error import HuemulResponseError
from risk_command_center.common.huemul_connection import HuemulConnection
from risk_command_center.common.huemul_functions import huemulFunctions
from risk_command_center.internal.riskType.riskType_response_model import RiskTypeResponseModel
import json

class RiskTypeProvider(HuemulResponseToBloc):
    
    #
    # RiskTypeCreate
    # @param riskTypeModel riskTypeModel
    # @return HuemulResponseBloc[ProcessExecResponseModel]
    #
    def riskTypeCreate(self, riskTypeModel):
        #self = HuemulResponseBloc()
        try:
            huemulFunctions.deleteArgs(riskTypeModel)
            dataIn = json.dumps(riskTypeModel, default=lambda obj: obj.__dict__)
            self.message = "starting postRequest"
            huemulResponse = HuemulConnection(connectObject=self.connectObject).postRequest(
                route = "riskTypes/v1/",
                data = dataIn,
            )

            #get status from connection
            self.message = "starting fromResponseProvider"
            self.fromResponseProvider(huemulResponseProvider = huemulResponse)
            if (self.isSuccessful):
                self.data = [] if len(huemulResponse.dataRaw) == 0 else list(map(lambda x: RiskTypeResponseModel(**x) ,huemulResponse.dataRaw))
        except Exception as e:
            self.errors.append(
                HuemulResponseError(errorId = "APP-101", errorTxt = str(e))
            )

        return self


        