import asyncio
import logging
from asyncio.futures import Future

import enum
from google.protobuf import message as _message
from typing import Any, Set, Optional

from mini import MoveRobotDirection, MiniApiResultType, MouthLampMode, \
    MouthLampColor, ServicePlatform, LanType
from mini.pb2.codemao_faceanalyze_pb2 import FaceAnalyzeResponse
from mini.pb2.codemao_facedetect_pb2 import FaceDetectResponse
from mini.pb2.codemao_facerecognise_pb2 import FaceRecogniseResponse
from mini.pb2.codemao_getaudiolist_pb2 import GetAudioListResponse
from mini.pb2.codemao_getinfrareddistance_pb2 import GetInfraredDistanceResponse
from mini.pb2.codemao_getregisterfaces_pb2 import GetRegisterFacesResponse
from mini.pb2.codemao_recogniseobject_pb2 import RecogniseObjectResponse
from mini.pb2.codemao_takepicture_pb2 import TakePictureResponse
from .channels.websocket_client import AbstractMsgHandler as _AbstractMsgHandler
from .channels.websocket_client import ubt_websocket as _websocket
from .dns.dns_browser import WiFiDeviceListener, WiFiDevice
from .dns.dns_browser import browser as _browser

_log = logging.getLogger(__name__)
_log.addHandler(logging.StreamHandler())
if _log.level == logging.NOTSET:
    _log.setLevel(logging.INFO)

browser = _browser()
websocket = _websocket()


def set_log_level(level: int, save_file: str = None):
    """Set the sdk log level

    Args:
        level: logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR
        save_file: Need to save to a file, fill in the log file path
    """
    _log.setLevel(level)

    from .dns.dns_browser import log as log1
    log1.setLevel(level)

    from .channels.websocket_client import log as log2
    log2.setLevel(level)

    from .dns.zeroconf import log as log3
    log3.setLevel(level)
    log3.addHandler(logging.StreamHandler())

    if save_file is not None:
        file_handler = logging.FileHandler(save_file)
        _log.addHandler(file_handler)
        log1.addHandler(file_handler)
        log2.addHandler(file_handler)


@enum.unique
class RobotType(enum.Enum):
    """
    Robot Product Type
    """
    DEDU = 1
    """
    AlphaMini China Education Edition
    """
    MINI = 2
    """
    AlphaMini China Standard Edition
    """
    EDU = 3
    """
    AlphaMini Oversea Education Edition
    """
    KOR = 4
    """
    AlphaMini Korea Edition
    """
    OTOC = 5
    """
    AlphaMini Oversea ToC Edition
    """


def set_robot_type(robot: RobotType):
    """Set the robot product type to be linked

    Args:
        robot: Value is: RobotType.EDU, RobotType.KOR, RobotType.MINI or RobotType.DEDU

    """
    if robot == RobotType.MINI:
        from .dns import dns_browser
        dns_browser.service_type = "_Mini_mini_channel_server._tcp.local."
    elif robot == RobotType.DEDU:
        from .dns import dns_browser
        dns_browser.service_type = "_Dedu_mini_channel_server._tcp.local."
    elif robot == RobotType.EDU:
        from .dns import dns_browser
        dns_browser.service_type = "_Edu_mini_channel_server._tcp.local."
    elif robot == RobotType.KOR:
        from .dns import dns_browser
        dns_browser.service_type = "_Kor_mini_channel_server._tcp.local."
    elif robot == RobotType.OTOC:
        from .dns import dns_browser
        dns_browser.service_type = "_OToC_mini_channel_server._tcp.local."
    else:
        print(f"不支持的机器人产品类型")


class _GetWiFiDeviceListListener(WiFiDeviceListener):
    """Obtain the monitoring of robot equipment in batches

    Args:
        devices: Set[WiFiDevice] or None
    """
    devices: Set[WiFiDevice]

    def __init__(self, devices):
        self.devices: Set[WiFiDevice] = devices or set()

    def on_device_updated(self, device: WiFiDevice) -> None:
        """
        机器人设备更新了
        Args:
            device: WiFiDevice
        """
        self.devices.update([device])

    def on_device_removed(self, device: WiFiDevice) -> None:
        """
        机器人设备从局域网中移除了
        Args:
            device: WFiDevice
        """
        self.devices.remove(device)

    def on_device_found(self, device: WiFiDevice) -> None:
        """
        扫描到一个机器人设备
        Args:
            device: WFiDevice
        """
        self.devices.add(device)


async def _get_user_input(devices: tuple) -> int:
    try:
        i: int = 0
        for device in devices:
            print('{0}.{1}'.format(i, device))
            i += 1
        num_text = input(f'请输入选择连接的机器人序号:')
    except Exception as e:
        raise e
    else:
        return int(num_text)


def _start_scan(loop: asyncio.AbstractEventLoop, name: str) -> Future:
    """
    开启一个扫描机器人设备的Future
    Args:
        loop: 当前事件loop
        name: 指定设备名称

    Returns:
        asyncio.Future
    """
    fut = loop.create_future()

    class _InnerLister(WiFiDeviceListener):

        @staticmethod
        def set_result(future: Future, device: WiFiDevice):
            if future.cancelled() or future.done():
                return
            _log.info(f"found device : {device}")
            future.set_result(device)

        def on_device_found(self, device: WiFiDevice) -> None:
            if device.name.endswith(name):
                if fut.cancelled() or fut.done():
                    return
                loop.run_in_executor(None, browser.stop_scan)
                loop.call_soon(_InnerLister.set_result, fut, device)

        def on_device_updated(self, device: WiFiDevice) -> None:
            if device.name.endswith(name):
                if fut.cancelled() or fut.done():
                    return
                loop.run_in_executor(None, browser.stop_scan)
                loop.call_soon(_InnerLister.set_result, fut, device)

        def on_device_removed(self, device: WiFiDevice) -> None:
            if device.name.endswith(name):
                if fut.cancelled() or fut.done():
                    return
                loop.call_soon(_InnerLister.set_result, fut, device)

    _log.info("start scanning...")
    browser.add_listener(_InnerLister())
    browser.start_scan(0)

    return fut


async def _get_device_by_name(name: str, timeout: int) -> Optional[WiFiDevice]:
    """
    获取当前局域网内，指定名字的机器人设备信息
    Args:
        name: 设备序列号
        timeout: 扫描超时时间

    Returns:
        Optional[WiFiDevice]
    """

    async def start_scan_async():
        return await _start_scan(asyncio.get_running_loop(), name)

    try:
        device: WiFiDevice = await asyncio.wait_for(start_scan_async(), timeout)
        return device
    except asyncio.TimeoutError:
        _log.warning(f'scan device timeout')
        return None
    finally:
        browser.stop_scan()
        _log.info("stop scan finished.")


async def _get_device_list(timeout: int) -> tuple:
    """
    获取当前局域网内所有机器人设备信息
    Args:
        timeout: 超时时间

    Returns:
        Optional[WiFiDevice]
    """
    devices: Set[WiFiDevice] = set()
    browser.add_listener(_GetWiFiDeviceListListener(devices))
    browser.start_scan(0)
    await asyncio.sleep(timeout)
    browser.remove_all_listener()
    browser.stop_scan()
    return tuple(devices)


async def _connect(device: WiFiDevice) -> bool:
    """
    连接机器人设备

    Args:
        device (WiFiDevice): 指定机器人设备对象

    Returns:
        bool: 是否连接设备成功

    """
    return await websocket.connect(device.address)


def _register_msg_handler(cmd: int, handler: _AbstractMsgHandler):
    """
    注册命令监听器

    Args:
        cmd: 支持的命令请查看: mini.apis.cmdid
        handler: 命令处理器

    """
    websocket.register_msg_handler(cmd, handler)


def _unregister_msg_handler(cmd: int, handler: _AbstractMsgHandler):
    """
    反注册命令监听器

    Args:
        cmd: 支持的命令请查看: mini.apis.cmdid
        handler: 命令处理器
    """
    websocket.unregister_msg_handler(cmd, handler)


async def _send_msg(cmd: int, message: _message.Message, timeout: int) -> Any:
    """
    发送一个消息给机器人

    Args:
        cmd:支持的命令请查看: mini.apis.cmdid
        message:  消息类在: mini.pb2 包内
        timeout: 超时时间
    """
    return await websocket.send_msg(cmd, message, timeout)


async def _release():
    """
    断开链接，释放资源
    """
    await websocket.shutdown()


# -----------------------------------------------------------------#
async def get_device_by_name(name: str, timeout: int) -> Optional[WiFiDevice]:
    """
    Get the robot device information with the specified name in the current LAN

    Args:
        name: device serial number
        timeout: scan timeout

    Returns:
        Optional[WiFiDevice]
    """
    return await _get_device_by_name(name, timeout)


async def get_device_list(timeout: int) -> tuple:
    """Get all the robot device information in the current LAN

    Args:
        timeout: timeout

    Returns:
        Optional[WiFiDevice]
    """
    return await _get_device_list(timeout)


async def connect(device: WiFiDevice) -> bool:
    """Connect robot equipment

    Args:
        device (WiFiDevice): Specify the robot device object

    Returns:
        bool: Whether the device is connected successfully
    """
    return await _connect(device)


async def release():
    """
    Disconnect the link and release resources
    """
    await _release()


async def enter_program() -> bool:
    """Enter programming mode api

    Robot enters programming mode

    Returns:
        bool
    """

    from mini.apis.api_setup import StartRunProgram
    (resultType, response) = await StartRunProgram().execute()
    await asyncio.sleep(6)
    return resultType == MiniApiResultType.Success and response.isSuccess


async def quit_program() -> bool:
    """Exit programming mode api

    Robot exits programming mode

    Returns:
            bool
    """

    from mini.apis.api_setup import StopRunProgram
    return await StopRunProgram(is_serial=False).execute()


async def play_action(action_name: str = None) -> bool:
    """Execute built-in action api

    The robot performs a built-in action with a specified name

    The action name can be obtained with get_action_list

    Args:
        action_name (str): action name

    Returns:
        bool
    """
    from mini.apis.api_action import PlayAction
    block: PlayAction = PlayAction(True, action_name)
    (resultType, response) = await block.execute()
    _log.info(f'play_action result:{response}')
    return resultType == MiniApiResultType.Success and response.isSuccess


async def stop_action() -> bool:
    """Stop action

    If the action is an uninterruptible action, stop_action returns False

    Returns:
        bool
    """
    from mini.apis.api_action import StopAllAction
    block: StopAllAction = StopAllAction()
    (resultType, response) = await block.execute()
    _log.info(f'stop_action result:{response}')
    return resultType == MiniApiResultType.Success and response.isSuccess


async def play_custom_action(action_name: str = None) -> bool:
    """Execute custom action api

    Let the robot perform a custom action with a specified name and wait for the result

    The action name can be obtained by get_custom_action_list

    Args:
        action_name (str): custom action name

    Returns:
        bool
    """
    from mini.apis.api_action import PlayCustomAction
    block: PlayCustomAction = PlayCustomAction(True, action_name)
    (resultType, response) = await block.execute()
    _log.info(f'play_custom_action result:{response}')
    return resultType == MiniApiResultType.Success and response.isSuccess


async def stop_custom_action() -> bool:
    """Stop custom action

    If the action is an uninterruptible action, stop_action returns False

    Returns:
        bool
    """

    from mini.apis.api_action import StopCustomAction
    block: StopCustomAction = StopCustomAction()
    (resultType, response) = await block.execute()
    _log.info(f'stop_custom_action result:{response}')
    return resultType == MiniApiResultType.Success and response.isSuccess


async def move(direction: MoveRobotDirection = MoveRobotDirection.FORWARD,
               step: int = 1) -> bool:
    """Control robot movement

    Control the robot to move 10 steps to the left (LEFTWARD) and wait for the execution result

    Args:
        direction (MoveRobotDirection): direction
        step (int): number of steps

    Returns:
        bool
    """

    from mini.apis.api_action import MoveRobot
    block: MoveRobot = MoveRobot(True, direction, step)
    (resultType, response) = await block.execute()
    _log.info(f'move result:{response}')
    return resultType == MiniApiResultType.Success and response.isSuccess


async def get_action_list() -> list:
    """Get action list

    Get the list of actions built into the robot system, and wait for the reply result

    Returns:
        []: Action list
    """
    from mini.apis.api_action import GetActionList
    from mini import RobotActionType
    block: GetActionList = GetActionList(True, RobotActionType.INNER)
    (resultType, response) = await block.execute()
    if resultType == MiniApiResultType.Success and response.isSuccess:
        return response.actionList
    else:
        return []


async def get_custom_action_list() -> list:
    """Get a list of custom actions

    Get the action list under the robot/sdcard/customize/actions and wait for the reply result

    Returns:
        []: Custom action list
    """

    from mini.apis.api_action import GetActionList
    from mini import RobotActionType
    block: GetActionList = GetActionList(True, RobotActionType.INNER)
    (resultType, response) = await block.execute()
    if resultType == MiniApiResultType.Success and response.isSuccess:
        return response.actionList
    else:
        return []


async def wiki(query: str) -> bool:
    """Query encyclopedia demo

    Query encyclopedia, for example: query content "you must choose", and wait for the result, the robot broadcasts the

    query result

    Args:
        query (str): query keyword

    Returns:
        bool
    """

    from mini.apis.api_content import QueryWiKi
    block: QueryWiKi = QueryWiKi(True, query)
    (resultType, response) = await block.execute()
    _log.info(f'wiki result:{response}')
    return resultType == MiniApiResultType.Success and response.isSuccess


async def translate(query: str,
                    from_lan: LanType = None, to_lan: LanType = None,
                    platform: ServicePlatform = ServicePlatform.BAIDU) -> bool:
    """translation

         For example: Use Baidu Translate to translate "张学友" from Chinese to English, and wait for the result,

         the robot broadcasts the translation result:

         translate(query="张学友",from_lan=CN,to_lan=EN,platform=GOOGLE)

     Args:
         query (str): keyword
         from_lan (LanType): source language
         to_lan (LanType): target language
         platform (ServicePlatform): GOOGLE, Only Support Google
    Returns:
        bool
    """

    from mini.apis.api_content import StartTranslate
    block: StartTranslate = StartTranslate(True, query, from_lan=from_lan, to_lan=to_lan, platform=platform)
    (resultType, response) = await block.execute()
    _log.info(f'translate result:{response}')
    return resultType == MiniApiResultType.Success and response.isSuccess


async def play_expression(express_name: str) -> bool:
    """Do an Expression

    Let the robot play a built-in expression of express_name and wait for the reply result

    Args:
        express_name (str): emoticon file name, such as: "codemao1"
    Returns:
        bool
    """

    from mini.apis.api_expression import PlayExpression
    block: PlayExpression = PlayExpression(True, express_name)
    (resultType, response) = await block.execute()
    _log.info(f'play expression result:{response}')
    return resultType == MiniApiResultType.Success and response.isSuccess


async def play_behavior(behavior_name: str) -> bool:
    """Do a dance

    Let the robot start to dance a dance named behavior_name and wait for the response result

    Args:
        behavior_name (str): e.g. "dance_0004"

    Returns:
        bool
    """

    from mini.apis.api_behavior import StartBehavior
    block: StartBehavior = StartBehavior(True, behavior_name)
    (resultType, response) = await block.execute()
    _log.info(f'play behavior result:{response}')
    return resultType == MiniApiResultType.Success and response.isSuccess


async def stop_behavior() -> bool:
    """stop dance

    Returns:
        bool
    """
    from mini.apis.api_behavior import StopBehavior
    block: StopBehavior = StopBehavior(True)
    (resultType, response) = await block.execute()
    _log.info(f'stop behavior result:{response}')
    return resultType == MiniApiResultType.Success and response.isSuccess


async def set_MouthLamp_NormalMode(color: MouthLampColor = MouthLampColor.RED, duration: int = 1000) -> bool:
    """
    Set mouth light always on mode and wait for the result

    Args:
        color (MouthLampColor): Mouth lamp color, default RED
        duration (int): unit ms, duration

    Returns:
        bool

    """
    return await _set_mouthlamp_mode(mode=MouthLampMode.NORMAL, color=color, duration=duration)


async def set_MouthLamp_BreathMode(breath_duration: int = 1000,
                                   color: MouthLampColor = MouthLampColor.RED, duration: int = 1000) -> bool:
    """
    Set mouth light breathing mode and wait for the result

    Args:
        breath_duration (int): unit ms, the duration of one breath
        color (MouthLampColor): Mouth lamp color, default RED
        duration (int): unit ms, duration

    Returns:
        bool
    """
    return await _set_mouthlamp_mode(mode=MouthLampMode.BREATH, breath_duration=breath_duration, color=color,
                                     duration=duration)


async def _set_mouthlamp_mode(mode: MouthLampMode = MouthLampMode.NORMAL, color: MouthLampColor = MouthLampColor.RED,
                              duration: int = 1000, breath_duration: int = 1000) -> bool:
    """Set mouth light mode

    Set the robot's mouth light to normal mode, green and always on for 3s, and wait for the reply result

    When mode=NORMAL, the duration parameter works, indicating how long it will be on

    When mode=BREATH, the breath_duration parameter indicates how often to breathe

    After the setting takes effect, the robot will immediately return the

    setting result (it has nothing to do with the set duration parameter)

    Args:
        mode: mouth light mode, 0: normal mode, 1: breathing mode
        color: the color of the mouth light, 1: red, 2: green, 3: blue
        duration: duration, in milliseconds, -1 means always on
        breath_duration: the duration of one blink, in milliseconds

    Returns:
        bool
    """

    from mini.apis.api_expression import SetMouthLamp
    block: SetMouthLamp = SetMouthLamp(True, mode, color, duration, breath_duration)
    (resultType, response) = await block.execute()
    _log.info(f'set MouthLamp mode result:{response}')
    return resultType == MiniApiResultType.Success and response.isSuccess


async def switch_MouthLamp(is_open: bool = True) -> bool:
    """Switch mouth light

    Turn on and off the robot's mouth light and wait for the result

    Args:
        is_open: bool

    Returns:
        bool
    """

    from mini.apis.api_expression import ControlMouthLamp
    block: ControlMouthLamp = ControlMouthLamp(True, is_open)
    (resultType, response) = await block.execute()
    _log.info(f'switch MouthLamp result:{response}')
    return resultType == MiniApiResultType.Success and response.isSuccess


async def play_tts(text: str) -> bool:
    """Play tts

    Make the robot start playing a period of tts and wait for the result

    Args:
        text: str, for example: "Hello, I am Wukong, la la la",

    Returns:
        bool
    """

    from mini.apis.api_sound import StartPlayTTS
    block: StartPlayTTS = StartPlayTTS(True, text)
    (resultType, response) = await block.execute()
    _log.info(f'play tts result:{response}')
    return resultType == MiniApiResultType.Success and response.isSuccess


async def stop_tts() -> bool:
    """Stop speech synthesis broadcast, and wait for the result

    Returns:
        bool
    """

    from mini.apis.api_sound import StopPlayTTS
    block: StopPlayTTS = StopPlayTTS(True)
    (resultType, response) = await block.execute()
    _log.info(f'stop tts result:{response}')
    return resultType == MiniApiResultType.Success and response.isSuccess


async def play_online_audio(url: str) -> bool:
    """Play online sound effects

    Make the robot play an online sound effect,

    And wait for the result

    Args:
        url: str, for example: http://yun.lnpan.com/music/download/ring/000/075/5653bae83917a892589b372782175dd8.amr
             Supported formats are mp3, amr, wav, etc.
    Returns:
        bool
    """

    from mini import AudioStorageType
    from mini.apis.api_sound import PlayAudio
    block: PlayAudio = PlayAudio(True,
                                 url,
                                 AudioStorageType.NET_PUBLIC)
    (resultType, response) = await block.execute()
    _log.info(f'play online audio result:{response}')
    return resultType == MiniApiResultType.Success and response.isSuccess


async def play_local_audio(local_file: str) -> bool:
    """Play local sound effects

    Make the robot play a local built-in sound effect, the sound effect name is "read_016", and wait for the result

    Args:
        local_file:

    Returns:
        bool
    """

    from mini.apis.api_sound import PlayAudio
    from mini import AudioStorageType
    block: PlayAudio = PlayAudio(True,
                                 local_file,
                                 AudioStorageType.PRESET_LOCAL)
    (resultType, response) = await block.execute()
    _log.info(f'play local audio result:{response}')
    return resultType == MiniApiResultType.Success and response.isSuccess


async def stop_audio() -> bool:
    """Stop all audio that is playing

    Stop all sound effects and wait for the result

    Returns:
        bool
    """

    from mini.apis.api_sound import StopAllAudio
    block: StopAllAudio = StopAllAudio(True)
    (resultType, response) = await block.execute()
    _log.info(f'stop audio result:{response}')
    return resultType == MiniApiResultType.Success and response.isSuccess


async def get_system_audio_list() -> GetAudioListResponse:
    """Get a list of sound effects

    Get the list of sound effects built into the robot and wait for the result

    #GetAudioListResponse.audio ([Audio]): audio effect list

       #Audio.name: Audio effect name

       #Audio.suffix: audio suffix

    #GetAudioListResponse.isSuccess: Is it successful, True or False

    #GetAudioListResponse.resultCode: Result code

    Returns:
        GetAudioListResponse
    """

    from mini.apis.api_sound import FetchAudioList
    from mini import AudioSearchType
    block: FetchAudioList = FetchAudioList(True, search_type=AudioSearchType.INNER)
    (resultType, response) = await block.execute()
    _log.info(f'stop audio result:{response}')
    return response


async def get_custom_audio_list() -> GetAudioListResponse:
    """Get a list of sound effects

    Get the list of sound effects placed by the robot developer under /sdcard/customize/music/, and wait for the result

    #GetAudioListResponse.audio ([Audio]): Audio effect list

        #Audio.name: Audio effect name

        #Audio.suffix: audio suffix

    #GetAudioListResponse.isSuccess: Is it successful, True or False

    #GetAudioListResponse.resultCode: Result code

    Returns:
        GetAudioListResponse
    """

    from mini.apis.api_sound import FetchAudioList
    from mini import AudioSearchType
    block: FetchAudioList = FetchAudioList(True, search_type=AudioSearchType.CUSTOM)
    (resultType, response) = await block.execute()
    _log.info(f'stop audio result:{response}')
    return response


async def change_volume(volume: float = 0.5) -> bool:
    """Adjust the robot volume demo

    Set the robot volume to 0~1 and wait for the reply result

    Args:
        volume: float default 0.5

    Returns:
        bool
    """

    from mini.apis.api_sound import ChangeRobotVolume
    block: ChangeRobotVolume = ChangeRobotVolume(True, volume)
    (resultType, response) = await block.execute()
    _log.info(f'change volume result:{response}')
    return resultType == MiniApiResultType.Success and response.isSuccess


async def face_detect() -> FaceDetectResponse:
    """Face count detection

    Do a face count detection and wait for the reply result

    #FaceDetectResponse.count: the number of faces

    #FaceDetectResponse.isSuccess: Is it successful, True or False

    #FaceDetectResponse.resultCode: Return code

    Returns:
        FaceDetectResponse
    """

    from mini.apis.api_sence import FaceDetect
    block: FaceDetect = FaceDetect(True, 10)
    (resultType, response) = await block.execute()
    _log.info(f'face detect result:{response}')
    return response


async def face_analysis() -> FaceAnalyzeResponse:
    """Face analysis (gender)

    Do a face information (gender, age) detection, and wait for the reply result

    When multiple people are in front of the camera, return the face information that accounts for the

    largest proportion of the screen.

    Return value: Example {"age": 24, "gender": 99, "height": 238, "width": 238}

             age: age

             gender: [1, 100], females less than 50 are females, males greater than 50

             height: the height of the face in the camera image

             width: the width of the face in the camera image

    #FaceAnalyzeResponse.faceInfos: face information array [FaceInfoResponse]

    #FaceInfoResponse.gender (int) :[1,100], females less than 50, males greater than 50

    #FaceInfoResponse.age: age

    #FaceInfoResponse.width: The width of the face in the camera screen

    #FaceInfoResponse.height: The height of the face in the camera screen

    #FaceAnalyzeResponse.isSuccess: Is it successful, True or False

    #FaceAnalyzeResponse.resultCode: Return code

    Returns:
        FaceAnalyzeResponse
    """

    from mini.apis.api_sence import FaceAnalysis
    block: FaceAnalysis = FaceAnalysis(True, 10)
    (resultType, response) = await block.execute()
    _log.info(f'face analysis result:{response}')
    return response


async def face_recognise() -> FaceRecogniseResponse:
    """Face recognition

    Do a face recognition test and wait for the result

    #FaceRecogniseResponse.faceInfos: [FaceInfoResponse] face information array

    #FaceInfoResponse.id: face id

    #FaceInfoResponse.name: name, if it is a stranger, the default name is "stranger"

    #FaceInfoResponse.gender: gender

    #FaceInfoResponse.age: age

    #FaceRecogniseResponse.isSuccess: Is it successful, True or False

    #FaceRecogniseResponse.resultCode: Return code

    Returns:
        RecogniseObjectResponse
    """

    from mini.apis.api_sence import FaceRecognise
    (resultType, response) = await FaceRecognise(True, 10).execute()
    _log.info(f'face recognise result:{response}')
    return response


async def flower_recognise() -> RecogniseObjectResponse:
    """Flower and grass recognition

    Let the robot do a flower and grass recognition (you need to manually place the flower or flower photo in front of the robot),

    and wait for the result.

    #RecogniseObjectResponse.objects: Recognition result array [str]

    #RecogniseObjectResponse.isSuccess: Is it successful, True or False

    #RecogniseObjectResponse.resultCode: Return code

    Returns:
        RecogniseObjectResponse
    """

    from mini.apis.api_sence import ObjectRecognise
    from mini import ObjectRecogniseType
    block: ObjectRecognise = ObjectRecognise(True, ObjectRecogniseType.FLOWER, 10)
    (resultType, response) = await block.execute()
    _log.info(f'flower_recognise result:{response}')
    return response


async def fruit_recognise() -> RecogniseObjectResponse:
    """Fruit recognition

    Let the robot do a fruit recognition (you need to manually put the fruit or fruit photo in front of the robot),

    and wait for the result.

    #RecogniseObjectResponse.objects: Recognition result array [str]

    #RecogniseObjectResponse.isSuccess: Is it successful

    #RecogniseObjectResponse.resultCode: Return code

    Returns:
        RecogniseObjectResponse
    """

    from mini.apis.api_sence import ObjectRecognise
    from mini import ObjectRecogniseType
    block: ObjectRecognise = ObjectRecognise(True, ObjectRecogniseType.FRUIT, 10)
    (resultType, response) = await block.execute()
    _log.info(f'fruit_recognize result:{response}')
    return response


async def gesture_recognise() -> RecogniseObjectResponse:
    """Gesture Recognition

    Let the robot do a user gesture recognition, (need to make a gesture in front of the robot), and wait for the result

    #RecogniseObjectResponse.objects: Recognition result array [str]

    #RecogniseObjectResponse.isSuccess: Is it successful

    #RecogniseObjectResponse.resultCode: Return code

    Returns:
        RecogniseObjectResponse
    """

    from mini.apis.api_sence import ObjectRecognise
    from mini import ObjectRecogniseType
    block: ObjectRecognise = ObjectRecognise(True, ObjectRecogniseType.GESTURE, 10)
    (resultType, response) = await block.execute()
    _log.info(f'gesture_recognize result:{response}')
    return response


async def take_picture_immediately() -> TakePictureResponse:
    """Take pictures

    Let the robot take a photo immediately and wait for the result

    #TakePictureResponse.isSuccess: Is it successful, True or False

    #TakePictureResponse.code: Return code

    #TakePictureResponse.picPath: The storage path of the photo in the robot

    Returns:
        TakePictureResponse
    """

    from mini.apis.api_sence import TakePicture
    from mini import TakePictureType
    (resultType, response) = await TakePicture(take_picture_type=TakePictureType.IMMEDIATELY).execute()
    _log.info(f'take picture immediately result:{response}')
    return response


async def take_picture() -> TakePictureResponse:
    """Take pictures

    Let the robot find the face before taking a picture and wait for the result

    #TakePictureResponse.isSuccess: Is it successful, True or False

    #TakePictureResponse.code: Return code

    #TakePictureResponse.picPath: The storage path of the photo in the robot

    Returns:
        TakePictureResponse
    """

    from mini.apis.api_sence import TakePicture
    from mini import TakePictureType
    (resultType, response) = await TakePicture(take_picture_type=TakePictureType.FINDFACE).execute()
    _log.info(f'take picture result:{response}')
    return response


async def get_register_faces() -> GetRegisterFacesResponse:
    """Get registered face information

    Get all the face information registered in the robot and wait for the result

    #GetRegisterFacesResponse.faceInfos: [FaceInfoResponse] face information array

        #FaceInfoResponse.id: face id

        #FaceInfoResponse.name: name

        #FaceInfoResponse.gender: gender

        #FaceInfoResponse.age: age

    #GetRegisterFacesResponse.isSuccess: Is it successful, True or False

    #GetRegisterFacesResponse.resultCode: Return code

    Returns:
        GetRegisterFacesResponse

    """

    from mini.apis.api_sence import GetRegisterFaces
    (resultType, response) = await GetRegisterFaces().execute()
    _log.info(f'get register faces result:{response}')
    return response


async def get_infrared_distance() -> GetInfraredDistanceResponse:
    """Infrared distance detection

    Get the infrared distance detected by the current robot and wait for the result

    #GetInfraredDistanceResponse.distance: Infrared distance

    Returns:
        GetInfraredDistanceResponse
    """

    from mini.apis.api_sence import GetInfraredDistance
    (resultType, response) = await GetInfraredDistance().execute()
    _log.info(f'get infrared distance result:{response}')
    return response
