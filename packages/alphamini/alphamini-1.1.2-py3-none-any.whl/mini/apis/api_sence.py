#!/usr/bin/env python3

import enum

from ..apis.base_api import BaseApi, DEFAULT_TIMEOUT
from ..apis.cmdid import _PCProgramCmdId
from ..pb2.codemao_faceanalyze_pb2 import FaceAnalyzeRequest, FaceAnalyzeResponse
from ..pb2.codemao_facedetect_pb2 import FaceDetectRequest, FaceDetectResponse
from ..pb2.codemao_facerecognise_pb2 import FaceRecogniseRequest, FaceRecogniseResponse
from ..pb2.codemao_getinfrareddistance_pb2 import GetInfraredDistanceRequest, GetInfraredDistanceResponse
from ..pb2.codemao_getregisterfaces_pb2 import GetRegisterFacesRequest, GetRegisterFacesResponse
from ..pb2.codemao_recogniseobject_pb2 import RecogniseObjectRequest, RecogniseObjectResponse
from ..pb2.codemao_takepicture_pb2 import TakePictureRequest, TakePictureResponse
from ..pb2.pccodemao_message_pb2 import Message


class FaceDetect(BaseApi):
    """Detect the number of faces api

    Args:
        is_serial (bool): Whether to wait for a reply, the default is True
        timeout (int): timeout time, must be greater than 0

    #FaceDetectResponse.count: the number of faces

    #FaceDetectResponse.isSuccess: Is it successful

    #FaceDetectResponse.resultCode: Return code

    #FaceDetectResponse.commandId
    """

    def __init__(self, is_serial: bool = True, timeout: int = 10):
        assert isinstance(timeout, int) and timeout > 0, 'FaceDetect : timeout should be positive'
        self.__is_serial = is_serial
        self.__timeout = timeout

    async def execute(self):
        """
        Execute instructions for detecting the number of faces

        Returns:
            FaceDetectResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT

        request = FaceDetectRequest()
        request.timeout = self.__timeout

        cmd_id = _PCProgramCmdId.FACE_DETECT_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            FaceDetectResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = FaceDetectResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class FaceAnalysis(BaseApi):
    """Face analysis api

    Analyze gender and age through face recognition

    When multiple people are in front of the camera, return to the one with the largest face area

    Args:
        is_serial (bool): Whether to wait for a reply, the default is True
        timeout (int): timeout

    Return example: FaceAnalyzeResponse{"age":24,"gender":99,"height":238,"width":238}

    #FaceAnalyzeResponse.faceInfos: face information array [FaceInfoResponse]

    #FaceInfoResponse.gender (int) :[0,100], females less than 50, males greater than 50

    #FaceInfoResponse.age: age

    #FaceInfoResponse.width: The width of the face in the camera screen

    #FaceInfoResponse.height: The height of the face in the camera screen


    #FaceAnalyzeResponse.isSuccess: Is it successful, True or False

    #FaceAnalyzeResponse.resultCode: Return code

    """

    def __init__(self, is_serial: bool = True, timeout: int = 10):
        assert isinstance(timeout, int) and timeout > 0, 'FaceAnalysis : timeout should be positive'
        self.__is_serial = is_serial
        self.__timeout = timeout

    async def execute(self):
        """
        Execute face analysis commands

        Returns:
            FaceAnalyzeResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT
        request = FaceAnalyzeRequest()
        request.timeout = self.__timeout

        cmd_id = _PCProgramCmdId.FACE_ANALYSIS_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            FaceAnalyzeResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = FaceAnalyzeResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


@enum.unique
class ObjectRecogniseType(enum.Enum):
    """
    Object recognition type
    ALL: All Object

    FRUIT: Fruit

    GESTURE: Gesture

    FLOWER: Flower
    """
    ALL = 0  # All object
    FRUIT = 1  # Fruit
    GESTURE = 2  # Gesture
    FLOWER = 3  # flower


class ObjectRecognise(BaseApi):
    """Object recognition api

    The robot recognizes the corresponding object (fruit/gesture/flower) through the camera

    Args:
        is_serial (bool): Whether to wait for a reply, the default is True
        object_type (ObjectRecogniseType): Object recognition type, default FRUIT, fruit
        timeout (int): timeout

    #RecogniseObjectResponse.objects: array of object names [str]

    #RecogniseObjectResponse.isSuccess: Is it successful

    #RecogniseObjectResponse.resultCode: Return code
    """

    def __init__(self, is_serial: bool = True, object_type: ObjectRecogniseType = ObjectRecogniseType.FRUIT,
                 timeout: int = 10):
        assert isinstance(timeout, int) and timeout > 0, 'ObjectRecognise : timeout should be positive'
        assert isinstance(object_type, ObjectRecogniseType), 'ObjectRecognise : objectType should be ' \
                                                             'ObjectRecogniseType instance '
        self.__is_serial = is_serial
        self.__object_type = object_type.value
        self.__timeout = timeout

    async def execute(self):
        """
        Execute object recognition commands

        Returns:
            RecogniseObjectResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT

        request = RecogniseObjectRequest()
        request.objectType = self.__object_type
        request.timeout = self.__timeout

        cmd_id = _PCProgramCmdId.RECOGNISE_OBJECT_REQUEST.value

        return await self.send(cmd_id, request, timeout)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            RecogniseObjectResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = RecogniseObjectResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class FaceRecognise(BaseApi):
    """Face recognition api

    The robot recognizes all facial information (acquaintances/strangers) through the camera

    Args:
        is_serial (bool): Whether to wait for a reply, the default is True
        timeout (int): timeout

    #FaceRecogniseResponse.faceInfos([FaceInfoResponse]): face information array

    #FaceInfoResponse.id: face id

    #FaceInfoResponse.name: name, if it is a stranger, the default name is "stranger"

    #FaceRecogniseResponse.isSuccess: Is it successful, True or False

    #FaceRecogniseResponse.resultCode: Return code

    #FaceRecogniseResponse.commandId
    """

    def __init__(self, is_serial: bool = True, timeout: int = 10):
        assert isinstance(timeout, int) and timeout > 0, 'ObjectRecognise : timeout should be positive'
        self.__is_serial = is_serial
        self.__timeout = timeout

    async def execute(self):
        """
        Execute facial recognition commands

        Returns:
            FaceRecogniseResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT
        request = FaceRecogniseRequest()
        request.timeout = self.__timeout

        cmd_id = _PCProgramCmdId.FACE_RECOGNISE_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            FaceRecogniseResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = FaceRecogniseResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


@enum.unique
class TakePictureType(enum.Enum):
    """
    Type of photo

    IMMEDIATELY: Take pictures immediately

    FINDFACE: Find faces and take photos
    """
    IMMEDIATELY = 0  # Take pictures immediately
    FINDFACE = 1  # Find faces and take photos


class TakePicture(BaseApi):
    """Photo api

    Control the robot to take pictures

    Args:
        is_serial (bool): Whether to wait for a reply, the default is True
        take_picture_type (TakePictureType): Take picture type, default IMMEDIATELY, take picture immediately

    #TakePictureResponse.isSuccess: Is it successful, True or False

    #TakePictureResponse.code: Return code

    #TakePictureResponse.picPath: The storage path of the photo in the robot (sdcard/)
    """

    def __init__(self, is_serial: bool = True, take_picture_type: TakePictureType = TakePictureType.IMMEDIATELY):
        assert isinstance(take_picture_type, TakePictureType), 'TakePicture : take_picture_type should be ' \
                                                               'TakePictureType instance '
        self.__is_serial = is_serial
        self.__type = take_picture_type.value

    async def execute(self):
        """
        Execute photo command

        Returns:
            TakePictureResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT
        request = TakePictureRequest()
        request.type = self.__type

        cmd_id = _PCProgramCmdId.TAKE_PICTURE_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            TakePictureResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = TakePictureResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class GetInfraredDistance(BaseApi):
    """Get infrared distance api

    Get the infrared distance of the obstacle closest to the front of the robot

    Args:
        is_serial (bool): Whether to wait for a reply, the default is True

    #GetInfraredDistanceResponse.distance: Infrared distance
    """

    def __init__(self, is_serial: bool = True):
        self.__is_serial = is_serial

    async def execute(self):
        """
        Execute command to obtain infrared distance

        Returns:
            GetInfraredDistanceResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT
        request = GetInfraredDistanceRequest()

        cmd_id = _PCProgramCmdId.GET_INFRARED_DISTANCE_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            GetInfraredDistanceResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = GetInfraredDistanceResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class GetRegisterFaces(BaseApi):
    """Get the registered face list api

    Obtain the face list data registered in the robot

    Args:
        is_serial (bool): Whether to wait for a reply, the default is True

    #GetRegisterFacesResponse.faceInfos([FaceInfoResponse]): face information array

    #FaceInfoResponse.id: face id

    #FaceInfoResponse.name: name

    #GetRegisterFacesResponse.isSuccess: Is it successful, True or False

    #GetRegisterFacesResponse.resultCode: Return code

    """

    def __init__(self, is_serial: bool = True):
        self.__is_serial = is_serial

    async def execute(self):
        """
        Execute the command to get the list of registered faces

        Returns:
            GetRegisterFacesResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT
        request = GetRegisterFacesRequest()

        cmd_id = _PCProgramCmdId.GET_REGISTER_FACES_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            GetRegisterFacesResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = GetRegisterFacesResponse()
            response.ParseFromString(data)
            return response
        else:
            return None
