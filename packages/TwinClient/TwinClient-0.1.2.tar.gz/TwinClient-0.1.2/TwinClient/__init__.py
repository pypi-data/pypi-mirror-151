#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------------
# Descripttion: https://github.com/sxhxliang
# version: 0.0.1
# Author: Shihua Liang (sxhx.liang@gmail.com)
# FilePath: /01孪生体创建/python-sdk/TwinClient/__init__.py
# Create: 2022-05-02 23:00:07
# LastAuthor: Please set LastEditors
# lastTime: 2022-05-09 17:32:39
# --------------------------------------------------------

__version__ = '0.1.0'


from .v20220507.base_config import TwinClientConfig, DTMS_REGISTER_HOST
from .v20220507.twin_asset import TwinAsset
from .v20220507.schema import AssetTypeModel, AssetTwinSubtypeModel
from .v20220507.twin_definitions import TwinDefinition
from .v20220507.twin_api import TwinInstance


default_config = TwinClientConfig()

class TwinClient():
    """docstring for TwinClient."""
    def __init__(self, cfg: TwinClientConfig=default_config):
        print("初始化默认客户端")
        self.cfg = cfg
        self.asset = TwinAsset(cfg)
        self.twin_definition = TwinDefinition(cfg)
        self.twin = TwinInstance(cfg)
    
    def get_config(self):
        return self.cfg


def default_twin_client():
    return TwinClient(default_config)