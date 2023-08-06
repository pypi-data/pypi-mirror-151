#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------------
# Descripttion: https://github.com/sxhxliang
# version: 0.0.1
# Author: Shihua Liang (sxhx.liang@gmail.com)
# FilePath: /01孪生体创建/python-sdk/TwinClient/v20220501/twin_definitions.py
# Create: 2022-05-02 23:05:23
# LastAuthor: Please set LastEditors
# lastTime: 2022-05-09 10:41:36
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

from .base_config import (TwinClientConfig,
                          rest_get, rest_post, rest_delete, rest_put,
                          QueryWhere
                        )
from .base_config import (
    DTMS_REGISTER_HOST,
    DTMS_REGISTER_RELATION_HOST,
    DTMS_TWINDEF_HOST,
    DTMS_TWIN_HOST
)

from .twin_asset import TwinAsset
from .schema import (
            AssetTypeModel, AssetTwinSubtypeModel, AssetRelationModel, AssetTypeEnum,
            TwinTypeModel, TwinAttributes,
            SubTwinTypeModel, TwinTypeInResponse)



class TwinDefinition(object):
    """docstring for TwinAsset."""
    def __init__(self, cfg: TwinClientConfig):
        super(TwinDefinition, self).__init__()
        self.cfg = cfg
        
        self.twin_asset = TwinAsset(self.cfg)
        
        self.twin_category = None
        self.twin_type = None
        self.sub_twin_type = None
        
        #保存所有资产和孪生体信息
        # self.twin_category_infos = {}
        # self.twin_type_infos = {}
        # self.sub_twin_infos = {}
        
        # print(cfg.tenantId, cfg.dtmsregistry, cfg.dtmstwin, cfg.dtmstwindef)
        

        self.query = QueryWhere()
    # def create_twin_category(self, asset_model: AssetTypeModel):
    #     """
    #     第一步创建 twin_category
    #     """
    #     assert asset_model.asset_type == AssetTypeEnum.twin_category
        
    #     response = rest_post(DTMS_REGISTER_HOST, asset_model.json())
    #     # 保存返回的消息
    #     self.twin_category_infos[asset_model.code] = response
    #     # response 包含 _id 字段 (for create asset relation)
    #     return response

    def create_twin_type(self, twin_type_model: TwinTypeModel) -> TwinTypeInResponse:
        """
        第一步创建 twin_type
        """
        # assert twin_model.asset_type == AssetTypeEnum.twin_type
        print(twin_type_model.json())
        
        # self.get_twin_definitions_by_twin_type_code(twin_type_model.co)

        response_json = rest_post(DTMS_TWINDEF_HOST, twin_type_model.json())
        # 保存返回的消息
        # self.twin_type_infos[twin_model.code] = response
        return TwinTypeInResponse(**response_json)

    def create_sub_twin_type(self, sub_twin_type_model: SubTwinTypeModel) -> TwinTypeInResponse:
        """
        第二步创建 sub_twin_type
        "pId":"1650799384972",        // 必须 这个 pId 是 定义 twin_type（人员模型）模型的返回的 id
        "category": "people_cates",   // 必须 类别资产
        "twinType": "people_twin",    // 必须 孪生体
        "subTwinType": "people_drug", // 必须 子孪生体
        """
        # assert twin_model.asset_type == AssetTypeEnum.twin_type
        print(sub_twin_type_model.json())
        # 判断资产 Type 是否存在
        self.twin_asset.get_asset_by_code(sub_twin_type_model.category)
        self.twin_asset.get_asset_by_code(sub_twin_type_model.twinType)
        self.twin_asset.get_asset_by_code(sub_twin_type_model.subTwinType)
        sub_twin_type_model.pId
        
        

        response_json = rest_post(DTMS_TWINDEF_HOST, sub_twin_type_model.json())
        # 保存返回的消息
        # self.twin_type_infos[twin_model.code] = response
        return TwinTypeInResponse(**response_json)
    
    # 暂时不适合用
    def update_attributes_by_uuid(self, attributes : TwinAttributes):
        # TwinAttribute
        # •功能说明：根据definitionId修改definition信息
        # •参数说明：
        # /v1/{tenantId}/twins/definitions/{definitionId}/attributes
        # put
        url = path.join(DTMS_TWINDEF_HOST, attributes._id, attributes)
        response_json = rest_put(url, TwinAttributes.attributes.json())
        # 保存返回的消息
        # self.twin_type_infos[twin_model.code] = response
        return TwinTypeInResponse(**response_json)
    
    def where(self, **kwargs):
        print(kwargs)
        self.query.filter(**kwargs)
        return self

    def find(self, **kwargs):
        if kwargs: self.query.filter(**kwargs)
        print(self.query.query_condition)
        url = DTMS_TWINDEF_HOST
        if "id" in self.query.query_condition.keys():
            url = path.join(DTMS_TWINDEF_HOST, str(self.query.query_condition["id"]))
            print(url)
        response_json = rest_get(url, self.query.query_condition)
        self.query.empty()
        return response_json
    
    def categories(self, category:str):
        
        """_summary_
            功能说明：根据category和twinType查询指定的definition信息
            /v1/{tenantId}/twins/definitions/categories/{categoryType}
            
            例子：twin_client.twin_definition.categories("people_cates")
        Returns:
            _type_: _description_
        """
        url = path.join(DTMS_TWINDEF_HOST, "categories", category)
        response_json = rest_get(url)
        # 保存返回的消息
        # self.twin_type_infos[twin_model.code] = response
        return response_json
    
    def get_twin_definitions(self, query=None):
        """_summary_
            通过 twin_type = code 的所有twin_sub_type
            /v1/{{tenantId}}/twins/definitions?twinType=people_twin
        Args:
            query (json object): _description_ 如 {"twinType": code}
        """
        response_json = rest_get(DTMS_TWINDEF_HOST, query)
        # 保存返回的消息
        # self.twin_type_infos[twin_model.code] = response
        return response_json
    
    def get_twin_definition_by_id(self, id):
        """_summary_
            创建返回的id
        Args:
            id (str): _description_
        """
        return self.where({"id": id}).find()
        # response_json = rest_get(DTMS_TWINDEF_HOST, {"twinType": code})
        # # 保存返回的消息
        # # self.twin_type_infos[twin_model.code] = response
        # return response_json
    
    def get_twin_definitions_by_twin_type_code(self, code: str):
        """_summary_
            通过 twin_type = code 的所有twin_sub_type
            /v1/{{tenantId}}/twins/definitions?twinType=people_twin
        Args:
            code (str): _description_
        """
        response_json = rest_get(DTMS_TWINDEF_HOST, {"twinType": code})
        # 保存返回的消息
        # self.twin_type_infos[twin_model.code] = response
        return response_json

    def get_twin_definitions_by_twin_type_and_category(self, category:str, twin_type: str):
        
        """_summary_
            功能说明：根据category和twinType查询指定的definition信息
            /v1/{tenantId}/twins/definitions/categories/{category}/types/{twinType}
        Returns:
            _type_: _description_
        """
        url = path.join(DTMS_TWINDEF_HOST, "categories", category, "types", twin_type)
        response_json = rest_get(url)
        # 保存返回的消息
        # self.twin_type_infos[twin_model.code] = response
        return response_json

    def get_twin_definitions_by_twin_category(self, category:str):
        
        """_summary_
            功能说明：根据category和twinType查询指定的definition信息
            /v1/{tenantId}/twins/definitions/categories/{categoryType}
        Returns:
            _type_: _description_
        """
        return self.categories(category)
        
    def update_sub_twin_instance(self, twin_infos: object):
        
        # assert twin_model.asset_type == AssetTypeEnum.twin_type
        # print(sub_twin_type_model.json())
        # twin_infos json 通过查询获取
        # twin_infos 样例数据
        # {
        #     "data": {
        #         "auto": false,
        #         "data_test": "test"
        #         "_id": uuid,
        #     }
        # }
        url = path.join(DTMS_TWINDEF_HOST, twin_infos["data"]["_id"])
        response = rest_put(url, twin_infos)
        # 保存返回的消息
        # self.twin_type_infos[twin_model.code] = response
        return response
    
    
    # {{dtmstwin}}/v1/wuhan/twins/{{twinId}}
    # def create_twin_subtype(self, asset_model: AssetTwinSubtypeModel):
    #     """
    #     第三步创建 twin_subtype
    #     注意：定义twin_subtype的时候，需要一个pid指定上级目录的code，比如父节点code=people_twin
    #     """
    #     assert asset_model.asset_type == AssetTypeEnum.twin_subtype
        
    #     parent_asset = self.get_asset_by_code(asset_model.pid)
    #     if parent_asset["code"] == 200 and ["total"] == 0:
    #         print("parent_asset:-----", parent_asset)
    #         return {'message': '查询不到pid 资产 !'}
    #     response = rest_post(DTMS_REGISTER_HOST, asset_model.json())
    #     # response 包含 _id 字段 (for create asset relation)
    #     # 保存返回的消息
    #     self.twin_type_infos[asset_model.code] = response
    #     return response
        
    
    # def create_asset_relation(self, asset_relation_model: AssetRelationModel):
    #     """
    #     第四步创建 关系
    #     """
    #     try:
    #         from_asset_version= uuid.UUID(asset_relation_model.from_asset).version
    #         to_asset_version= uuid.UUID(asset_relation_model.to_asset).version
    #         # 判断版本一致
    #         assert from_asset_version == to_asset_version
    #     except Exception as e:
    #         print("Error: create asset relation {} ({}) error; error code: {}".format(asset_relation_model.from_asset, asset_relation_model.to_asset, e))
    #         return
    #     response = rest_post(DTMS_REGISTER_RELATION_HOST, asset_relation_model.json())
    #     # 保存返回的消息
    #     # self.twin_relation_infos[asset_relation_model.code] = response
    #     return response
        
        
    # def get_asset_by_code(self, code :str):
    #     """_summary_
    #     eg: {{dtmsregistry}}/{{tenantId}}/asset?code=people_cates
    #     Args:
    #         code (_type_): _description_
    #     Returns:
    #         _type_: _description_
    #         {"owner": "dtostwin", "code": "people_cates", "asset_type": "twin_category", "name": "\u4eba\u5458\u7c7b\u522b", "extension_value": {}, "create_user": "registry", "version": "1.0.0", "status": "valid"}
    #     """
    #     response = rest_get(DTMS_REGISTER_HOST, {"code": code})
    #     return response
    
    # def get_asset_by_params(self, params :object):
    #     """_summary_
    #     eg:     asset?code=people_cates
    #             asset?extension_value.developer=liangshihua
                
    #     Args:
    #         params (json): 要查询的字段
    #     Returns:
    #         _type_: _description_
    #         {"owner": "dtostwin", "code": "people_cates", "asset_type": "twin_category", "name": "\u4eba\u5458\u7c7b\u522b", "extension_value": {}, "create_user": "registry", "version": "1.0.0", "status": "valid"}
    #     """
    #     response = rest_get(DTMS_REGISTER_HOST, params)
    #     return response
    
    # def delect_asset_by_id(self, asset_uuid:str):
    #     """
    #     删除资产
    #     Args:
    #         asset_uuid (str): 资产id uuid 类型
    #     """
    #     # {{dtmsregistry}}/{{tenantId}}/asset/asset_uuid
        
    #     try:
    #         uuid.UUID(asset_uuid).version
    #         # 判断版本一致
    #     except Exception as e:
    #         print("Error:  error; error code: {}".format(e))
    #         return
    #     response = rest_delete(DTMS_REGISTER_HOST+'/'+ asset_uuid)
    #     # TODO 删除对应的资产
    #     print("删除资产成功 ", "asset_uuid:", asset_uuid)
    #     return response
    

    # def create_assets(self, asset_models: List[AssetTypeModel]):
    #     """
    #     批量创建资产
    #     Args:
    #         asset_models (List[AssetTypeModel]): _description_
    #     """
    #     res = []
    #     for asset_model in asset_models:
    #         res.append(getattr(self, asset_model.asset_type)(asset_model))
