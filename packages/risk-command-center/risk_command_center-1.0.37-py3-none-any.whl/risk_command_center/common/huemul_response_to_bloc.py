from ast import Try
import time
from warnings import catch_warnings
from risk_command_center.common.huemul_response_provider import HuemulResponseProvider

#
# @author Sebastián Rodríguez Robotham
# base class to create, get, getAll methods exposed to user
# @tparam T class Model
#


class HuemulResponseToBloc(HuemulResponseProvider):
    def __init__(self, connectObject, **args):
        self.data = "" #huemulResponseProvider.dataRaw
        self.connectObject = connectObject
        self.isSuccessful = False
        # status code: 200 OK, 500 error, etc
        self.httpStatusCode = ""
        # text to client
        self.message = "Not started"
        self.startDate = ""
        self.endDate = ""
        self.elapsedTimeMS = -1
        self.transactionId = ""
        # api response version
        self.apiVersion = ""

        #error detail
        self.errors = []
        #data detail
        self.dataRaw = ""
        #extra info detail
        self.extraInfoRaw = ""

        if (len(args) == 1 and "huemulResponseProvider" in args):
            self.fromResponseProvider(args["huemulResponseProvider"])

        


    def fromResponseProvider(self, huemulResponseProvider):
        self.data = huemulResponseProvider.dataRaw #huemulResponseProvider.dataRaw
        self.isSuccessful = huemulResponseProvider.isSuccessful
        # status code: 200 OK, 500 error, etc
        self.httpStatusCode = huemulResponseProvider.httpStatusCode
        # text to client
        self.message = huemulResponseProvider.message
        self.startDate = huemulResponseProvider.startDate
        self.endDate = huemulResponseProvider.endDate
        self.elapsedTimeMS = huemulResponseProvider.elapsedTimeMS
        self.transactionId = huemulResponseProvider.transactionId
        # api response version
        self.apiVersion = huemulResponseProvider.apiVersion

        #error detail
        self.errors = huemulResponseProvider.errors
        #data detail
        self.dataRaw = huemulResponseProvider.dataRaw
        #extra info detail
        self.extraInfoRaw = huemulResponseProvider.extraInfoRaw

    #
    #analyze error and determine attempts strategy
    # @param result create/get/getAll response (HuemulResponseBloc type)
    # @param attempt attempt number
    # @return Boolean
    #
    def analyzeErrors(self, attempt):
        continueInLoop = True

        if (self.isSuccessful):
            #all right, exit
            continueInLoop = False
        elif (attempt < self.connectObject.huemulCommon.getTotalAttempt()):
            #send errors
            self.connectObject.huemulLogging.logMessageInfo(self.message)
            self.connectObject.huemulLogging.logMessageInfo(str(self.errors))
            try:
                errorText = ';'.join(map(lambda x: str(x["errorId"]) + ": " + x["errorTxt"],self.errors))
            except Exception as e:
                errorText = "error try to catch error: " + str(e)

            self.connectObject.huemulLogging.logMessageError("errors details: " + errorText)
            self.connectObject.huemulLogging.logMessageError("errors transaction-id: " + self.transactionId)
            #wait from second attempt
            if (attempt > 1):
                # wait 10 seconds and try to call again
                self.connectObject.huemulLogging.logMessageError("waiting 10 seconds.....")
                time.sleep(10)
            

            #get all possible errors
            connectionError = len(list(filter(lambda x: x["errorId"] == "APP-101", self.errors)))
            connectionError = -1 if connectionError == 0 else connectionError
            unAuthorizedError = len(list(filter(lambda x: x["errorId"] == "2040", self.errors))) # indexWhere(p => p.errorId == "2040")
            unAuthorizedError = -1 if unAuthorizedError == 0 else unAuthorizedError
            forbiddenError = len(list(filter(lambda x: x["errorId"] == "2030", self.errors))) # indexWhere(p => p.errorId == "2030")
            forbiddenError = -1 if forbiddenError == 0 else forbiddenError

            if (forbiddenError):
                self.connectObject.huemulLogging.logMessageError("forbidden")

            if (unAuthorizedError > -1):
                self.connectObject.huemulLogging.logMessageError("attempt " + str(attempt) + " of " + str(self.connectObject.huemulCommon.getTotalAttempt()))
                #check if error = unauthorized, try to login again
                continueInLoop = True
            elif (connectionError > -1):
                self.connectObject.huemulLogging.logMessageError("attempt " + str(attempt) + " of " + str(self.connectObject.huemulCommon.getTotalAttempt()))
                #raised error from HuemulConnection method
                continueInLoop = True
            else:
                #unknown error (maybe data), exit and return error
                continueInLoop = False

        else:
            continueInLoop = False


        return continueInLoop
    