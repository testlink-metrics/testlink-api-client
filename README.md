# testlink-api-client

## XML-RPC Client For TestLink
##### [testlink api xmlrpc ref doc](https://github.com/TestLinkOpenSourceTRMS/testlink-code/blob/testlink_1_9/lib/api/xmlrpc/v1/xmlrpc.class.php)
##### Installation
```bash
#!/bin/bash
pip install TestlinkApiCLient
```
##### Usage
```python
#!/usr/bin/env python
import TestlinkApiClient.xmlrpc import TestlinkClient

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

# Create a Test Case into the suite 
testlink.create_test_case(project_name='Project Name', suite_name='Suite Name', testcase_name='Test Case Title') 
testlink.create_test_case(project_name='Project Name', suite_name='Suite Name', testcase_name='Test Case Title', summary='Test Case Summary', steps='Test Case Steps')
## Steps is a list, every step format could find from testlink.step_template
```

## Rest Client For TestLink
In The Future
