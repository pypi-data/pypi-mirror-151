from risk_command_center.internal.riskRule.riskRule_bloc import RiskRuleBloc
from risk_command_center.internal.riskRule.riskRule_model import RiskRuleModel

#
# create new riskRule for process to calculate likelihood
# riskId: String,
# processId: String,
# riskLhId: String,
# ruleIdLocal: string,
# ruleName: string,
# ruleFormula: string,
# connection,
# ruleEnabled: bool,
# @return Boolean
#  
def createProcessLikelihoodRule(riskId, processId, riskLhId, ruleIdLocal, ruleName, ruleFormula, connection, ruleEnabled = True, raiseErrorIfFail = True):
    if (not connection.canExecute):
        connection.huemulLogging.logMessageError(message = "cant execute: ")
        return

    connection.huemulLogging.logMessageInfo(message = "creating Risk Rule at risk " + riskId + ", processId " + processId + " riskLhId: " + riskLhId + " ruleIdLocal: " + ruleIdLocal + " name: " + ruleName)

    _riskRuleModel = RiskRuleModel(
        riskId = riskId,
        ruleIdLocal = ruleIdLocal,
        ruleType = "LIKELIHOOD",
        processId = processId,
        elementId = riskLhId,
        ruleName = ruleName,
        ruleFormula = ruleFormula,
        ruleEnabled = ruleEnabled,
        orgId= connection.huemulCommon.getOrgId()
    )

    riskRuleResult = RiskRuleBloc().riskRuleCreate(riskRuleModel=_riskRuleModel,connectObject=connection)
    #if error
    if (not riskRuleResult.isSuccessful):
        connection._canExecute = False
        connection._errorMessage = riskRuleResult.message if (len(riskRuleResult.errors) == 0) else riskRuleResult.errors[0]["errorTxt"]
        connection.huemulLogging.logMessageError(message = "error in riskRule: " + connection._errorMessage)

        if (raiseErrorIfFail):
            connection.huemulLogging.logMessageError(message = "error" + connection._errorMessage)
            raise NameError(connection._errorMessage)
        else:
            connection.huemulLogging.logMessageError(message = "error" + connection._errorMessage)
            return False

    #if all ok, continue
    # return id

    return True


#
# create new riskRule for process to calculate impact
# riskId: String,
# processId: String,
# riskImpactId: String,
# ruleIdLocal: string,
# ruleName: string,
# ruleFormula: string,
# connection,
# ruleEnabled: bool,
# @return Boolean
#  
def createProcessImpactRule(riskId, processId, riskImpactId, ruleIdLocal, ruleName, ruleFormula, connection, ruleEnabled = True, raiseErrorIfFail = True):
    if (not connection.canExecute):
        connection.huemulLogging.logMessageError(message = "cant execute: ")
        return

    connection.huemulLogging.logMessageInfo(message = "creating Risk Rule at risk " + riskId + ", processId " + processId + " riskImpactId: " + riskImpactId + " ruleIdLocal: " + ruleIdLocal + " name: " + ruleName)

    _riskRuleModel = RiskRuleModel(
        riskId = riskId,
        ruleIdLocal = ruleIdLocal,
        ruleType = "IMPACT",
        processId = processId,
        elementId = riskImpactId,
        ruleName = ruleName,
        ruleFormula = ruleFormula,
        ruleEnabled = ruleEnabled,
        orgId= connection.huemulCommon.getOrgId()
    )

    riskRuleResult = RiskRuleBloc().riskRuleCreate(riskRuleModel=_riskRuleModel,connectObject=connection)
    #if error
    if (not riskRuleResult.isSuccessful):
        connection._canExecute = False
        connection._errorMessage = riskRuleResult.message if (len(riskRuleResult.errors) == 0) else riskRuleResult.errors[0]["errorTxt"]
        connection.huemulLogging.logMessageError(message = "error in riskRule: " + connection._errorMessage)

        if (raiseErrorIfFail):
            connection.huemulLogging.logMessageError(message = "error" + connection._errorMessage)
            raise NameError(connection._errorMessage)
        else:
            connection.huemulLogging.logMessageError(message = "error" + connection._errorMessage)
            return False

    #if all ok, continue
    # return id

    return True


#
# create new riskRule for risk to calculate likelihood
# riskId: String,
# riskLhId: String,
# ruleIdLocal: string,
# ruleName: string,
# ruleFormula: string,
# connection,
# ruleEnabled: bool,
# @return Boolean
#  
def createRiskLikelihoodRule(riskId, riskLhId, ruleIdLocal, ruleName, ruleFormula, connection, ruleEnabled = True, raiseErrorIfFail = True):
    if (not connection.canExecute):
        connection.huemulLogging.logMessageError(message = "cant execute: ")
        return

    connection.huemulLogging.logMessageInfo(message = "creating Risk Rule at risk " + riskId + ", riskLhId: " + riskLhId + " ruleIdLocal: " + ruleIdLocal + " name: " + ruleName)

    _riskRuleModel = RiskRuleModel(
        riskId = riskId,
        ruleIdLocal = ruleIdLocal,
        ruleType = "LIKELIHOOD",
        processId = "",
        elementId = riskLhId,
        ruleName = ruleName,
        ruleFormula = ruleFormula,
        ruleEnabled = ruleEnabled,
        orgId= connection.huemulCommon.getOrgId()
    )

    riskRuleResult = RiskRuleBloc().riskRuleCreate(riskRuleModel=_riskRuleModel,connectObject=connection)
    #if error
    if (not riskRuleResult.isSuccessful):
        connection._canExecute = False
        connection._errorMessage = riskRuleResult.message if (len(riskRuleResult.errors) == 0) else riskRuleResult.errors[0]["errorTxt"]
        connection.huemulLogging.logMessageError(message = "error in riskRule: " + connection._errorMessage)

        if (raiseErrorIfFail):
            connection.huemulLogging.logMessageError(message = "error" + connection._errorMessage)
            raise NameError(connection._errorMessage)
        else:
            connection.huemulLogging.logMessageError(message = "error" + connection._errorMessage)
            return False

    #if all ok, continue
    # return id

    return True


#
# create new riskRule for risk to calculate impact
# riskId: String,
# riskImpactId: String,
# ruleIdLocal: string,
# ruleName: string,
# ruleFormula: string,
# connection,
# ruleEnabled: bool,
# @return Boolean
#  
def createRiskImpactRule(riskId, riskImpactId, ruleIdLocal, ruleName, ruleFormula, connection, ruleEnabled = True, raiseErrorIfFail = True):
    if (not connection.canExecute):
        connection.huemulLogging.logMessageError(message = "cant execute: ")
        return

    connection.huemulLogging.logMessageInfo(message = "creating Risk Rule at risk " + riskId + ", riskImpactId: " + riskImpactId + " ruleIdLocal: " + ruleIdLocal + " name: " + ruleName)

    _riskRuleModel = RiskRuleModel(
        riskId = riskId,
        ruleIdLocal = ruleIdLocal,
        ruleType = "IMPACT",
        processId = "",
        elementId = riskImpactId,
        ruleName = ruleName,
        ruleFormula = ruleFormula,
        ruleEnabled = ruleEnabled,
        orgId= connection.huemulCommon.getOrgId()
    )

    riskRuleResult = RiskRuleBloc().riskRuleCreate(riskRuleModel=_riskRuleModel,connectObject=connection)
    #if error
    if (not riskRuleResult.isSuccessful):
        connection._canExecute = False
        connection._errorMessage = riskRuleResult.message if (len(riskRuleResult.errors) == 0) else riskRuleResult.errors[0]["errorTxt"]
        connection.huemulLogging.logMessageError(message = "error in riskRule: " + connection._errorMessage)

        if (raiseErrorIfFail):
            connection.huemulLogging.logMessageError(message = "error" + connection._errorMessage)
            raise NameError(connection._errorMessage)
        else:
            connection.huemulLogging.logMessageError(message = "error" + connection._errorMessage)
            return False

    #if all ok, continue
    # return id

    return True