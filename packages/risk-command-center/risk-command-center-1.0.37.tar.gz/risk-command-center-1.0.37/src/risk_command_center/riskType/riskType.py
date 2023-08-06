from risk_command_center.internal.riskType.riskType_bloc import RiskTypeBloc
from risk_command_center.internal.riskType.riskType_model import RiskTypeModel

#
# create new riskType
# @param riskTypeId: String,
# @param riskTypeName: String,
# @return Boolean
#  
def create(riskTypeId, riskTypeName, connection, raiseErrorIfFail = True):
    if (not connection.canExecute):
        connection.huemulLogging.logMessageError(message = "cant execute: ")
        return

    connection.huemulLogging.logMessageInfo(message = "creating riskType Id: " + riskTypeId)

    _riskTypeModel = RiskTypeModel(
        riskTypeId = riskTypeId, 
        riskTypeName = riskTypeName, 
        orgId= connection.huemulCommon.getOrgId(),
    )

    riskTypeResult = RiskTypeBloc().riskTypeCreate(riskTypeModel=_riskTypeModel,connectObject=connection)
    #if error
    if (not riskTypeResult.isSuccessful):
        connection._canExecute = False
        connection._errorMessage = riskTypeResult.message if (len(riskTypeResult.errors) == 0) else riskTypeResult.errors[0]["errorTxt"]
        connection.huemulLogging.logMessageError(message = "error in riskType: " + connection._errorMessage)

        if (raiseErrorIfFail):
            connection.huemulLogging.logMessageError(message = "error" + connection._errorMessage)
            raise NameError(connection._errorMessage)
        else:
            connection.huemulLogging.logMessageError(message = "error" + connection._errorMessage)
            return False

    #if all ok, continue
    # return id

    return True