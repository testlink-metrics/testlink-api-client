# testlink-api-client
[![org](https://img.shields.io/badge/org-truth%20%26%20insurance%20workshop-informational)](http://bx.baoxian-sz.com)
![author](https://img.shields.io/badge/author-v.stone@163.com-informational)
![github](https://img.shields.io/github/license/seoktaehyeon/testlink-api-client)
[![pypi](https://img.shields.io/pypi/v/TestlinkApiClient.svg)](https://pypi.org/project/TestlinkApiClient/)
[![ref](https://img.shields.io/badge/ref-testlink%20api%20xmlrpc-informational)](https://github.com/TestLinkOpenSourceTRMS/testlink-code/blob/testlink_1_9/lib/api/xmlrpc/v1/xmlrpc.class.php)

## XML-RPC Client For TestLink

##### Installation
```bash
#!/bin/bash
pip install TestlinkApiCLient
```
##### Usage
```python
#!/usr/bin/env python
from TestlinkApiClient.xmlrpc import TestlinkClient

# Connect Testlink
testlink = TestlinkClient(url='Testlink Access Url', user='Testlink Username', dev_key='Personal Api Key')

# List Project
testlink.list_project()

# List Test Plan of the project
testlink.list_project_test_plan(project_name='Project Name')

# List Suite of the project root path
testlink.list_suite(project_name='Project Name')

# List Suite of the suite
testlink.list_suite(project_name='Project Name', suite_name='Suite Name')

# List Test Case of the suite
testlink.get_suite(project_name='Project Name', suite_name='Suite Name')

# Get the Test Case
testlink.get_test_case(project_name='Project Name', testcase_ext_id='Testcase external ID')

# Create Project
testlink.create_project(project_name='Project Name')
testlink.create_project(project_name='Project Name', prefix='Prefix')

# Create a Test Case into the suite 
testlink.create_test_case(project_name='Project Name', suite_name='Suite Name', testcase_name='Test Case Title') 
testlink.create_test_case(project_name='Project Name', suite_name='Suite Name', testcase_name='Test Case Title', summary='Test Case Summary', steps='Test Case Steps')
## Steps is a list, every step format could find from testlink.step_template
```

## Rest Client For TestLink
In The Future
