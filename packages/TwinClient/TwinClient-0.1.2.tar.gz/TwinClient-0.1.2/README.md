# twin client python-sdk

### install

```bash
pip3 install TwinClient
```


## demo

```python

config = TwinClientConfig(
                    owner = "dtos",
                    tenantId=tenantId,
                    dtmsregistry=dtmsregistry,
                    dtmstwindef=dtmstwindef,
                    dtmstwin=dtmstwin
                )

twin_client = TwinClient(config)

   # 查询 subtype
query = {
    "subType.type": "people_drug"
}
# "-created"    按created降序
# "created"     按created升序
res = twin_client.twin.where(**query).offset(0).limit(10).sort("-created").select()
print(res)

```
