#
# departmentId: String,
# departmentName: String,
# departmentDescription: String,
# orgId: String,

class DepartmentModel:
    def __init__(self, departmentId, departmentName, departmentDescription, orgId):
        self.departmentId = departmentId
        self.departmentName = departmentName
        self.departmentDescription = departmentDescription
        self.orgId = orgId