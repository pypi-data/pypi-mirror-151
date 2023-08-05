#!/usr/bin/env python3

from ..apis.api_config import LanType, ServicePlatform
from ..apis.base_api import BaseApi, DEFAULT_TIMEOUT
from ..apis.cmdid import _PCProgramCmdId
from ..pb2.cloudtranslate_pb2 import Translate
from ..pb2.cloudwiki_pb2 import WiKi
from ..pb2.codemao_translate_pb2 import TranslateResponse, TranslateRequest
from ..pb2.codemao_wiki_pb2 import WikiRequest, WikiResponse
from ..pb2.pccodemao_message_pb2 import Message


class QueryWiKi(BaseApi):
    """Encyclopedia api

    Default Tencent Encyclopedia

    Args:
         is_serial (bool): Whether to wait for a reply, the default is True
         query (str): query content, cannot be empty or None

    #WikiResponse.isSuccess: Is it successful

    #WikiResponse.resultCode: Return code
    """

    def __init__(self, is_serial: bool = True, query: str = None):
        assert isinstance(query, str) and len(query), 'QueryWiKi query should be available'
        self.__is_serial = is_serial
        self.__query = query
        self.__platform = ServicePlatform.TENCENT.value

    async def execute(self):
        """
        Execute encyclopedia instructions

        Returns:
            WikiResponse

        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT

        wiki = WiKi()
        wiki.query = self.__query
        wiki.platform = self.__platform

        request = WikiRequest()
        request.wiki.CopyFrom(wiki)

        cmd_id = _PCProgramCmdId.WIKI_REQUEST.value

        return await self.send(cmd_id, request, timeout)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            WikiResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = WikiResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class StartTranslate(BaseApi):
    """Translation api

    Default Baidu translation

    Args:
         is_serial (bool): Whether to wait for a reply, the default is True
         query (str): The translated content, cannot be empty or None
         from_lan (LanType): the original language of the translation, default CN, Chinese
         to_lan (LanType): target language for translation, default EN, English
         platform (ServicePlatform): translation platform, default BAIDU, use Baidu translation

    #TranslateResponse.isSuccess: Is it successful, True or False

    #TranslateResponse.resultCode: Result code
    """

    def __init__(self, is_serial: bool = True, query: str = None,
                 from_lan: LanType = LanType.CN,
                 to_lan: LanType = LanType.EN,
                 platform: ServicePlatform = ServicePlatform.BAIDU):
        assert isinstance(query, str) and len(query) > 0, 'Translate : query should be available'
        assert isinstance(from_lan, LanType), 'Translate : from_lan should be LanType instance'
        assert isinstance(to_lan, LanType), 'Translate : to_lan should be LanType instance'
        assert isinstance(platform, ServicePlatform), 'Translate : platform should be ServicePlatform instance'
        self.__is_serial = is_serial
        self.__query = query
        # self.__prefix = prefix
        # self.__suffix = suffix
        self.__from_lan = from_lan.value
        self.__to_lan = to_lan.value
        self.__platform = platform.value

    async def execute(self):
        """
        Execute translation instructions

        Returns:
            TranslateResponse
        """
        timeout = 0
        if self.__is_serial:
            timeout = DEFAULT_TIMEOUT

        translate = Translate()
        translate.query = self.__query
        # translate.prefix = self.__prefix
        # translate.suffix = self.__suffix
        translate.platform = self.__platform
        # translate.from = self.__fromLan
        setattr(translate, "from", self.__from_lan)
        translate.to = self.__to_lan
        # setattr(translate, "to", self.__toLan)

        request = TranslateRequest()
        request.translate.CopyFrom(translate)

        cmd_id = _PCProgramCmdId.TRANSLATE_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def _parse_msg(self, message):
        """

        Args:
            message (Message):待解析的Message对象

        Returns:
            TranslateResponse
        """
        if isinstance(message, Message):
            data = message.bodyData
            response = TranslateResponse()
            response.ParseFromString(data)
            return response
        else:
            return None
