from __future__ import annotations

from pydantic import BaseModel

from .types import *

__all__ = [
    'Method',
    'GetUpdates',
    'SetWebhook',
    'DeleteWebhook',
    'GetWebhookInfo',
    'GetMe',
    'LogOut',
    'Close',
    'SendMessage',
    'ForwardMessage',
    'CopyMessage',
    'SendPhoto',
    'SendAudio',
    'SendDocument',
    'SendVideo',
    'SendAnimation',
    'SendVoice',
    'SendVideoNote',
    'SendMediaGroup',
    'SendLocation',
    'EditMessageLiveLocation',
    'StopMessageLiveLocation',
    'SendVenue',
    'SendContact',
    'SendPoll',
    'SendDice',
    'SendChatAction',
    'GetUserProfilePhotos',
    'GetFile',
    'BanChatMember',
    'UnbanChatMember',
    'RestrictChatMember',
    'PromoteChatMember',
    'SetChatAdministratorCustomTitle',
    'BanChatSenderChat',
    'UnbanChatSenderChat',
    'SetChatPermissions',
    'ExportChatInviteLink',
    'CreateChatInviteLink',
    'EditChatInviteLink',
    'RevokeChatInviteLink',
    'ApproveChatJoinRequest',
    'DeclineChatJoinRequest',
    'SetChatPhoto',
    'DeleteChatPhoto',
    'SetChatTitle',
    'SetChatDescription',
    'PinChatMessage',
    'UnpinChatMessage',
    'UnpinAllChatMessages',
    'LeaveChat',
    'GetChat',
    'GetChatMemberCount',
    'SetChatStickerSet',
    'DeleteChatStickerSet',
    'AnswerCallbackQuery',
    'SetMyCommands',
    'DeleteMyCommands',
    'GetMyCommands',
    'SetChatMenuButton',
    'SetMyDefaultAdministratorRights',
    'GetMyDefaultAdministratorRights',
    'EditMessageText',
    'EditMessageCaption',
    'EditMessageMedia',
    'EditMessageReplyMarkup',
    'StopPoll',
    'DeleteMessage',
    'SendSticker',
    'GetStickerSet',
    'UploadStickerFile',
    'CreateNewStickerSet',
    'AddStickerToSet',
    'SetStickerPositionInSet',
    'DeleteStickerFromSet',
    'SetStickerSetThumb',
    'AnswerInlineQuery',
    'AnswerWebAppQuery',
    'SendInvoice',
    'AnswerShippingQuery',
    'AnswerPreCheckoutQuery',
    'SetPassportDataErrors',
    'SendGame',
    'SetGameScore',
    'GetGameHighScores',
]


class Method(BaseModel):

    def request(self) -> dict | list | bool | str | int:
        from .context import ctx

        return ctx.bot.request(self)


# === Getting updates

class GetUpdates(Method):
    offset: int = None
    limit: int = None
    timeout: int = None
    allowed_updates: list[str] = None

    def request(self) -> list[Update]:
        result = super().request()
        return [Update(**i) for i in result]


class SetWebhook(Method):
    url: str
    certificate: InputFile = None
    ip_address: str = None
    max_connections: int = None
    allowed_updates: list[str] = None
    drop_pending_updates: bool = None

    def request(self) -> bool:
        result = super().request()
        return result


class DeleteWebhook(Method):
    drop_pending_updates: bool = None

    def request(self) -> bool:
        result = super().request()
        return result


class GetWebhookInfo(Method):

    def request(self) -> WebhookInfo:
        result = super().request()
        return WebhookInfo(**result)


# === Available methods

class GetMe(Method):

    def request(self) -> User:
        result = super().request()
        return User(**result)


class LogOut(Method):

    def request(self) -> bool:
        result = super().request()
        return result


class Close(Method):

    def request(self) -> bool:
        result = super().request()
        return result


class SendMessage(Method):
    chat_id: int | str = None
    text: str
    parse_mode: str = None
    entities: list[MessageEntity] = None
    disable_web_page_preview: bool = None
    disable_notification: bool = None
    protect_content: bool = None
    reply_to_message_id: int = None
    allow_sending_without_reply: bool = None
    reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply = None

    def request(self) -> Message:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.parse_mode = self.parse_mode or ctx.bot.parse_mode
        self.disable_web_page_preview = self.disable_web_page_preview or ctx.bot.disable_web_page_preview
        self.disable_notification = self.disable_notification or ctx.bot.disable_notification
        self.protect_content = self.protect_content or ctx.bot.protect_content
        self.allow_sending_without_reply = self.allow_sending_without_reply or ctx.bot.allow_sending_without_reply

        result = super().request()
        return Message(**result)


class ForwardMessage(Method):
    chat_id: int | str
    from_chat_id: int | str = None
    disable_notification: bool = None
    protect_content: bool = None
    message_id: int = None

    def request(self) -> Message:
        from .context import ctx

        self.from_chat_id = self.from_chat_id or ctx.chat.id
        self.disable_notification = self.disable_notification or ctx.bot.disable_notification
        self.protect_content = self.protect_content or ctx.bot.protect_content
        self.message_id = self.message_id or ctx.message.message_id

        result = super().request()
        return Message(**result)


class CopyMessage(Method):
    chat_id: int | str
    from_chat_id: int | str = None
    message_id: int = None
    caption: str = None
    parse_mode: str = None
    caption_entities: list[MessageEntity] = None
    disable_notification: bool = None
    protect_content: bool = None
    reply_to_message_id: int = None
    allow_sending_without_reply: bool = None
    reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply = None

    def request(self) -> MessageId:
        from .context import ctx

        self.from_chat_id = self.from_chat_id or ctx.chat.id
        self.message_id = self.message_id or ctx.message.message_id
        self.parse_mode = self.parse_mode or ctx.bot.parse_mode
        self.disable_notification = self.disable_notification or ctx.bot.disable_notification
        self.protect_content = self.protect_content or ctx.bot.protect_content
        self.allow_sending_without_reply = self.allow_sending_without_reply or ctx.bot.allow_sending_without_reply

        result = super().request()
        return MessageId(**result)


class SendPhoto(Method):
    chat_id: int | str = None
    photo: InputFile | str
    caption: str = None
    parse_mode: str = None
    caption_entities: list[MessageEntity] = None
    disable_notification: bool = None
    protect_content: bool = None
    reply_to_message_id: int = None
    allow_sending_without_reply: bool = None
    reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply = None

    def request(self) -> Message:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.parse_mode = self.parse_mode or ctx.bot.parse_mode
        self.disable_notification = self.disable_notification or ctx.bot.disable_notification
        self.protect_content = self.protect_content or ctx.bot.protect_content
        self.allow_sending_without_reply = self.allow_sending_without_reply or ctx.bot.allow_sending_without_reply

        result = super().request()
        return Message(**result)


class SendAudio(Method):
    chat_id: int | str = None
    audio: InputFile | str
    caption: str = None
    parse_mode: str = None
    caption_entities: list[MessageEntity] = None
    duration: int = None
    performer: str = None
    title: str = None
    thumb: InputFile | str = None
    disable_notification: bool = None
    protect_content: bool = None
    reply_to_message_id: int = None
    allow_sending_without_reply: bool = None
    reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply = None

    def request(self) -> Message:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.parse_mode = self.parse_mode or ctx.bot.parse_mode
        self.disable_notification = self.disable_notification or ctx.bot.disable_notification
        self.protect_content = self.protect_content or ctx.bot.protect_content
        self.allow_sending_without_reply = self.allow_sending_without_reply or ctx.bot.allow_sending_without_reply

        result = super().request()
        return Message(**result)


class SendDocument(Method):
    chat_id: int | str = None
    document: InputFile | str
    thumb: InputFile | str = None
    caption: str = None
    parse_mode: str = None
    caption_entities: list[MessageEntity] = None
    disable_content_type_detection: bool = None
    disable_notification: bool = None
    protect_content: bool = None
    reply_to_message_id: int = None
    allow_sending_without_reply: bool = None
    reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply = None

    def request(self) -> Message:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.parse_mode = self.parse_mode or ctx.bot.parse_mode
        self.disable_notification = self.disable_notification or ctx.bot.disable_notification
        self.protect_content = self.protect_content or ctx.bot.protect_content
        self.allow_sending_without_reply = self.allow_sending_without_reply or ctx.bot.allow_sending_without_reply

        result = super().request()
        return Message(**result)


class SendVideo(Method):
    chat_id: int | str = None
    video: InputFile | str
    duration: int = None
    width: int = None
    height: int = None
    thumb: InputFile | str = None
    caption: str = None
    parse_mode: str = None
    caption_entities: list[MessageEntity] = None
    supports_streaming: bool = None
    disable_notification: bool = None
    protect_content: bool = None
    reply_to_message_id: int = None
    allow_sending_without_reply: bool = None
    reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply = None

    def request(self) -> Message:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.parse_mode = self.parse_mode or ctx.bot.parse_mode
        self.disable_notification = self.disable_notification or ctx.bot.disable_notification
        self.protect_content = self.protect_content or ctx.bot.protect_content
        self.allow_sending_without_reply = self.allow_sending_without_reply or ctx.bot.allow_sending_without_reply

        result = super().request()
        return Message(**result)


class SendAnimation(Method):
    chat_id: int | str = None
    animation: InputFile | str
    duration: int = None
    width: int = None
    height: int = None
    thumb: InputFile | str = None
    caption: str = None
    parse_mode: str = None
    caption_entities: list[MessageEntity] = None
    disable_notification: bool = None
    protect_content: bool = None
    reply_to_message_id: int = None
    allow_sending_without_reply: bool = None
    reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply = None

    def request(self) -> Message:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.parse_mode = self.parse_mode or ctx.bot.parse_mode
        self.disable_notification = self.disable_notification or ctx.bot.disable_notification
        self.protect_content = self.protect_content or ctx.bot.protect_content
        self.allow_sending_without_reply = self.allow_sending_without_reply or ctx.bot.allow_sending_without_reply

        result = super().request()
        return Message(**result)


class SendVoice(Method):
    chat_id: int | str = None
    voice: InputFile | str
    caption: str = None
    parse_mode: str = None
    caption_entities: list[MessageEntity] = None
    duration: int = None
    disable_notification: bool = None
    protect_content: bool = None
    reply_to_message_id: int = None
    allow_sending_without_reply: bool = None
    reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply = None

    def request(self) -> Message:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.parse_mode = self.parse_mode or ctx.bot.parse_mode
        self.disable_notification = self.disable_notification or ctx.bot.disable_notification
        self.protect_content = self.protect_content or ctx.bot.protect_content
        self.allow_sending_without_reply = self.allow_sending_without_reply or ctx.bot.allow_sending_without_reply

        result = super().request()
        return Message(**result)


class SendVideoNote(Method):
    chat_id: int | str = None
    video_note: InputFile | str
    duration: int = None
    length: int = None
    thumb: InputFile | str = None
    disable_notification: bool = None
    protect_content: bool = None
    reply_to_message_id: int = None
    allow_sending_without_reply: bool = None
    reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply = None

    def request(self) -> Message:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.disable_notification = self.disable_notification or ctx.bot.disable_notification
        self.protect_content = self.protect_content or ctx.bot.protect_content
        self.allow_sending_without_reply = self.allow_sending_without_reply or ctx.bot.allow_sending_without_reply

        result = super().request()
        return Message(**result)


class SendMediaGroup(Method):
    chat_id: int | str = None
    media: list[InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo]
    disable_notification: bool = None
    protect_content: bool = None
    reply_to_message_id: int = None
    allow_sending_without_reply: bool = None

    def request(self) -> list[Message]:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.disable_notification = self.disable_notification or ctx.bot.disable_notification
        self.protect_content = self.protect_content or ctx.bot.protect_content
        self.allow_sending_without_reply = self.allow_sending_without_reply or ctx.bot.allow_sending_without_reply

        result = super().request()
        return [Message(**i) for i in result]


class SendLocation(Method):
    chat_id: int | str = None
    latitude: float
    longitude: float
    horizontal_accuracy: float = None
    live_period: int = None
    heading: int = None
    proximity_alert_radius: int = None
    disable_notification: bool = None
    protect_content: bool = None
    reply_to_message_id: int = None
    allow_sending_without_reply: bool = None
    reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply = None

    def request(self) -> Message:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.disable_notification = self.disable_notification or ctx.bot.disable_notification
        self.protect_content = self.protect_content or ctx.bot.protect_content
        self.allow_sending_without_reply = self.allow_sending_without_reply or ctx.bot.allow_sending_without_reply

        result = super().request()
        return Message(**result)


class EditMessageLiveLocation(Method):
    chat_id: int | str = None
    message_id: int = None
    inline_message_id: str = None
    latitude: float
    longitude: float
    horizontal_accuracy: float = None
    heading: int = None
    proximity_alert_radius: int = None
    reply_markup: InlineKeyboardMarkup = None

    def request(self) -> Message | bool:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id

        result = super().request()
        if result is True:
            return result
        return Message(**result)


class StopMessageLiveLocation(Method):
    chat_id: int | str = None
    message_id: int = None
    inline_message_id: str = None
    reply_markup: InlineKeyboardMarkup = None

    def request(self) -> Message | bool:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id

        result = super().request()
        if result is True:
            return result
        return Message(**result)


class SendVenue(Method):
    chat_id: int | str = None
    latitude: float
    longitude: float
    title: str
    address: str
    foursquare_id: str = None
    foursquare_type: str = None
    google_place_id: str = None
    google_place_type: str = None
    disable_notification: bool = None
    protect_content: bool = None
    reply_to_message_id: int = None
    allow_sending_without_reply: bool = None
    reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply = None

    def request(self) -> Message:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.disable_notification = self.disable_notification or ctx.bot.disable_notification
        self.protect_content = self.protect_content or ctx.bot.protect_content
        self.allow_sending_without_reply = self.allow_sending_without_reply or ctx.bot.allow_sending_without_reply

        result = super().request()
        return Message(**result)


class SendContact(Method):
    chat_id: int | str = None
    phone_number: str
    first_name: str
    last_name: str = None
    vcard: str = None
    disable_notification: bool = None
    protect_content: bool = None
    reply_to_message_id: int = None
    allow_sending_without_reply: bool = None
    reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply = None

    def request(self) -> Message:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.disable_notification = self.disable_notification or ctx.bot.disable_notification
        self.protect_content = self.protect_content or ctx.bot.protect_content
        self.allow_sending_without_reply = self.allow_sending_without_reply or ctx.bot.allow_sending_without_reply

        result = super().request()
        return Message(**result)


class SendPoll(Method):
    chat_id: int | str = None
    question: str
    options: list[str]
    is_anonymous: bool = None
    type: str = None
    allows_multiple_answers: bool = None
    correct_option_id: int = None
    explanation: str = None
    explanation_parse_mode: str = None
    explanation_entities: list[MessageEntity] = None
    open_period: int = None
    close_date: int = None
    is_closed: bool = None
    disable_notification: bool = None
    protect_content: bool = None
    reply_to_message_id: int = None
    allow_sending_without_reply: bool = None
    reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply = None

    def request(self) -> Message:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.disable_notification = self.disable_notification or ctx.bot.disable_notification
        self.protect_content = self.protect_content or ctx.bot.protect_content
        self.allow_sending_without_reply = self.allow_sending_without_reply or ctx.bot.allow_sending_without_reply

        result = super().request()
        return Message(**result)


class SendDice(Method):
    chat_id: int | str = None
    emoji: str = None
    disable_notification: bool = None
    protect_content: bool = None
    reply_to_message_id: int = None
    allow_sending_without_reply: bool = None
    reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply = None

    def request(self) -> Message:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.disable_notification = self.disable_notification or ctx.bot.disable_notification
        self.protect_content = self.protect_content or ctx.bot.protect_content
        self.allow_sending_without_reply = self.allow_sending_without_reply or ctx.bot.allow_sending_without_reply

        result = super().request()
        return Message(**result)


class SendChatAction(Method):
    chat_id: int | str = None
    action: str

    def request(self) -> bool:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id

        result = super().request()
        return result


class GetUserProfilePhotos(Method):
    user_id: int = None
    offset: int = None
    limit: int = None

    def request(self) -> UserProfilePhotos:
        from .context import ctx

        self.user_id = self.user_id or ctx.user.id

        result = super().request()
        return UserProfilePhotos(**result)


class GetFile(Method):
    file_id: str

    def request(self) -> File:
        result = super().request()
        return File(**result)


class BanChatMember(Method):
    chat_id: int | str = None
    user_id: int = None
    until_date: int = None
    revoke_messages: bool = None

    def request(self) -> bool:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.user_id = self.user_id or ctx.user.id

        result = super().request()
        return result


class UnbanChatMember(Method):
    chat_id: int | str = None
    user_id: int = None
    only_if_banned: bool = None

    def request(self) -> bool:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.user_id = self.user_id or ctx.user.id

        result = super().request()
        return result


class RestrictChatMember(Method):
    chat_id: int | str = None
    user_id: int = None
    permissions: ChatPermissions
    until_date: int = None

    def request(self) -> bool:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.user_id = self.user_id or ctx.user.id

        result = super().request()
        return result


class PromoteChatMember(Method):
    chat_id: int | str = None
    user_id: int = None
    is_anonymous: bool = None
    can_manage_chat: bool = None
    can_post_messages: bool = None
    can_edit_messages: bool = None
    can_delete_messages: bool = None
    can_manage_video_chats: bool = None
    can_restrict_members: bool = None
    can_promote_members: bool = None
    can_change_info: bool = None
    can_invite_users: bool = None
    can_pin_messages: bool = None

    def request(self) -> bool:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.user_id = self.user_id or ctx.user.id

        result = super().request()
        return result


class SetChatAdministratorCustomTitle(Method):
    chat_id: int | str = None
    user_id: int = None
    custom_title: str

    def request(self) -> bool:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.user_id = self.user_id or ctx.user.id

        result = super().request()
        return result


class BanChatSenderChat(Method):
    chat_id: int | str = None
    sender_chat_id: int = None

    def request(self) -> bool:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.sender_chat_id = self.sender_chat_id or ctx.message.sender_chat.id

        result = super().request()
        return result


class UnbanChatSenderChat(Method):
    chat_id: int | str = None
    sender_chat_id: int = None

    def request(self) -> bool:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.sender_chat_id = self.sender_chat_id or ctx.message.sender_chat.id

        result = super().request()
        return result


class SetChatPermissions(Method):
    chat_id: int | str = None
    permissions: ChatPermissions

    def request(self) -> bool:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id

        result = super().request()
        return result


class ExportChatInviteLink(Method):
    chat_id: int | str = None

    def request(self) -> str:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id

        result = super().request()
        return result


class CreateChatInviteLink(Method):
    chat_id: int | str = None
    name: str = None
    expire_date: int = None
    member_limit: int = None
    creates_join_request: bool = None

    def request(self) -> ChatInviteLink:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id

        result = super().request()
        return ChatInviteLink(**result)


class EditChatInviteLink(Method):
    chat_id: int | str = None
    invite_link: str
    name: str = None
    expire_date: int = None
    member_limit: int = None
    creates_join_request: bool = None

    def request(self) -> ChatInviteLink:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id

        result = super().request()
        return ChatInviteLink(**result)


class RevokeChatInviteLink(Method):
    chat_id: int | str = None
    invite_link: str

    def request(self) -> ChatInviteLink:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id

        result = super().request()
        return ChatInviteLink(**result)


class ApproveChatJoinRequest(Method):
    chat_id: int | str = None
    user_id: int = None

    def request(self) -> bool:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.user_id = self.user_id or ctx.user.id

        result = super().request()
        return result


class DeclineChatJoinRequest(Method):
    chat_id: int | str = None
    user_id: int = None

    def request(self) -> bool:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.user_id = self.user_id or ctx.user.id

        result = super().request()
        return result


class SetChatPhoto(Method):
    chat_id: int | str = None
    photo: InputFile

    def request(self) -> bool:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id

        result = super().request()
        return result


class DeleteChatPhoto(Method):
    chat_id: int | str = None

    def request(self) -> bool:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id

        result = super().request()
        return result


class SetChatTitle(Method):
    chat_id: int | str = None
    title: str

    def request(self) -> bool:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id

        result = super().request()
        return result


class SetChatDescription(Method):
    chat_id: int | str = None
    description: str = None

    def request(self) -> bool:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id

        result = super().request()
        return result


class PinChatMessage(Method):
    chat_id: int | str = None
    message_id: int = None
    disable_notification: bool = None

    def request(self) -> bool:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.message_id = self.message_id or ctx.message.message_id
        self.disable_notification = self.disable_notification or ctx.bot.disable_notification

        result = super().request()
        return result


class UnpinChatMessage(Method):
    chat_id: int | str = None
    message_id: int = None

    def request(self) -> bool:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.message_id = self.message_id or ctx.message.message_id

        result = super().request()
        return result


class UnpinAllChatMessages(Method):
    chat_id: int | str = None

    def request(self) -> bool:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id

        result = super().request()
        return result


class LeaveChat(Method):
    chat_id: int | str = None

    def request(self) -> bool:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id

        result = super().request()
        return result


class GetChat(Method):
    chat_id: int | str = None

    def request(self) -> Chat:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id

        result = super().request()
        return Chat(**result)


# class GetChatAdministrators(Method):
#     chat_id: int | str
#
#     def request(self) -> list[ChatMember]:
#         result = super().request()
#         return [ChatMember(**i) for i in result]


class GetChatMemberCount(Method):
    chat_id: int | str = None

    def request(self) -> int:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id

        result = super().request()
        return result


# class GetChatMember(Method):
#     chat_id: int | str
#     user_id: int
#
#     def request(self) -> ChatMember:
#         result = super().request()
#         return ChatMember(**result)


class SetChatStickerSet(Method):
    chat_id: int | str = None
    sticker_set_name: str

    def request(self) -> bool:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id

        result = super().request()
        return result


class DeleteChatStickerSet(Method):
    chat_id: int | str = None

    def request(self) -> bool:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id

        result = super().request()
        return result


class AnswerCallbackQuery(Method):
    callback_query_id: str = None
    text: str = None
    show_alert: bool = None
    url: str = None
    cache_time: int = None

    def request(self) -> bool:
        from .context import ctx

        self.callback_query_id = self.callback_query_id or ctx.callback_query.id

        result = super().request()
        return result


class SetMyCommands(Method):
    commands: list[BotCommand]
    scope: BotCommandScope = None
    language_code: str = None

    def request(self) -> bool:
        result = super().request()
        return result


class DeleteMyCommands(Method):
    scope: BotCommandScope = None
    language_code: str = None

    def request(self) -> bool:
        result = super().request()
        return result


class GetMyCommands(Method):
    scope: BotCommandScope = None
    language_code: str = None

    def request(self) -> list[BotCommand]:
        result = super().request()
        return [BotCommand(**i) for i in result]


class SetChatMenuButton(Method):
    chat_id: int = None
    menu_button: MenuButton = None

    def request(self) -> bool:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id

        result = super().request()
        return result


# class GetChatMenuButton(Method):
#     chat_id: int = None
#
#     def request(self) -> MenuButton:
#         result = super().request()
#         return MenuButton(**result)


class SetMyDefaultAdministratorRights(Method):
    rights: ChatAdministratorRights = None
    for_channels: bool = None

    def request(self) -> bool:
        result = super().request()
        return result


class GetMyDefaultAdministratorRights(Method):
    for_channels: bool = None

    def request(self) -> ChatAdministratorRights:
        result = super().request()
        return ChatAdministratorRights(**result)


# == Updating messages

class EditMessageText(Method):
    chat_id: int | str = None
    message_id: int = None
    inline_message_id: str = None
    text: str
    parse_mode: str = None
    entities: list[MessageEntity] = None
    disable_web_page_preview: bool = None
    reply_markup: InlineKeyboardMarkup = None

    def request(self) -> Message | bool:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.message_id = self.message_id or ctx.message.message_id

        result = super().request()
        if result is True:
            return result
        return Message(**result)


class EditMessageCaption(Method):
    chat_id: int | str = None
    message_id: int = None
    inline_message_id: str = None
    caption: str = None
    parse_mode: str = None
    caption_entities: list[MessageEntity] = None
    reply_markup: InlineKeyboardMarkup = None

    def request(self) -> Message | bool:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.message_id = self.message_id or ctx.message.message_id

        result = super().request()
        if result is True:
            return result
        return Message(**result)


class EditMessageMedia(Method):
    chat_id: int | str = None
    message_id: int = None
    inline_message_id: str = None
    media: InputMedia
    reply_markup: InlineKeyboardMarkup = None

    def request(self) -> Message | bool:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.message_id = self.message_id or ctx.message.message_id

        result = super().request()
        if result is True:
            return result
        return Message(**result)


class EditMessageReplyMarkup(Method):
    chat_id: int | str = None
    message_id: int = None
    inline_message_id: str = None
    reply_markup: InlineKeyboardMarkup = None

    def request(self) -> Message | bool:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.message_id = self.message_id or ctx.message.message_id

        result = super().request()
        if result is True:
            return result
        return Message(**result)


class StopPoll(Method):
    chat_id: int | str = None
    message_id: int = None
    reply_markup: InlineKeyboardMarkup = None

    def request(self) -> Poll:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.message_id = self.message_id or ctx.message.message_id

        result = super().request()
        return Poll(**result)


class DeleteMessage(Method):
    chat_id: int | str = None
    message_id: int = None

    def request(self) -> bool:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.message_id = self.message_id or ctx.message.message_id

        result = super().request()
        return result


# === Stickers

class SendSticker(Method):
    chat_id: int | str = None
    sticker: InputFile | str
    disable_notification: bool = None
    protect_content: bool = None
    reply_to_message_id: int = None
    allow_sending_without_reply: bool = None
    reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply = None

    def request(self) -> Message:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.disable_notification = self.disable_notification or ctx.bot.disable_notification
        self.protect_content = self.protect_content or ctx.bot.protect_content
        self.allow_sending_without_reply = self.allow_sending_without_reply or ctx.bot.allow_sending_without_reply

        result = super().request()
        return Message(**result)


class GetStickerSet(Method):
    name: str

    def request(self) -> StickerSet:
        result = super().request()
        return StickerSet(**result)


class UploadStickerFile(Method):
    user_id: int = None
    png_sticker: InputFile

    def request(self) -> File:
        from .context import ctx

        self.user_id = self.user_id or ctx.user.id

        result = super().request()
        return File(**result)


class CreateNewStickerSet(Method):
    user_id: int = None
    name: str
    title: str
    png_sticker: InputFile | str = None
    tgs_sticker: InputFile = None
    webm_sticker: InputFile = None
    emojis: str
    contains_masks: bool = None
    mask_position: MaskPosition = None

    def request(self) -> bool:
        from .context import ctx

        self.user_id = self.user_id or ctx.user.id

        result = super().request()
        return result


class AddStickerToSet(Method):
    user_id: int = None
    name: str
    png_sticker: InputFile | str = None
    tgs_sticker: InputFile = None
    webm_sticker: InputFile = None
    emojis: str
    mask_position: MaskPosition = None

    def request(self) -> bool:
        from .context import ctx

        self.user_id = self.user_id or ctx.user.id

        result = super().request()
        return result


class SetStickerPositionInSet(Method):
    sticker: str
    position: int

    def request(self) -> bool:
        result = super().request()
        return result


class DeleteStickerFromSet(Method):
    sticker: str

    def request(self) -> bool:
        result = super().request()
        return result


class SetStickerSetThumb(Method):
    name: str
    user_id: int = None
    thumb: InputFile | str = None

    def request(self) -> bool:
        from .context import ctx

        self.user_id = self.user_id or ctx.user.id

        result = super().request()
        return result


# === Inline mode


class AnswerInlineQuery(Method):
    inline_query_id: str = None
    results: list[InlineQueryResult]
    cache_time: int = None
    is_personal: bool = None
    next_offset: str = None
    switch_pm_text: str = None
    switch_pm_parameter: str = None

    def request(self) -> bool:
        from .context import ctx

        self.inline_query_id = self.inline_query_id or ctx.inline_query.id

        result = super().request()
        return result


class AnswerWebAppQuery(Method):
    web_app_query_id: str
    result: InlineQueryResult

    def request(self) -> SentWebAppMessage:
        result = super().request()
        return SentWebAppMessage(**result)


# === Payments

class SendInvoice(Method):
    chat_id: int | str = None
    title: str
    description: str
    payload: str
    provider_token: str
    currency: str
    prices: list[LabeledPrice]
    max_tip_amount: int = None
    suggested_tip_amounts: list[int] = None
    start_parameter: str = None
    provider_data: str = None
    photo_url: str = None
    photo_size: int = None
    photo_width: int = None
    photo_height: int = None
    need_name: bool = None
    need_phone_number: bool = None
    need_email: bool = None
    need_shipping_address: bool = None
    send_phone_number_to_provider: bool = None
    send_email_to_provider: bool = None
    is_flexible: bool = None
    disable_notification: bool = None
    protect_content: bool = None
    reply_to_message_id: int = None
    allow_sending_without_reply: bool = None
    reply_markup: InlineKeyboardMarkup = None

    def request(self) -> Message:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id

        result = super().request()
        return Message(**result)


class AnswerShippingQuery(Method):
    shipping_query_id: str
    ok: bool
    shipping_options: list[ShippingOption] = None
    error_message: str = None

    def request(self) -> bool:
        result = super().request()
        return result


class AnswerPreCheckoutQuery(Method):
    pre_checkout_query_id: str
    ok: bool
    error_message: str = None

    def request(self) -> bool:
        result = super().request()
        return result


# === Telegram Passport

class SetPassportDataErrors(Method):
    user_id: int = None
    errors: list[PassportElementError]

    def request(self) -> bool:
        from .context import ctx

        self.user_id = self.user_id or ctx.user.id

        result = super().request()
        return result


# === Games

class SendGame(Method):
    chat_id: int = None
    game_short_name: str
    disable_notification: bool = None
    protect_content: bool = None
    reply_to_message_id: int = None
    allow_sending_without_reply: bool = None
    reply_markup: InlineKeyboardMarkup = None

    def request(self) -> Message:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.disable_notification = self.disable_notification or ctx.bot.disable_notification
        self.protect_content = self.protect_content or ctx.bot.protect_content
        self.allow_sending_without_reply = self.allow_sending_without_reply or ctx.bot.allow_sending_without_reply

        result = super().request()
        return Message(**result)


class SetGameScore(Method):
    user_id: int = None
    score: int
    force: bool = None
    disable_edit_message: bool = None
    chat_id: int = None
    message_id: int = None
    inline_message_id: str = None

    def request(self) -> Message | bool:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.user_id = self.user_id or ctx.user.id
        self.message_id = self.message_id or ctx.message.message_id

        result = super().request()
        if result is True:
            return result
        return Message(**result)


class GetGameHighScores(Method):
    user_id: int = None
    chat_id: int = None
    message_id: int = None
    inline_message_id: str = None

    def request(self) -> list[GameHighScore]:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        self.user_id = self.user_id or ctx.user.id
        self.message_id = self.message_id or ctx.message.message_id

        result = super().request()
        return [GameHighScore(**i) for i in result]
