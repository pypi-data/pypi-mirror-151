from risk_command_center.common.huemul_response_to_bloc import HuemulResponseToBloc
from risk_command_center.common.huemul_response_error import HuemulResponseError
from risk_command_center.common.huemul_connection import HuemulConnection
from risk_command_center.common.huemul_functions import huemulFunctions
from risk_command_center.internal.riskIncident.riskIncident_response_model import RiskIncidentResponseModel
import json

class RiskIncidentProvider(HuemulResponseToBloc):
    
    #
    # RiskIncidentCreate
    # @param riskIncidentModel riskIncidentModel
    # @return HuemulResponseBloc[ProcessExecResponseModel]
    #
    def riskIncidentCreate(self, riskIncidentModel):
        #self = HuemulResponseBloc()
        try:
            huemulFunctions.deleteArgs(riskIncidentModel)
            dataIn = json.dumps(riskIncidentModel, default=lambda obj: obj.__dict__)
            self.message = "starting postRequest"
            huemulResponse = HuemulConnection(connectObject=self.connectObject).postRequest(
                route = "riskIncident/v1/",
                data = dataIn,
            )

            #get status from connection
            self.message = "starting fromResponseProvider"
            self.fromResponseProvider(huemulResponseProvider = huemulResponse)
            if (self.isSuccessful):
                self.data = [] if len(huemulResponse.dataRaw) == 0 else list(map(lambda x: RiskIncidentResponseModel(**x) ,huemulResponse.dataRaw))
        except Exception as e:
            self.errors.append(
                HuemulResponseError(errorId = "APP-101", errorTxt = str(e))
            )

        return self


        