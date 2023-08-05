#!/usr/bin/env python3

import enum

from ..apis.base_api import BaseApi, DEFAULT_TIMEOUT
from ..apis.cmdid import _PCProgramCmdId
from ..pb2.codemao_controlmouthlamp_pb2 import ControlMouthRequest, ControlMouthResponse
from ..pb2.codemao_playexpression_pb2 import PlayExpressionRequest, PlayExpressionResponse
from ..pb2.codemao_setmouthlamp_pb2 import SetMouthLampRequest, SetMouthLampResponse
from ..pb2.pccodemao_message_pb2 import Message


@enum.unique
class RobotExpressionType(enum.Enum):
    """
    Robot expression type

    INNER (built-in): Unmodifiable emoticon files built into the robot
    """
    # CUSTOM(Custom): Emoticon files placed in the sdcard/customize/expresss directory that can be modified by the
    # developer
    INNER = 0  # Built-in emoji
    # CUSTOM = 1 # Custom emoji


class PlayExpression(BaseApi):
    """Play built-in emoji api

    Let the robot eyes show an expression

    Args:
        is_serial (bool): Whether to wait for a reply, the default is True
        express_name (str): emoticon name, cannot be empty or None

    #PlayExpressionResponse.isSuccess: Is it successful

    #PlayExpressionResponse.resultCode: Return code

    """

    def __init__(self, is_serial: bool = True, express_name: str = None):
        assert express_name is not None and len(express_name), 'PlayExpression: expressName should be available'
        self.__is_serial = is_serial
        self.__express_name = express_name
        self.__dir_type = RobotExpressionType.INNER.value

    async def execute(self):
        """
        Execute the play emoticon command

        Returns:
            PlayExpressionResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT

        request = PlayExpressionRequest()
        request.expressName = self.__express_name
        request.dirType = self.__dir_type

        cmd_id: int = _PCProgramCmdId.PLAY_EXPRESSION_REQUEST.value

        return await self.send(cmd_id, request, timeout)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            PlayExpressionResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = PlayExpressionResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


@enum.unique
class MouthLampColor(enum.Enum):
    """
    Mouth light color

    RED: red

    GREEN: Green

    WHITE: white
    """
    RED = 1  # red
    GREEN = 2  # green
    WHITE = 4  # white


@enum.unique
class MouthLampMode(enum.Enum):
    """
    Mouth light mode

    NORMAL (normal mode): constant light mode

    BREATH (breathing mode): Breathing mode
    """
    NORMAL = 0  # Normal mode
    BREATH = 1  # Breathing mode


class SetMouthLamp(BaseApi):
    """Set mouth light api

    Set parameters such as the mode and color of the mouth light

    When mode=NORMAL, the duration parameter works, indicating how long it will be on

    When mode=BREATH, the breath_duration parameter indicates how often to breathe

    After the setting takes effect, the robot will immediately return the setting result (it has nothing to do with the set duration parameter)

    Args:
         is_serial (bool): Whether to wait for a reply, the default is True
         mode (MouthLampMode): Mouth lamp mode, default NORMAL, normal (constant light) mode
         color (MouthLampColor): Mouth lamp color, default RED, red
         duration (int): duration, in milliseconds, -1 means unlimited time, when the length is set to more than 10s, the result will be returned within 10s
         breath_duration (int): the duration of one blink, in milliseconds

    #SetMouthLampResponse.isSuccess: Is it successful

    #SetMouthLampResponse.resultCode: Return code
    """

    def __init__(self, is_serial: bool = True, mode: MouthLampMode = MouthLampMode.NORMAL,
                 color: MouthLampColor = MouthLampColor.RED, duration: int = 1000, breath_duration: int = 1000):
        assert isinstance(mode, MouthLampMode), 'SetMouthLamp: mode should be MouthLampMode instance'
        assert isinstance(color, MouthLampColor), 'SetMouthLamp: color should be MouthLampColor instance'
        self.serial = is_serial
        self.__is_serial = self.serial
        self.__mode = mode.value
        self.__color = color.value
        self.__duration = duration
        self.__breath_duration = breath_duration

    async def execute(self):
        """
        Execute the command to set the mouth light

        Returns:
            SetMouthLampResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT

        request = SetMouthLampRequest()
        request.model = self.__mode
        request.color = self.__color
        if request.color == 4:
            request.redValue = 0xff
            request.greenValue = 0xff
            request.blueValue = 0xff

        request.duration = self.__duration
        request.breathDuration = self.__breath_duration

        cmd_id = _PCProgramCmdId.SET_MOUTH_LAMP_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            SetMouthLampResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = SetMouthLampResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class ControlMouthLamp(BaseApi):
    """Control mouth light switch api

    Turn on/off the mouth light

    Args:
        is_serial (bool): Whether to wait for a reply, the default is True
        is_open (bool): Whether to turn on the mouth light. Default true, turn on the mouth light

    #ControlMouthResponse.isSuccess: Is it successful

    #ControlMouthResponse.resultCode: Return code
    """

    def __init__(self, is_serial: bool = True, is_open: bool = True):

        self.__is_serial = is_serial
        self.__is_open = is_open

    async def execute(self):
        """
        Execute the command to control the mouth light

        Returns:
            ControlMouthResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT

        request = ControlMouthRequest()
        request.isOpen = self.__is_open

        cmd_id = _PCProgramCmdId.SWITCH_MOUTH_LAMP_REQUEST.value

        return await self.send(cmd_id, request, timeout)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            ControlMouthResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = ControlMouthResponse()
            response.ParseFromString(data)
            return response
        else:
            return None
