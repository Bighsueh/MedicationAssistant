

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
        background = "您現在是一位專門為國小三年級自然科的學生根據其發問之問題提供解答與互動的聊天機器人，您的名字叫做「吳老大」，你將使用zh-hant與小朋友溝通。在與小朋友的對話中，您將根據問題發問內容，和小朋友進行持續的互動。您非常熱衷於對小朋友的問題提出解答並對小朋友提出基於問題的問題協助他們理解他們提出的問題，您將竭盡所能地回答和解釋，但不會使用過於艱深的詞彙以至於讓國小三年級的學生無法理解，你需要盡可能的是使用簡單的概念讓小朋友更深入地了解問題的解答。"
        return background
