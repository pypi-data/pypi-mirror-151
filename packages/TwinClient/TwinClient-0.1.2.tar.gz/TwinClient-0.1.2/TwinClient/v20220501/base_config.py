#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------------
# Descripttion: https://github.com/sxhxliang
# version: 0.0.1
# Author: Shihua Liang (sxhx.liang@gmail.com)
# FilePath: /01孪生体创建/python-sdk/TwinClient/v20220501/base_config.py
# Create: 2022-05-02 23:06:08
# LastAuthor: Please set LastEditors
# lastTime: 2022-05-09 10:41:10
# --------------------------------------------------------

from ast import Pass
import json
import requests


TENANT_ID = "dongxihu"
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



class TwinClientConfig(object):
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
                dtmstwindef=DTMS_TWINDEF):
        super(TwinClientConfig, self).__init__()

        self.owner = owner
        self.tenantId = tenantId
        self.dtmsregistry = dtmsregistry
        self.dtmstwindef = dtmstwindef
        self.dtmstwin = dtmstwin
        
    def get_host_v2(self):
        # {{dtmsregistry}}/{{tenantId}}/asset
        DTMS_REGISTER_HOST = "{}/{}/asset".format(self.dtmsregistry, self.tenantId)
        DTMS_REGISTER_RELATION_HOST = "{}/{}/relation".format(DTMS_REGISTER, TENANT_ID)
        # {{dtmstwindef}}/v1/{{tenantId}}/twins/definitions
        DTMS_TWINDEF_HOST = "{}/v1/{}/twins/definitions".format(self.dtmstwindef, self.tenantId)
        # {{dtmstwin}}/v1/wuhan/twins
        DTMS_TWIN_HOST = "{}/v1/wuhan/twins".format(self.dtmstwin)

    def update_host_version(self, info):
        pass
    

def rest_post(url: str, data: object):
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=data, headers=headers)
    print("======== post ========")
    print(response.text+"\n")
    try:
        return json.loads(response.text)
    except:
        pass
        # print('except:')
    finally:
        # print('finally     ')
        pass

    return response.text

def rest_put(url: str, data: object):
    headers = {'Content-type': 'application/json'}
    response = requests.put(url, data=data, headers=headers)
    print("======== post ========")
    print(response.text+"\n")
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
    print("======== delete ========")
    print(response.text+"\n")
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
    response = requests.get(url, params)
    # print("======== get ========")
    print(response.text+"\n")
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