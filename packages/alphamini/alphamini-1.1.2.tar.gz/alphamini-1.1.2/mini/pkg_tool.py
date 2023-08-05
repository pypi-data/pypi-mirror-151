import asyncio
import enum
import os

import websockets

import mini
from mini import WiFiDevice as _WiFiDevice
from mini.channels import msg_utils
from mini.pb2.pccodemao_message_pb2 import Message as _Message
from mini.pb2.pccodemao_messageheader_pb2 import MessageHeader as _MessageHeader

_found_devices = {}


@enum.unique
class _PCPyCmdId(enum.Enum):
    """
    Tool command number
     """
    PYPI_INSTALL_WHEEL_REQUEST = 1
    """
    Installation package
    """

    PYPI_UNINSTALL_WHEEL_REQUEST = 2
    """
    Uninstall package
    """

    PYPI_GET_WHEEL_INFO_REQUEST = 3
    """
    Get package information
    """

    PYPI_RUN_WHEEL_REQUEST = 4
    """
    execute program
    """

    PYPI_GET_WHEEL_LIST_REQUEST = 5
    """
    Get a list of installers
    """

    PYPI_START_RECORD_REQUEST = 6
    """Get recording data, only supported by Mini
    """

    PYPI_SWITCH_ADB_REQUEST = 7
    """ switch ADB
    """

    PYPI_UPLOAD_SCRIPT_REQUEST = 8
    """Upload python script to the robot
    """

    PYPI_CHECK_UPLOAD_SCRIPT_REQUEST = 9
    """Check if the python script has been uploaded to the robot
    """

    PYPI_RUN_UPLOAD_SCRIPT_REQUEST = 10
    """Execute a python script that has been uploaded
    """

    PYPI_STOP_UPLOAD_SCRIPT_REQUEST = 11
    """Stop executing a certain python script that has been uploaded
    """

    PYPI_LIST_UPLOAD_SCRIPT_REQUEST = 12
    """Get a list of uploaded python scripts
    """


def _read_into_buffer(filename) -> bytes:
    buf = bytearray(os.path.getsize(filename))
    with open(filename, 'rb') as f:
        f.readinto(buf)
    return bytes(buf)


async def _send_msg1(websocket, message: _Message) -> str:
    await websocket.send(msg_utils.base64_encode(message.SerializeToString()))
    result: str = ""
    while True:
        try:
            _data = await websocket.recv()
            _bytes = msg_utils.base64_decode(_data)
            msg: _Message = msg_utils.parse_msg(_bytes)
            header: _MessageHeader = msg.header
            if header.command == _PCPyCmdId.PYPI_INSTALL_WHEEL_REQUEST.value:
                from mini.tool.pb2.PyPi_InstallWheel_pb2 import InstallWheelResponse
                response: InstallWheelResponse = InstallWheelResponse()
                response.ParseFromString(msg.bodyData)
                print("{0}".format(response.message))
            elif header.command == _PCPyCmdId.PYPI_UNINSTALL_WHEEL_REQUEST.value:
                from mini.tool.pb2.PyPi_UninstallWheel_pb2 import UninstallWheelResponse
                response: UninstallWheelResponse = UninstallWheelResponse()
                response.ParseFromString(msg.bodyData)
                print("{0}".format(response.message))
            elif header.command == _PCPyCmdId.PYPI_RUN_WHEEL_REQUEST.value:
                from mini.tool.pb2.PyPi_RunWheel_pb2 import RunWheelResponse
                response: RunWheelResponse = RunWheelResponse()
                response.ParseFromString(msg.bodyData)
                print("{0}".format(response.message))
            elif header.command == _PCPyCmdId.PYPI_GET_WHEEL_INFO_REQUEST.value:
                from mini.tool.pb2.PyPi_GetWheelInfo_pb2 import GetWheelInfoResponse
                response: GetWheelInfoResponse = GetWheelInfoResponse()
                response.ParseFromString(msg.bodyData)
                return response.message
            elif header.command == _PCPyCmdId.PYPI_GET_WHEEL_LIST_REQUEST.value:
                from mini.tool.pb2.PyPi_GetWheelList_pb2 import GetWheelListResponse
                response: GetWheelListResponse = GetWheelListResponse()
                response.ParseFromString(msg.bodyData)
                if response.resultCode != 0:
                    return response.error
                else:
                    return "\n".join(response.Wheels)
            elif header.command == _PCPyCmdId.PYPI_UPLOAD_SCRIPT_REQUEST.value:
                from mini.tool.pb2.PyPi_UploadScript_pb2 import UploadScriptResponse
                response: UploadScriptResponse = UploadScriptResponse()
                response.ParseFromString(msg.bodyData)
                print("command {0} return <{1}, {2}>".format(header.command, response.resultCode, response.message))
                return response.message
            elif header.command == _PCPyCmdId.PYPI_CHECK_UPLOAD_SCRIPT_REQUEST.value:
                from mini.tool.pb2.PyPi_UploadScript_pb2 import UploadScriptResponse
                response: UploadScriptResponse = UploadScriptResponse()
                response.ParseFromString(msg.bodyData)
                print("command {0} return <{1}, {2}>".format(header.command, response.resultCode, response.message))
                return response.message
            elif header.command == _PCPyCmdId.PYPI_RUN_UPLOAD_SCRIPT_REQUEST.value:
                from mini.tool.pb2.PyPi_UploadScript_pb2 import UploadScriptResponse
                response: UploadScriptResponse = UploadScriptResponse()
                response.ParseFromString(msg.bodyData)
                print("command {0} return <{1}, {2}>".format(header.command, response.resultCode, response.message))
                return response.message
            elif header.command == _PCPyCmdId.PYPI_STOP_UPLOAD_SCRIPT_REQUEST.value:
                from mini.tool.pb2.PyPi_UploadScript_pb2 import UploadScriptResponse
                response: UploadScriptResponse = UploadScriptResponse()
                response.ParseFromString(msg.bodyData)
                print("command {0} return <{1}, {2}>".format(header.command, response.resultCode, response.message))
                return response.message
            elif header.command == _PCPyCmdId.PYPI_LIST_UPLOAD_SCRIPT_REQUEST.value:
                from mini.tool.pb2.PyPi_UploadScript_pb2 import ListUploadScriptResponse
                response: ListUploadScriptResponse = ListUploadScriptResponse()
                response.ParseFromString(msg.bodyData)
                print("command {0} return {1}".format(header.command, response.uploadScripts))
                return "ex"
            elif header.target == -1:
                print(f"不支持的指令cmd={header.command}")
            else:
                print(f"不支持的指令cmd={header.command}")

        except Exception as e:
            if isinstance(e, websockets.ConnectionClosedOK):
                # print(f"connection closed ok!")
                break
            else:
                raise e
    return result


async def _send_msg0(message: _Message, device: _WiFiDevice) -> str:
    try:
        async with websockets.connect('ws://{}:{!r}'.format(device.address, 8801)) as websocket:
            return await _send_msg1(websocket, message)
    except Exception as e:
        return ""


def _get_eggInfo_path():
    return _get_file('.', 'egg-info', True)


def _get_file(dir_path: str, suffix: str, is_dir: bool = False):
    for temp_path in os.listdir(dir_path):
        temp_path = os.path.join(dir_path, temp_path)
        if is_dir:
            if not os.path.isdir(temp_path):
                continue
        else:
            if not os.path.isfile(temp_path):
                continue

        if temp_path.endswith(suffix):
            result = os.path.abspath(temp_path)
            return result


def _remove_dir(dir_path: str):
    """
    删除目录
    :param dir_path: 需要删除的目录
    """
    if isinstance(dir_path, str) and os.path.exists(dir_path) and os.path.isdir(dir_path):
        import shutil
        shutil.rmtree(dir_path)
    elif dir_path is not None and os.path.exists(dir_path):
        os.remove(dir_path)


def setup_py_pkg(project_dir: str) -> str:
    """
    Package a py project into a .whl file.

    Args:
        project_dir: project file root directory

    Returns:
        str: the absolute path of the generated .whl file
    """
    # 校验目录
    if not os.path.isdir(project_dir):
        print('project_dir must be a directory')
        return ""
    # 将当前进程工作目录切换到工程目录
    os.chdir(project_dir)
    # 清空产物目录
    build_path = 'build'
    egg_info_path = _get_eggInfo_path()
    dist_path = 'dist'
    _remove_dir(build_path)
    _remove_dir(egg_info_path)
    _remove_dir(dist_path)

    os.mkdir(build_path)
    os.mkdir(dist_path)

    # 找到setup文件
    setup_path = 'setup.py'

    if not os.path.isfile(setup_path):
        print('setup.py not exist')
        return ""

    # 打包
    import sys
    if sys.version_info < (3, 0):
        os.system(f"python {setup_path} sdist bdist_wheel")
    else:
        import platform
        if platform.system() == 'Windows':
            os.system(f'python {setup_path} sdist bdist_wheel')
        else:
            os.system(f'python3 {setup_path} sdist bdist_wheel')

    # 删除其他临时文件
    egg_info_path = _get_eggInfo_path()
    _remove_dir(build_path)
    _remove_dir(egg_info_path)

    result = _get_file(dist_path, '.whl')
    print(f'result {result}')
    return result


def _build_install_py_pkg_msg(package_path: str, debug: bool) -> _Message:
    from mini.tool.pb2.PyPi_InstallWheel_pb2 import InstallWheelRequest
    request = InstallWheelRequest()
    # 获取文件路径中的文件名
    request.wheelName = os.path.basename(package_path)
    # 把文件转成字节
    request.serializePacket = _read_into_buffer(package_path)
    request.debug = debug
    cmd_id = _PCPyCmdId.PYPI_INSTALL_WHEEL_REQUEST.value
    # message
    message: _Message = msg_utils.build_request_msg(cmd_id, 0, request)
    return message


def install_py_pkg(package_path: str, robot_id: str, debug: bool = False):
    """
    Install a py program installation package on the robot with the specified serial number.

    Args:
        package_path: the absolute path of the installation package
        robot_id: robot serial number
        debug: Whether to print the log when pkg is uninstalled on the robot side

    Returns:
        None
    """
    # 校验文件
    if not os.path.isfile(package_path):
        print(f'file is not exist:{package_path}')
        return

    base_name = os.path.basename(package_path)

    if not base_name.endswith('.whl'):
        print(f'文件不是一个pypi安装包')
        return

    device: _WiFiDevice = _found_devices.get(robot_id)
    # 搜索设备
    if device is None:
        device = asyncio.get_event_loop().run_until_complete(mini.get_device_by_name(robot_id, 10))
        if device is None:
            print(f"不能找到机器人:{robot_id}")
            return
        else:
            _found_devices[robot_id] = device
    # 上传
    asyncio.run(_send_msg0(_build_install_py_pkg_msg(package_path, debug), device))


def _build_uninstall_py_pkg_msg(pkg_name: str, debug: bool) -> _Message:
    from mini.tool.pb2.PyPi_UninstallWheel_pb2 import UninstallWheelRequest
    request = UninstallWheelRequest()
    # pkg name
    request.wheelName = os.path.basename(pkg_name)
    request.debug = debug
    cmd_id = _PCPyCmdId.PYPI_UNINSTALL_WHEEL_REQUEST.value
    # message
    message: _Message = msg_utils.build_request_msg(cmd_id, 0, request)
    return message


def uninstall_py_pkg(pkg_name: str, robot_id: str, debug: bool = False):
    """
    Uninstall an installed py program from the robot with the specified serial number. For example, there is a py program whose setup.py file is configured as follows:
        setuptools.setup(

            name="tts_demo",

            ...#Omitted

         ),

    Then, its pkg_name is "tts_demo".

    Args:
        pkg_name: program name
        robot_id: robot serial number
        debug: Whether to print the log when pkg is uninstalled on the robot side

    Returns:
        None

    """
    device: _WiFiDevice = _found_devices.get(robot_id)
    # 搜索设备
    if device is None:
        device = asyncio.get_event_loop().run_until_complete(mini.get_device_by_name(robot_id, 10))
        if device is None:
            print(f"不能找到机器人:{robot_id}")
            return
        else:
            _found_devices[robot_id] = device
    # 卸载
    asyncio.run(_send_msg0(_build_uninstall_py_pkg_msg(pkg_name, debug), device))


def _build_query_py_pkg_msg(pkg_name: str) -> _Message:
    from mini.tool.pb2.PyPi_GetWheelInfo_pb2 import GetWheelInfoRequest
    request = GetWheelInfoRequest()
    # pkg name
    request.wheelName = os.path.basename(pkg_name)
    cmd_id = _PCPyCmdId.PYPI_GET_WHEEL_INFO_REQUEST.value
    # message
    message: _Message = msg_utils.build_request_msg(cmd_id, 0, request)
    return message


def query_py_pkg(pkg_name: str, robot_id: str) -> str:
    """
    Query the py program specified by pkg_name on the robot, and its detailed information, for example, there is a py program, and its setup.py file is configured as follows:

    setuptools.setup(

        name="tts_demo",

        version="0.0.2",

        author='Gino Deng',

        author_email='jingjing.deng@ubtrobot.com',

        description="demo with mini_sdk",

        long_description='demo with mini_sdk,xxxxxxx',

        long_description_content_type="text/markdown",

        license="GPLv3",

        packages=setuptools.find_packages(),

        classifiers=[

            "Programming Language :: Python :: 3",

            "Programming Language :: Python :: 3.6",

            "Programming Language :: Python :: 3.7",

            "Programming Language :: Python :: 3.8",

            "License :: OSI Approved :: MIT License",

            "Operating System :: OS Independent",

        ],

        install_requires=[

            'alphamini',

        ],

    ),

    When querying, specify pkg_name="tts_demo", and the returned information is as follows:

        Name: tts-demo

        Version: 0.0.2

        Summary: demo with mini_sdk

        Home-page: UNKNOWN

        Author: Gino Deng

        Author-email: jingjing.deng@ubtrobot.com

        License: GPLv3

        Location: /data/data/com.termux/files/usr/lib/python3.8/site-packages

        Requires: alphamini

        Required-by:

    Args:
        pkg_name: py program name,
        robot_id: robot serial number

    Returns:
        str: install package trust information
    """
    device: _WiFiDevice = _found_devices.get(robot_id)
    # 搜索设备
    if device is None:
        device = asyncio.get_event_loop().run_until_complete(mini.get_device_by_name(robot_id, 10))
        if device is None:
            print(f"不能找到机器人:{robot_id}")
            return ""
        else:
            _found_devices[robot_id] = device
    # 查询
    return asyncio.run(_send_msg0(_build_query_py_pkg_msg(pkg_name), device))


def _build_list_py_pkg_msg():
    from mini.tool.pb2.PyPi_GetWheelList_pb2 import GetWheelListRequest
    request = GetWheelListRequest()
    cmd_id = _PCPyCmdId.PYPI_GET_WHEEL_LIST_REQUEST.value
    # message
    message: _Message = msg_utils.build_request_msg(cmd_id, 0, request)
    return message


def list_py_pkg(robot_id: str) -> str:
    """
    List the py programs installed on the robot, for example:

         Package Version

         ---------- -------

         alphamini 0.1.0

         ifaddr 0.1.7

         pip 20.1.1

         protobuf 3.12.2

         setuptools 47.3.1

         six 1.15.0

         tts-demo 0.0.2

         websockets 8.1

         wheel 0.34.2

    Args:
        robot_id: robot serial number

    Returns:
         str: name of all py programs-version number
    """
    device: _WiFiDevice = _found_devices.get(robot_id)
    # 搜索设备
    if device is None:
        device = asyncio.get_event_loop().run_until_complete(mini.get_device_by_name(robot_id, 10))
        if device is None:
            print(f"不能找到机器人:{robot_id}")
            return ""
        else:
            _found_devices[robot_id] = device
    # 查询
    return asyncio.run(_send_msg0(_build_list_py_pkg_msg(), device))


def _build_run_py_pkg_msg(entry_point: str, debug: bool) -> _Message:
    from mini.tool.pb2.PyPi_RunWheel_pb2 import RunWheelRequest
    request = RunWheelRequest()
    # pkg main entry
    request.wheelName = entry_point
    request.debug = debug
    cmd_id = _PCPyCmdId.PYPI_RUN_WHEEL_REQUEST.value
    # message
    message: _Message = msg_utils.build_request_msg(cmd_id, 0, request)
    return message


def run_py_pkg(entry_point: str, robot_id: str, debug: bool = False):
    """
    Trigger a specified py program to run on the specified robot. :

    Args:
        entry_point: The name of the console scripts of the py program, for example, in the setup.py file,

        such as configuration entry_points=(

                         'console_scripts': [

                             'XXX = Packages.Modules:XXX'

                         ],

                     }, the program entry name is xxx

        robot_id: robot serial number
        debug: Whether to return the log when the program is executed

    Returns:
        None
    """
    device: _WiFiDevice = _found_devices.get(robot_id)
    # 搜索设备
    if device is None:
        device = asyncio.get_event_loop().run_until_complete(mini.get_device_by_name(robot_id, 10))
        if device is None:
            print(f"不能找到机器人:{robot_id}")
            return
        else:
            _found_devices[robot_id] = device
    # 触发
    asyncio.run(_send_msg0(_build_run_py_pkg_msg(entry_point, debug), device))


def _build_switch_adb_msg(switch: bool):
    from mini.tool.pb2.PyPi_AdbSwitch_pb2 import AdbSwitchRequest
    request = AdbSwitchRequest()
    # pkg main entry
    request.open = switch
    cmd_id = _PCPyCmdId.PYPI_SWITCH_ADB_REQUEST.value
    # message
    message: _Message = msg_utils.build_request_msg(cmd_id, 0, request)
    return message


def switch_adb(robot_id: str, switch: bool = True):
    """
    Turn on the robot ADB debugging switch
    Args:
        switch: bool, True or False
        robot_id: robot serial number

    Returns:
        None
    """
    device: _WiFiDevice = _found_devices.get(robot_id)
    # 搜索设备
    if device is None:
        device = asyncio.get_event_loop().run_until_complete(mini.get_device_by_name(robot_id, 10))
        if device is None:
            print(f"不能找到机器人:{robot_id}")
            return
        else:
            _found_devices[robot_id] = device
    # 触发
    asyncio.run(_send_msg0(_build_switch_adb_msg(switch), device))


def _build_upload_script_msg(file_name: str = None, content: bytes = None, cmd_id: int = 1):
    from mini.tool.pb2.PyPi_UploadScript_pb2 import UploadScript
    request = UploadScript()
    if file_name is not None:
        request.fileName = file_name
    if content is not None:
        request.content = content
    # message
    message: _Message = msg_utils.build_request_msg(cmd_id, 0, request)
    return message


# 上传python脚本到机器人
def upload_script(cmd_id: int, robot_id: str, file_name: str = None, content: bytes = None):
    pyCmdId = _PCPyCmdId.PYPI_UPLOAD_SCRIPT_REQUEST
    if cmd_id == 1:
        pyCmdId = _PCPyCmdId.PYPI_UPLOAD_SCRIPT_REQUEST
    elif cmd_id == 2:
        pyCmdId = _PCPyCmdId.PYPI_CHECK_UPLOAD_SCRIPT_REQUEST
    elif cmd_id == 3:
        pyCmdId = _PCPyCmdId.PYPI_RUN_UPLOAD_SCRIPT_REQUEST
    elif cmd_id == 4:
        pyCmdId = _PCPyCmdId.PYPI_STOP_UPLOAD_SCRIPT_REQUEST
    elif cmd_id == 5:
        pyCmdId = _PCPyCmdId.PYPI_LIST_UPLOAD_SCRIPT_REQUEST
    else:
        pyCmdId = _PCPyCmdId.PYPI_LIST_UPLOAD_SCRIPT_REQUEST

    device: _WiFiDevice = _found_devices.get(robot_id)
    # 搜索设备
    if device is None:
        device = asyncio.get_event_loop().run_until_complete(mini.get_device_by_name(robot_id, 10))
        if device is None:
            print(f"不能找到机器人:{robot_id}")
            return
        else:
            _found_devices[robot_id] = device
    # 触发
    return asyncio.run(_send_msg0(_build_upload_script_msg(file_name, content, pyCmdId.value), device))
