from datetime import datetime

import testlink
from unittest import (
    TestCase,
    TestLoader,
    TextTestResult,
    TextTestRunner)
from pprint import pprint
import os

# import subprocess
from TestWebApp import *

# args = ["python", "test_module.py"]
# subprocess.call(args)
# tls.reportTCResult(a_TestCaseID, a_TestPlanID, 'a build name', 'f', 'some notes', user='a user login name', platformid=a_platformID)

# https://www.reddit.com/r/learnpython/comments/28eoz9/python_unittest_do_something_different_if_test/


# suite = unittest.TestLoader().loadTestsFromTestCase(MyTest)
# out = unittest.TextTestRunner(verbosity=2).run(suite)
# print (out)

OK = 'ok'
FAIL = 'fail'
ERROR = 'error'
SKIP = 'skip'


class JsonTestResult(TextTestResult):

    def __init__(self, stream, descriptions, verbosity):
        super_class = super(JsonTestResult, self)
        super_class.__init__(stream, descriptions, verbosity)

        # TextTestResult has no successes attr
        self.successes = []

    def addSuccess(self, test):
        # addSuccess do nothing, so we need to overwrite it.
        super(JsonTestResult, self).addSuccess(test)
        self.successes.append(test)

    def json_append(self, test, result, out):
        suite = test.__class__.__name__
        if suite not in out:
            out[suite] = {OK: [], FAIL: [], ERROR: [], SKIP: []}
        if result is OK:
            out[suite][OK].append(test._testMethodName)
        elif result is FAIL:
            out[suite][FAIL].append(test._testMethodName)
        elif result is ERROR:
            out[suite][ERROR].append(test._testMethodName)
        elif result is SKIP:
            out[suite][SKIP].append(test._testMethodName)
        else:
            raise KeyError("No such result: {}".format(result))
        return out

    def jsonify(self):
        json_out = dict()
        for t in self.successes:
            json_out = self.json_append(t, OK, json_out)

        for t, _ in self.failures:
            json_out = self.json_append(t, FAIL, json_out)

        for t, _ in self.errors:
            json_out = self.json_append(t, ERROR, json_out)

        for t, _ in self.skipped:
            json_out = self.json_append(t, SKIP, json_out)

        return json_out


if __name__ == '__main__':
    # redirector default output of unittest to /dev/null
    with open(os.devnull, 'w') as null_stream:
        # new a runner and overwrite resultclass of runner
        runner = TextTestRunner(stream=null_stream)
        runner.resultclass = JsonTestResult

        # create a testsuite
        suite = TestLoader().loadTestsFromTestCase(TestWebApp)

        # run the testsuite
        result = runner.run(suite)

        # print json output
        pprint(result.jsonify())

        passedTest = list(map(lambda test: test._testMethodName, result.successes))

        print(passedTest)
        if 'test_detectChangesInSortedHighest' in passedTest:
            resultTest = 'p'
        else:
            resultTest = 'f'

        tls = testlink.TestLinkHelper().connect(testlink.TestlinkAPIClient)

        tc_info = tls.getTestCase(None, testcaseexternalid='TA-6')
        print(tc_info)
        tc_info = tls.getProjectTestPlans('1')
        print(tc_info)
        # tls.reportTCResult(4, 2, 'SampleBuild', 'f', 'some notes', user='user', platformid='1')
        tls.reportTCResult(None, 2, None, resultTest, 'some notes', guess=True,
                           testcaseexternalid='TA-6',
                           platformname='platform',
                           execduration=3.9, timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"),
                           steps=[{'step_number': 1, 'result': resultTest, 'notes': 'result note for passed step 1'},{'step_number' : 2, 'result': 'p', 'notes': ''}])