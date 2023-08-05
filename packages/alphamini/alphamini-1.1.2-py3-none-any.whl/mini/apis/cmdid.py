#!/usr/bin/env python3

import enum


@enum.unique
class _PCProgramCmdId(enum.Enum):
    """
    Command number configuration
    """

    RESPONSE_BASE = 1000

    PLAY_ACTION_REQUEST = 1
    """Play action
    """

    MOVE_ROBOT_REQUEST = 2
    """move robot
    """

    STOP_ACTION_REQUEST = 3
    """Stop action
    """

    PLAY_TTS_REQUEST = 4
    """Play tts
    """

    FACE_DETECT_REQUEST = 5
    """Face number recognition
    """

    FACE_ANALYSIS_REQUEST = 6
    """ Face recognition (male female)
    """

    RECOGNISE_OBJECT_REQUEST = 7
    """ Object Gesture Flower and Grass Recognition
    """

    FACE_RECOGNISE_REQUEST = 8
    """ recognizes someone
    """

    TAKE_PICTURE_REQUEST = 9
    """Photo
    """

    PLAY_EXPRESSION_REQUEST = 10
    """Play emoticons
    """

    SET_MOUTH_LAMP_REQUEST = 11
    """Set the mouth light
    """

    SUBSCRIBE_INFRARED_DISTANCE_REQUEST = 12
    """Subscribe to infrared detection obstacle distance: monitor
    """

    SUBSCRIBE_ROBOT_POSTURE_REQUEST = 13
    """Subscribe robot gesture: monitor
    """

    SUBSCRIBE_HEAD_RACKET_REQUEST = 14
    """Subscribe to beat head events: monitor
    """

    CONTROL_BEHAVIOR_REQUEST = 15
    """Control behavior
    """

    GET_ROBOT_VERSION_REQUEST = 16
    """Get the version number
    """
    GET_ROBOT_VERSION_RESPONSE = RESPONSE_BASE + GET_ROBOT_VERSION_REQUEST

    GET_INFRARED_DISTANCE_REQUEST = 19
    """Get infrared distance
    """

    REVERT_ORIGIN_REQUEST = 20
    """Stop all operations
    """

    DISCONNECTION_REQUEST = 21
    """Disconnect tcp
    """

    SWITCH_MOUTH_LAMP_REQUEST = 22
    """ switch mouth light
    """

    PLAY_AUDIO_REQUEST = 23
    """Play sound effects
    """

    STOP_AUDIO_REQUEST = 24
    """Stop sound effect
    """

    GET_AUDIO_LIST_REQUEST = 25
    """Get a list of sound effects
    """

    TRANSLATE_REQUEST = 26
    """translation
    """

    WIKI_REQUEST = 27
    """Wiki
    """

    CHANGE_ROBOT_VOLUME_REQUEST = 28
    """Change the robot volume
    """

    PLAY_ONLINE_MUSIC_REQUEST = 29
    """Play online music
    """

    FACE_DETECT_TASK_REQUEST = 30
    """Face detection task (continuous detection): monitor
    """

    GET_REGISTER_FACES_REQUEST = 31
    """Get a list of acquaintances
    """

    FACE_RECOGNISE_TASK_REQUEST = 32
    """Face recognition (continuous recognition): monitor
    """

    GET_ACTION_LIST = 33
    """Get a list of robot actions
    """

    CONTROL_ROBOT_AUDIO_RECORD = 34
    """Control robot recording/playing/pause, etc.
    """

    SPEECH_RECOGNISE = 35
    """Voice recognition: monitor
    """

    GET_SERVER_INFO = 36
    """Get server information
    """

    PLAY_CUSTOM_ACTION_REQUEST = 37
    """Play custom actions
    """

    STOP_CUSTOM_ACTION_REQUEST = 38
    """Stop custom action
    """

    STOP_SPEECH_RECOGNISE_REQUEST = 39
    """Stop speech recognition
    """

    GET_ROBOT_LANGUAGE_MODE = 40
    """Get the robot language model-only supported on Edu products
    """

    SET_ROBOT_LANGUAGE = 41
    """Set robot language--Only supported on Edu products
    """
