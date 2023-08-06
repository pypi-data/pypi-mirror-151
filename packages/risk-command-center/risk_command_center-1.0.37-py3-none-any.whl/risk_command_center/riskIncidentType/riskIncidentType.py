from risk_command_center.internal.riskIncidentType.riskIncidentType_bloc import RiskIncidentTypeBloc
from risk_command_center.internal.riskIncidentType.riskIncidentType_model import RiskIncidentTypeModel

#
# create new riskIncidentType
# ritIdUser: String,
# ritName: String,
# ritDescription: String,
# riskId: string,
# riskImpactId: string,
# @return Boolean
#  
def create(ritIdUser, ritName, ritDescription, riskId, riskImpactId, connection, raiseErrorIfFail = True):
    if (not connection.canExecute):
        connection.huemulLogging.logMessageError(message = "cant execute: ")
        return

    connection.huemulLogging.logMessageInfo(message = "creating Risk Incident Type Id: " + ritIdUser)

    _riskIncidentTypeModel = RiskIncidentTypeModel(
        ritIdUser = ritIdUser, 
        ritName = ritName, 
        ritDescription = ritDescription, 
        riskId = riskId,
        riskImpactId = riskImpactId,
        orgId= connection.huemulCommon.getOrgId(),
    )

    riskIncidentTypeResult = RiskIncidentTypeBloc().riskIncidentTypeCreate(riskIncidentTypeModel=_riskIncidentTypeModel,connectObject=connection)
    #if error
    if (not riskIncidentTypeResult.isSuccessful):
        connection._canExecute = False
        connection._errorMessage = riskIncidentTypeResult.message if (len(riskIncidentTypeResult.errors) == 0) else riskIncidentTypeResult.errors[0]["errorTxt"]
        connection.huemulLogging.logMessageError(message = "error in riskIncidentType: " + connection._errorMessage)

        if (raiseErrorIfFail):
            connection.huemulLogging.logMessageError(message = "error" + connection._errorMessage)
            raise NameError(connection._errorMessage)
        else:
            connection.huemulLogging.logMessageError(message = "error" + connection._errorMessage)
            return False

    #if all ok, continue
    # return id

    return True