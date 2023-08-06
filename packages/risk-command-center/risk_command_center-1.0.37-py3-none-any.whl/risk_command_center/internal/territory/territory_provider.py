from risk_command_center.common.huemul_response_to_bloc import HuemulResponseToBloc
from risk_command_center.common.huemul_response_error import HuemulResponseError
from risk_command_center.common.huemul_connection import HuemulConnection
from risk_command_center.common.huemul_functions import huemulFunctions
from risk_command_center.internal.territory.territory_response_model import TerritoryResponseModel
import json

class TerritoryProvider(HuemulResponseToBloc):
    
    #
    # TerritoryCreate
    # @param territoryModel territoryModel
    # @return HuemulResponseBloc[ProcessExecResponseModel]
    #
    def territoryCreate(self, territoryModel):
        #self = HuemulResponseBloc()
        try:
            huemulFunctions.deleteArgs(territoryModel)
            dataIn = json.dumps(territoryModel, default=lambda obj: obj.__dict__)
            self.message = "starting postRequest"
            huemulResponse = HuemulConnection(connectObject=self.connectObject).postRequest(
                route = "territories/v1/",
                data = dataIn,
            )

            #get status from connection
            self.message = "starting fromResponseProvider"
            self.fromResponseProvider(huemulResponseProvider = huemulResponse)
            if (self.isSuccessful):
                self.data = [] if len(huemulResponse.dataRaw) == 0 else list(map(lambda x: TerritoryResponseModel(**x) ,huemulResponse.dataRaw))
        except Exception as e:
            self.errors.append(
                HuemulResponseError(errorId = "APP-101", errorTxt = str(e))
            )

        return self


        