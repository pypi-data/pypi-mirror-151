#
# departmentId: String,
#
class DepartmentResponseModel:
    def __init__(self, departmentId, **args):
        self.departmentId = departmentId
        self.args = args