from .layer1 import BotLayer1
from .. import filters
from .. import utils
from ..handlers import Handler


class BotLayer2(BotLayer1):

    def on_update(self):
        _filters = []

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_any_message(self):
        _filters = [filters.IsAnyMessage()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_message(
            self,
            text: str | list[str] | filters.Text | list[filters.Text] = None,
            command: str | list[str] | filters.Command | list[filters.Command] = None,
    ):
        _filters = [filters.message_type.Text()]

        for t in utils.listify(text):
            _filters.append(filters.Text.cast(t))

        for c in utils.listify(command):
            _filters.append(filters.Command.cast(c))

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_callback_query(self):
        _filters = [filters.IsCallbackQuery()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    # ===

    def on_text(self):
        _filters = [filters.message_type.Text()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_animation(self):
        _filters = [filters.message_type.Animation()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_audio(self):
        _filters = [filters.message_type.Audio()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_document(self):
        _filters = [filters.message_type.Document()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_photo(self):
        _filters = [filters.message_type.Photo()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_sticker(self):
        _filters = [filters.message_type.Sticker()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_video(self):
        _filters = [filters.message_type.Video()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_video_note(self):
        _filters = [filters.message_type.VideoNote()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_voice(self):
        _filters = [filters.message_type.Voice()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_contact(self):
        _filters = [filters.message_type.Contact()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_dice(self):
        _filters = [filters.message_type.Dice()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_game(self):
        _filters = [filters.message_type.Game()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_poll(self):
        _filters = [filters.message_type.Poll()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_venue(self):
        _filters = [filters.message_type.Venue()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_location(self):
        _filters = [filters.message_type.Location()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_new_chat_members(self):
        _filters = [filters.message_type.NewChatMembers()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_left_chat_member(self):
        _filters = [filters.message_type.LeftChatMember()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_new_chat_title(self):
        _filters = [filters.message_type.NewChatTitle()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_new_chat_photo(self):
        _filters = [filters.message_type.NewChatPhoto()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_delete_chat_photo(self):
        _filters = [filters.message_type.DeleteChatPhoto()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_group_chat_created(self):
        _filters = [filters.message_type.GroupChatCreated()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_supergroup_chat_created(self):
        _filters = [filters.message_type.SupergroupChatCreated()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_channel_chat_created(self):
        _filters = [filters.message_type.ChannelChatCreated()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_message_auto_delete_timer_changed(self):
        _filters = [filters.message_type.MessageAutoDeleteTimerChanged()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_migrate_to_chat_id(self):
        _filters = [filters.message_type.MigrateToChatId()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_migrate_from_chat_id(self):
        _filters = [filters.message_type.MigrateFromChatId()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_pinned_message(self):
        _filters = [filters.message_type.PinnedMessage()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_invoice(self):
        _filters = [filters.message_type.Invoice()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_successful_payment(self):
        _filters = [filters.message_type.SuccessfulPayment()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_connected_website(self):
        _filters = [filters.message_type.ConnectedWebsite()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_passport_data(self):
        _filters = [filters.message_type.PassportData()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_proximity_alert_triggered(self):
        _filters = [filters.message_type.ProximityAlertTriggered()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_video_chat_scheduled(self):
        _filters = [filters.message_type.VideoChatScheduled()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_video_chat_started(self):
        _filters = [filters.message_type.VideoChatStarted()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_video_chat_ended(self):
        _filters = [filters.message_type.VideoChatEnded()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_video_chat_participants_invited(self):
        _filters = [filters.message_type.VideoChatParticipantsInvited()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_web_app_data(self):
        _filters = [filters.message_type.WebAppData()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _
