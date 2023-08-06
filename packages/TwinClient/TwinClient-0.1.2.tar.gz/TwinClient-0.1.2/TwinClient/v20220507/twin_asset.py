#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------------
# Descripttion: https://github.com/sxhxliang
# version: 0.0.1
# Author: Shihua Liang (sxhx.liang@gmail.com)
# FilePath: /05 代码/Users/shihua/Documents/武汉东西湖社会治理指挥中心/04接口文档/01孪生体创建/python-sdk/TwinClient/v20220507/twin_asset.py
# Create: 2022-05-07 12:57:40
# LastAuthor: Please set LastEditors
# lastTime: 2022-05-12 09:56:04
# --------------------------------------------------------

from os import path
import uuid
from typing import List

from .base_config import (TwinClientConfig, rest_get, rest_post, rest_delete, QueryWhere)
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
        
        self.query = QueryWhere()
        # print(cfg.tenantId, cfg.dtmsregistry, cfg.dtmstwin, cfg.dtmstwindef)
        
    def create(self, asset_model: AssetTypeModel):
        """_summary_
            创建资产
        Args:
            asset_model (AssetTypeModel): _description_

        Returns:
            _type_: _description_
        """
        # pid 通过 relation 定义了
        # 注意：定义twin_subtype的时候，需要一个pid指定上级目录的code，比如父节点code=people_twin

        if hasattr(asset_model, "pid") and asset_model.pid is not None:
            asset = self.exist_asset(code=asset_model.pid)
            if not asset:
                return False
        return rest_post(self.cfg.dtms_registry_host, asset_model.json())

    
    def delete(self, asset_uuid: str):
        url = path.join(self.cfg.dtms_registry_host, asset_uuid)
        # print(url)
        return rest_delete(url)
        
    def where(self, **kwargs):
        self.query.filter(**kwargs)
        return self

    def where_extension(self, **kwargs):
        new_kwargs={}
        for k in kwargs:
            new_kwargs["extension_value."+k ] = kwargs[k]
        self.query.filter(**new_kwargs)
        return self
    
    def find(self, id=None):
        url = self.cfg.dtms_registry_host
        if id: url = path.join(url, id)
        print(url, self.query.query_condition)
        response_json = rest_get(url, self.query.query_condition)
        self.query.empty()
        return response_json
    
    def select(self):
        response_json = rest_get(self.cfg.dtms_registry_host, self.query.query_condition)
        self.query.empty()
        return response_json

    def exist_asset(self,  **kwargs):
        """_summary_
            校验asset是否存在
        Returns:
            _type_: _description_
        """
        # print("校验asset是否存在",  kwargs)
        assets = self.where( **kwargs).find()
        if assets['code'] == 200 and assets["total"] > 0:
            # print("存在pid")
            return assets
        return False
        
    def create_twin_category_asset(self, asset_model: AssetTypeModel):
        """
        第一步创建 twin_category
        """
        assert asset_model.asset_type == AssetTypeEnum.twin_category
        return self.create(asset_model)

    def create_twin_type_asset(self, asset_model: AssetTypeModel):
        """
        第二步创建 twin_type
        """
        assert asset_model.asset_type == AssetTypeEnum.twin_type
        return self.create(asset_model)

    def create_twin_subtype_asset(self, asset_model: AssetTwinSubtypeModel):
        """
        第三步创建 twin_subtype
        // 注意：定义twin_subtype的时候，需要一个pid指定上级目录的code，比如父节点code=people_twin
        """
        assert asset_model.asset_type == AssetTypeEnum.twin_subtype
        return self.create(asset_model)

    def create_relation(self, asset_relation_model: AssetRelationModel) -> AssetRelationInResponseModel:
        """
        第四步创建 关系
        """
        if self.exist_asset(_id=asset_relation_model.from_asset) and self.exist_asset(_id=asset_relation_model.to_asset):
            response = rest_post(self.cfg.dtms_registry_relation_host, asset_relation_model.json())
            # 保存返回的消息
            # self.twin_relation_infos[asset_relation_model.code] = response
            return response
            # return AssetRelationInResponseModel(**response)
        else:
            print("校验asset 不存在")
            return False
    
    def create_relation_by_code(self, asset_relation_model: AssetRelationModel):
        try:
            # code 转换成 uuid
            asset_relation_model.from_asset = self.get_uuid_by_code(asset_relation_model.from_asset)
            asset_relation_model.to_asset = self.get_uuid_by_code(asset_relation_model.to_asset)
        except Exception as e:
            print("Error: create asset relation {} ({}) error; error code: {}".format(asset_relation_model.from_asset, asset_relation_model.to_asset, e))
            return
        response = rest_post(self.cfg.dtms_registry_relation_host, asset_relation_model.json())
        # 保存返回的消息
        print(response)
        return response
        # self.twin_relation_infos[asset_relation_model.code] = response
        # return AssetRelationInResponseModel(**response)

    def get_asset_by_code(self, code :str):
        """_summary_
        eg: {{dtmsregistry}}/{{tenantId}}/asset?code=people_cates
        Args:
            code (_type_): _description_
        Returns:
            _type_: _description_
            {"owner": "dtostwin", "code": "people_cates", "asset_type": "twin_category", "name": "\u4eba\u5458\u7c7b\u522b", "extension_value": {}, "create_user": "registry", "version": "1.0.0", "status": "valid"}
        """
        assets = self.where(code=code).find()
        return assets
    
    def get_uuid_by_code(self, code):
        """_summary_
            uuid = twin_client.asset.get_uuid_by_code("people_twin")
        Args:
            code (str): _description_
        Returns:
            _type_: uuid or false
        """
        assets = self.where(code=code).find()
        if assets['code'] == 200 and assets["total"] > 0:
            return assets["data"][0]["_id"]
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
        return self.where(**params).find()
    
    def delete_asset_by_id(self, asset_uuid:str):
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
        return self.delete(asset_uuid)

    def create_assets(self, asset_models: List[AssetTypeModel]):
        """
        批量创建资产
        Args:
            asset_models (List[AssetTypeModel]): _description_
        """
        res = []
        for asset_model in asset_models:
            res.append(getattr(self, asset_model.asset_type)(asset_model))
    
    


