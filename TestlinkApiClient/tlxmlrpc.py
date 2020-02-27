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
        self.client = ServerProxy(self.url).tl
        tl_about = self.client.about()
        print(tl_about)
        print(self.client.ping())
        dev_key_valid = self.client.checkDevKey(self.dev_key)
        assert dev_key_valid is True, dev_key_valid[0].get('message')
        user_valid = self.client.doesUserExist({'devKey': dev_key, 'user': user})
        assert user_valid is True, user_valid[0].get('message')
        self.step_template = {
            'step_number': '1',
            'actions': 'step#1',
            'expected_results': 'result#1',
            'execution_type': '1'  # Manual
        }

    @staticmethod
    def _check_results(rsp_results):
        if isinstance(rsp_results, list) and len(rsp_results) == 1 and rsp_results[0].get('code'):
            raise Exception(rsp_results[0])

    def _create_project(self, project_name: str, prefix=None):
        """
        tl.createTestProject
        :param project_name:
        :param prefix:
        :return:
        """
        param = self.dev_key.copy()
        param['testprojectname'] = project_name
        param['testcaseprefix'] = prefix if prefix else project_name
        results = self.client.createTestProject(param)
        self._check_results(results)
        return results

    def _get_projects(self):
        """
        tl.getProjects
        :return:
        """
        param = self.dev_key.copy()
        results = self.client.getProjects(param)
        self._check_results(results)
        return results

    def _get_project_by_name(self, project_name: str):
        """
        tl.getTestProjectByName
        :param project_name:
        :return:
        """
        param = self.dev_key.copy()
        param['testprojectname'] = project_name
        results = self.client.getTestProjectByName(param)
        self._check_results(results)
        return results

    def _get_project_id(self, project_name: str):
        return self._get_project_by_name(project_name).get('id')

    def _get_project_prefix(self, project_name: str):
        return self._get_project_by_name(project_name).get('prefix')

    def _get_project_test_plans(self, project_name: str):
        """
        tl.getProjectTestPlans
        :param project_name:
        :return:
        """
        param = self.dev_key.copy()
        param['testprojectid'] = self._get_project_id(project_name)
        results = self.client.getProjectTestPlans(param)
        self._check_results(results)
        return results

    def _get_plan_by_name(self, project_name: str, plan_name: str):
        """
        tl.getTestPlanByName
        :param project_name:
        :param plan_name:
        :return:
        """
        param = self.dev_key.copy()
        param['testprojectname'] = project_name
        param['testplanname'] = plan_name
        results = self.client.getTestPlanByName(param)
        self._check_results(results)
        return results

    def _get_test_plan_id(self, project_name: str, plan_name: str):
        results = self._get_plan_by_name(project_name, plan_name)
        if results.get('id'):
            return results.get('id')
        else:
            raise Exception('No test plan: %s in project: %s' % (plan_name, project_name))

    def _get_root_suites(self, project_name: str):
        """
        tl.getFirstLevelTestSuitesForTestProject
        :param project_name:
        :return:
        """
        param = self.dev_key.copy()
        param['testprojectid'] = self._get_project_id(project_name)
        results = self.client.getFirstLevelTestSuitesForTestProject(param)
        self._check_results(results)
        return results

    def _get_suites(self, project_name: str, suite_name: str, suite_id=None):
        """
        tl.getTestSuitesForTestSuite
        :param project_name:
        :param suite_name:
        :param suite_id:
        :return:
        """
        param = self.dev_key.copy()
        param['testprojectid'] = self._get_project_id(project_name)
        param['testsuiteid'] = suite_id if suite_id else self._get_suite_id(project_name, suite_name)
        results = self.client.getTestSuitesForTestSuite(param)
        self._check_results(results)
        return results

    def _get_suite(self, project_name: str, suite_name: str):
        """
        tl.getTestSuite
        :param project_name:
        :param suite_name:
        :return:
        """
        param = self.dev_key.copy()
        param['prefix'] = self._get_project_prefix(project_name)
        param['testsuitename'] = suite_name
        results = self.client.getTestSuite(param)
        self._check_results(results)
        return results

    def _get_suite_id(self, project_name, suite_name: str):
        results = self._get_suite(project_name, suite_name)
        if len(results) == 0:
            raise Exception('No suite: %s in project: %s' % (suite_name, project_name))
        elif len(results) == 1:
            return results[0].get('id')
        else:
            ids = list()
            for result in results:
                ids.append(result.get('id'))
            raise Exception('Find same name suites: %s %s in project: %s' % (suite_name, ids, project_name))

    def _create_suite(self, project_name: str, suite_name: str, parent_suite_name=None):
        """
        tl.createTestSuite
        :param project_name:
        :param suite_name:
        :param parent_suite_name:
        :return:
        """
        param = self.dev_key.copy()
        param['prefix'] = self._get_project_prefix(project_name)
        param['testsuitename'] = suite_name
        if parent_suite_name:
            param['parentid'] = self._get_suite_id(project_name, parent_suite_name)
        results = self.client.createTestSuite(param)
        self._check_results(results)
        return results

    def _get_test_cases(self, project_name: str, suite_name: str):
        """
        tl.getTestCasesForTestSuite
        :param project_name:
        :param suite_name:
        :return:
        """
        param = self.dev_key.copy()
        param['testsuiteid'] = self._get_suite_id(project_name, suite_name)
        return self.client.getTestCasesForTestSuite(param)

    def _create_test_case(self, project_name: str, suite_name: str, case_name: str,
                          summary='', steps='', suite_id=None):
        """
        tl.createTestCase
        :param project_name:
        :param suite_name:
        :param case_name:
        :param summary:
        :param steps:
        :param suite_id:
        :return:
        """
        param = self.dev_key.copy()
        param['testprojectid'] = self._get_project_id(project_name)
        param['testsuiteid'] = suite_id if suite_id else self._get_suite_id(project_name, suite_name)
        param['testcasename'] = case_name
        param['authorlogin'] = self.user
        param['summary'] = summary
        param['steps'] = steps
        results = self.client.createTestCase(param)
        self._check_results(results)
        return results

    def _update_test_steps(self, case_ext_id: str, steps):
        """
        tl.createTestCaseSteps
        :param case_ext_id:
        :param steps:
        :return:
        """
        param = self.dev_key.copy()
        param['action'] = 'update'
        param['testcaseexternalid'] = case_ext_id
        param['steps'] = steps
        results = self.client.createTestCaseSteps(param)
        self._check_results(results)
        return results

    def _get_last_execution_result(self, project_name: str, plan_name: str, case_ext_id: str):
        """
        tl.getLastExecutionResult
        :param project_name:
        :param plan_name:
        :param case_ext_id:
        :return:
        """
        param = self.dev_key.copy()
        param['testcaseexternalid'] = case_ext_id
        param['testplanid'] = self._get_test_plan_id(project_name, plan_name)
        results = self.client.getLastExecutionResult(param)
        self._check_results(results)
        return results

    def _set_case_execution_result(self, project_name: str, plan_name: str, build_name: str,
                                   case_ext_id: str, case_exe_result: str, notes=''):
        """
        tl.reportTCResult
        :param project_name:
        :param plan_name:
        :param build_name:
        :param case_ext_id:
        :param case_exe_result: p, f, b
        :param notes:
        :return:
        """
        param = self.dev_key.copy()
        param['testplanid'] = self._get_test_plan_id(project_name, plan_name)
        param['buildname'] = build_name
        param['testcaseexternalid'] = case_ext_id
        param['status'] = case_exe_result
        param['notes'] = notes
        results = self.client.reportTCResult(param)
        self._check_results(results)
        return results

    # Project Operations
    def list_project(self):
        names = list()
        for project in self._get_projects():
            names.append(project.get('name'))
        return names

    # def get_project(self):
    #     pass

    def create_project(self, project_name: str, prefix=None):
        return self._create_project(project_name, prefix)[0].get('id')

    def delete_project(self, project_name: str):
        param = self.dev_key.copy()
        param['testprojectid'] = self._get_project_id(project_name)
        results = self.client.deleteTestProject(param)
        self._check_results(results)
        return results

    # Plan Operations
    def list_plan(self, project_name: str):
        names = list()
        for testplan in self._get_project_test_plans(project_name):
            names.append(testplan.get('name'))
        return names

    # def get_plan(self):
    #     pass
    #
    # def create_plan(self):
    #     pass
    #
    # def delete_plan(self):
    #     pass

    # Suite Operations
    def list_suite(self, project_name: str, suite_name=None, suite_id=None):
        names = list()
        if suite_name is None:
            for suite in self._get_root_suites(project_name):
                names.append(suite.get('name'))
        else:
            results = self._get_suites(project_name, suite_name, suite_id)
            for suite in results:
                names.append(results.get(suite).get('name'))
        return names

    def get_suite(self, project_name: str, suite_name: str):
        testcases = dict()
        for testcase in self._get_test_cases(project_name, suite_name):
            testcases[testcase.get('external_id')] = testcase.get('name')
        return testcases

    def create_suite(self, project_name: str, suite_name: str, parent_suite_name=None):
        return self._create_suite(project_name, suite_name, parent_suite_name)[0].get('id')

    # Case Operations
    def get_case(self, project_name: str, case_ext_id: str):
        param = self.dev_key.copy()
        param['testprojectid'] = self._get_project_id(project_name)
        param['testcaseexternalid'] = case_ext_id
        results = self.client.getTestCase(param)
        self._check_results(results)
        return results

    def create_case(self, project_name: str, suite_name: str, case_name: str,
                    summary='', steps='', suite_id=None):
        param = self.dev_key.copy()
        param['testprojectid'] = self._get_project_id(project_name)
        param['testsuiteid'] = suite_id if suite_id else self._get_suite_id(project_name, suite_name)
        param['testcasename'] = case_name
        param['authorlogin'] = self.user
        param['summary'] = summary
        param['steps'] = steps
        results = self.client.createTestCase(param)
        self._check_results(results)
        case_id = {
            'id': results[0]['additionalInfo']['id'],
            'external_id': results[0]['additionalInfo']['external_id'],
        }
        prefix = self._get_project_prefix(project_name)
        print('ID: %s | External ID: %s-%s | Case Title: %s'
              % (case_id['id'], prefix, case_id['external_id'], case_name))
        return case_id

    def update_step(self, case_ext_id: str, steps):
        return self._update_test_steps(case_ext_id, steps).get('feedback')

    def set_execution_result(self, project_name: str, plan_name: str, build_name: str,
                             case_ext_id: str, case_exe_result: str, notes=''):
        if case_exe_result.lower() in ['p', 'pass', 'passed']:
            case_exe_result = 'p'
        elif case_exe_result.lower() in ['f', 'fail', 'failed']:
            case_exe_result = 'f'
        elif case_exe_result.lower() in ['b', 'block', 'blocked']:
            case_exe_result = 'b'
        rc_result = self._set_case_execution_result(project_name, plan_name, build_name,
                                                    case_ext_id, case_exe_result, notes)
        return rc_result[0].get('message')

    def get_last_execution_result(self, project_name: str, plan_name: str, case_ext_id: str):
        exe_result = self._get_last_execution_result(project_name, plan_name, case_ext_id)[0].get('status')
        if exe_result is True:
            return 'notrun'
        elif exe_result == 'f':
            return 'fail'
        elif exe_result == 'p':
            return 'pass'
        elif exe_result == 'b':
            return 'block'


if __name__ == '__main__':
    print('This is TestLink XML-RPC client')
