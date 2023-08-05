COMMON = (
    (100, "Request parameter error, please upgrade the system"),
    (101, "The operation is not authorized, please try again later"),
    (102, "AlphaMini is busy, please try again later"),
    (103, "System error, please upgrade the system"),
    (104, "AlphaMini is busy, please try again later"),
    (105, "AlphaMini is busy, please try again later"),
    (106, "AlphaMini is busy, please try again later"),
    (107, "System error, please upgrade the system"),
    (108, "System error, please upgrade the system"),
    (109, "System error, please upgrade the system"),
    (110, "System error, please upgrade the system"),

    (400, "Request parameter error, please upgrade the system"),
    (401, "The operation is not authorized, please try again later"),
    (403, "AlphaMini is busy, please try again later"),
    (404, "System error, please upgrade the system"),
    (408, "AlphaMini is busy, please try again later"),
    (409, "AlphaMini is busy, please try again later"),
    (500, "AlphaMini is busy, please try again later"),
    (501, "System error, please upgrade the system"),
    (504, "System error, please upgrade the system"),
    (1006, "System error, please upgrade the system"),
    (1007, "System error, please upgrade the system"),

    (-61, "The account is in arrears"),
    (-64, "The account has been frozen"),
    (-81, "Privacy mode is turned on, this function cannot be used"),
    (-92, "Privacy mode is turned on, this function cannot be used"),
    (-1, "The robot failed to stand up"),
    (-2, "AlphaMini's battery is low, please recharge and click again"),
    (-3, "AlphaMini fell down, please help AlphaMini to try again"),
    (-4, "AlphaMini is under video surveillance, please try again later."),
    (-5, "AlphaMini is on a call, please try again after the call is over"),
    (-7, "AlphaMini is upgrading, wait until I finish upgrading and try it out"),
    (-8, "AlphaMini is doing a difficult move, wait until he finishes it and try again"),
    (-9, "AlphaMini has not been bound yet, please bind him on your phone"),
)
# """
# General error code description
# """

SPEECH = (
    (1001, "AlphaMini is busy, please try again later"),
    (1002, "Network error, please try again later"),
    (1003, "TTS content is empty, synthesis failed"),
    (1004, "Playing failed, audio resource has expired"),
    (1005, "The audio is empty, please select a sound effect"),
    (1006, "Network error, please try again later"),
    (1007, "Network error, please try again later"),
    (0, ""),
)
# """
# Voice related error code description
# """

CONTENT = (
    (1101, "AlphaMini is busy, please try again later"),
    (1102, "Network error, please try again later"),
    (1103, "TTS content is empty, synthesis failed"),
    (1104, "Play failed, audio resource has expired"),
    (0, "The audio is empty, please select a sound effect"),
)
# """
# Content broadcast related error code description
# """

VISION = (
    (1201, "In order to detect the face, please look at AlphaMini's eyes and don't shake"),
    (1202, "You have entered face information"),
    (1203,
     "The number of face information has reached the upper limit, please delete the face in the APP AlphaMini friends and try again"),
    (1204,
     "The number of face information has reached the upper limit, please delete the face in the APP AlphaMini friends and try again"),
    (1205, "AlphaMini is entering face information, please try again later"),
    (1206, "Too many faces have been detected, please try again later"),
    (1207, "Face input was interrupted, please try again later"),
    (1208, "AlphaMini's battery is low, unable to add new friends"),
    (1209, "Network error, please try again later"),
    (1210, "AlphaMini is busy, please try again later"),
    (1211, "AlphaMini is reading the picture book, please try again later"),
    (1212, "AlphaMini is monitoring, please try again later"),
    (1213, "AlphaMini is on the phone, please try again later"),
    (1214, "Network error, please try again later"),
    (1215, "The camera failed to start, please try again"),
    (1216, "The camera seems to be blocked, please remove the blocking and try again"),
    (1217, "Recognition timeout"),
)
# """
# Detect related error code description
# """

MOTION = (
    (1301, "AlphaMini is busy, please try again later"),
    (1302, "AlphaMini is busy, please try again later"),
    (1304, "The robot servo is malfunctioning"),
    (1305, "Robot Servo Self-Protection"),
    (1306, "File missing, please upgrade the system"),
    (1307, "Data abnormal, please upgrade the system"),
    (1308, "Data abnormal, please upgrade the system"),
    (1309, "Data abnormal, please upgrade the system"),
    (1310, "Data abnormal, please upgrade the system"),
    (1311, "The action is being downloaded, please try again later"),
    (1312, "Performance of new action was interrupted"),
    (1313, "Action stop interrupt"),
    (1314, "Action stop interrupted"),
    (1315, "Action stop interrupted"),
)
# """
# Motion control related error code description
# """

EXPRESS = (
    (1401, "Action stop interrupt"),
    (1402, "The robot servo is malfunctioning"),
    (1403, "Robot Servo Self-Protection"),
    (1404, "Performance of new action was interrupted"),
    (1405, "File missing, please upgrade the system"),
    (1406, "Data is abnormal, please upgrade the system"),
    (1407, "Data is abnormal, please upgrade the system"),
    (1408, "Data is abnormal, please upgrade the system"),
    (1409, "Data is abnormal, please upgrade the system"),

    (1410, "The action is being downloaded, please try again later"),

    (1411, "File missing, please upgrade the system"),
    (1412, "File missing, please upgrade the system"),
    (1413, "Data is abnormal, please upgrade the system"),
    (1414, "Data is abnormal, please upgrade the system"),
    (1415, "Data abnormal, please upgrade the system"),
    (1416, "AlphaMini is busy, please try again later"),
    (1417, "Data is abnormal, please upgrade the system"),
)


# """
# Emoticon related error code description
# """


def get_common_error_str(error_code: int) -> str:
    """
    Map general error codes to error descriptions

    Args:
        error_code (int): Error code, in COMMON, otherwise it returns "unknown error"

    Returns:
        str: error description

    """
    if error_code == 0:
        return ""

    ret: str = "未知错误"
    for t in COMMON:
        if t[0] == error_code:
            ret = t[1]
            break
    return ret


def get_speech_error_str(error_code: int) -> str:
    """
    Map voice-related error codes to error descriptions

    Args:
        error_code (int): Error code, in SPEECH, otherwise it returns None

    Returns:
        str: error description

    """
    ret = None
    for t in SPEECH:
        if t[0] == error_code:
            ret = t[1]
            break
    if ret:
        return ret
    else:
        return get_common_error_str(error_code)


def get_content_error_str(error_code: int) -> str:
    """
    Map content broadcast related error codes to error descriptions

    Args:
        error_code (int): Error code, in CONTENT, otherwise it returns None

    Returns:
        str: error description

    """
    ret = None
    for t in CONTENT:
        if t[0] == error_code:
            ret = t[1]
            break
    if ret:
        return ret
    else:
        return get_common_error_str(error_code)


def get_vision_error_str(error_code: int) -> str:
    """
    Map error codes related to detection to error descriptions

    Args:
        error_code (int): Error code, in VISION, otherwise it returns None

    Returns:
        str: error description

    """
    ret = None
    for t in VISION:
        if t[0] == error_code:
            ret = t[1]
            break
    if ret:
        return ret
    else:
        return get_common_error_str(error_code)


def get_motion_error_str(error_code: int) -> str:
    """
    Map motion control related error codes to error descriptions

    Args:
        error_code (int): Error code, in MOTION, otherwise it returns None

    Returns:
        str: error description
    """
    ret = None
    for t in MOTION:
        if t[0] == error_code:
            ret = t[1]
            break
    if ret:
        return ret
    else:
        return get_common_error_str(error_code)


def get_express_error_str(error_code: int) -> str:
    """
    Mapping expression-related error codes to error descriptions

    Args:
        error_code (int): Error code, in EXPRESS, otherwise it returns None

    Returns:
        str: error description

    """
    ret = None
    for t in EXPRESS:
        if t[0] == error_code:
            ret = t[1]
            break
    if ret:
        return ret
    else:
        return get_common_error_str(error_code)
