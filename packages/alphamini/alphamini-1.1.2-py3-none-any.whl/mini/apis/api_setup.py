#!/usr/bin/env python3

from ..apis.base_api import BaseApi, DEFAULT_TIMEOUT
from ..apis.cmdid import _PCProgramCmdId
from ..pb2.codemao_revertorigin_pb2 import RevertOriginRequest, RevertOriginResponse
from ..pb2.pccodemao_disconnection_pb2 import DisconnectionRequest, DisconnectionResponse
from ..pb2.pccodemao_getappversion_pb2 import GetAppVersionRequest, GetAppVersionResponse
from ..pb2.pccodemao_message_pb2 import Message


class StartRunProgram(BaseApi):
    """Enter programming mode api

    Robot enters programming mode

    Args:
        is_serial (bool): Whether to wait for a reply, the default is True

    #GetAppVersionResponse.isSuccess: Is it successful

    #GetAppVersionResponse.resultCode: Return code

    #GetAppVersionResponse.version
    """

    def __init__(self, is_serial: bool = True):
        self.__is_serial = is_serial

    async def execute(self):
        """
        Execute the instruction to enter the programming mode

        Returns:
            GetAppVersionResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT

        request = GetAppVersionRequest()

        cmd_id = _PCProgramCmdId.GET_ROBOT_VERSION_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            GetAppVersionResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = GetAppVersionResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class StopRunProgram(BaseApi):
    """Exit programming mode api

    Robot exits programming mode

    Args:
        is_serial (bool): Whether to wait for a reply, the default is True
    """

    def __init__(self, is_serial: bool = True, ):
        self.__is_serial = is_serial

    async def execute(self):
        """
        Execute exit programming mode instruction

        Returns:
            DisconnectionResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT

        request = DisconnectionRequest()

        cmd_id = _PCProgramCmdId.DISCONNECTION_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def _parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = DisconnectionResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class RevertOrigin(BaseApi):
    """Reset api

    Robot reset

    Args:
        is_serial (bool): Whether to wait for a reply, the default is True

    #RevertOriginResponse.isSuccess: Is it successful

    #RevertOriginResponse.resultCode: Return code
    """

    def __init__(self, is_serial: bool = True):
        self.__is_serial = is_serial

    async def execute(self):
        """
        Execute robot reset instruction

        Returns:
            RevertOriginResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT

        request = RevertOriginRequest()

        cmd_id = _PCProgramCmdId.REVERT_ORIGIN_REQUEST.value

        return await self.send(cmd_id, request, timeout)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            RevertOriginResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = RevertOriginResponse()
            response.ParseFromString(data)
            return response
        else:
            return None
