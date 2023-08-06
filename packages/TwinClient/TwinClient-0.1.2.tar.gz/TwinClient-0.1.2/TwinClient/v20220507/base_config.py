#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------------
# Descripttion: https://github.com/sxhxliang
# version: 0.0.1
# Author: Shihua Liang (sxhx.liang@gmail.com)
# FilePath: /05 代码/Users/shihua/Documents/武汉东西湖社会治理指挥中心/04接口文档/01孪生体创建/python-sdk/TwinClient/v20220507/base_config.py
# Create: 2022-05-07 12:57:40
# LastAuthor: Please set LastEditors
# lastTime: 2022-05-12 16:58:19
# --------------------------------------------------------

from ast import Pass
import json
import requests


TENANT_ID = "dongxihu"
DATA_VERSION = "1.0.0"
DTMS_REGISTER = "http://dtosregistry-dtmsregistry.dit.dtos.city"
DTMS_TWINDEF = "http://dtostwin-dtmstwindef2.dit.dtos.city"
DTMS_TWIN = "http://dtostwin-dtmstwin2.dit.dtos.city"


# # {{dtmsregistry}}/{{tenantId}}/asset
# DTMS_REGISTER_HOST = "{}/{}/asset"
# # {{dtmstwindef}}/v1/{{tenantId}}/twins/definitions
# DTMS_TWINDEF_HOST = "{}/v1/{}/twins/definitions"
# # {{dtmstwin}}/v1/wuhan/twins
# DTMS_TWIN_HOST = "{}/v1/wuhan/twins"

# 默认 接口地址
# {{dtmsregistry}}/{{tenantId}}/asset
DTMS_REGISTER_HOST = "{}/{}/asset".format(DTMS_REGISTER, TENANT_ID)
# {{dtmsregistry}}/{{tenantId}}/relation
DTMS_REGISTER_RELATION_HOST = "{}/{}/relation".format(DTMS_REGISTER, TENANT_ID)
# {{dtmstwindef}}/v1/{{tenantId}}/twins/definitions
DTMS_TWINDEF_HOST = "{}/v1/{}/twins/definitions".format(DTMS_TWINDEF, TENANT_ID)
# {{dtmstwin}}/v1/wuhan/twins
DTMS_TWIN_HOST = "{}/v1/{}/twins".format(DTMS_TWIN, TENANT_ID)

# /v1/{tenantId}/twins/definitions POST {definition} {id:xxx,status:200}
# •功能说明：新增definition定义
# •参数说明：
# /v1/{tenantId}/twins/definitions/{definitionId}
# PUT

# {definition}
# {id:xxx,status:200}
# •功能说明：根据definitionId修改definition信息
# •参数说明：
# /v1/{tenantId}/twins/definitions/{definitionId}/attributes
# put

# {definition}全量

# {id:xxx,status:200}
# •功能说明：修改制定definition的attributes属性
# •参数说明：data为全量的definitionbody
# /v1/{tenantId}/twins/definitions
# GET
# 见P18

# {data:[{definition}],
# status: 200,total:}
# •功能说明：查询definition列表
# •参数说明：
# /v1/{tenantId}/twins/definitions/{definitionId}
# GET


# {data: {definition},
# status: 200}
# •功能说明：根据definitionId查询definition信息
# •参数说明：
# /v1/{tenantId}/twins/definitions/categories/{category}/types/{twinType}
# GET


# {data:[{definition}], status:200,total:}
# •功能说明：根据category和twinType查询指定的definition信息
# •参数说明：
# /v1/{tenantId}/twins/definitions/categories/{categoryType}
# GET


# {status:200,
# data:[{definition}],
# total:}
# •功能说明：根据category查询definitions信息
# •参数说明：
# /v1/{tenantId}/twins/definitions/schema/system
# GET


# {schema}
# •功能说明：查询definition json schema定义
# •参数说明：
# /v1/{tenantId}/twins/definitions/{definitionId}
# DELETE


# {status:200}
# •功能说明：根据definitionId删除definition信息
# •参数说明：
# /v1/{tenantId}/twins/definitions/{definitionId}/groups
# GET


# {status:200,data:[string]}
# •功能说明：根据definitionId查询definition中attributes定义的所有group信息，返回字符串array
# •参数说明：



class TwinClientConfig():
    """docstring for TwinClientConfig
        tenantId = "wuhan"
        dtmsregistry = "http://dtosregistry-dtmsregistry.dit.dtos.city"
        dtmstwindef = "http://dtostwin-dtmstwindef2.dit.dtos.city"
        dtmstwin = "http://dtostwin-dtmstwin2.dit.dtos.city"

    """
    def __init__(self, 
                owner=None,
                tenantId=TENANT_ID, 
                dtmsregistry=DTMS_REGISTER,
                dtmstwin=DTMS_TWIN,
                dtmstwindef=DTMS_TWINDEF,
                version = DATA_VERSION):
        """_summary_
            初始化租户和接口地址
        Args:
            owner (str): 拥有者
            tenantId (str): 租户
            dtmsregistry (str): 资产注册接口地址
            dtmstwin (str): 孪生接口地址
            dtmstwindef (str): 孪生体定义接口地址
            version (str): 数据版本
        """

        self.owner = owner

        self.update_host(tenantId, dtmsregistry, dtmstwin, dtmstwindef)
        self.version = version
        
    def get_host_v2(self):
        print("config init")
        # {{dtmsregistry}}/{{tenantId}}/asset
        self.dtms_registry_host = "{}/{}/asset".format(self.dtmsregistry, self.tenantId)
        # {{dtmsregistry}}/{{tenantId}}/relation
        self.dtms_registry_relation_host = "{}/{}/relation".format(self.dtmsregistry, self.tenantId)
        # {{dtmstwindef}}/v1/{{tenantId}}/twins/definitions
        self.dtms_twin_def_host = "{}/v1/{}/twins/definitions".format(self.dtmstwindef, self.tenantId)
        # {{dtmstwin}}/v1/wuhan/twins
        self.dtms_twin_host = "{}/v1/{}/twins".format(self.dtmstwin, self.tenantId)
    
    def print_config(self):
        print("tenantId:\n          ", self.tenantId)
        print("dtmstwindef:\n           ", self.dtmstwindef)
        print("dtmsregistry:\n          ", self.dtmsregistry)
        print("dtmsrelation:\n          ", self.dtmsrelation)
        print("dtmstwin:\n          ", self.dtmstwin)
        # 
        print("dtms_registry_host:\n          ", self.dtms_registry_host)
        print("dtms_registry_relation_host:\n          ",self.dtms_registry_relation_host)
        print("dtms_twin_def_host:\n          ",self.dtms_twin_def_host)
        print("dtms_twin_host:\n          ",self.dtms_twin_host)

    def update_host(self, tenantId, dtmsregistry, dtmstwin, dtmstwindef):
        """_summary_
            更新租户和接口地址
        Args:
            tenantId (str): 租户
            dtmsregistry (str): 资产注册接口地址
            dtmstwin (str): 孪生接口地址
            dtmstwindef (str): 孪生体定义接口地址
        """
        self.tenantId = tenantId
        self.dtmsregistry = dtmsregistry
        self.dtmsrelation = "{}/{}/relation".format(dtmsregistry, tenantId)
        self.dtmstwindef = dtmstwindef
        self.dtmstwin = dtmstwin
        self.get_host_v2()
    

def rest_post(url: str, data: object):
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=data, headers=headers)
    # print("======== post ========")
    # print(response.text+"\n")
    try:
        return json.loads(response.text)
    except:
        pass
        # print('except:')
    finally:
        # print('finally     ')
        pass

    return response.text

def rest_put(url: str, data):
    headers = {'Content-type': 'application/json'}
    response = requests.put(url, json=data, headers=headers)
    # print("======== post ========")
    # print(response.text+"\n")
    try:
        return json.loads(response.text)
    except:
        pass
        # print('except:')
    finally:
        # print('finally     ')
        pass

    return response.text

def rest_delete(url):
    headers = {'Content-type': 'application/json'}
    response = requests.delete(url, headers=headers)
    # print("======== delete ========")
    # print(response.text+"\n")
    try:
        return json.loads(response.text)
    except:
        pass
        # print('except:')
    finally:
        # print('finally     ')
        pass

    return response.text



def rest_get(url, params=None):
    # print(url, params)
    response = requests.get(url, params)
    # print("======== get ========")
    # print("======== get ========", response.text+"\n")
    try:
        return json.loads(response.text)
    except:
        pass
        # print('except:')
    finally:
        # print('finally     ')
        pass

    return response.text



class QueryWhere():
    def __init__(self):
        self.query_condition = {}

    def filter(self, **kwargs):
        self.query_condition.update(kwargs)
        return self
    
    def empty(self):
        self.query_condition = {}