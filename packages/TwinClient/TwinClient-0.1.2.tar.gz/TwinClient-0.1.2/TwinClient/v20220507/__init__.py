#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------------
# Descripttion: https://github.com/sxhxliang
# version: 0.0.1
# Author: Shihua Liang (sxhx.liang@gmail.com)
# FilePath: /01孪生体创建/python-sdk/TwinClient/v20220507/__init__.py
# Create: 2022-05-07 12:57:40
# LastAuthor: Please set LastEditors
# lastTime: 2022-05-09 11:03:06
# --------------------------------------------------------

from .base_config import TENANT_ID, TwinClientConfig, DTMS_REGISTER_HOST
from .twin_asset import TwinAsset
from .schema import AssetTypeModel, AssetTwinSubtypeModel
from .twin_definitions import TwinDefinition