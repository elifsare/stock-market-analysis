from langchain.tools import BaseTool
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os

class SlackNotifier(BaseTool):
    name = "slack_notifier"
    description = "Send notifications to Slack channel"

    def __init__(self):
        self.client = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))
        self.default_channel = os.getenv('SLACK_CHANNEL', '#market-alerts')

    def _run(self, message: str, channel: str = None) -> str:
        try:
            response = self.client.chat_postMessage(
                channel=channel or self.default_channel,
                text=message
            )
            return f"Message sent successfully: {response['ts']}"
        except SlackApiError as e:
            return f"Error sending message: {str(e)}"

    async def _arun(self, message: str) -> str:
        raise NotImplementedError("Async not implemented")
