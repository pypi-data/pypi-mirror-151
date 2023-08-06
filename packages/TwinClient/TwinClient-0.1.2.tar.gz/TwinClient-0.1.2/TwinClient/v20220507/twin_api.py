#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------------
# Descripttion: https://github.com/sxhxliang
# version: 0.0.1
# Author: Shihua Liang (sxhx.liang@gmail.com)
# FilePath: /01孪生体创建/python-sdk/TwinClient/v20220507/twin_api.py
# Create: 2022-05-07 12:57:40
# LastAuthor: Please set LastEditors
# lastTime: 2022-05-09 16:16:34
# --------------------------------------------------------

import uuid
from os import path
from typing import List

from .base_config import (TwinClientConfig, rest_get, rest_post, rest_delete, rest_put, QueryWhere)

from .schema import (
            TwinBaseModel, TwinInstance,
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
        
        self.query = QueryWhere()
        
    def create(self, twin_data: TwinBaseModel):
        """_summary_
            创建孪生体实例
            {{dtmstwin}}/v1/{{tenantId}}/twins
            
            {   
                "name": "吸毒人员测试姓名2",
                "thing": "thing02",
                "category":"people_cates",
                "type":"people_twin",
                "subType":"people_drug",
                "definitionId":"1651910540710",
                "version": "1.0.0",
                "fullname": "thing02"
            }

        Args:
            twin_data (TwinBaseModel): _description_ 孪生体数据, 需要继承 TwinBaseModel
        """
        response = rest_post(self.cfg.dtms_twin_host, twin_data.json())
        return response

    def delete(self, id):
        """_summary_
            根据id 删除定义的 twin
            # {{dtmstwin}}/v1/{{tenantId}}/twins/{{twinId}}/1651907397272
        Args:
            id (_type_): _description_
        """
        
        url = path.join(self.cfg.dtms_twin_host, str(id))
        return rest_delete(url) 
    
    def find(self, uu_id: str)-> TwinInstance:
        """_summary_
            {{dtmstwin}}/v1/{{tenantId}}/twins/{{twinId}}
        Args:
            uu_id (str): _description_

        Returns:
            TwinInstance: _description_
        """
        uuid_version= uuid.UUID(uu_id).version
        if not uuid_version:
            print("请输入正确的 uuid" )
            return False
        
        response = rest_get(path.join(self.cfg.dtms_twin_host, uu_id))
        # 保存返回的消息
        # self.twin_type_infos[twin_model.code] = response
        return response
    
    def select(self):
        response_json = rest_get(self.cfg.dtms_twin_host, self.query.query_condition)
        self.query.empty()
        return response_json
    
    # def selectSubType(self):
    #     response_json = rest_get(self.cfg.dtms_twin_host, self.query.query_condition)
    #     self.query.empty()
    #     return response_json
    
    def where(self, **kwargs):
        self.query.filter(**kwargs)
        return self
        # pass
        # 样例：
        # /v1/twins?
        # from=1
        # &size=10
        # &tenant=XX
        # &name=reg(XX)
        # &twinType=XX
        # &sort=attr1,attr2,-attr3
        # &number=[xx,yy]
        # &attr=ne(null)
        # &dwithin=wgsLocation(lng,lat,min,max)
        # &intersects=wgsLocation(lng lat,lng1,lat1)
        
    def sort(self, key: str):
        """_summary_
            结果排序，关键字sort
            sort=-attrName1 含义 按attrName1 降序 
            sort=attrName1  含义 按attrName1 升序排列
            sort=attrName1,attrName2,-attrName3,…. 含义按多个字段排序
        Args:
            key (str): _description_

        Returns:
            _type_: _description_
        """
        sort_key = {"sort": key}
        self.query.filter(**sort_key)
        return self
    
    def offset(self, offset):
        offset = {"from": offset}
        self.query.filter(**offset)
        return self
        
    def limit(self, limit):
        self.query.filter(size=limit)
        return self
        
    def update(self, uu_id: str, data):
        """_summary_
            {{dtmstwin}}/v1/{{tenantId}}/twins/{{twinId}}
        Args:
            uu_id (str): _description_

        Returns:
            _type_: _description_
        """
        uuid_version= uuid.UUID(uu_id).version
        if not uuid_version:
            print("请输入正确的 uuid" )
            return False
        url = path.join(self.cfg.dtms_twin_host, uu_id)
        print(url, data)
        response = rest_put(url, data)
        # 保存返回的消息
        # self.twin_type_infos[twin_model.code] = response
        return response
    
    def update_twin_by_uuid(self, uu_id: str, data: object):
        return self.update(uu_id, data)
        
        
        
            
        

