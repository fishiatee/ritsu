import os
from osu import AsynchronousClient, AsynchronousAuthHandler, Scope

client = AsynchronousClient(auth=AsynchronousAuthHandler(client_id=os.environ.get("RITSU_OSU_OAUTH_CLIENT_ID"),
                                                         client_secret=os.environ.get("RITSU_OSU_OAUTH_CLIENT_SECRET"),
                                                         redirect_url="RITSU_BOT",
                                                         scope=Scope.default()))

def get_client() -> AsynchronousClient:
    return client