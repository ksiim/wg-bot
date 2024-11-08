

from models.dbs.models import User
from models.dbs.orm import Orm
from utils.wireguard import WireGuard


async def delete_unsubscribed_people():
    users = await Orm.get_users_with_ended_subscription()
    wg = WireGuard()
    for user in users:
        await disconnect_user(user.telegram_id, wg)
    
async def disconnect_user(user: User, wg: WireGuard):
    user_public_key = user.public_key
    if user_public_key is None:
        return
    await Orm.update_public_key(user.telegram_id, None)
    await Orm.unsubscribe_user(user.telegram_id)
    wg.remove_peer_from_server_config(user_public_key)