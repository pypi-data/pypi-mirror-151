from typing import Any, Awaitable, Callable, Optional, final, TYPE_CHECKING

from telegrambots.wrapper.types.objects import CallbackQuery, Message

from ...contexts import CallbackQueryContext, MessageContext
from .handler_template import SealedHandler

if TYPE_CHECKING:
    from telegrambots.wrapper.types.objects import Update

    from ...filters._filters.filter_template import Filter
    from ...dispatcher import Dispatcher


class MessageHandler(SealedHandler[MessageContext, Message]):
    def __init__(
        self,
        dp: "Dispatcher",
        tag: str,
        processor: Callable[[MessageContext], Awaitable[None]],
        filter: Optional["Filter[Message]"] = None,
        continue_after: Optional[list[str]] = None,
        allow_continue_after_self: bool = False,
        priority: int = 0,
    ) -> None:
        super().__init__(
            dp,
            tag,
            Message,
            processor,
            filter,
            continue_after,
            allow_continue_after_self,
            priority,
        )

    @final
    def _build_context(self, update: "Update[Message]", *args: Any, **kwargs: Any):
        return MessageContext(
            self.dp,
            update,
            self.tag,
            *args,
            **kwargs,
        )


class CallbackQueryHandler(SealedHandler[CallbackQueryContext, CallbackQuery]):
    def __init__(
        self,
        dp: "Dispatcher",
        tag: str,
        processor: Callable[[CallbackQueryContext], Awaitable[None]],
        filter: Optional["Filter[CallbackQuery]"] = None,
        continue_after: Optional[list[str]] = None,
        allow_continue_after_self: bool = False,
        priority: int = 0,
    ) -> None:
        super().__init__(
            dp,
            tag,
            CallbackQuery,
            processor,
            filter,
            continue_after,
            allow_continue_after_self,
            priority,
        )

    @final
    def _build_context(
        self, update: "Update[CallbackQuery]", *args: Any, **kwargs: Any
    ):
        return CallbackQueryContext(
            self.dp,
            update,
            self.tag,
            *args,
            **kwargs,
        )
