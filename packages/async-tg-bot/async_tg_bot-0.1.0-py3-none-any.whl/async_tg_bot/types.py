from __future__ import annotations

from pydantic import BaseModel

__all__ = [
    'Message',
    'User',
    'Update',
    'Chat',
    'Type'
]


class Type(BaseModel):
    pass


class MessageId(Type):
    message_id: int


class ChatPhoto(Type):
    pass


class ChatPermissions(Type):
    pass


class ChatLocation(Type):
    pass


class Chat(Type):  # +
    id: int
    type: str
    title: str | None
    username: str | None
    first_name: str | None
    last_name: str | None
    photo: ChatPhoto | None
    bio: str | None
    has_private_forwards: bool | None
    description: str | None
    invite_link: str | None
    pinned_message: Message | None
    permissions: ChatPermissions | None
    slow_mode_delay: int | None
    message_auto_delete_time: int | None
    has_protected_content: bool | None
    sticker_set_name: str | None
    can_set_sticker_set: bool | None
    linked_chat_id: int | None
    location: ChatLocation | None


class Animation(Type):
    pass


class Audio(Type):
    pass


class Document(Type):
    pass


class Sticker(Type):
    pass


class Video(Type):
    pass


class VideoNote(Type):
    pass


class Voice(Type):
    pass


class Contact(Type):
    pass


class Dice(Type):
    pass


class Game(Type):
    pass


class Poll(Type):
    pass


class Venue(Type):
    pass


class Location(Type):
    pass


class MessageAutoDeleteTimerChanged(Type):
    pass


class Invoice(Type):
    pass


class SuccessfulPayment(Type):
    pass


class PassportData(Type):
    pass


class ProximityAlertTriggered(Type):
    pass


class VideoChatScheduled(Type):
    pass


class VideoChatStarted(Type):
    pass


class VideoChatEnded(Type):
    pass


class VideoChatParticipantsInvited(Type):
    pass


class WebAppData(Type):
    pass


class InlineKeyboardMarkup(Type):
    pass


class Message(Type):  # +
    message_id: int
    # from_: User | None
    # sender_chat: Chat | None
    date: int
    # chat: Chat
    # forward_from: User | None
    # forward_from_chat: Chat | None
    # forward_from_message_id: int | None
    # forward_signature: str | None
    # forward_sender_name: str | None
    # forward_date: int | None
    # is_automatic_forward: bool | None
    # reply_to_message: Message | None
    # via_bot: User | None
    # edit_date: int | None
    # has_protected_content: bool | None
    # media_group_id: str | None
    # author_signature: str | None
    text: str | None
    # entities: list | None
    # animation: Animation | None
    # audio: Audio | None
    # document: Document | None
    # photo: list | None
    # sticker: Sticker | None
    # video: Video | None
    # video_note: VideoNote | None
    # voice: Voice | None
    # caption: str | None
    # caption_entities: list | None
    # contact: Contact | None
    # dice: Dice | None
    # game: Game | None
    # poll: Poll | None
    # venue: Venue | None
    # location: Location | None
    # new_chat_members: list | None
    # left_chat_member: User | None
    # new_chat_title: str | None
    # new_chat_photo: list | None
    # delete_chat_photo: bool | None
    # group_chat_created: bool | None
    # supergroup_chat_created: bool | None
    # channel_chat_created: bool | None
    # message_auto_delete_timer_changed: MessageAutoDeleteTimerChanged | None
    # migrate_to_chat_id: int | None
    # migrate_from_chat_id: int | None
    # pinned_message: Message | None
    # invoice: Invoice | None
    # successful_payment: SuccessfulPayment | None
    # connected_website: str | None
    # passport_data: PassportData | None
    # proximity_alert_triggered: ProximityAlertTriggered | None
    # video_chat_scheduled: VideoChatScheduled | None
    # video_chat_started: VideoChatStarted | None
    # video_chat_ended: VideoChatEnded | None
    # video_chat_participants_invited: VideoChatParticipantsInvited | None
    # web_app_data: WebAppData | None
    reply_markup: InlineKeyboardMarkup | None


class User(Type):  # +
    id: int
    is_bot: bool
    first_name: str
    last_name: str | None
    username: str | None
    language_code: str | None
    can_join_groups: bool | None
    can_read_all_group_messages: bool | None
    supports_inline_queries: bool | None


class InlineQuery(Type):
    pass


class ChosenInlineResult(Type):
    pass


class CallbackQuery(Type):
    pass


class ShippingQuery(Type):
    pass


class PreCheckoutQuery(Type):
    pass


class PollAnswer(Type):
    pass


class ChatMemberUpdated(Type):
    pass


class ChatJoinRequest(Type):
    pass


class Update(Type):  # +
    update_id: int
    message: Message | None
    edited_message: Message | None
    channel_post: Message | None
    edited_channel_post: Message | None
    inline_query: InlineQuery | None
    chosen_inline_result: ChosenInlineResult | None
    callback_query: CallbackQuery | None
    shipping_query: ShippingQuery | None
    pre_checkout_query: PreCheckoutQuery | None
    poll: Poll | None
    poll_answer: PollAnswer | None
    my_chat_member: ChatMemberUpdated | None
    chat_member: ChatMemberUpdated | None
    chat_join_request: ChatJoinRequest | None
