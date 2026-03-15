import os
from osu import AsynchronousClient, AsynchronousAuthHandler, Scope

client = AsynchronousClient(auth=AsynchronousAuthHandler(client_id=os.environ.get("RITSU_OSU_OAUTH_CLIENT_ID"),
                                                         client_secret=os.environ.get("RITSU_OSU_OAUTH_CLIENT_SECRET"),
                                                         redirect_url="WE_DO_NOT_NEED_THIS",
                                                         scope=Scope.default()))

def get_client() -> AsynchronousClient:
    return client