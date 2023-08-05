#!/usr/bin/env python3
import enum

from ..apis.base_api import BaseApi, DEFAULT_TIMEOUT
from ..apis.cmdid import _PCProgramCmdId
from ..pb2.codemao_getactionlist_pb2 import GetActionListRequest, GetActionListResponse
from ..pb2.codemao_moverobot_pb2 import MoveRobotRequest, MoveRobotResponse
from ..pb2.codemao_playaction_pb2 import PlayActionRequest, PlayActionResponse
from ..pb2.codemao_playcustomaction_pb2 import PlayCustomActionRequest, PlayCustomActionResponse
from ..pb2.codemao_stopaction_pb2 import StopActionRequest, StopActionResponse
from ..pb2.codemao_stopcustomaction_pb2 import StopCustomActionRequest, StopCustomActionResponse
from ..pb2.pccodemao_message_pb2 import Message


class PlayAction(BaseApi):
    """Execute built-in action API

     The robot performs a built-in action with a specified name
     The action name can be obtained with GetActionList APi

    Args:
        is_serial (bool): Whether to wait for a reply, the default is True
        action_name (str): Action name, cannot be none or empty string

    #PlayActionResponse.isSuccess : True or False

    #PlayActionResponse.resultCode : Result Code

    """

    def __init__(self, is_serial: bool = True, action_name: str = None):
        """执行动作api初始化
        """
        assert isinstance(action_name, str) and action_name is not None and len(
            action_name), 'PlayAction actionName should be available'
        self.__is_serial = is_serial
        self.__action_name = action_name

    async def execute(self):
        """Send instructions to execute actions

        Returns:
            PlayActionResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT
        request = PlayActionRequest()
        request.actionName = self.__action_name

        cmd_id = _PCProgramCmdId.PLAY_ACTION_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def _parse_msg(self, message):
        """解析回复指令

        Args:
            message (Message):待解析的Message对象

        Returns:
            PlayActionResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = PlayActionResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class StopAllAction(BaseApi):
    """Stop all action API

    Stop all actions being performed, stop the specified custom action.

    if the action is an uninterruptible action, StopCustomActionResponse.resultCode = 403

    Args
        is_serial (bool): Whether to wait for a reply, the default is True

    """

    def __init__(self, is_serial: bool = True):
        self.__is_serial = is_serial

    async def execute(self):
        """
        Send command to stop all actions

        Returns:
            StopActionResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT

        request = StopActionRequest()

        cmd_id = _PCProgramCmdId.STOP_ACTION_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            StopActionResponse

            #StopCustomActionResponse.isSuccess : 是否成功

            #StopCustomActionResponse.resultCode : 返回码

        """
        if isinstance(message, Message):
            data = message.bodyData
            response = StopActionResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


@enum.unique
class MoveRobotDirection(enum.Enum):
    """Robot moving direction

    FORWARD :  move forward

    BACKWARD : move backward

    LEFTWARD : move leftward

    RIGHTWARD : move rightward
    """
    FORWARD = 3  # 向前
    BACKWARD = 4  # 向后
    LEFTWARD = 1  # 向左
    RIGHTWARD = 2  # 向右


class MoveRobot(BaseApi):
    """Control robot moving-API

     Control the robot to move n steps in a certain direction (MoveRobotDirection)

    Args:
        is_serial (bool): Whether to wait for a reply, the default is True
        direction (MoveRobotDirection): Robot movement direction, default FORWARD, move forward
        step (int): Number of steps, default 1 step

    #MoveRobotResponse.isSuccess : True or False

    #MoveRobotResponse.code : Result Code

    """

    def __init__(self, is_serial: bool = True, direction: MoveRobotDirection = MoveRobotDirection.FORWARD,
                 step: int = 1):
        assert isinstance(direction, MoveRobotDirection), 'MoveRobot : direction should be MoveRobotDirection instance'
        assert isinstance(step, int) and step > 0, 'MoveRobot : step should be Positive'
        self.__is_serial = is_serial
        self.__direction = direction.value
        self.__step = step

    async def execute(self):
        """Send robot movement instructions

        Returns:
            MoveRobotResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT

        request = MoveRobotRequest()
        request.direction = self.__direction
        request.step = self.__step

        cmd_id = _PCProgramCmdId.MOVE_ROBOT_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            MoveRobotResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = MoveRobotResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


@enum.unique
class RobotActionType(enum.Enum):
    """
    Robot action resource type

    INNER (built-in): the unmodifiable motion file built into the robot

    CUSTOM (custom): Action files that can be modified by the developer placed in the sdcard/customize/actions directory

    """
    INNER = 0  # 内置
    CUSTOM = 1  # 自定义


class GetActionList(BaseApi):
    """Get robot action resource list API

     Get a list of action files stored in the robot's local (built-in/custom)

     Args:
         is_serial (bool): Whether to wait for a reply, the default is True
         action_type (RobotActionType): Action type, default is INNER, built-in action

     #GetActionListResponse.actionList ([str]): Action list, str array

     #GetActionListResponse.isSuccess: Is it successful, True Or False

     #GetActionListResponse.resultCode: Result Code

    """

    def __init__(self, is_serial: bool = True, action_type: RobotActionType = RobotActionType.INNER):
        assert isinstance(action_type, RobotActionType), 'GetActionList : action_type should be RobotActionType ' \
                                                         'instance '
        self.__is_serial = is_serial
        self.__action_type = action_type.value

    async def execute(self):
        """Send command to get list of robot actions

        Returns:
            GetActionListResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT

        request = GetActionListRequest()
        request.actionType = self.__action_type

        cmd_id = _PCProgramCmdId.GET_ACTION_LIST.value

        return await self.send(cmd_id, request, timeout)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            GetActionListResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = GetActionListResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class PlayCustomAction(BaseApi):
    """xecute custom action api

    Let the robot perform a custom action with a specified name.

    Action name can be obtained with GetActionList.

    Args:
         is_serial (bool): Whether to wait for a reply, the default is True
         action_name (str): custom action name, cannot be empty or None

    #PlayCustomActionResponse.isSuccess: Is it successful

    #PlayCustomActionResponse.resultCode: Return code
    """

    def __init__(self, is_serial: bool = True, action_name: str = None):

        assert isinstance(action_name, str) and len(action_name) > 0, 'PlayCustomAction : actionName should be ' \
                                                                      'available '
        self.__is_serial = is_serial
        self.__action_name = action_name

    async def execute(self):
        """execute custom action instructions

        Returns:
            PlayCustomActionResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT

        request = PlayCustomActionRequest()
        request.actionName = self.__action_name

        cmd_id = _PCProgramCmdId.PLAY_CUSTOM_ACTION_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            PlayCustomActionResponse
        """

        if isinstance(message, Message):
            data = message.bodyData
            response = PlayCustomActionResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class StopCustomAction(BaseApi):
    """Stop custom action API

     Stop the specified custom action, if the action is an uninterruptible action, StopCustomActionResponse.resultCode = 403

     Args:
         is_serial (bool): Whether to wait for a reply, the default is True
         action_name (str): custom action name, cannot be empty or None

     #StopCustomActionResponse.isSuccess: Is it successful

     #StopCustomActionResponse.resultCode: Return code

    """

    def __init__(self, is_serial: bool = True, action_name: str = None):
        assert isinstance(action_name, str) and len(action_name) > 0, 'StopCustomAction actionName should be available'
        self.__is_serial = is_serial
        self.__action_name = action_name

    async def execute(self):
        """Execute stop custom action command

        Returns:
            StopCustomActionResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT

        request = StopCustomActionRequest()
        request.actionName = self.__action_name

        cmd_id = _PCProgramCmdId.STOP_CUSTOM_ACTION_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            StopCustomActionResponse
        """

        if isinstance(message, Message):
            data = message.bodyData
            response = StopCustomActionResponse()
            response.ParseFromString(data)
            return response
        else:
            return None
