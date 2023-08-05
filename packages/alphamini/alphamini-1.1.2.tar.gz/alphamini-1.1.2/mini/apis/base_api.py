#!/usr/bin/env python3
import abc
import asyncio
import enum
from abc import ABC
from typing import Callable, Union

from ..channels.websocket_client import ubt_websocket as _UBTWebSocket, AbstractMsgHandler

DEFAULT_TIMEOUT = 300

socket = _UBTWebSocket()


@enum.unique
class MiniApiResultType(enum.Enum):
    """
    Api return result status type

    Success: Received robot reply

    Timeout: Reply to the robot received within the timeout period

    Unsupported: The instruction is not supported

    """
    Success = 1  # Success
    Timeout = 2  # Timeout
    Unsupported = 3  # Unsupported command


class BaseApi(abc.ABC):
    """Message api base class
    """

    async def send(self, cmd_id: int, message, timeout: int) -> Union[object, bool]:
        """Send message method

        Note: Called internally by subclass functions, subclass instances cannot be called.

        Args:
            cmd_id (int): Supported command id, for example: mini.apis.cmdid.PLAY_ACTION_REQUEST
            message (Message): Supported message entity, for example: mini.pb2.PlayActionRequest
            timeout (int): timeout time. When timeout<=0, it means that there is no need to wait for the robot to reply.When timeout>0, it means that it needs to wait for the robot to reply.

        Returns:
            If the instruction is not supported, return tuple(MiniApiResultType.Unsupported,None)

            If the instruction is supported

            When timeout<=0, bool is returned, indicating whether the message was sent successfully

            When timeout>0

            If the message times out or fails to be sent, tuple(MiniApiResultType.Timeout,None) is returned

            If the message has a reply, it will return tuple(MiniApiResultType.Success,result), result is the corresponding reply message

        """
        assert cmd_id >= 0, 'cmdId should not be negative number in BaseApi'
        assert message is not None, 'message should not be none in BaseApi'
        # 通用的发送消息逻辑
        if timeout <= 0:
            return await socket.send_msg0(cmd_id, message)
        else:
            result = await socket.send_msg(cmd_id, message, timeout)
            if result:
                if result.header.target == -1:
                    import logging
                    log = logging.getLogger(__name__)
                    log.addHandler(logging.StreamHandler())
                    log.setLevel(logging.WARNING)
                    log.warning(f'当前机器人版本不支持命令:cmd={message.header.command}, 请升级机器人系统版本.')
                    return MiniApiResultType.Unsupported, None
                else:
                    return MiniApiResultType.Success, self._parse_msg(result)
            else:
                return MiniApiResultType.Timeout, None

    async def execute(self):
        """Send instructions

        After serializing the supported message, write it to the socket
        Implemented by subclasses
        """
        raise NotImplementedError()

    def _parse_msg(self, message):
        """解析回复指令

        将收到的Message对象包含的消息数据反序列化为相应的response
        由子类实现，仅供子类内部调用
        Args:
            message: Message对象
        """
        raise NotImplementedError()


class BaseApiNeedResponse(BaseApi, abc.ABC):
    """
    The message api base class that needs to be replied, timeout cannot be empty
    """

    async def send(self, cmd_id, data, timeout: int):
        """Override the parent method

        Check timeout, must be >0
        """

        assert timeout > 0, 'timeout should be Positive number in BaseApiNeedResponse'
        return await super().send(cmd_id, data, timeout)


class BaseApiNoNeedResponse(BaseApi, ABC):
    """Message api base class without reply
    """

    async def send(self, cmd_id, message, timeout: int = 0):
        """Override the parent method

        Set timeout to 0
        """

        return await super().send(cmd_id, message, 0)


class BaseEventApi(BaseApiNoNeedResponse, AbstractMsgHandler, ABC):
    """Event class message api base class

    When the event handler is registered, the event message actively pushed by the robot

    Args:
        cmd_id (int): registered instruction id
        message (Message): the registration message sent to the robot
        is_repeat (bool): Whether to repeat the monitoring, the default is True
        timeout (int): timeout time, the default is 0
        handler (Callable): event message handler, f(message)

    """

    def __init__(self, cmd_id: int, message, is_repeat: bool = True, timeout: int = 0,
                 handler: 'Callable[..., None]' = None):
        """初始化事件类消息
        """
        super().__init__()
        self.__cmd_id = cmd_id
        self.__request = message
        self.__is_repeat = is_repeat
        self.__timeout = timeout
        self.__handler = handler

        if is_repeat:
            self.__repeatCount = -1
        else:
            self.__repeatCount = 1

    def set_handler(self, handler: 'Callable[..., None]' = None):
        """Set up event message handler

        Args:
            handler (Callable): event message handler, f(message)

        """
        self.__handler = handler

    def start(self):
        """Start the listener
        """

        # 发送消息
        asyncio.create_task(self.send(cmd_id=self.__cmd_id, message=self.__request))
        # 注册监听
        socket.register_msg_handler(cmd=self.__cmd_id, handler=self)

    def stop(self):
        """Stop listener

        The subclass needs to notify the robot to stop reporting the event
        """

        # 移除消息监听
        socket.unregister_msg_handler(cmd=self.__cmd_id, handler=self)

    # AbstractMsgHandler
    def handle_msg(self, message):
        # 处理监听次数
        if self.__repeatCount > 0:
            # 有监听次数
            self.__handle_msg(message)
            self.__repeatCount -= 1
        elif self.__repeatCount == -1:
            # 无限监听
            self.__handle_msg(message)

    def __handle_msg(self, message):
        if message.header.target == -1:
            import logging
            log = logging.getLogger(__name__)
            log.addHandler(logging.StreamHandler())
            log.setLevel(logging.WARNING)
            log.warning(f'当前机器人版本不支持命令:cmd={message.header.command}, 请升级机器人系统版本.')
            return
        if self.__handler is not None:
            self.__handler(self._parse_msg(message))
