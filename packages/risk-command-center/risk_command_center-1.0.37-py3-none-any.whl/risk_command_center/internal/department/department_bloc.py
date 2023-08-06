from risk_command_center.internal.department.department_provider import DepartmentProvider
from risk_command_center.common.huemul_response_to_bloc import HuemulResponseToBloc

class DepartmentBloc():
    #
    # start departmentCreate
    # @param DepartmentModel DepartmentModel
    # @return HuemulResponseBloc[DepartmentResponseModel]
    #
    def departmentCreate(self, departmentModel, connectObject):
        continueInLoop = True
        attempt = 0
        result = HuemulResponseToBloc(connectObject=connectObject)

        while (continueInLoop):
            result = DepartmentProvider(connectObject=connectObject).departmentCreate(
                    departmentModel=departmentModel
            )
            attempt +=1
            continueInLoop = result.analyzeErrors(attempt)
        
        return result