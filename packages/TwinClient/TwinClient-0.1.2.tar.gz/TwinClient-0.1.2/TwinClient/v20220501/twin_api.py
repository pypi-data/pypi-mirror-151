#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------------
# Descripttion: https://github.com/sxhxliang
# version: 0.0.1
# Author: Shihua Liang (sxhx.liang@gmail.com)
# FilePath: /01孪生体创建/python-sdk/TwinClient/v20220501/twin_api.py
# Create: 2022-05-07 00:11:11
# LastAuthor: Please set LastEditors
# lastTime: 2022-05-09 10:41:23
# --------------------------------------------------------

import requests
import json
import random
import pandas as pd
import copy
import logging
import datetime
import math
# import dict
import uuid
from os import path
from typing import List

from .base_config import (TwinClientConfig, rest_get, rest_post, rest_delete, rest_put)
from .base_config import (
    DTMS_REGISTER_HOST,
    DTMS_REGISTER_RELATION_HOST,
    DTMS_TWINDEF_HOST,
    DTMS_TWIN_HOST
)
from .schema import (
            AssetTypeModel, AssetTwinSubtypeModel, AssetRelationModel, AssetTypeEnum,
            TwinTypeModel, SubTwinTypeModel)


class TwinInstance(object):
    """docstring for TwinAsset."""
    def __init__(self, cfg: TwinClientConfig):
        super(TwinInstance, self).__init__()
        self.cfg = cfg
        
        self.twin_category = None
        self.twin_type = None
        self.sub_twin_type = None
        
        #保存所有资产和孪生体信息
        # self.twin_category_infos = {}
        # self.twin_type_infos = {}
        # self.sub_twin_infos = {}
        
    def get_twin_by_uuid(self, uu_id: str):
        """_summary_
            {{dtmstwin}}/v1/wuhan/twins/{{twinId}}
        Args:
            uu_id (str): _description_

        Returns:
            _type_: _description_
        """
        uuid_version= uuid.UUID(uu_id).version
        if not uuid_version:
            print("请输入正确的 uuid" )
            return False
        
        response = rest_get(path.join(DTMS_TWIN_HOST, uu_id))
        # 保存返回的消息
        # self.twin_type_infos[twin_model.code] = response
        return response
        
    def update_twin_by_uuid(self, uu_id: str, data: object):
        """_summary_
            {{dtmstwin}}/v1/wuhan/twins/{{twinId}}
        Args:
            uu_id (str): _description_

        Returns:
            _type_: _description_
        """
        uuid_version= uuid.UUID(uu_id).version
        if not uuid_version:
            print("请输入正确的 uuid" )
            return False
        response = rest_put(path.join(DTMS_TWIN_HOST, uu_id), data)
        # 保存返回的消息
        # self.twin_type_infos[twin_model.code] = response
        return response
        
        
        
            
        

