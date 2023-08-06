from risk_command_center.internal.territory.territory_bloc import TerritoryBloc
from risk_command_center.internal.territory.territory_model import TerritoryModel

#
# create new territory
# @param territoryId: String,
# @param territoryName: String,
# @param territoryAddress: String,
# @return Boolean
#  
def create(territoryId, territoryName, territoryAddress, connection, raiseErrorIfFail = True):
    if (not connection.canExecute):
        connection.huemulLogging.logMessageError(message = "cant execute: ")
        return

    connection.huemulLogging.logMessageInfo(message = "creating territory Id: " + territoryId)

    _territoryModel = TerritoryModel(
        territoryId = territoryId, 
        territoryName = territoryName, 
        territoryAddress = territoryAddress, 
        orgId= connection.huemulCommon.getOrgId(),
    )

    territoryResult = TerritoryBloc().territoryCreate(territoryModel=_territoryModel,connectObject=connection)
    #if error
    if (not territoryResult.isSuccessful):
        connection._canExecute = False
        connection._errorMessage = territoryResult.message if (len(territoryResult.errors) == 0) else territoryResult.errors[0]["errorTxt"]
        connection.huemulLogging.logMessageError(message = "error in territory: " + connection._errorMessage)

        if (raiseErrorIfFail):
            connection.huemulLogging.logMessageError(message = "error" + connection._errorMessage)
            raise NameError(connection._errorMessage)
        else:
            connection.huemulLogging.logMessageError(message = "error" + connection._errorMessage)
            return False

    #if all ok, continue
    # return id

    return True