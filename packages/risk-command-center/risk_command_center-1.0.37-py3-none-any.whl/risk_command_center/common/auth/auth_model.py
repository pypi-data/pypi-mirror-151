
# consumerId: String,
# consumerSecret: String,
# orgId: String,
# applicationName: String,
# urlService: String
class AuthModel:
    def __init__(self, consumerId = "", consumerSecret = "", orgId = "", applicationName = "", urlService = "", sessionId = ""):
        self.consumerId = consumerId
        self.consumerSecret = consumerSecret
        self.orgId = orgId
        self.applicationName = applicationName
        self.urlService = urlService
        self.sessionId = sessionId
        