#!/usr/bin/env python3

import enum

from ..apis.api_config import ServicePlatform
from ..apis.base_api import BaseApi, DEFAULT_TIMEOUT
from ..apis.cmdid import _PCProgramCmdId
from ..pb2 import cloudstorageurls_pb2
from ..pb2.codemao_changerobotvolume_pb2 import ChangeRobotVolumeRequest, ChangeRobotVolumeResponse
from ..pb2.codemao_controlrobotrecord_pb2 import ControlRobotRecordRequest, ControlRobotRecordResponse
from ..pb2.codemao_controltts_pb2 import ControlTTSRequest, ControlTTSResponse
from ..pb2.codemao_getaudiolist_pb2 import GetAudioListRequest, GetAudioListResponse
from ..pb2.codemao_playaudio_pb2 import PlayAudioRequest, PlayAudioResponse
from ..pb2.codemao_playonlinemusic_pb2 import MusicRequest, MusicResponse
from ..pb2.codemao_stopaudio_pb2 import StopAudioRequest, StopAudioResponse
from ..pb2.pccodemao_message_pb2 import Message


@enum.unique
class TTSControlType(enum.Enum):
    """
    TTS control type

    START: start playing tts

    STOP: Stop playing tts
    """
    START = 1  # play
    STOP = 0  # stop


class StartPlayTTS(BaseApi):
    """Start playing TTS api

    The robot plays the synthesized TTS voice

    Args:
        is_serial (bool): Whether to wait for a reply, the default is True
        text (str): The text to be played, cannot be empty or None

    #ControlTTSResponse.isSuccess: Is it successful, True or False

    #ControlTTSResponse.resultCode: Return code
    """

    def __init__(self, is_serial: bool = True, text: str = None):
        assert isinstance(text, str) and len(text), 'StartPlayTTS : tts text should be available'
        self.__is_serial = is_serial
        self.__text = text
        self.__type = TTSControlType.START.value

    async def execute(self):
        """
        Execute the TTS command to start playing

        Returns:
            ControlTTSResponse

        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT

        request = ControlTTSRequest()
        request.text = self.__text
        request.type = self.__type

        cmd_id = _PCProgramCmdId.PLAY_TTS_REQUEST.value

        return await self.send(cmd_id, request, timeout)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            ControlTTSResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = ControlTTSResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class StopPlayTTS(BaseApi):
    """Stop playing TTS api

    The robot stops playing TTS voice

    Args:
        is_serial (bool): Whether to wait for a reply, the default is True

    #ControlTTSResponse.isSuccess: Is it successful

    #ControlTTSResponse.resultCode: Return code
    """

    def __init__(self, is_serial: bool = True):
        self.__isSerial = is_serial
        self.__type = TTSControlType.STOP.value

    async def execute(self):
        """
        Execute the stop playing TTS command

        Returns:
            ControlTTSResponse

        """
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = ControlTTSRequest()
        request.type = self.__type

        cmd_id = _PCProgramCmdId.PLAY_TTS_REQUEST.value

        return await self.send(cmd_id, request, timeout)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            ControlTTSResponse

        """
        if isinstance(message, Message):
            data = message.bodyData
            response = ControlTTSResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class _PlayTTS(BaseApi):
    """Play/stop TTS api

    The robot plays the synthesized TTS voice

    When control_type is STOP, it means stop all TTS being played

    Args:
        is_serial (bool): Whether to wait for a reply, the default is True
        text (str): The text to be played, cannot be empty or None
        control_type (TTSControlType): control type, default START, start playing

    #ControlTTSResponse.isSuccess: Is it successful, True or False

    #ControlTTSResponse.resultCode: Return code
    """

    def __init__(self, is_serial: bool = True, text: str = None, control_type: TTSControlType = TTSControlType.START):
        assert text is not None and len(text), 'tts text should be available'
        self.__isSerial = is_serial
        self.__text = text
        self.__type = control_type.value

    async def execute(self):
        """
        Execution control TTS instruction

        Returns:
            ControlTTSResponse
        """
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = ControlTTSRequest()
        request.text = self.__text
        request.type = self.__type

        cmd_id = _PCProgramCmdId.PLAY_TTS_REQUEST.value

        return await self.send(cmd_id, request, timeout)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            ControlTTSResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = ControlTTSResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


@enum.unique
class AudioStorageType(enum.Enum):
    """
    Audio storage type

    NET_PUBLIC: public network

    PRESET_LOCAL: The robot is built locally

    CUSTOMIZE_LOCAL: Robot local customization

    """
    # ALIYUN_PRIVATE = 1 # Alibaba Private Cloud
    NET_PUBLIC = 2  # Public network
    PRESET_LOCAL = 3  # Local built-in
    CUSTOMIZE_LOCAL = 4  # Local customization


class PlayAudio(BaseApi):
    """Play audio api

    The robot plays the specified audio, supports mp3, wav, amr, etc.

    Args:
        is_serial (bool): Whether to wait for a reply, the default is True
        url (str): audio address, when storage_type is NET_PUBLIC, url is the URL of the audio file; when storage_type is PRESET_LOCAL/CUSTOMIZE_LOCAL,
                    url is the local audio name (the local audio name can be obtained through the FetchAudioList interface)
        storage_type (AudioStorageType): Audio storage type, default NET_PUBLIC, public network
        volume (float): volume size, range [0.0,1.0], default 1.0

    #PlayAudioResponse.isSuccess: Is it successful

    #PlayAudioResponse.resultCode: Return code

    """

    def __init__(self, is_serial: bool = True, url: str = None,
                 storage_type: AudioStorageType = AudioStorageType.NET_PUBLIC, volume: float = 1.0):

        assert isinstance(url, str) and len(url), 'PlayAudio : url should be available'
        assert isinstance(volume, float) and 0 <= volume <= 1.0, 'PlayAudio : volume should be in range[0,1]'
        assert isinstance(storage_type, AudioStorageType), 'PlayAudio : storage_type shoule be AudioStorageType ' \
                                                           'instance '
        self.__is_serial = is_serial
        self.__url = url
        self.__volume = volume
        self.__cloudStorageType = storage_type.value

    async def execute(self):
        """
        Execute the play audio command

        Returns:
            PlayAudioResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT

        cloud = cloudstorageurls_pb2.CloudStorage()
        cloud.type = self.__cloudStorageType
        cloud.url.extend([self.__url])

        request = PlayAudioRequest()

        request.cloud.CopyFrom(cloud)
        request.volume = self.__volume

        cmd_id = _PCProgramCmdId.PLAY_AUDIO_REQUEST.value

        return await self.send(cmd_id, request, timeout)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            PlayAudioResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = PlayAudioResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class StopAllAudio(BaseApi):
    """Stop all audio APIs

    The robot stops all audio being played

    Args:
        is_serial (bool): Whether to wait for a reply, the default is True

    #StopAudioResponse.isSuccess: Is it successful　

    #StopAudioResponse.resultCode: Return code

    """

    def __init__(self, is_serial: bool = True):
        self.__is_serial = is_serial

    async def execute(self):
        """
        Execute stop all audio commands

        Returns:
            StopAudioResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT

        request = StopAudioRequest()

        cmd_id = _PCProgramCmdId.STOP_AUDIO_REQUEST.value

        return await self.send(cmd_id, request, timeout)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            StopAudioResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = StopAudioResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


@enum.unique
class AudioSearchType(enum.Enum):
    """
    Audio query type

    INNER (built-in): unmodifiable sound effects built into the robot,

    CUSTOM (custom): placed in the sdcard/customize/music directory and can be modified by the developer
    """
    INNER = 0  # Built-in
    CUSTOM = 1  # Custom


class FetchAudioList(BaseApi):
    """Get the audio list api of the robot

    Get the audio list stored in the robot rom or sdcard

    Args:
        is_serial (bool): Whether to wait for a reply, the default is True
        search_type (AudioSearchType): search type, default INNER, built-in robot

    #GetAudioListResponse.audio ([Audio]): Audio effect list

    #Audio.name: Audio effect name

    #Audio.suffix: audio suffix

    #GetAudioListResponse.isSuccess: Is it successful

    #GetAudioListResponse.resultCode: Return code

    """

    def __init__(self, is_serial: bool = True, search_type: AudioSearchType = AudioSearchType.INNER):
        assert isinstance(search_type, AudioSearchType), 'FetchAudioList : search_type should be AudioSearchType ' \
                                                         'instance '
        self.__is_serial = is_serial
        self.__search_type = search_type.value

    async def execute(self):
        """
        Execute get audio list command

        Returns:
            GetAudioListResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT

        request = GetAudioListRequest()

        request.searchType = self.__search_type

        cmd_id = _PCProgramCmdId.GET_AUDIO_LIST_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            GetAudioListResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = GetAudioListResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class __PlayOnlineMusic(BaseApi):
    """Play online song api

    To play QQ music online songs, the robot needs to be bound to the app and authorized

    Args:
        is_serial (bool): Whether to wait for a reply, the default is True
        name (str): song name, cannot be empty or None

    #MusicResponse.isSuccess: Is it successful

    #MusicResponse.resultCode: Return code

    """

    def __init__(self, is_serial: bool = True, name: str = None):
        assert name is not None and len(name), 'PlayOnlineMusic name should be available'
        self.__is_serial = is_serial
        self.__name = name
        self.__platform = ServicePlatform.TENCENT.value

    async def execute(self):
        """
        Execute instructions to play online songs

        Returns:
            MusicResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT

        request = MusicRequest()

        request.platform = self.__platform
        request.name = self.__name

        cmd_id = _PCProgramCmdId.PLAY_ONLINE_MUSIC_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            MusicResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = MusicResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class ChangeRobotVolume(BaseApi):
    """Set robot volume api

    Adjust the robot volume

    Args:
        is_serial (bool): Whether to wait for a reply, the default is True
        volume (float): volume, range [0.0,1.0], default 0.5

    #ChangeRobotVolumeResponse.isSuccess: Is it successful

    #ChangeRobotVolumeResponse.resultCode: Return code

    """

    def __init__(self, is_serial: bool = True, volume: float = 0.5):
        assert isinstance(volume, float) and 0.0 <= volume <= 1.0, 'ChangeRobotVolume : volume should be in range[' \
                                                                   '0.0,1.0] '
        self.__is_serial = is_serial
        self.__volume = volume

    async def execute(self):
        """Send command to set robot volume

        Returns:
            ChangeRobotVolumeResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT

        request = ChangeRobotVolumeRequest()
        request.volume = self.__volume

        cmd_id = _PCProgramCmdId.CHANGE_ROBOT_VOLUME_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            ChangeRobotVolumeResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = ChangeRobotVolumeResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


@enum.unique
class RobotAudioRecordControlType(enum.Enum):
    """
    Robot recording control type
    """
    START_RECORD = 0  # Start recording
    STOP_RECORD = 1  # Stop recording
    START_PLAY = 2  # Start playing
    STOP_PLAY = 3  # Stop playing
    PAUSE_PLAY = 4  # Pause playback
    CONTINUE_PLAY = 5  # Continue playing
    RENAME_FILE = 6  # Rename file


class ControlRobotAudioRecord(BaseApi):
    """Control robot recording/playing api

     Args:
         is_serial (bool): Whether to wait for a reply, the default is True
         control_type (RobotAudioRecordControlType): control type, default START_RECORD, start recording
         time_limit (int): The length of the recording, in ms, the default is 60000ms, which is 60s
         file_name (str): Recording file storage name
         new_file_name (str): rename the name of the recording file

     #ControlRobotRecordResponse.isSuccess: Is it successful

     #ControlRobotRecordResponse.resultCode: Return code

     #ControlRobotRecordResponse.id: The name of the generated recording file

    """

    def __init__(self, is_serial: bool = True,
                 control_type: RobotAudioRecordControlType = RobotAudioRecordControlType.START_RECORD,
                 time_limit: int = 60000, file_name: str = None,
                 new_file_name: str = None):
        assert isinstance(control_type, RobotAudioRecordControlType), 'ControlRobotAudioRecord : control_type should ' \
                                                                      'be RobotAudioRecordControlType instance '
        self.__is_serial = is_serial
        self.__control_type = control_type.value
        self.__timeLimit = time_limit
        self.__id = file_name
        self.__newId = new_file_name

    async def execute(self):
        """Send control recording instructions

        Returns:
            ControlRobotRecordResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT
        request = ControlRobotRecordRequest()
        request.type = self.__control_type
        request.timeLimit = self.__timeLimit

        if isinstance(self.__id, str):
            request.id = self.__id

        if isinstance(self.__newId, str):
            request.newId = self.__newId

        cmd_id = _PCProgramCmdId.CONTROL_ROBOT_AUDIO_RECORD.value
        return await self.send(cmd_id, request, timeout)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            ControlRobotRecordResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = ControlRobotRecordResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class RobotAudioStartRecord(ControlRobotAudioRecord):
    """Robot starts recording api

     Control the robot to start recording

     Args:
         is_serial (bool): Whether to wait for a reply, the default is True
         time_limit (int): The length of the recording, in ms, the default is 60000ms, which is 60s

     #ControlRobotRecordResponse.isSuccess: Is it successful

     #ControlRobotRecordResponse.resultCode: Return code

     #ControlRobotRecordResponse.id: The name of the generated recording file
    """

    def __init__(self, is_serial: bool = True, time_limit: int = 60000):
        assert isinstance(time_limit, int) and time_limit > 0, f'{self.__class__.__name__}  : time_limit should be ' \
                                                               f'positive '
        ControlRobotAudioRecord.__init__(self, is_serial=is_serial, time_limit=time_limit,
                                         control_type=RobotAudioRecordControlType.START_RECORD)


class RobotAudioStopRecord(ControlRobotAudioRecord):
    """Robot stop recording api

     Control the robot to stop recording

     Args:
         is_serial (bool): Whether to wait for a reply, the default is True

     #ControlRobotRecordResponse.isSuccess: Is it successful

     #ControlRobotRecordResponse.resultCode: Return code

     #ControlRobotRecordResponse.id: The name of the generated recording file

    """

    def __init__(self, is_serial: bool = True):
        ControlRobotAudioRecord.__init__(self, is_serial=is_serial,
                                         control_type=RobotAudioRecordControlType.STOP_RECORD)


class RobotAudioStartPlay(ControlRobotAudioRecord):
    """The robot starts to play the recording api

     Control the robot to start playing the recording

     Args:
         is_serial (bool): Whether to wait for a reply, the default is True
         file_name (str): recording file name, cannot be empty or None

     #ControlRobotRecordResponse.isSuccess: Is it successful

     #ControlRobotRecordResponse.resultCode: Return code

     #ControlRobotRecordResponse.id: The name of the generated recording file

    """

    def __init__(self, is_serial: bool = True, file_name: str = None):
        assert isinstance(file_name, str) and len(file_name), f'{self.__class__.__name__}  : file_name should be ' \
                                                              f'available '
        ControlRobotAudioRecord.__init__(self, is_serial=is_serial, file_name=file_name,
                                         control_type=RobotAudioRecordControlType.START_PLAY)


class RobotAudioStopPlay(ControlRobotAudioRecord):
    """The robot stops playing the recording api

     Control the robot to stop playing the recording

     Args:
         is_serial (bool): Whether to wait for a reply, the default is True

     #ControlRobotRecordResponse.isSuccess: Is it successful

     #ControlRobotRecordResponse.resultCode: Return code

     #ControlRobotRecordResponse.id: The name of the generated recording file

    """

    def __init__(self, is_serial: bool = True):
        ControlRobotAudioRecord.__init__(self, is_serial=is_serial, control_type=RobotAudioRecordControlType.STOP_PLAY)


class RobotAudioPausePlay(ControlRobotAudioRecord):
    """The robot pauses the recording api

     Control the robot to pause the recording

     Args:
         is_serial (bool): Whether to wait for a reply, the default is True

     #ControlRobotRecordResponse.isSuccess: Is it successful

     #ControlRobotRecordResponse.resultCode: Return code

     #ControlRobotRecordResponse.id: The name of the generated recording file

    """

    def __init__(self, is_serial: bool = True):
        ControlRobotAudioRecord.__init__(self, is_serial=is_serial, control_type=RobotAudioRecordControlType.PAUSE_PLAY)


class RobotAudioContinuePlay(ControlRobotAudioRecord):
    """The robot continues to play the recording api

     Control the robot to continue playing the recording

     Args:
         is_serial (bool): Whether to wait for a reply, the default is True

     #ControlRobotRecordResponse.isSuccess: Is it successful

     #ControlRobotRecordResponse.resultCode: Return code

     #ControlRobotRecordResponse.id: The name of the generated recording file

    """

    def __init__(self, is_serial: bool = True):
        ControlRobotAudioRecord.__init__(self, is_serial=is_serial,
                                         control_type=RobotAudioRecordControlType.CONTINUE_PLAY)


class RobotAudioRenameFile(ControlRobotAudioRecord):
    """Robot rename recording file api

     Control the robot to rename the recording file

     Args:
         is_serial (bool): Whether to wait for a reply, the default is True
         file_name (str): recording file name, cannot be empty or None

     #ControlRobotRecordResponse.isSuccess: Is it successful

     #ControlRobotRecordResponse.resultCode: Return code

     #ControlRobotRecordResponse.id: The name of the generated recording file

    """

    def __init__(self, is_serial: bool = True, file_name: str = None, new_file_name: str = None):
        assert isinstance(file_name, str) and len(file_name), f'{self.__class__.__name__} : file_name should be ' \
                                                              f'available '
        assert isinstance(new_file_name, str) and len(new_file_name), f'{self.__class__.__name__} : new_file_name ' \
                                                                      f'should be available '
        ControlRobotAudioRecord.__init__(self, is_serial=is_serial, file_name=file_name, new_file_name=new_file_name,
                                         control_type=RobotAudioRecordControlType.RENAME_FILE)
