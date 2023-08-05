#!/usr/bin/env python3

# 每种传感器做一个单例对象进行监听

import asyncio
import enum

from ..apis.base_api import BaseEventApi, BaseApiNoNeedResponse
from ..apis.cmdid import _PCProgramCmdId
from ..pb2.codemao_facedetecttask_pb2 import FaceDetectTaskRequest, FaceDetectTaskResponse
from ..pb2.codemao_facerecognisetask_pb2 import FaceRecogniseTaskRequest, FaceRecogniseTaskResponse
from ..pb2.codemao_observefallclimb_pb2 import ObserveFallClimbRequest, ObserveFallClimbResponse
from ..pb2.codemao_observeheadracket_pb2 import ObserveHeadRacketRequest, ObserveHeadRacketResponse
from ..pb2.codemao_observeinfrareddistance_pb2 import ObserveInfraredDistanceRequest, ObserveInfraredDistanceResponse
from ..pb2.codemao_speechrecognise_pb2 import SpeechRecogniseRequest, SpeechRecogniseResponse
from ..pb2.codemao_stopspeechrecognise_pb2 import StopSpeechRecogniseRequest, StopSpeechRecogniseResponse
from ..pb2.pccodemao_message_pb2 import Message


class ObserveSpeechRecognise(BaseEventApi):
    """Monitor speech recognition api

    Monitor voice recognition events, and the robot reports the text after voice recognition

    #SpeechRecogniseResponse.text: The recognized text

    #SpeechRecogniseResponse.isSuccess: Is it successful

    #SpeechRecogniseResponse.resultCode: Return code

    """

    async def execute(self):
        pass

    def __init__(self):

        cmd_id = _PCProgramCmdId.SPEECH_RECOGNISE.value

        message = SpeechRecogniseRequest()

        BaseEventApi.__init__(self, cmd_id=cmd_id, message=message)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            SpeechRecogniseResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = SpeechRecogniseResponse()
            response.ParseFromString(data)
            return response
        else:
            return None

    def stop(self):
        """
        Stop speech recognition, stop monitoring speech recognition

        Returns:
            None
        """

        asyncio.create_task(_StopSpeechRecognise().execute())

        super().stop()


class _StopSpeechRecognise(BaseApiNoNeedResponse):
    """停止语音识别api

    #StopSpeechRecogniseResponse.isSuccess : 是否成功

    #StopSpeechRecogniseResponse.resultCode : 返回码
    """

    async def execute(self):
        """
        执行停止语音识别指令

        Returns:
            bool: 是否发送指令成功
        """

        request = StopSpeechRecogniseRequest()

        cmd_id = _PCProgramCmdId.STOP_SPEECH_RECOGNISE_REQUEST.value

        return await self.send(cmd_id, request)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            StopSpeechRecogniseResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = StopSpeechRecogniseResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class ObserveFaceDetect(BaseEventApi):
    """Monitor the number of faces api

    Monitor the number of faces events, and the robot reports the number of detected faces

    Single detection timeout time 1s, detection interval 1s

    #FaceDetectTaskResponse.count(int): the number of faces

    #FaceDetectTaskResponse.isSuccess: Is it successful, True or False

    #FaceDetectTaskResponse.resultCode: Return code
    """

    async def execute(self):
        pass

    def __init__(self):

        cmd_id = _PCProgramCmdId.FACE_DETECT_TASK_REQUEST.value

        request = FaceDetectTaskRequest()

        # 单次侦测超时时间
        request.timeout = 1000

        # 侦测间隔时间
        request.period = 1000

        # 任务延时时间
        request.delay = 0

        # 检测开关
        request.switch = True

        BaseEventApi.__init__(self, cmd_id=cmd_id, message=request)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            FaceDetectTaskResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = FaceDetectTaskResponse()
            response.ParseFromString(data)
            return response
        else:
            return None

    def stop(self):
        """
        Stop detecting the number of faces, stop monitoring the number of faces

        Returns:
            None
        """

        asyncio.create_task(_StopFaceDetect().execute())

        super().stop()


class _StopFaceDetect(BaseApiNoNeedResponse):
    """停止人脸个数检测api

    """

    async def execute(self):
        """
        执行停止人脸个数检测指令

        Returns:
            None
        """

        request = FaceDetectTaskRequest()

        # 检测开关
        request.switch = False

        cmd_id = _PCProgramCmdId.FACE_DETECT_TASK_REQUEST.value

        return await self.send(cmd_id, request)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            FaceDetectTaskResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = FaceDetectTaskResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class ObserveFaceRecognise(BaseEventApi):
    """Monitor face recognition api

    Monitor face recognition events, and the robot reports the recognized face information (array)

    If it is a registered face, return face details: id, name, gender, age

    If it is a stranger, return name: "stranger"

    Single detection timeout time 1s, detection interval 1s

    # FaceRecogniseTaskResponse.faceInfos: [FaceInfoResponse] face information array

    # FaceInfoResponse.id, FaceInfoResponse.name,FaceInfoResponse.gender,FaceInfoResponse.age: face details

    # FaceRecogniseTaskResponse.isSuccess: Is it successful, True or False

    # FaceRecogniseTaskResponse.resultCode: Return code

    """

    async def execute(self):
        pass

    def __init__(self):

        cmd_id = _PCProgramCmdId.FACE_RECOGNISE_TASK_REQUEST.value

        request = FaceRecogniseTaskRequest()

        # 单次侦测超时时间
        request.timeout = 1000

        # 侦测间隔时间
        request.period = 1000

        # 任务延时时间
        request.delay = 0

        # 检测开关
        request.switch = True

        BaseEventApi.__init__(self, cmd_id=cmd_id, message=request)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            FaceRecogniseTaskResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = FaceRecogniseTaskResponse()
            response.ParseFromString(data)
            return response
        else:
            return None

    def stop(self):
        """
        Stop face recognition, stop monitoring face recognition

        Returns:
            None
        """

        asyncio.create_task(_StopFaceRecognise().execute())

        super().stop()


class _StopFaceRecognise(BaseApiNoNeedResponse):
    """停止人脸识别api

    """

    async def execute(self):
        """
        执行停止人脸识别指令

        Returns:
            FaceRecogniseTaskResponse
        """

        request = FaceRecogniseTaskRequest()

        # 检测开关
        request.switch = False

        cmd_id = _PCProgramCmdId.FACE_RECOGNISE_TASK_REQUEST.value

        return await self.send(cmd_id, request)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            FaceRecogniseTaskResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = FaceRecogniseTaskResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class ObserveInfraredDistance(BaseEventApi):
    """Monitor infrared distance api

    Monitor infrared distance events, the robot reports the detected infrared distance to the nearest obstacle in front of you

    Detection cycle 1s

    # ObserveInfraredDistanceResponse.distance: infrared distance

    """

    async def execute(self):
        pass

    def __init__(self):

        cmd_id = _PCProgramCmdId.SUBSCRIBE_INFRARED_DISTANCE_REQUEST.value

        request = ObserveInfraredDistanceRequest()

        # 检测周期
        request.samplingPeriod = 1000

        # 检测开关
        request.isSubscribe = True

        BaseEventApi.__init__(self, cmd_id=cmd_id, message=request)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            ObserveInfraredDistanceResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = ObserveInfraredDistanceResponse()
            response.ParseFromString(data)
            return response
        else:
            return None

    def stop(self):
        """
        Stop infrared distance detection, stop monitoring infrared distance

        Returns:
            None
        """

        asyncio.create_task(_StopObserveInfraredDistance().execute())

        super().stop()


class _StopObserveInfraredDistance(BaseApiNoNeedResponse):
    """停止红外距离监测api

    """

    async def execute(self):
        """
        执行停止红外监测指令

        Returns:
            ObserveInfraredDistanceResponse
        """

        request = ObserveInfraredDistanceRequest()

        # 检测开关
        request.isSubscribe = False

        cmd_id = _PCProgramCmdId.FACE_RECOGNISE_TASK_REQUEST.value

        return await self.send(cmd_id, request)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            ObserveInfraredDistanceResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = ObserveInfraredDistanceResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


@enum.unique
class RobotPosture(enum.Enum):
    """
    Robot pose

    STAND: standing

    SPLITS_LEFT: Left lunge

    SPLITS_RIGHT: Right lunge

    SIT_DOWN: sit down

    SQUAT_DOWN: Squat down

    KNEELING: kneel down

    LYING: lying on the side

    LYING_DOWN: lie flat

    SPLITS_LEFT_1: Left split

    SPLITS_RIGHT_2: Right split

    BEND: Bent over
    """
    STAND = 1  # 站立
    SPLITS_LEFT = 2  # 左弓步
    SPLITS_RIGHT = 3  # 右弓步
    SIT_DOWN = 4  # 坐下
    SQUAT_DOWN = 5  # 蹲下
    KNEELING = 6  # 跪下
    LYING = 7  # 侧躺
    LYING_DOWN = 8  # 平躺
    SPLITS_LEFT_1 = 9  # 左劈叉
    SPLITS_RIGHT_2 = 10  # 右劈叉
    BEND = 11  # 弯腰


class ObserveRobotPosture(BaseEventApi):
    """Monitor robot attitude api

    Monitor robot posture change events, and the machine reports the current posture RobotPosture (when the posture changes)

    #ObserveFallClimbResponse.status: Machine posture, the value corresponds to RobotPosture

    """

    async def execute(self):
        pass

    def __init__(self):

        cmd_id = _PCProgramCmdId.SUBSCRIBE_ROBOT_POSTURE_REQUEST.value

        request = ObserveFallClimbRequest()

        # 检测开关
        request.isSubscribe = True

        BaseEventApi.__init__(self, cmd_id=cmd_id, message=request)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            ObserveFallClimbResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = ObserveFallClimbResponse()
            response.ParseFromString(data)
            return response
        else:
            return None

    def stop(self):
        """
        Stop robot pose detection, stop monitoring robot pose

        Returns:
            None
        """

        asyncio.create_task(_StopObserveRobotPosture().execute())

        super().stop()


class _StopObserveRobotPosture(BaseApiNoNeedResponse):
    """停止监听机器人姿态api

    """

    async def execute(self):
        """
        执行停止机器人姿态监测

        Returns:
            ObserveFallClimbResponse
        """

        request = ObserveFallClimbRequest()

        # 检测开关
        request.isSubscribe = False

        cmd_id = _PCProgramCmdId.SUBSCRIBE_ROBOT_POSTURE_REQUEST.value

        return await self.send(cmd_id, request)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            ObserveFallClimbResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = ObserveFallClimbResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


@enum.unique
class HeadRacketType(enum.Enum):
    """
    Head shot

    SINGLE_CLICK: click

    LONG_PRESS: Long press

    DOUBLE_CLICK: double click
    """
    SINGLE_CLICK = 1  # 单击
    LONG_PRESS = 2  # 长按
    DOUBLE_CLICK = 3  # 双击


class ObserveHeadRacket(BaseEventApi):
    """Listen to the head event api

    Monitor the head event, and report the head type when the robot's head is tapped

    # ObserveHeadRacketResponse.type: Racket head type, HeadRacketType
    """

    async def execute(self):
        pass

    def __init__(self):

        cmd_id = _PCProgramCmdId.SUBSCRIBE_HEAD_RACKET_REQUEST.value

        message = ObserveHeadRacketRequest()

        # 检测开关
        message.isSubscribe = True

        BaseEventApi.__init__(self, cmd_id=cmd_id, message=message)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            ObserveHeadRacketResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = ObserveHeadRacketResponse()
            response.ParseFromString(data)
            return response
        else:
            return None

    def stop(self):
        """
        Stop the detection of the robot head event, stop listening to the robot head event

        Returns:
            None
        """

        asyncio.create_task(_StopObserveHeadRacket().execute())

        super().stop()


class _StopObserveHeadRacket(BaseApiNoNeedResponse):
    """停止拍头事件监测api

    """

    async def execute(self):
        """
        执行停止拍头事件监测指令

        Returns:
            ObserveHeadRacketResponse
        """

        request = ObserveHeadRacketRequest()

        # 检测开关
        request.isSubscribe = False

        cmd_id = _PCProgramCmdId.SUBSCRIBE_ROBOT_POSTURE_REQUEST.value

        return await self.send(cmd_id, request)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            ObserveHeadRacketResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = ObserveHeadRacketResponse()
            response.ParseFromString(data)
            return response
        else:
            return None
