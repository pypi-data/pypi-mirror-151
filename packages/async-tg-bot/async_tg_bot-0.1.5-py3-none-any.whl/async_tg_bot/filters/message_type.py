from .filter import Filter
from ..types import Update

__all__ = [
    'Text',
    'Animation',
    'Audio',
    'Document',
    'Photo',
    'Sticker',
    'Video',
    'VideoNote',
    'Voice',
    'Contact',
    'Dice',
    'Game',
    'Poll',
    'Venue',
    'Location',
    'NewChatMembers',
    'LeftChatMember',
    'NewChatTitle',
    'NewChatPhoto',
    'DeleteChatPhoto',
    'GroupChatCreated',
    'SupergroupChatCreated',
    'ChannelChatCreated',
    'MessageAutoDeleteTimerChanged',
    'MigrateToChatId',
    'MigrateFromChatId',
    'PinnedMessage',
    'Invoice',
    'SuccessfulPayment',
    'ConnectedWebsite',
    'PassportData',
    'ProximityAlertTriggered',
    'VideoChatScheduled',
    'VideoChatStarted',
    'VideoChatEnded',
    'VideoChatParticipantsInvited',
    'WebAppData',
]


class Text(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.text)
        except AttributeError:
            return False


class Animation(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.animation)
        except AttributeError:
            return False


class Audio(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.audio)
        except AttributeError:
            return False


class Document(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.document)
        except AttributeError:
            return False


class Photo(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.photo)
        except AttributeError:
            return False


class Sticker(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.sticker)
        except AttributeError:
            return False


class Video(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.video)
        except AttributeError:
            return False


class VideoNote(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.video_note)
        except AttributeError:
            return False


class Voice(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.voice)
        except AttributeError:
            return False


class Contact(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.contact)
        except AttributeError:
            return False


class Dice(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.dice)
        except AttributeError:
            return False


class Game(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.game)
        except AttributeError:
            return False


class Poll(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.poll)
        except AttributeError:
            return False


class Venue(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.venue)
        except AttributeError:
            return False


class Location(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.location)
        except AttributeError:
            return False


class NewChatMembers(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.new_chat_members)
        except AttributeError:
            return False


class LeftChatMember(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.left_chat_member)
        except AttributeError:
            return False


class NewChatTitle(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.new_chat_title)
        except AttributeError:
            return False


class NewChatPhoto(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.new_chat_photo)
        except AttributeError:
            return False


class DeleteChatPhoto(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.delete_chat_photo)
        except AttributeError:
            return False


class GroupChatCreated(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.group_chat_created)
        except AttributeError:
            return False


class SupergroupChatCreated(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.supergroup_chat_created)
        except AttributeError:
            return False


class ChannelChatCreated(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.channel_chat_created)
        except AttributeError:
            return False


class MessageAutoDeleteTimerChanged(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.message_auto_delete_timer_changed)
        except AttributeError:
            return False


class MigrateToChatId(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.migrate_to_chat_id)
        except AttributeError:
            return False


class MigrateFromChatId(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.migrate_from_chat_id)
        except AttributeError:
            return False


class PinnedMessage(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.pinned_message)
        except AttributeError:
            return False


class Invoice(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.invoice)
        except AttributeError:
            return False


class SuccessfulPayment(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.successful_payment)
        except AttributeError:
            return False


class ConnectedWebsite(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.connected_website)
        except AttributeError:
            return False


class PassportData(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.passport_data)
        except AttributeError:
            return False


class ProximityAlertTriggered(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.proximity_alert_triggered)
        except AttributeError:
            return False


class VideoChatScheduled(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.video_chat_scheduled)
        except AttributeError:
            return False


class VideoChatStarted(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.video_chat_started)
        except AttributeError:
            return False


class VideoChatEnded(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.video_chat_ended)
        except AttributeError:
            return False


class VideoChatParticipantsInvited(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.video_chat_participants_invited)
        except AttributeError:
            return False


class WebAppData(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.web_app_data)
        except AttributeError:
            return False
