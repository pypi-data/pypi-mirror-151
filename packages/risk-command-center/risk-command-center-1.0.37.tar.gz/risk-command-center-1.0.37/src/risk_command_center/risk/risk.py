from risk_command_center.internal.risk.risk_bloc import RiskBloc
from risk_command_center.internal.risk.risk_model import RiskModel

#
# create new risk
# @param riskId: String,
# @param departmentId: String,
# @param riskTypeId: String,
# @param userEmail: String,
# @param riskName: String,
# @param riskSource: String,
# @param riskEffect: String,
# @param riskTrigger: String,
# @param riskCrossArea: Bool,
# @param riskDate: Date
# @return Boolean
#  
def create(riskId, departmentId, riskTypeId, userEmail, riskName, riskSource, riskEffect, riskTrigger, riskCrossArea, riskDate, connection, raiseErrorIfFail = True):
    if (not connection.canExecute):
        connection.huemulLogging.logMessageError(message = "cant execute: ")
        return

    connection.huemulLogging.logMessageInfo(message = "creating risk Id: " + riskId)

    _riskModel = RiskModel(
        riskId = riskId, 
        departmentId = departmentId,
        riskTypeId = riskTypeId, 
        userEmail = userEmail, 
        riskName = riskName, 
        riskSource = riskSource, 
        riskEffect = riskEffect, 
        riskTrigger = riskTrigger, 
        riskCrossArea = riskCrossArea, 
        riskDate = riskDate,
        orgId= connection.huemulCommon.getOrgId(),
    )

    riskResult = RiskBloc().riskCreate(RiskModel=_riskModel,connectObject=connection)
    #if error
    if (not riskResult.isSuccessful):
        connection._canExecute = False
        connection._errorMessage = riskResult.message if (len(riskResult.errors) == 0) else riskResult.errors[0]["errorTxt"]
        connection.huemulLogging.logMessageError(message = "error in risk: " + connection._errorMessage)

        if (raiseErrorIfFail):
            connection.huemulLogging.logMessageError(message = "error" + connection._errorMessage)
            raise NameError(connection._errorMessage)
        else:
            connection.huemulLogging.logMessageError(message = "error" + connection._errorMessage)
            return False

    #if all ok, continue
    # connectObject._processExecStepId = riskResult.data[0].processExecStepId

    return True