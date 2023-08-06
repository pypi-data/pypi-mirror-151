#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------------
# Descripttion: https://github.com/sxhxliang
# version: 0.0.1
# Author: Shihua Liang (sxhx.liang@gmail.com)
# FilePath: /01孪生体创建/python-sdk/TwinClient/v20220501/schema.py
# Create: 2022-05-05 16:40:02
# LastAuthor: Please set LastEditors
# lastTime: 2022-05-09 10:41:17
# --------------------------------------------------------

from typing import Optional, List
from enum import Enum
from xmlrpc.client import boolean

from pydantic import BaseModel



# ===================== 资产 模型  ===================== 

class AssetTypeEnum(str, Enum):
    twin_category = "twin_category" # 一级
    twin_type = "twin_type"         # 二级
    twin_subtype = "twin_subtype"   # 三级 具体 实例化 twin
    

# 强制要求扩展数据
class AssetExtensionValue(BaseModel):
    tenant: str
    developer: str

class AssetTypeModel(BaseModel):
    """_summary_
        "owner": "dtostwin",             // 
        "code": "people_cates",          // code 是唯一的，相当于数据库的主键，通过{{dtmsregistry}}/{{tenantId}}/asset?code=people_cates查询
        "asset_type": "twin_category",   // 这资产类型是 twin_category，相当于一级目录节点，
        "name": "人员类别",               // name 是用来 展示的 可以中文或者英文
        "extension_value": {
        },                               // 扩展一些实际还需要的参数，key-value 模式，注意，目前强制要求扩展数据
        "create_user": "registry",       // 自定义版本
        "version": "1.0.0",              //自定义版本 such as 1.0.0, 1.0.1, 1.0.1, 1.2.0
        "status": "valid"
    """
    owner: str                          # 
    code: str                           # code 是唯一的，相当于数据库的主键，通过{{dtmsregistry}}/{{tenantId}}/asset?code=people_cates查询
    asset_type: AssetTypeEnum           # 这资产类型是 twin_category，相当于一级目录节点，
    name: str                           # name 是用来 展示的 可以中文或者英文
    extension_value: Optional[AssetExtensionValue]      # 扩展一些实际还需要的参数，key-value 模式
    create_user: Optional[str]          
    version: Optional[str]              # 自定义版本
    status: Optional[str] = "valid"

class AssetTwinSubtypeModel(AssetTypeModel):
    r"""
    注意：定义twin_subtype的时候，需要一个pid指定上级目录的code，比如父节点code=people_twin
    """
    pid: str
    
class AssetRelationModel(BaseModel):
    r"""
    定义资产关系
    {
        "name":"people_attachment",
        "from_asset": "e3c9cc62-38fb-4049-8de2-3cc8f4e249fb", 子 uuid
        "to_asset": "bc1f100e-b648-4197-b2f2-da0d428c3c92", 父 uuid
        "type": "attachment" 
    }
    """
    name: str
    from_asset: str
    to_asset: str
    type: str
    
class AssetRelationInResponseModel(BaseModel):
    r"""
        {
            "from_asset": "b8487bfb-4534-48db-8171-0e94cd6d2be3",
            "name": "dxh_people_attachment",
            "to_asset": "3b69783c-48ef-4fcf-909d-33d7423a95d1",
            "create_user": "registry",
            "type": "attachment",
            "tenant": "wuhan",
            "create_time": "2022-04-24 17:17:50",
            "_id": "a20dc2ab-57f7-488b-b546-263da6028983"
        }
    """
    from_asset: str
    name: str
    to_asset: str
    create_user: str
    type: str
    tenant: str
    create_time: str
    _id: str
            
# ===================== twin 模型  ===================== 

class TwinAttribute(BaseModel):
    displayName: str
    index: str
    type: str
    required: boolean
    name: str
    layerVisible: boolean 
    desc: Optional[str]
    default: Optional[str]
    
class TwinAttributes(BaseModel):
    _id: str
    attributes: List[TwinAttribute]
    
class TwinTypeModel(BaseModel):
    """_summary_
    "featureStoreType": "kairosDB",
    "featuresAdditions": true,
    "attributesAddition": false,
    "command": [],
    "features": [],
    "category": "people_cates",
    "twinType": "people_twin",
    "name": "人员类别-自然人模型",
    "attributes":[
        {
            "displayName": "姓名",
            "index": true,
            "type": "text",
            "required": true,
            "name": "fullname",
            "layerVisible":true,
            "desc": "姓名",
            "default":""
        },{
            "displayName": "年龄",
            "index": true,
            "type": "text",
            "required": false,
            "name": "age",
            "layerVisible":true,
            "desc": "年龄",
            "default":""
        }],
    "actions": [],
    "desc": "人员类别-自然人模型",
    "tenant":"wuhan",
    "version":"1.0.0"
    """
    featureStoreType: str = "kairosDB"
    featuresAdditions: boolean = True
    attributesAddition: boolean = True
    command: List = []
    features: List = []  # 动态属性
    category: str       # 动态属性
    twinType: str
    pId: Optional[str]             # subTwinType 需要
    subTwinType: Optional[str]     # subTwinType 需要
    name: str
    attributes: List[TwinAttribute]
    actions: List
    desc: str
    tenant: str
    version: str
 
class SubTwinTypeModel(TwinTypeModel):
    """_summary_
    
        吸毒人 pid 
        "pId":"1650799384972",        // 必须 这个 pId 是 定义 twin_type（人员模型）模型的返回的 id
        "category": "people_cates",   // 必须 类别资产
        "twinType": "people_twin",    // 必须 孪生体
        "subTwinType": "people_drug", // 必须 子孪生体
        
        "attributes":[
            {
                "displayName": "初次发现日期",
                "index": true,
                "type": "text",
                "required": false,
                "name": "first_discovery_at",
                "layerVisible":true,
                "desc": "初次发现日期",
                "default":"0"
            },{
                "displayName": "管控情况",
                "index": true,
                "type": "text",
                "required": false,
                "name": "managed_status",
                "layerVisible":true,
                "desc": "管控情况",
                "default":"0"
            }
        ]
    Args:
        TwinTypeModel (_type_): _description_
    """
    pId: str
    subTwinType: str

class TwinTypeInResponse(BaseModel):
    """_summary_
    {
        "id": "1650799384972",
        "message": "Init Definition Success",
        "status": 200
    }
    Args:
        TwinTypeModel (_type_): _description_
    """
    id: str
    message: str
    status: int
    
class Twin(BaseModel):
    """_summary_
        用于保存 twin 数据
    Args:
        BaseModel (_type_): _description_
    """
    id: str
    data: Optional[object]