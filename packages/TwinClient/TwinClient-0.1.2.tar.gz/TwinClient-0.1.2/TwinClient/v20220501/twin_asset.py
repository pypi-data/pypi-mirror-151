#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------------
# Descripttion: https://github.com/sxhxliang
# version: 0.0.1
# Author: Shihua Liang (sxhx.liang@gmail.com)
# FilePath: /01孪生体创建/python-sdk/TwinClient/v20220501/twin_asset.py
# Create: 2022-05-02 23:04:59
# LastAuthor: Please set LastEditors
# lastTime: 2022-05-09 10:41:30
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
from os import path
import uuid
from typing import List

from .base_config import (TwinClientConfig, rest_get, rest_post, rest_delete)
from .base_config import (
    DTMS_REGISTER_HOST,
    DTMS_REGISTER_RELATION_HOST,
    DTMS_TWINDEF_HOST,
    DTMS_TWIN_HOST
)
from .schema import (
            AssetTypeModel,
            AssetTwinSubtypeModel,
            AssetRelationModel,
            AssetTypeEnum,
            AssetRelationInResponseModel)

class TwinAsset(object):
    """docstring for TwinAsset."""
    def __init__(self, cfg: TwinClientConfig):
        super(TwinAsset, self).__init__()
        self.cfg = cfg
        
        self.twin_category = None
        self.twin_type = None
        self.sub_twin_type = None
        
        #保存所有资产和孪生体信息
        self.twin_category_infos = {}
        self.twin_type_infos = {}
        self.sub_twin_infos = {}
        
        # print(cfg.tenantId, cfg.dtmsregistry, cfg.dtmstwin, cfg.dtmstwindef)
        
    
    def create_twin_category_asset(self, asset_model: AssetTypeModel):
        """
        第一步创建 twin_category
        """
        assert asset_model.asset_type == AssetTypeEnum.twin_category
        
        response = rest_post(DTMS_REGISTER_HOST, asset_model.json())
        # 保存返回的消息
        self.twin_category_infos[asset_model.code] = response
        return response

    def create_twin_type_asset(self, asset_model: AssetTypeModel):
        """
        第二步创建 twin_type
        """
        assert asset_model.asset_type == AssetTypeEnum.twin_type

        response = rest_post(DTMS_REGISTER_HOST, asset_model.json())
        # 保存返回的消息
        self.twin_type_infos[asset_model.code] = response
        return response

    def create_twin_subtype_asset(self, asset_model: AssetTwinSubtypeModel):
        """
        第三步创建 twin_subtype
        // 注意：定义twin_subtype的时候，需要一个pid指定上级目录的code，比如父节点code=people_twin
        """
        assert asset_model.asset_type == AssetTypeEnum.twin_subtype
        
        parent_uuid = self.get_uuid_by_code(asset_model.pid)
        if not parent_uuid:
            print("查询不到 pid 资产 !", asset_model.pid)
            return {'message': '查询不到pid 资产 !'}
        response = rest_post(DTMS_REGISTER_HOST, asset_model.json())
        # 保存返回的消息
        self.twin_type_infos[asset_model.code] = response
        return response
        
    
    def create_asset_relation(self, asset_relation_model: AssetRelationModel) -> AssetRelationInResponseModel:
        """
        第四步创建 关系
        """
        try:
            from_asset_version= uuid.UUID(asset_relation_model.from_asset).version
            to_asset_version= uuid.UUID(asset_relation_model.to_asset).version
            # 判断版本一致
            assert from_asset_version == to_asset_version
            # 判断资产是否存在
            from_asset = self.get_asset_by_params({"_id": asset_relation_model.from_asset})
            to_asset = self.get_asset_by_params({"_id": asset_relation_model.to_asset})
        except Exception as e:
            print("Error: create asset relation {} ({}) error; error code: {}".format(asset_relation_model.from_asset, asset_relation_model.to_asset, e))
            return
        response = rest_post(DTMS_REGISTER_RELATION_HOST, asset_relation_model.json())
        # 保存返回的消息
        # self.twin_relation_infos[asset_relation_model.code] = response
        return AssetRelationInResponseModel(**response)
    
    def create_asset_relation_by_code(self, asset_relation_model: AssetRelationModel):
        try:
            # code 转换成 uuid
            asset_relation_model.from_asset = self.get_uuid_by_code(asset_relation_model.from_asset)
            asset_relation_model.to_asset = self.get_uuid_by_code(asset_relation_model.to_asset)
        except Exception as e:
            print("Error: create asset relation {} ({}) error; error code: {}".format(asset_relation_model.from_asset, asset_relation_model.to_asset, e))
            return
        response = rest_post(DTMS_REGISTER_RELATION_HOST, asset_relation_model.json())
        # 保存返回的消息
        # self.twin_relation_infos[asset_relation_model.code] = response
        return response
        
        
    def get_asset_by_code(self, code :str):
        """_summary_
        eg: {{dtmsregistry}}/{{tenantId}}/asset?code=people_cates
        Args:
            code (_type_): _description_
        Returns:
            _type_: _description_
            {"owner": "dtostwin", "code": "people_cates", "asset_type": "twin_category", "name": "\u4eba\u5458\u7c7b\u522b", "extension_value": {}, "create_user": "registry", "version": "1.0.0", "status": "valid"}
        """
        response = rest_get(DTMS_REGISTER_HOST, {"code": code})
        return response
    
    def get_uuid_by_code(self, code):
        # 判断资产是否存在 并
        asset = self.get_asset_by_params({"code": code})
        if asset['code'] == 200 and asset["total"] > 0:
            # 根据
            return asset["data"][0]["_id"]
        return False
        
    
    def get_asset_by_params(self, params :object):
        """_summary_
        eg:     asset?code=people_cates
                asset?extension_value.developer=liangshihua
                
        Args:
            params (json): 要查询的字段
        Returns:
            _type_: _description_
            {"owner": "dtostwin", "code": "people_cates", "asset_type": "twin_category", "name": "\u4eba\u5458\u7c7b\u522b", "extension_value": {}, "create_user": "registry", "version": "1.0.0", "status": "valid"}
        """
        response = rest_get(DTMS_REGISTER_HOST, params)
        return response
    
    def delect_asset_by_id(self, asset_uuid:str):
        """
        删除资产
        Args:
            asset_uuid (str): 资产id uuid 类型
        """
        # {{dtmsregistry}}/{{tenantId}}/asset/asset_uuid
        
        try:
            uuid.UUID(asset_uuid).version
            # 判断版本一致
        except Exception as e:
            print("Error:  error; error code: {}".format(e))
            return
        url = path.join(DTMS_REGISTER_HOST, asset_uuid)
        response = rest_delete(path.join(DTMS_REGISTER_HOST, asset_uuid))
        # TODO 删除对应的资产
        print("删除资产成功 ", "asset_uuid:", asset_uuid)
        return response
    

    def create_assets(self, asset_models: List[AssetTypeModel]):
        """
        批量创建资产
        Args:
            asset_models (List[AssetTypeModel]): _description_
        """
        res = []
        for asset_model in asset_models:
            res.append(getattr(self, asset_model.asset_type)(asset_model))
    
    


