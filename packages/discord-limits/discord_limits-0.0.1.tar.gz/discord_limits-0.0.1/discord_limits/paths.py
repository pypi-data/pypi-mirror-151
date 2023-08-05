from .errors import *
import discord_limits.objects as DiscordObjects

class Paths:

    """
    Audit Log
    """

    async def get_audit_logs(self, guild_id, limit = 50, before = None, after = None, user_id = None, action_type = None):
        if 1 > limit or limit > 100:
            raise InvalidParams('limit must be between 1 and 100')

        path = f'/guilds/{guild_id}/audit-logs'
        bucket = 'GET' + path
        
        params = {'limit': limit}
        if before is not None:
            params['before'] = before
        if after is not None:
            params['after'] = after
        if user_id is not None:
            params['user_id'] = user_id
        if action_type is not None:
            params['action_type'] = action_type

        return await self._request('GET', path, bucket, params=params)

    """
    Channel
    """

    async def get_channel(self, channel_id):
        path = f'/channels/{channel_id}'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def edit_channel(self, channel_id, reason = None, **options):
        path = f'/channels/{channel_id}'
        bucket = 'PATCH' + path
        valid_keys = (
            'name',
            'parent_id',
            'topic',
            'bitrate',
            'nsfw',
            'user_limit',
            'position',
            'permission_overwrites',
            'rate_limit_per_user',
            'type',
            'rtc_region',
            'video_quality_mode',
            'archived',
            'auto_archive_duration',
            'locked',
            'invitable',
            'default_auto_archive_duration',
            'flags',
        )
        payload = {k: v for k, v in options.items() if k in valid_keys}
        return await self._request('PATCH', path, bucket, json=payload, headers={'X-Audit-Log-Reason': reason})

    async def delete_channel(self, channel_id, reason = None):
        path = f'/channels/{channel_id}'
        bucket = 'DELETE' + path
        return await self._request('DELETE', path, bucket, headers={'X-Audit-Log-Reason': reason})
        
    async def get_channel_messages(self, channel_id, limit=50, before = None, after = None, around = None):
        path = f'/channels/{channel_id}/messages'
        bucket = 'GET' + path
        if 1 > limit or limit > 100:
            raise InvalidParams('limit must be between 1 and 100')
        
        params = {
            'limit': limit,
        }

        if before is not None:
            params['before'] = before
        if after is not None:
            params['after'] = after
        if around is not None:
            params['around'] = around

        return await self._request('GET', path, bucket, params=params)
    
    async def get_message(self, channel_id, message_id):
        path = f'/channels/{channel_id}/messages/{message_id}'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def create_message(self, channel_id, content = None, tts=None, embeds = None, allowed_mentions = None, message_reference = None, components = None, sticker_ids = None):
        path = f'/channels/{channel_id}/messages'
        bucket = 'POST' + path

        if content is None and embeds is None and sticker_ids is None:
            raise InvalidParams('content, embeds or sticker_ids must be provided')

        payload = {}

        if content is not None:
            payload['content'] = content
        if tts is not None:
            payload['tts'] = tts
        if embeds is not None:
            payload['embeds'] = embeds
        if allowed_mentions is not None:
            payload['allowed_mentions'] = allowed_mentions
        if message_reference is not None:
            payload['message_reference'] = message_reference
        if components is not None:
            payload['components'] = components
        if sticker_ids is not None:
            payload['sticker_ids'] = sticker_ids
        
        return await self._request('POST', path, bucket, json=payload)

    async def crosspost_message(self, channel_id, message_id):
        path = f'/channels/{channel_id}/messages/{message_id}/crosspost'
        bucket = 'POST' + path
        return await self._request('POST', path, bucket)

    async def add_reaction(self, channel_id, message_id, emoji):
        path = f'/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me'
        bucket = 'PUT' + path
        return await self._request('PUT', path, bucket)

    async def remove_own_reaction(self, channel_id, message_id, emoji):
        path = f'/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me'
        bucket = 'DELETE' + path
        return await self._request('DELETE', path, bucket)

    async def remove_reaction(self, channel_id, message_id, emoji, member_id):
        path = f'/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/{member_id}'
        bucket = 'DELETE' + path
        return await self._request('DELETE', path, bucket)

    async def get_reactions(self, channel_id, message_id, emoji, limit=25, after = None):
        path = f'/channels/{channel_id}/messages/{message_id}/reactions/{emoji}'
        bucket = 'GET' + path
        params = {
            'limit': limit,
        }
        if after is not None:
            params['after'] = after
        
        return await self._request('GET', path, bucket, params=params)

    async def clear_reactions(self, channel_id, message_id):
        path = f'/channels/{channel_id}/messages/{message_id}/reactions'
        bucket = 'DELETE' + path
        return await self._request('DELETE', path, bucket)

    async def clear_single_reaction(self, channel_id, message_id, emoji):
        path = f'/channels/{channel_id}/messages/{message_id}/reactions/{emoji}'
        bucket = 'DELETE' + path
        return await self._request('DELETE', path, bucket)

    async def edit_message(self, channel_id, message_id, content = None, embeds = None, allowed_mentions = None, components = None):
        path = f'/channels/{channel_id}/messages/{message_id}'
        bucket = 'PATCH' + path
        payload = {}

        if content is not None:
            payload['content'] = content
        if embeds is not None:
            payload['embeds'] = embeds
        if allowed_mentions is not None:
            payload['allowed_mentions'] = allowed_mentions
        if components is not None:
            payload['components'] = components
        
        self._request('PATCH', path, bucket, json=payload)

    async def delete_message(self, channel_id, message_id, reason = None):
        path = f'/channels/{channel_id}/messages/{message_id}'
        bucket = 'DELETE' + path
        return await self._request('DELETE', path, bucket, headers={'X-Audit-Log-Reason': reason})

    async def bulk_delete_messages(self, channel_id, message_ids, reason = None):
        path = f'/channels/{channel_id}/messages/bulk-delete'
        bucket = 'POST' + path
        payload = {
            'messages': message_ids,
        }
        return await self._request('POST', path, bucket, json=payload, headers={'X-Audit-Log-Reason': reason})

    async def edit_channel_permissions(self, channel_id, target, allow, deny, type, reason = None):
        path = f'/channels/{channel_id}/permissions/{target}'
        bucket = 'PUT' + path
        payload = {'id': target, 'allow': allow, 'deny': deny, 'type': type}
        return await self._request('PUT', path, bucket, json=payload, headers={'X-Audit-Log-Reason': reason})

    async def get_channel_invites(self, channel_id):
        path = f'/channels/{channel_id}/invites'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def create_channel_invite(self, channel_id, *, reason = None, max_age = 0, max_uses = 0, temporary = False, unique = True, target_type = None, target_user_id = None, target_application_id = None):
        path = f'/channels/{channel_id}/invites'
        bucket = 'POST' + path
        payload = {
            'max_age': max_age,
            'max_uses': max_uses,
            'temporary': temporary,
            'unique': unique,
        }

        if target_type:
            payload['target_type'] = target_type

        if target_user_id:
            payload['target_user_id'] = target_user_id

        if target_application_id:
            payload['target_application_id'] = str(target_application_id)

        return await self._request('POST', path, bucket, json=payload, headers={'X-Audit-Log-Reason': reason})

    async def delete_channel_permissions(self, channel_id, target, reason = None):
        path = f'/channels/{channel_id}/permissions/{target}'
        bucket = 'DELETE' + path
        return await self._request('DELETE', path, bucket, headers={'X-Audit-Log-Reason': reason})

    async def follow_news_channel(self, channel_id, webhook_channel_id, reason = None):
        path = f'/channels/{channel_id}/followers'
        bucket = 'POST' + path
        payload = {
            'webhook_channel_id'(webhook_channel_id),
        }
        return await self._request('POST', path, bucket, json=payload, headers={'X-Audit-Log-Reason': reason})

    async def start_typing(self, channel_id):
        path = f'/channels/{channel_id}/typing'
        bucket = 'POST' + path
        return await self._request('POST', path, bucket)

    async def get_pinned_messages(self, channel_id):
        path = f'/channels/{channel_id}/pins'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def pin_message(self, channel_id, message_id, reason = None):
        path = f'/channels/{channel_id}/pins/{message_id}'
        bucket = 'PUT' + path
        return await self._request('PUT', path, bucket, headers={'X-Audit-Log-Reason': reason})

    async def unpin_message(self, channel_id, message_id, reason = None):
        path = f'/channels/{channel_id}/pins/{message_id}'
        bucket = 'DELETE' + path
        return await self._request('DELETE', path, bucket, headers={'X-Audit-Log-Reason': reason})
    
    async def add_group_recipient(self, channel_id, user_id, access_token, nickname = None):
        path = f'/channels/{channel_id}/recipients/{user_id}'
        bucket = 'PUT' + path
        payload = {
            'access_token': access_token,
            'nick': nickname
        }
        return await self._request

    async def remove_group_recipient(self, channel_id, user_id):
        path = f'/channels/{channel_id}/recipients/{user_id}'
        bucket = 'DELETE' + path
        return await self._request('DELETE', path, bucket)

    async def start_thread_with_message(self, channel_id, message_id, *, name, auto_archive_duration, rate_limit_per_user, reason = None):
        path = f'/channels/{channel_id}/messages/{message_id}/threads'
        bucket = 'POST' + path
        payload = {
            'name': name,
            'auto_archive_duration': auto_archive_duration,
            'rate_limit_per_user': rate_limit_per_user,
        }

        return await self._request('POST', path, bucket, json=payload, headers={'X-Audit-Log-Reason': reason})

    async def start_thread_without_message(self, channel_id, name, auto_archive_duration, type, invitable = True, rate_limit_per_user = None, reason = None):
        path = f'/channels/{channel_id}/threads'
        bucket = 'POST' + path
        payload = {
            'name': name,
            'auto_archive_duration': auto_archive_duration,
            'type': type,
            'invitable': invitable,
            'rate_limit_per_user': rate_limit_per_user,
        }

        return await self._request('POST', path, bucket, json=payload, headers={'X-Audit-Log-Reason': reason})

    async def start_thread_in_forum(self, channel_id, name, auto_archive_duration, rate_limit_per_user = None, reason = None, **message):
        path = f'/channels/{channel_id}/threads'
        bucket = 'POST' + path
        if message.get('content') is None and message.get('embeds') is None and message.get('sticker_ids') is None:
            raise InvalidParams('content, embeds or sticker_ids must be provided for the message')
        elif auto_archive_duration == 60 or auto_archive_duration == 1440 or auto_archive_duration == 4320 or auto_archive_duration == 10080:
            raise InvalidParams('auto_archive_duration must equal to 60, 1440, 4320 or 10080')
        elif 0 > rate_limit_per_user or rate_limit_per_user > 21600:
            raise InvalidParams('rate_limit_per_user must be between 0 and 21600')
        valid_message_keys = (
            'content',
            'embeds',
            'allowed_mentions',
            'components',
            'sticker_ids',
        )
        payload = {
            'name': name[:100],
            'auto_archive_duration': auto_archive_duration,
            'rate_limit_per_user': rate_limit_per_user,
        }
        payload['message'] = {k: v for k, v in message.items() if k in valid_message_keys}
        return await self._request('POST', path, bucket, json=payload, headers={'X-Audit-Log-Reason': reason})

    async def join_thread(self, channel_id):
        path = f'/channels/{channel_id}/thread-members/@me'
        bucket = 'PUT' + path
        return await self._request('PUT', path, bucket)

    async def add_user_to_thread(self, channel_id, user_id):
        path = f'/channels/{channel_id}/thread-members/{user_id}'
        bucket = 'PUT' + path
        return await self._request('PUT', path, bucket)

    async def leave_thread(self, channel_id):
        path = f'/channels/{channel_id}/thread-members/@me'
        bucket = 'DELETE' + path
        return await self._request('DELETE', path, bucket)

    async def remove_user_from_thread(self, channel_id, user_id):
        path = f'/channels/{channel_id}/thread-members/{user_id}'
        bucket = 'DELETE' + path
        return await self._request('DELETE', path, bucket)
    
    async def get_thread_member(self, channel_id, user_id):
        path = f'/channels/{channel_id}/thread-members/{user_id}'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def get_thread_members(self, channel_id):
        path = f'/channels/{channel_id}/thread-members'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def get_public_archived_threads(self, channel_id, before = None, limit = 50):
        path = f'/channels/{channel_id}/threads/archived/public'
        bucket = 'GET' + path

        params = {}
        if before:
            params['before'] = before
        params['limit'] = limit
        return await self._request('GET', path, bucket, params=params)

    async def get_private_archived_threads(self, channel_id, before = None, limit = 50):
        path = f'/channels/{channel_id}/threads/archived/private'
        bucket = 'GET' + path

        params = {}
        if before:
            params['before'] = before
        params['limit'] = limit
        return await self._request('GET', path, bucket, params=params)

    async def get_joined_private_archived_threads(self, channel_id, before = None, limit = 50):
        path = f'/channels/{channel_id}/users/@me/threads/archived/private'
        bucket = 'GET' + path
        params = {}
        if before:
            params['before'] = before
        params['limit'] = limit
        return await self._request('GET', path, bucket, params=params)

    """
    Emoji
    """

    async def get_guild_emojis(self, guild_id):
        path = f'/guilds/{guild_id}/emojis'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def get_guild_emoji(self, guild_id, emoji_id):
        path = f'/guilds/{guild_id}/emojis/{emoji_id}'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    """
    async def create_guild_emoji(self, guild_id, name,image, *, roles = None, reason = None):
        payload = {
            'name': name,
            'image': image,
            'roles': roles or [],
        }

        r = Route('POST', '/guilds/{guild_id}/emojis', guild_id=guild_id)
        return await self._request(r, json=payload, reason=reason)
    """

    async def edit_custom_emoji(self, guild_id, emoji_id, name=None, roles=None, reason = None):
        path = f'/guilds/{guild_id}/emojis/{emoji_id}'
        bucket = 'PATCH' + path
        payload = {}
        if name is not None:
            payload['name'] = name
        if roles is not None:
            payload['roles'] = roles
        return await self._request('PATCH', path, bucket, json=payload, headers={'X-Audit-Log-Reason': reason})

    async def delete_custom_emoji(self, guild_id, emoji_id, reason = None):
        path = f'/guilds/{guild_id}/emojis/{emoji_id}'
        bucket = 'DELETE' + path
        return await self._request('DELETE', path, bucket, headers={'X-Audit-Log-Reason': reason})

    """
    Guild
    """

    async def create_guild(self, name, verification_level = None, default_message_notifications = None, explicit_content_filter = None, roles = None, channels = None, afk_channel_id = None, afk_timeout = None, system_channel_id = None, system_channel_flags = None):
        path = '/guilds'
        bucket = 'POST' + path
        payload = {
            'name': name,
        }
        if verification_level is not None:
            payload['verification_level'] = verification_level
        if default_message_notifications is not None:
            payload['default_message_notifications'] = default_message_notifications
        if explicit_content_filter is not None:
            payload['explicit_content_filter'] = explicit_content_filter
        if roles is not None:
            payload['roles'] = roles
        if channels is not None:
            payload['channels'] = channels
        if afk_channel_id is not None:
            payload['afk_channel_id'] = afk_channel_id
        if afk_timeout is not None:
            payload['afk_timeout'] = afk_timeout
        if system_channel_id is not None:
            payload['system_channel_id'] = system_channel_id
        if system_channel_flags is not None:
            payload['system_channel_flags'] = system_channel_flags        

        return await self._request('POST', path, bucket, json=payload)

    async def get_guild(self, guild_id, with_counts = True):
        path = f'/guilds/{guild_id}'
        bucket = 'GET' + path
        params = {'with_counts': with_counts}
        return await self._request('GET', path, bucket, params=params)

    async def get_guild_preview(self, guild_id):
        path = f'/guilds/{guild_id}/preview'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def edit_guild(self, guild_id, reason=None, **options):
        path = f'/guilds/{guild_id}'
        bucket = 'PATCH' + path

        payload = {}

        valid_keys = (
            'name',
            'region',
            'verification_level',
            'default_message_notifications',
            'explicit_content_filter',
            'afk_channel_id',
            'afk_timeout',
            'owner_id',
            'system_channel_id',
            'system_channel_flags',
            'rules_channel_id',
            'public_updates_channel_id',
            'preferred_locale',
            'features',
            'description',
            'premium_progress_bar_enabled',
        )
        payload.update({k: v for k, v in options.items() if k in valid_keys and v is not None})     

        self._request('PATCH', path, bucket, json=payload, headers={'X-Audit-Log-Reason': reason})

    async def delete_guild(self, guild_id):
        path = f'/guilds/{guild_id}'
        bucket = 'DELETE' + path
        return await self._request('DELETE', path, bucket)

    async def get_guild_channels(self, guild_id):
        path = f'/guilds/{guild_id}/channels'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def create_channel(self, guild_id, name, *, reason = None, **options):

        path = f'/guilds/{guild_id}/channels'
        bucket = 'POST' + path

        payload = {
            'name': name,
        }

        valid_keys = (
            'type',
            'topic',
            'bitrate',
            'user_limit',
            'rate_limit_per_user',
            'position',
            'permission_overwrites',
            'parent_id',
            'nsfw',
            'default_auto_archive_duration',
        )
        payload.update({k: v for k, v in options.items() if k in valid_keys and v is not None})

        return await self._request('POST', path, bucket, json=payload, headers={'X-Audit-Log-Reason': reason})

    async def edit_channel_position(self, guild_id, channel_id, position, sync_permissions, parent_id, reason = None):
        path = f'/guilds/{guild_id}/channels'
        bucket = 'PATCH' + path

        payload = {
            'id': channel_id,
            'position': position,
            'lock_permissions': sync_permissions,
            'parent_id': parent_id
        }

        return await self._request('PATCH', path, bucket, json=payload, headers={'X-Audit-Log-Reason': reason})

    async def get_active_threads(self, guild_id):
        path = f'/guilds/{guild_id}/threads/active'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def get_member(self, guild_id, member_id):
        path = f'/guilds/{guild_id}/members/{member_id}'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def get_members(self, guild_id, limit=1, after=None):
        if 1 > limit or limit > 1000:
            raise InvalidParams('limit must be between 1 and 1000')

        path = f'/guilds/{guild_id}/members'
        bucket = 'GET' + path

        params = {
            'limit': limit,
        }
        if after is not None:
            params['after'] = after

        return await self._request('GET', path, bucket, params=params)

    async def search_guild_members(self, guild_id, query, limit=1):
        if 1 > limit or limit > 1000:
            raise InvalidParams('limit must be between 1 and 1000')

        path = f'/guilds/{guild_id}/members/search'
        bucket = 'GET' + path

        params = {
            'limit': limit,
            'query': query,
        }
        return await self._request('GET', path, bucket, params=params)

    async def add_guild_member(self, guild_id, user_id, access_token, nick=None, roles=None, mute=False, deaf=False):
        path = f'/guilds/{guild_id}/members/{user_id}'
        bucket = 'PUT' + path

        payload = {
            'access_token': access_token,
            'mute': mute,
            'deaf': deaf
        }

        if nick is not None:
            payload['nick'] = nick
        if roles is not None:
            payload['roles'] = roles

        return await self._request('PUT', path, bucket, json=payload)

    async def modify_guild_member(self, user_id, guild_id, nick=None, roles=None, mute = None, deafen = None, channel_id=None, timeout=None, reason = None):
        path = f'/guilds/{guild_id}/members/{user_id}'
        bucket = 'PATCH' + path
        payload = {}
        if nick is not None:
            payload['nick'] = nick
        if roles is not None:
            payload['roles'] = roles
        if mute is not None:
            payload['mute'] = mute
        if deafen is not None:
            payload['deaf'] = deafen
        if channel_id is not None:
            payload['channel_id'] = channel_id
        if timeout is not None:
            payload['timeout'] = timeout

        return await self._request('PATCH', path, bucket, json=payload, headers={'X-Audit-Log-Reason': reason})

    async def modify_current_member(self, guild_id, nick, reason=None):
        path = f'/guilds/{guild_id}/members/@me'
        bucket = 'PATCH' + path
        payload = {
            'nick': nick
        }
        return await self._request('PATCH', path, bucket, json=payload, headers={'X-Audit-Log-Reason': reason})

    async def add_role(self, guild_id, user_id, role_id, reason = None):
        path = f'/guilds/{guild_id}/members/{user_id}/roles/{role_id}'
        bucket = 'PUT' + path
        return await self._request('PUT', path, bucket, headers={'X-Audit-Log-Reason': reason})

    async def remove_role(self, guild_id, user_id, role_id, *, reason = None):
        path = f'/guilds/{guild_id}/members/{user_id}/roles/{role_id}'
        bucket = 'DELETE' + path
        return await self._request('DELETE', path, bucket, headers={'X-Audit-Log-Reason': reason})

    async def kick(self, user_id, guild_id, reason = None):
        path = f'/guilds/{guild_id}/members/{user_id}'
        bucket = 'DELETE' + path
        return await self._request('DELETE', path, bucket, headers={'X-Audit-Log-Reason': reason})

    async def get_bans(self, guild_id, limit, before = None,  after = None):
        path = f'/guilds/{guild_id}/bans'
        bucket = 'GET' + path
        params = {
            'limit': limit,
        }
        if before is not None:
            params['before'] = before
        if after is not None:
            params['after'] = after

        return await self._request('GET', path, bucket, params=params)

    async def get_ban(self, user_id, guild_id):
        path = f'/guilds/{guild_id}/bans/{user_id}'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def ban(self, user_id, guild_id, delete_message_days = 0, reason = None):
        if 0 > delete_message_days or delete_message_days > 7:
            raise InvalidParams('limit must be between 0 and 7')
        
        path = f'/guilds/{guild_id}/bans/{user_id}'
        bucket = 'PUT' + path

        params = {
            'delete_message_days': delete_message_days,
        }

        return await self._request('PUT', path, bucket, params=params, headers={'X-Audit-Log-Reason': reason})

    async def unban(self, user_id, guild_id, *, reason = None):
        path = f'/guilds/{guild_id}/bans/{user_id}'
        bucket = 'DELETE' + path
        return await self._request('DELETE', path, bucket, headers={'X-Audit-Log-Reason': reason})

    async def get_roles(self, guild_id):
        path = f'/guilds/{guild_id}/roles'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def create_role(self, guild_id, name=None, permissions=None, colour=None, hoist=None, unicode_emoji=None, mentionable=None, reason = None):
        path = f'/guilds/{guild_id}/roles'
        bucket = 'POST' + path
        payload = {}
        if name is not None:
            payload['name'] = name
        if permissions is not None:
            payload['permissions'] = permissions
        if colour is not None:
            payload['color'] = colour
        if hoist is not None:
            payload['hoist'] = hoist
        if unicode_emoji is not None:
            payload['unicode_emoji'] = unicode_emoji
        if mentionable is not None:
            payload['mentionable'] = mentionable
        return await self._request('POST', path, bucket, json=payload, headers={'X-Audit-Log-Reason': reason})

    async def move_role_position(self, guild_id, role_id, position, reason = None):
        path = f'/guilds/{guild_id}/roles'
        bucket = 'PATCH' + path
        payload = {
            'id': role_id,
            'position': position
        }
        return await self._request('PATCH', path, bucket, json=payload, headers={'X-Audit-Log-Reason': reason})

    async def edit_role(self, guild_id, role_id, reason = None, **fields):
        path = f'/guilds/{guild_id}/roles/{role_id}'
        bucket = 'PATCH' + path
        valid_keys = ('name', 'permissions', 'color', 'hoist', 'unicode_emoji', 'mentionable')
        payload = {k: v for k, v in fields.items() if k in valid_keys}
        return await self._request('PATCH', path, bucket, json=payload, headers={'X-Audit-Log-Reason': reason})

    async def delete_role(self, guild_id, role_id, reason = None):
        path = f'/guilds/{guild_id}/roles/{role_id}'
        bucket = 'DELETE' + path
        return await self._request('DELETE', path, bucket, headers={'X-Audit-Log-Reason': reason})

    async def estimate_pruned_members(self, guild_id, days=7, roles=None):
        if 1 > days or days > 30:
            raise InvalidParams('days must be between 1 and 30')

        path = f'/guilds/{guild_id}/prune'
        bucket = 'GET' + path
        
        params = {
            'days': days,
        }
        if roles is not None:
            params['include_roles'] = ', '.join(roles)

        return await self._request('GET', path, bucket, params=params)

    async def prune_members(self, guild_id, days=7, compute_prune_count=False, roles=None, reason = None):
        if 1 > days or days > 30:
            raise InvalidParams('days must be between 1 and 30')

        path = f'/guilds/{guild_id}/prune'
        bucket = 'POST' + path

        payload = {
            'days': days,
            'compute_prune_count': compute_prune_count,
        }
        if roles:
            payload['include_roles'] = ', '.join(roles)

        return await self._request('POST', path, bucket, json=payload, headers={'X-Audit-Log-Reason': reason})

    async def get_voice_regions(self, guild_id):
        path = f'/guilds/{guild_id}/regions'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def get_guild_invites(self, guild_id):
        path = f'/guilds/{guild_id}/invites'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def get_guild_integrations(self, guild_id):
        path = f'/guilds/{guild_id}/integrations'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def create_integration(self, guild_id, type, id):
        path = f'/guilds/{guild_id}/integrations'
        bucket = 'POST' + path

        payload = {
            'type': type,
            'id': id,
        }

        return await self._request('POST', path, bucket, json=payload)

    async def edit_integration(self, guild_id, integration_id, **payload):
        path = f'/guilds/{guild_id}/integrations/{integration_id}'
        bucket = 'PATCH' + path

        return await self._request('PATCH', path, bucket, json=payload)

    async def sync_integration(self, guild_id, integration_id):
        path = f'/guilds/{guild_id}/integrations/{integration_id}/sync'
        bucket = 'POST' + path

        return await self._request('POST', path, bucket)

    async def delete_guild_integration(self, guild_id, integration_id, *, reason = None):
        path = f'/guilds/{guild_id}/integrations/{integration_id}'
        bucket = 'DELETE' + path

        return await self._request('DELETE', path, bucket, headers={'X-Audit-Log-Reason': reason})

    async def get_guild_widget_settings(self, guild_id):
        path = f'/guilds/{guild_id}/widget'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def edit_widget(self, guild_id, enabled, channel_id, reason = None):
        path = f'/guilds/{guild_id}/widget'
        bucket = 'PATCH' + path
        payload = {
            'enabled': enabled,
            'channel_id': channel_id,
        }
        return await self._request('PATCH', path, bucket, json=payload, headers={'X-Audit-Log-Reason': reason})

    async def get_guild_widget(self, guild_id):
        path = f'/guilds/{guild_id}/widget.json'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def get_vanity_code(self, guild_id):
        path = f'/guilds/{guild_id}/vanity-url'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def change_vanity_code(self, guild_id, code, reason = None):
        path = f'/guilds/{guild_id}/vanity-url'
        bucket = 'PATCH' + path
        payload = {'code': code}
        return await self._request('PATCH', path, bucket, json=payload, headers={'X-Audit-Log-Reason': reason})

    async def get_guild_welcome_screen(self, guild_id):
        path = f'/guilds/{guild_id}/welcome-screen'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def edit_guild_welcome_screen(self, guild_id, enabled=None, welcome_channels=None, description=None, reason = None):
        path = f'/guilds/{guild_id}/welcome-screen'
        bucket = 'PATCH' + path

        payload = {
            'enabled': enabled,
            'welcome_channels': welcome_channels,
            'description': description
        }

        return await self._request('PATCH', path, bucket, json=payload, header={'X-Audit-Log-Reason': reason})

    async def edit_voice_state(self, guild_id, channel_id, suppress=None, request_to_speak_timestamp=None):
        path = f'/guilds/{guild_id}/voice-states/@me'
        bucket = 'PATCH' + path
        payload = {
            'channel_id': channel_id,
        }
        if suppress is not None:
            payload['suppress'] = suppress
        if request_to_speak_timestamp is not None:
            payload['request_to_speak_timestamp'] = request_to_speak_timestamp
        return await self._request('PATCH', path, bucket, json=payload)

    async def edit_users_voice_state(self, guild_id, user_id, channel_id, suppress=None):
        path = f'/guilds/{guild_id}/voice-states/{user_id}'
        bucket = 'PATCH' + path
        payload = {
            'channel_id': channel_id,
        }
        if suppress is not None:
            payload['suppress'] = suppress
        return await self._request('PATCH', path, bucket, json=payload)

    """
    Guild Scheduled Event
    """

    async def get_scheduled_events(self, guild_id, with_user_count):
        path = f'/guilds/{guild_id}/scheduled-events'
        bucket = 'GET' + path
        params = {'with_user_count': with_user_count}
        return await self._request('GET', path, bucket, params=params)

    async def create_guild_scheduled_event(self, guild_id, reason = None, **payload):
        path = f'/guilds/{guild_id}/scheduled-events'
        bucket = 'POST' + path
        valid_keys = (
            'channel_id',
            'entity_metadata',
            'name',
            'privacy_level',
            'scheduled_start_time',
            'scheduled_end_time',
            'description',
            'entity_type',
            'image',
        )
        payload = {k: v for k, v in payload.items() if k in valid_keys}

        return await self._request('POST', path, bucket, json=payload, headers={'X-Audit-Log-Reason': reason})

    async def get_scheduled_event(self, guild_id, guild_scheduled_event_id, with_user_count):
        path = f'/guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}'
        bucket = 'GET' + path
        params = {'with_user_count': with_user_count}
        return await self._request('GET', path, bucket, params=params)

    async def edit_scheduled_event(self, guild_id, guild_scheduled_event_id, *, reason = None, **payload):
        path = f'/guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}'
        bucket = 'PATCH' + path
        valid_keys = (
            'channel_id',
            'entity_metadata',
            'name',
            'privacy_level',
            'scheduled_start_time',
            'scheduled_end_time',
            'status',
            'description',
            'entity_type',
            'image',
        )
        payload = {k: v for k, v in payload.items() if k in valid_keys}

        return await self._request('PATCH', path, bucket, json=payload, headers={'X-Audit-Log-Reason': reason})

    async def delete_scheduled_event(self, guild_id, guild_scheduled_event_id, reason = None):
        path = f'/guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}'
        bucket = 'DELETE' + path
        return await self._request('DELETE', path, bucket, headers={'X-Audit-Log-Reason': reason})

    async def get_scheduled_event_users(self, guild_id, guild_scheduled_event_id, limit, with_member, before = None, after = None):
        path = f'/guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}/users'
        bucket = 'GET' + path

        params = {
            'limit': limit,
            'with_member': int(with_member),
        }

        if before is not None:
            params['before'] = before
        if after is not None:
            params['after'] = after

        return await self._request('GET', path, bucket, params=params)

    """
    Guild Template
    """

    async def get_template(self, code):
        path = f'/guilds/templates/{code}'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def create_from_template(self, code, name, icon):
        path = f'/guilds/templates/{code}'
        bucket = 'POST' + path
        payload = {
            'name': name,
        }
        if icon:
            payload['icon'] = icon
        return await self._request('POST', path, bucket, json=payload)

    async def get_guild_templates(self, guild_id):
        path = f'/guilds/{guild_id}/templates'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def create_template(self, guild_id, name, description=None):
        path = f'/guilds/{guild_id}/templates'
        bucket = 'POST' + path
        payload = {
            'name': name[:100],
        }
        if description is not None:
            payload['description'] = description[:120]
        return await self._request('POST', path, bucket, json=payload)

    async def sync_template(self, guild_id, code):
        path = f'/guilds/{guild_id}/templates/{code}'
        bucket = 'PUT' + path
        return await self._request('PUT', path, bucket)

    async def edit_template(self, guild_id, code, payload):
        path = f'/guilds/{guild_id}/templates/{code}'
        bucket = 'PATCH' + path
        valid_keys = (
            'name',
            'description',
        )
        payload = {k: v for k, v in payload.items() if k in valid_keys}
        return await self._request('PATCH', path, bucket, json=payload)

    async def delete_template(self, guild_id, code):
        path = f'/guilds/{guild_id}/templates/{code}'
        bucket = 'DELETE' + path
        return await self._request('DELETE', path, bucket)

    """
    Invite
    """

    async def get_invite(self, invite_id, *, with_counts = True, with_expiration = True, guild_scheduled_event_id = None):
        path = f'/invites/{invite_id}'
        bucket = 'GET' + path
        params = {
            'with_counts'(with_counts),
            'with_expiration'(with_expiration),
        }

        if guild_scheduled_event_id:
            params['guild_scheduled_event_id'] = guild_scheduled_event_id

        return await self._request('GET', path, bucket, params=params)

    async def delete_invite(self, invite_id, reason = None):
        path = f'/invites/{invite_id}'
        bucket = 'DELETE' + path
        return await self._request('DELETE', path, bucket, headers={'X-Audit-Log-Reason': reason})

    """
    Stage Instance
    """

    async def create_stage_instance(self, reason, **payload):
        path = '/stage-instances'
        bucket = 'POST' + path
        valid_keys = (
            'channel_id',
            'topic',
            'privacy_level',
        )
        payload = {k: v for k, v in payload.items() if k in valid_keys}

        return await self._request('POST', path, bucket, json=payload, headers={'X-Audit-Log-Reason': reason})

    async def get_stage_instance(self, channel_id):
        path = f'/stage-instances/{channel_id}'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def edit_stage_instance(self, channel_id, *, reason = None, **payload):
        path = f'/stage-instances/{channel_id}'
        bucket = 'PATCH' + path
        valid_keys = (
            'topic',
            'privacy_level',
        )
        payload = {k: v for k, v in payload.items() if k in valid_keys}

        return await self._request('PATCH', path, bucket, json=payload, headers={'X-Audit-Log-Reason': reason})

    async def delete_stage_instance(self, channel_id, reason = None):
        path = f'/stage-instances/{channel_id}'
        bucket = 'DELETE' + path
        return await self._request('DELETE', path, bucket, headers={'X-Audit-Log-Reason': reason})

    """
    Sticker
    """

    async def get_sticker(self, sticker_id):
        path = f'/stickers/{sticker_id}'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def list_nitro_sticker_packs(self):
        path = '/sticker-packs'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def list_guild_stickers(self, guild_id):
        path = f'/guilds/{guild_id}/stickers'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def get_guild_sticker(self, guild_id, sticker_id):
        path = f'/guilds/{guild_id}/stickers/{sticker_id}'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    """
    async def create_guild_sticker(self, guild_id, payload, file, reason):
        initial_bytes = file.fp.read(16)

        try:
            mime_type = _get_mime_type_for_image(initial_bytes)
        except ValueError:
            if initial_bytes.startswith(b'{'):
                mime_type = 'application/json'
            else:
                mime_type = 'application/octet-stream'
        finally:
            file.reset()

        form = [
            {
                'name': 'file',
                'value': file.fp,
                'filename': file.filename,
                'content_type': mime_type,
            }
        ]

        for k, v in payload.items():
            form.append(
                {
                    'name': k,
                    'value': v,
                }
            )

        return await self._request(
            Route('POST', '/guilds/{guild_id}/stickers', guild_id=guild_id), form=form, files=[file], reason=reason
        )
    """

    async def modify_guild_sticker(self, guild_id, sticker_id, *, name=None, description=None, tags=None, reason):
        path = f'/guilds/{guild_id}/stickers/{sticker_id}'
        bucket = 'PATCH' + path
        payload = {}
        if name is not None:
            payload['name'] = name
        if description is not None:
            payload['description'] = description
        if tags is not None:
            payload['tags'] = tags

        return await self._request('PATCH', path, bucket, json=payload, headers={'X-Audit-Log-Reason': reason})

    async def delete_guild_sticker(self, guild_id, sticker_id, reason):
        path = f'/guilds/{guild_id}/stickers/{sticker_id}'
        bucket = 'DELETE' + path
        return await self._request('DELETE', path, bucket, headers={'X-Audit-Log-Reason': reason})

    """
    User
    """

    async def get_current_user(self):
        path = '/users/@me'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def get_user(self, user_id):
        path = f'/users/{user_id}'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def edit_current_user(self, username):
        path = '/users/@me'
        bucket = 'PATCH' + path
        payload = {
            'username': username
        }
        return await self._request('PATCH', path, bucket, json=payload)

    async def get_current_user_guilds(self, limit=200, before = None, after = None):
        path = '/users/@me/guilds'
        bucket = 'GET' + path
        if 1 > limit or limit > 200:
            raise InvalidParams('limit must be between 1 and 200')
        
        params = {
            'limit': limit,
        }

        if before is not None:
            params['before'] = before
        if after is not None:
            params['after'] = after

        return await self._request('GET', path, bucket, params=params)

    async def get_current_user_guild_member(self, guild_id):
        path = f'/users/@me/guilds/{guild_id}/member'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def leave_guild(self, guild_id):
        path = f'/users/@me/guilds/{guild_id}'
        bucket = 'DELETE' + path
        return await self._request('DELETE', path, bucket)

    async def create_DM(self, recipient_id):
        payload = {
            'recipient_id': recipient_id,
        }
        path = f'/users/@me/channels'
        bucket = 'POST' + path

        return await self._request('POST', path, bucket, json=payload)

    async def create_group_DM(self, access_tokens, nicks=None):
        payload = {
            'access_tokens': access_tokens,
        }
        path = f'/users/@me/channels'
        bucket = 'POST' + path

        return await self._request('POST', path, bucket, json=payload)

    async def get_connections(self):
        path = '/users/@me/connections'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    """
    Voice
    """

    async def list_voice_regions(self):
        path = '/voice/regions'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    """
    Webhook
    """

    async def create_webhook(self, channel_id, name, avatar = None, reason = None):
        path = f'/channels/{channel_id}/webhooks'
        bucket = 'POST' + path
        payload = {
            'name': name,
        }
        if avatar is not None:
            payload['avatar'] = avatar

        return await self._request('POST', path, bucket, json=payload, headers={'X-Audit-Log-Reason': reason})

    async def get_channel_webhooks(self, channel_id):
        path = f'/channels/{channel_id}/webhooks'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def get_guild_webhooks(self, guild_id):
        path = f'/guilds/{guild_id}/webhooks'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def get_webhook(self, webhook_id):
        path = f'/webhooks/{webhook_id}'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def get_webhook_with_token(self, webhook_id, webhook_token):
        #Doesn't need to auth
        path = f'/webhooks/{webhook_id}/{webhook_token}'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket, auth=False)

    async def edit_webhook(self, webhook_id, name=None, channel_id=None, reason = None):
        path = f'/webhooks/{webhook_id}'
        bucket = 'PATCH' + path
        payload = {}
        if name is not None:
            payload['name'] = name
        if channel_id is not None:
            payload['channel_id'] = channel_id

        return await self._request('PATCH', path, bucket, json=payload, headers={'X-Audit-Log-Reason': reason})

    async def edit_webhook_with_token(self, webhook_id, webhook_token, name=None, channel_id=None, reason = None):
        # Doesn't need to auth
        path = f'/webhooks/{webhook_id}/{webhook_token}'
        bucket = 'PATCH' + path
        payload = {}

        if name is not None:
            payload['name'] = name
        if channel_id is not None:
            payload['channel_id'] = channel_id

        return await self._request('PATCH', path, bucket, json=payload, auth=False, headers={'X-Audit-Log-Reason': reason})

    async def delete_webhook(self, webhook_id, reason=None):
        path = f'/webhooks/{webhook_id}'
        bucket = 'DELETE' + path
        return await self._request('DELETE', path, bucket, headers={'X-Audit-Log-Reason': reason})

    async def delete_webhook_with_token(self, webhook_id, webhook_token, reason=None):
        # Doesn't need to auth
        path = f'/webhooks/{webhook_id}/{webhook_token}'
        bucket = 'DELETE' + path
        return await self._request('DELETE', path, bucket, auth=False, headers={'X-Audit-Log-Reason': reason})

    async def execute_webhook(self, webhook_id, webhook_token, wait=False, thread_id=None, content = None, username=None, avatar_url=None, tts = False, embeds = None, allowed_mentions = None, components = None):
        # Doesn't need to auth
        path = f'/webhooks/{webhook_id}/{webhook_token}'
        bucket = 'POST' + path
        if content is None and embeds is None:
            raise InvalidParams('content or embeds must be provided')

        params = {}
        if wait is not None:
            params['wait'] = wait
        if thread_id is not None:
            params['thread_id'] = thread_id

        payload = {}

        if content is not None:
            payload['content'] = content
        if username is not None:
            payload['username'] = username
        if avatar_url is not None:
            payload['avatar_url'] = avatar_url
        if tts is not None:
            payload['tts'] = tts
        if embeds is not None:
            payload['embeds'] = embeds
        if allowed_mentions is not None:
            payload['allowed_mentions'] = allowed_mentions
        if components is not None:
            payload['components'] = components
        
        return await self._request('POST', path, bucket, json=payload, params=params, auth=False)

    async def get_webhook_message(self, webhook_id, webhook_token, message_id):
        # Doesn't need to auth
        path = f'/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}'
        bucket = 'GET' + path
        return self._request('GET', path, bucket, auth=False)

    async def edit_webhook_message(self, webhook_id, webhook_token, message_id, thread_id=None, content = None, embeds = None, allowed_mentions = None, components = None):
        # Doesn't need to auth
        path = f'/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}'
        bucket = 'PATCH' + path

        payload = { 
            'content': content,
            'embeds': embeds,
            'allowed_mentions': allowed_mentions,
            'components': components
        }
        return self._request('PATCH', path, bucket, json=payload, auth=False)

    async def delete_webhook_message(self, webhook_id, webhook_token, message_id):
        # Doesn't need to auth
        path = f'/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}'
        bucket = 'DELETE' + path
        return self._request('DELETE', path, bucket, auth=False)

    """
    Interactions
    """

    async def create_interaction_response(self, interaction_id, interaction_token, type, data=None):
        path = f'/interactions/{interaction_id}/{interaction_token}/callback'
        bucket = 'POST' + path
        payload = {
            'type': type
        }
        if data is not None:
            payload['data'] = data
        return self._request('POST', path, bucket, json=payload)

    async def get_original_interaction_response(self, application_id, interaction_token):
        path = f'/webhooks/{application_id}/{interaction_token}/messages/@original'
        bucket = 'GET' + path
        return self._request('GET', path, bucket)

    async def edit_original_interaction_response(self, application_id, interaction_token, content = None, embeds = None, allowed_mentions = None, components = None):
        path = f'/webhooks/{application_id}/{interaction_token}/messages/@original'
        bucket = 'PATCH' + path

        payload = { 
            'content': content,
            'embeds': embeds,
            'allowed_mentions': allowed_mentions,
            'components': components
        }

        return self._request('PATCH', path, bucket, json=payload)

    async def delete_original_interaction_response(self, application_id, interaction_token):
        path = f'/webhooks/{application_id}/{interaction_token}/messages/@original'
        bucket = 'DELETE' + path
        return self._request('DELETE', path, bucket)

    async def create_followup_message(self, application_id, interaction_token, content = None, tts=None, embeds = None, allowed_mentions = None, components = None):
        path = f'/webhooks/{application_id}/{interaction_token}'
        bucket = 'POST' + path

        payload = {}

        if content is not None:
            payload['content'] = content
        if tts is not None:
            payload['tts'] = tts
        if embeds is not None:
            payload['embeds'] = embeds
        if allowed_mentions is not None:
            payload['allowed_mentions'] = allowed_mentions
        if components is not None:
            payload['components'] = components

        return self._request('POST', path, bucket, json=payload)

    async def get_followup_message(self, application_id, interaction_token, message_id):
        path = f'/webhooks/{application_id}/{interaction_token}/messages/{message_id}'
        bucket = 'GET' + path
        return self._request('GET', path, bucket)

    async def edit_followup_message(self, application_id, interaction_token, message_id, content = None, embeds = None, allowed_mentions = None, components = None):
        path = f'/webhooks/{application_id}/{interaction_token}/messages/{message_id}'
        bucket = 'PATCH' + path

        payload = { 
            'content': content,
            'embeds': embeds,
            'allowed_mentions': allowed_mentions,
            'components': components
        }

        return self._request('PATCH', path, bucket, json=payload)

    async def delete_followup_message(self, application_id, interaction_token, message_id):
        path = f'/webhooks/{application_id}/{interaction_token}/messages/{message_id}'
        bucket = 'DELETE' + path
        return self._request('DELETE', path, bucket)

    """
    Misc
    """

    async def get_gateway(self):
        # No token needed
        path = '/gateway'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket, auth=False)

    async def get_bot_gateway(self):
        path = '/gateway/bot'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)

    async def application_info(self):
        path = '/oauth2/applications/@me'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket)
    
    async def authorisation_info(self, bearer_token):
        path = '/oauth2/@me'
        bucket = 'GET' + path
        return await self._request('GET', path, bucket, headers={'Authorization': f'Bearer {bearer_token}'}, auth=False) # auth is False as a bearer_token is used

    """
    Extra's for ease of use
    """

    async def change_nickname(self, guild_id, user_id, nickname, reason = None):
        path = f'/guilds/{guild_id}/members/{user_id}'
        bucket = 'PATCH' + path
        payload = {
            'nick': nickname,
        }
        return await self._request('PATCH', path, bucket, json=payload, reason=reason)

    async def move_member(self, user_id, guild_id, channel_id, reason = None):
        return self.modify_guild_member(user_id, guild_id, channel_id=channel_id, reason=reason)