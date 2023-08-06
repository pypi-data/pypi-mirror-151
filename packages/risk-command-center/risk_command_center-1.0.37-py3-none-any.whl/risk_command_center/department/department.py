from risk_command_center.internal.department.department_bloc import DepartmentBloc
from risk_command_center.internal.department.department_model import DepartmentModel

#
# create new department
# @param departmentId: String,
# @param departmentName: String,
# @param departmentDescription: String,
# @return Boolean
#  
def create(departmentId, departmentName, departmentDescription, connection, raiseErrorIfFail = True):
    if (not connection.canExecute):
        connection.huemulLogging.logMessageError(message = "cant execute: ")
        return

    connection.huemulLogging.logMessageInfo(message = "creating department Id: " + departmentId)

    _departmentModel = DepartmentModel(
        departmentId = departmentId, 
        departmentName = departmentName, 
        departmentDescription = departmentDescription, 
        orgId= connection.huemulCommon.getOrgId(),
    )

    departmentResult = DepartmentBloc().departmentCreate(departmentModel=_departmentModel,connectObject=connection)
    #if error
    if (not departmentResult.isSuccessful):
        connection._canExecute = False
        connection._errorMessage = departmentResult.message if (len(departmentResult.errors) == 0) else departmentResult.errors[0]["errorTxt"]
        connection.huemulLogging.logMessageError(message = "error in department: " + connection._errorMessage)

        if (raiseErrorIfFail):
            connection.huemulLogging.logMessageError(message = "error" + connection._errorMessage)
            raise NameError(connection._errorMessage)
        else:
            connection.huemulLogging.logMessageError(message = "error" + connection._errorMessage)
            return False

    #if all ok, continue
    # return id

    return True