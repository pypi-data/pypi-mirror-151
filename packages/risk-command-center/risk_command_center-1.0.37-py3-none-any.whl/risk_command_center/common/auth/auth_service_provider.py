from risk_command_center.common.auth.auth_service_model import AuthServiceModel
from risk_command_center.common.huemul_response_error import HuemulResponseError
from risk_command_center.common.huemul_connection import HuemulConnection
import base64

from risk_command_center.common.huemul_response_to_bloc import HuemulResponseToBloc

class AuthServiceProvider(HuemulResponseToBloc):
    
    #
    # create new element
    # @param consumerId consumerId: String
    # @param consumerSecret consumerSecret: String
    # @param orgId orgId: String
    # @param applicationName applicationName: String
    #
    def authSignInService(self, consumerId, consumerSecret, orgId, applicationName):
        try:
            dataIn = consumerId + ":" + orgId + ":" + applicationName + ":" + consumerSecret
            bytes = dataIn.encode('ascii') #.getBytes(StandardCharsets.UTF_8)
            base64Str = base64.b64encode(bytes).decode('ascii')

            huemulResponse = HuemulConnection(connectObject=self.connectObject).authRequest(
                route = "authService/v1/sign-in-service/",
                data = base64Str,
                orgId = orgId
            )

            #get status from connection
            self.fromResponseProvider(huemulResponseProvider = huemulResponse)
            if (self.isSuccessful):
                self.data = [] if len(huemulResponse.dataRaw) == 0 else list(map(lambda x: AuthServiceModel(**x) ,huemulResponse.dataRaw))
        except Exception as e:
            self.errors.append(
                HuemulResponseError(errorId = "APP-101", errorTxt = str(e))
            )

        return self


        