import asyncio
from aiohttp import web
from botbuilder.schema import Activity
from botbuilder.core import BotFrameworkAdapter
from botbuilder.core.integration import aiohttp_error_middleware
from botframework.connector.auth import MicrosoftIdentityCredential
from botbuilder.azure import BotFrameworkAuthentication

APP_ID = 'fef5a24b-2311-40bc-a820-78b7b8421ba1'
APP_PASSWORD = 'cmP8Q~rOKmgqvhhCeZrwZAT4~YEiXsbSaBqPdb1h'
DIRECT_LINE_SECRET = 'yAV2dFV2r7E.fmaSa2EJD0Aj3pS53IGuiFHZ7E0lKyoiEkifslQMrPQ'

loop = asyncio.get_event_loop()

bot_framework_authentication = BotFrameworkAuthentication(APP_ID, APP_PASSWORD)
bot_adapter = BotFrameworkAdapter(bot_framework_authentication)

async def on_receive_activity(activity: Activity):
    # Your bot's logic here
    pass

async def receive_bot_framework_activities(request: web.Request):
    auth_header = request.headers.get('Authorization')
    if auth_header is None:
        return web.Response(status=401)

    channel_provider = bot_framework_authentication.get_channel_provider()
    credentials = MicrosoftIdentityCredential(auth_header, channel_provider)
    claims_identity = await credentials.get_claims_identity()
    activity = await request.json()
    response = await bot_adapter.process_activity(activity, claims_identity, on_receive_activity)
    return web.Response(status=response.status, headers=response.headers, content_type=response.content_type, body=response.body)

app = web.Application(middlewares=[aiohttp_error_middleware])
app.router.add_post('/api/messages', receive_bot_framework_activities)

if __name__ == '__main__':
    web.run_app(app, port=3978)
