#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xmlrpc.client import ServerProxy


class TestlinkClient(object):
    def __init__(self, url: str, user: str, dev_key: str):
        self.url = url + '/lib/api/xmlrpc/v1/xmlrpc.php'
        self.user = user
        self.dev_key = {
            'devKey': dev_key
        }
        self.client = ServerProxy(self.url)
        tl_about = self.client.tl.about()
        print(tl_about)
        print(self.client.tl.ping())
        self.client.tl.checkDevKey(self.dev_key)
        self.step_template = {
            'step_number': '1',
            'actions': 'step#1',
            'expected_results': 'result#1',
            'execution_type': '1'  # Manual
        }

    @staticmethod
    def _check_results(rsp_results):
        if isinstance(rsp_results, list) and rsp_results[0].get('code'):
            raise Exception(rsp_results[0])

    def _get_projects(self):
        param = self.dev_key.copy()
        results = self.client.tl.getProjects(param)
        self._check_results(results)
        return results

    def list_project(self):
        names = list()
        for project in self._get_projects():
            names.append(project.get('name'))
        return names

    def _get_project_id(self, project_name: str):
        param = self.dev_key.copy()
        param['testprojectname'] = project_name
        results = self.client.tl.getTestProjectByName(param).get('id')
        self._check_results(results)
        return results

    def _get_project_prefix(self, project_name: str):
        param = self.dev_key.copy()
        param['testprojectname'] = project_name
        return self.client.tl.getTestProjectByName(param).get('prefix')

    def _get_project_test_plans(self, project_name: str):
        param = self.dev_key.copy()
        param['testprojectid'] = self._get_project_id(project_name)
        results = self.client.tl.getProjectTestPlans(param)
        self._check_results(results)
        return results

    def list_project_test_plan(self, project_name: str):
        names = list()
        for testplan in self._get_project_test_plans(project_name):
            names.append(testplan.get('name'))
        return names

    def _get_test_plan_id(self, project_name: str, testplan_name: str):
        param = self.dev_key.copy()
        param['testprojectname'] = project_name
        param['testplanname'] = testplan_name
        results = self.client.tl.getTestPlanByName(param).get('id')
        self._check_results(results)
        return results

    def _get_root_suites(self, project_name: str):
        param = self.dev_key.copy()
        param['testprojectid'] = self._get_project_id(project_name)
        results = self.client.tl.getFirstLevelTestSuitesForTestProject(param)
        self._check_results(results)
        return results

    def _get_suites(self, project_name: str, suite_name: str):
        param = self.dev_key.copy()
        param['testprojectid'] = self._get_project_id(project_name)
        param['testsuiteid'] = self._get_suite_id(project_name, suite_name)
        return self.client.tl.getTestSuitesForTestSuite(param)

    def list_suite(self, project_name: str, suite_name=None):
        names = list()
        if suite_name is None:
            for suite in self._get_root_suites(project_name):
                names.append(suite.get('name'))
        else:
            for suite in self._get_suites(project_name, suite_name):
                names.append(suite.get('name'))
        return names

    def _get_suite_id(self, project_name, suite_name: str):
        param = self.dev_key.copy()
        param['prefix'] = self._get_project_prefix(project_name)
        param['testsuitename'] = suite_name
        results = self.client.tl.getTestSuite(param)[0].get('id')
        self._check_results(results)
        return results

    def _get_test_cases(self, project_name: str, suite_name: str):
        param = self.dev_key.copy()
        param['testsuiteid'] = self._get_suite_id(project_name, suite_name)
        return self.client.tl.getTestCasesForTestSuite(param)

    def get_suite(self, project_name: str, suite_name: str):
        testcases = dict()
        for testcase in self._get_test_cases(project_name, suite_name):
            testcases[testcase.get('external_id')] = testcase.get('name')
        return testcases

    def get_test_case(self, project_name: str, testcase_ext_id: str):
        param = self.dev_key.copy()
        param['testprojectid'] = self._get_project_id(project_name)
        param['testcaseexternalid'] = testcase_ext_id
        return self.client.tl.getTestCase(param)

    def create_test_case(self, project_name: str, suite_name: str, testcase_name: str, summary='', steps=''):
        param = self.dev_key.copy()
        param['testprojectid'] = self._get_project_id(project_name)
        param['testsuiteid'] = self._get_suite_id(project_name, suite_name)
        param['testcasename'] = testcase_name
        param['authorlogin'] = self.user
        param['summary'] = summary
        param['steps'] = steps
        results = self.client.tl.createTestCase(param)
        self._check_results(results)
        return results

    def create_project(self, project_name: str, prefix=None):
        param = self.dev_key.copy()
        param['testprojectname'] = project_name
        param['testcaseprefix'] = prefix if prefix else project_name
        results = self.client.tl.createTestProject(param)
        self._check_results(results)
        return results[0].get('id')

    def delete_project(self, project_name: str):
        param = self.dev_key.copy()
        param['testprojectid'] = self._get_project_id(project_name)
        results = self.client.tl.deleteTestProject(param)
        self._check_results(results)
        return results
