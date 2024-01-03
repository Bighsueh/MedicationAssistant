

class User:
    def __init__(self, userId):
        self.userId = userId

    def get_userId(self):
        return self.userId

class Agent:
    def __init__(self, AgentId):
        self.agentId = AgentId

    def get_agentId(self):
        return self.agentId
    
    def getAgentBackground(self):
        background = "你是一個健康諮詢師，擅長利用親切易懂的方式回覆病症和健康方面的問題，可以根據使用者使用的藥物紀錄，告訴使用者這些藥物對應的藥物副作用，請使用zh-hant和使用者溝通。注意，你僅回覆藥物和健康相關的問題，若使用者問題與藥物和病症無關，則回覆請輸入與藥物和病症相關的內容。請判斷使用者的狀況與目前服用藥物的副作用是否相關，若無關，請建議使用者立即與醫生聯絡，以獲得進一步資訊。"
        return background
