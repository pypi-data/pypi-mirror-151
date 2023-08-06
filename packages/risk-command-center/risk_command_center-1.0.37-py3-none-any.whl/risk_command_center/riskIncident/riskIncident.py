from risk_command_center.internal.riskIncident.riskIncident_bloc import RiskIncidentBloc
from risk_command_center.internal.riskIncident.riskIncident_model import RiskIncidentModel

#
# create new riskIncident
# ritIdUser: String,
# ritName: String,
# ritDescription: String,
# riskId: string,
# riskImpactId: string,
# @return Boolean
#  
def create(riskId, territoryId, riskIncidentName, riskIncidentPeriod, riskIncidentDate, riskIncidentMode, riskIncidentMoney, riskIncidentValue, connection, ritId="", ritIdUser="", riskControlId="", riskAssetId="", riskIncidentExternalId="", riskIncidentInfo="", riskIncidentIp="", riskIncidentDescription="", raiseErrorIfFail = True):
    if (not connection.canExecute):
        connection.huemulLogging.logMessageError(message = "cant execute: ")
        return

    connection.huemulLogging.logMessageInfo(message = "creating Risk Incident at risk " + riskId + ", territory " + territoryId + " name: " + riskIncidentName)

    _riskIncidentModel = RiskIncidentModel(
        riskId = riskId,
        territoryId = territoryId,
        riskControlId = riskControlId,
        riskAssetId = riskAssetId,
        riskIncidentName = riskIncidentName,
        riskIncidentDescription = riskIncidentDescription,
        riskIncidentPeriod = riskIncidentPeriod,
        riskIncidentDate = riskIncidentDate,
        riskIncidentMode = riskIncidentMode,
        riskIncidentExternalId = riskIncidentExternalId,
        riskIncidentInfo = riskIncidentInfo,
        riskIncidentIp = riskIncidentIp,
        riskIncidentMoney = riskIncidentMoney,
        riskIncidentValue = riskIncidentValue,
        ritId = ritId,
        ritIdUser = ritIdUser,
        orgId= connection.huemulCommon.getOrgId(),
    )

    riskIncidentResult = RiskIncidentBloc().riskIncidentCreate(riskIncidentModel=_riskIncidentModel,connectObject=connection)
    #if error
    if (not riskIncidentResult.isSuccessful):
        connection._canExecute = False
        connection._errorMessage = riskIncidentResult.message if (len(riskIncidentResult.errors) == 0) else riskIncidentResult.errors[0]["errorTxt"]
        connection.huemulLogging.logMessageError(message = "error in riskIncident: " + connection._errorMessage)

        if (raiseErrorIfFail):
            connection.huemulLogging.logMessageError(message = "error" + connection._errorMessage)
            raise NameError(connection._errorMessage)
        else:
            connection.huemulLogging.logMessageError(message = "error" + connection._errorMessage)
            return False

    #if all ok, continue
    # return id

    return True