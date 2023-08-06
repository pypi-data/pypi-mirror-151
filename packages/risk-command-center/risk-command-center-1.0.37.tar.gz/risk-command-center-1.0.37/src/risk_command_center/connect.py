from risk_command_center.common.auth.auth_service_bloc import AuthServiceBloc
from risk_command_center.common.huemul_error import HuemulError
from risk_command_center.common.huemul_common import HuemulCommon
from risk_command_center.common.huemul_logging import HuemulLogging

# authData: AuthModel
class Connect:
    def __init__(self, authData):
        self.authData = authData
        self.huemulLogging = HuemulLogging()
        self.huemulLogging.logMessageInfo(message = "WELCOME to the Huemul Risk Command Center...")

        self._canExecute = False
        self._isOpen = True
        self._errorMessage = ""
        self.othersParams = []
        self.controlClassName = "" #: String = Invoker(1).getClassName.replace("$", "")
        self.controlMethodName = "" #: String = Invoker(1).getMethodName.replace("$", "")
        #val controlFileName: String = Invoker(1).getFileName.replace("$", "")

        #create error and common object
        self.controlError = HuemulError(orgId=authData.orgId, huemulLogging=self.huemulLogging)
        self.huemulCommon = HuemulCommon()

        #### START        
        #login
        self.huemulLogging.logMessageInfo(message = "calling Ground Control for launch authorization...")
        authInfoResponse = AuthServiceBloc().authSignInService(self.authData, connectObject=self)

        if (not authInfoResponse.isSuccessful):
            self._canExecute = False
            self._errorMessage = authInfoResponse.message if (len(authInfoResponse.errors) == 0) else authInfoResponse.errors[0].errorTxt
            self.huemulLogging.logMessageError(message = "error: " + self._errorMessage)
            return

        #store credentials and token
        self.huemulCommon.setOrgId(authData.orgId)
        self.huemulCommon.setConsumerId(authData.consumerId)
        self.huemulCommon.setConsumerSecret(authData.consumerSecret)
        self.huemulCommon.setApplicationName(authData.applicationName)
        self.huemulCommon.setTokenId(authInfoResponse.data[0].tokenId)

        self.huemulLogging.logMessageInfo(message = "authorized...")
        self.canExecute = True
        self.huemulLogging.logMessageInfo(message = "STARTED!!!")

        ### END START
        
    def isOpen(self):
        return self._isOpen

    #/************************************************************************************/
    #/******************  R E S U L T S    ***********************************************/
    #/************************************************************************************

    
    

    #/************************************************************************************/
    #/******************  U T I L   F U N C T I O N S    *********************************/
    #/************************************************************************************/

    #
    # true for execute, false can't execute
    # @return
    #
    def canExecute(self):
        return self._canExecute

    #
    # return error message
    # @return
    #
    def getErrorMessage(self):
        return self._errorMessage
    
    