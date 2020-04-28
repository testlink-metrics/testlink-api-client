# testlink-api-client
[![org](https://img.shields.io/static/v1?style=for-the-badge&label=org&message=Truth%20%26%20Insurance%20Workshop&color=597ed9)](http://bx.baoxian-sz.com)
![author](https://img.shields.io/static/v1?style=for-the-badge&label=author&message=v.stone@163.com&color=blue)
![github](https://img.shields.io/github/license/testlink-metrics/testlink-api-client?style=for-the-badge)
[![pypi](https://img.shields.io/pypi/v/TestlinkApiClient.svg?style=for-the-badge)](https://pypi.org/project/TestlinkApiClient/)
[![ref](https://img.shields.io/badge/ref-testlink%20api%20xmlrpc-informational?style=for-the-badge)](https://github.com/TestLinkOpenSourceTRMS/testlink-code/blob/testlink_1_9/lib/api/xmlrpc/v1/xmlrpc.class.php)

## XML-RPC Client For TestLink

#### Installation
```bash
#!/bin/bash
pip install TestlinkApiCLient
```
#### Example
```python
#!/usr/bin/env python
from TestlinkApiClient.xmlrpc import TestlinkClient

# Connect Testlink
testlink = TestlinkClient(url='Testlink Access Url', user='Testlink Username', dev_key='Personal Api Key')

# List Project
testlink.list_project()
```

#### Function List
- Project Operations
```python
testlink.list_project()
testlink.create_project(project_name='Project Name')
testlink.create_project(project_name='Project Name', prefix='Prefix')
testlink.delete_project(project_name='Project Name')
```
- Plan Operations
```python
testlink.list_plan(project_name='Project Name')
```
- Suite Operations
```python
testlink.list_suite(project_name='Project Name')
testlink.list_suite(project_name='Project Name', suite_name='Suite Name')
testlink.get_suite(project_name='Project Name', suite_name='Suite Name')
testlink.create_suite(project_name='Project Name', suite_name='Suite Name')
testlink.create_suite(project_name='Project Name', suite_name='Suite Name', parent_suite_name='Parent Suite Name')
```
- Case Operations
```python
testlink.get_case(project_name='Project Name', case_ext_id='Test Case External ID')
testlink.create_case(project_name='Project Name', suite_name='Suite Name', case_name='Test Case Title') 
testlink.create_case(project_name='Project Name', suite_name='Suite Name', case_name='Test Case Title', summary='Test Case Summary', steps='Test Case Steps')
testlink.update_step(case_ext_id='Test Case External ID', steps='Test Case Steps')
testlink.set_execution_result(project_name='Project Name', plan_name='Plan Name', build_name='Build Name', 
                              case_ext_id='Test Case External ID', case_exe_result='Execition Result')
testlink.set_execution_result(project_name='Project Name', plan_name='Plan Name', build_name='Build Name', 
                              case_ext_id='Test Case External ID', case_exe_result='Execution Result', 
                              notes='Execution Log or Notes')
testlink.get_last_execution_result(project_name='Project Name', plan_name='Plan Name', case_ext_id='Test Case External ID')
```

#### Parameters Description
- Test Case Steps
> Steps is a list, every step format could find from testlink.step_template
- Execution Result
> PASS: p, pass, passed <br>
> FAIL: f, fail, failed <br>
> BLOCK: b, block, blocked


## Rest Client For TestLink
In The Future
