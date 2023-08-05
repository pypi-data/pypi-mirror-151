from unittest import TextTestResult
from unittest.signals import registerResult
from . import utils_lib
import sys
import time
import warnings
import string
import os
from jinja2 import Template, FileSystemLoader, Environment, PackageLoader, select_autoescape


class Result:
    def __init__(self):
        self.total = 0
        self.pass_rate = 0
        self.case_pass = 0
        self.case_fail = 0
        self.case_skip = 0
        self.case_error = 0
        self.run_time = 0
        self.table_rows = []
        self.node_info = None

    def compute_totals(self):
        self.total = self.case_pass + self.case_error + self.case_fail + self.case_skip
        if self.total - self.case_skip > 0:
            self.pass_rate = self.case_pass / (self.total - self.case_skip) * 100


def generated_report(logfile, template_name, result):
    if os.path.exists(logfile):
        os.unlink(logfile)

    file_loader = PackageLoader("os_tests", "templates")
    env = Environment(loader=file_loader)
    template = env.get_template(template_name)
    output = template.render(result=result)
    with open(logfile, "w+") as fh:
        fh.write(output)
    print("{} generated".format(os.path.realpath(logfile)))


class _WritelnDecorator(object):
    """Used to decorate file-like objects with a handy 'writeln' method"""
    def __init__(self,stream):
        self.stream = stream

    def __getattr__(self, attr):
        if attr in ('stream', '__getstate__'):
            raise AttributeError(attr)
        return getattr(self.stream,attr)

    def writeln(self, arg=None):
        if arg:
            self.write(arg)
        self.write('\n') # text-mode streams translate to \r\n if needed

class HTMLTestRunner(object):
    """A test runner class that displays results in textual form.

    It prints out the names of tests as they are run, errors as they
    occur, and a summary of the results at the end of the test run.
    """
    resultclass = TextTestResult

    def __init__(self, stream=None, descriptions=True, verbosity=1,
                 failfast=False, buffer=False, resultclass=None, warnings=None,
                 *, tb_locals=False):
        """Construct a TextTestRunner.

        Subclasses should accept **kwargs to ensure compatibility as the
        interface changes.
        """
        if stream is None:
            stream = sys.stderr
        self.stream = _WritelnDecorator(stream)
        self.descriptions = descriptions
        self.verbosity = verbosity
        self.failfast = failfast
        self.buffer = buffer
        self.tb_locals = tb_locals
        self.warnings = warnings
        if resultclass is not None:
            self.resultclass = resultclass

    def _makeResult(self):
        return self.resultclass(self.stream, self.descriptions, self.verbosity)

    def run(self, test, logdir=None):
        "Run the given test case or test suite."
        result = self._makeResult()
        test_result = Result()
        registerResult(result)
        result.failfast = self.failfast
        result.buffer = self.buffer
        result.tb_locals = self.tb_locals
        with warnings.catch_warnings():
            if self.warnings:
                # if self.warnings is set, use it to filter all the warnings
                warnings.simplefilter(self.warnings)
                # if the filter is 'default' or 'always', special-case the
                # warnings from the deprecated unittest methods to show them
                # no more than once per module, because they can be fairly
                # noisy.  The -Wd and -Wa flags can be used to bypass this
                # only when self.warnings is None.
                if self.warnings in ['default', 'always']:
                    warnings.filterwarnings('module',
                            category=DeprecationWarning,
                            message=r'Please use assert\w+ instead.')
            startTime = time.perf_counter()
            id = 0
            all_case_name = [ ts.id() for ts in test ]
            for ts in test:
                logdir = ts.params['results_dir']
                sum_txt = logdir + '/sum.log'
                case_status = None
                case_reason = None
                id += 1
                case_startTime = time.perf_counter()
                startTestRun = getattr(result, 'startTestRun', None)
                if startTestRun is not None:
                    startTestRun()
                try:
                    ts(result)
                finally:
                    stopTestRun = getattr(result, 'stopTestRun', None)
                    if stopTestRun is not None:
                        stopTestRun()
                    ts.duration = timeTaken = time.perf_counter() - case_startTime
                debug_log = "debug/" + ts.id() + '.debug'
                os.chdir(logdir)
                mapped_result = {'FAIL':result.failures, 'ERROR':result.errors, 'SKIP':result.skipped}
                for status in mapped_result.keys():
                    for ts_finished, reason in mapped_result[status]:
                        if ts_finished == ts:
                            if status == 'FAIL':
                                test_result.case_fail += 1
                            if status == 'ERROR':
                                test_result.case_error += 1
                            if status == 'SKIP':
                                test_result.case_skip += 1
                            case_status = status
                            case_reason = reason
                            with open(debug_log, 'a+') as fh:
                                fh.write(reason)
                                fh.write('{} - {}'.format(ts.id(), status))
                            break
                if not case_status:
                    test_result.case_pass += 1
                    with open(debug_log, 'a+') as fh:
                        fh.write('{} - PASS'.format(ts.id()))
                    case_status = 'PASS'
                    case_reason = ''
                test_result.table_rows.append((id, ts.id(), case_status, case_reason, ts.duration, debug_log))
                with open(sum_txt, 'a+') as fh:
                    fh.write('case: {} - {}\n'.format(ts.id(),case_status))
                    if case_reason:
                        fh.write('info: {}\n'.format(case_reason))
            stopTime = time.perf_counter()
        timeTaken = stopTime - startTime
        test_result.run_time = timeTaken
        all_case_name.sort()
        id = 0
        for case in all_case_name:
            id += 1
            is_pass = True
            os.chdir(logdir)
            debug_log = "debug/" + case + '.debug'
        if hasattr(result, 'separator2'):
            self.stream.writeln(result.separator2)
        test_result.compute_totals()
        with open("{}/debug/node_info".format(logdir)) as fh:
            test_result.node_info = fh.read()
        sum_html = os.path.join(logdir, "sum.html")
        generated_report(sum_html, "sum.html", test_result)
        sum_junit = os.path.join(logdir, "sum.xml")
        generated_report(sum_junit, "sum.xml", test_result)
        self.stream.writeln("{} generated".format(os.path.realpath(sum_txt)))
        #result.printErrors()
        if hasattr(result, 'separator2'):
            self.stream.writeln(result.separator2)
        run = result.testsRun
        self.stream.writeln("Ran %d test%s in %.3fs" %
                            (run, run != 1 and "s" or "", timeTaken))
        self.stream.writeln()

        expectedFails = unexpectedSuccesses = skipped = 0
        try:
            results = map(len, (result.expectedFailures,
                                result.unexpectedSuccesses,
                                result.skipped))
        except AttributeError:
            pass
        else:
            expectedFails, unexpectedSuccesses, skipped = results

        infos = []
        if not result.wasSuccessful():
            self.stream.write("FAILED")
            failed, errored = len(result.failures), len(result.errors)
            if failed:
                infos.append("failures=%d" % failed)
            if errored:
                infos.append("errors=%d" % errored)
        else:
            self.stream.write("OK")
        if skipped:
            infos.append("skipped=%d" % skipped)
        if expectedFails:
            infos.append("expected failures=%d" % expectedFails)
        if unexpectedSuccesses:
            infos.append("unexpected successes=%d" % unexpectedSuccesses)
        if infos:
            self.stream.writeln(" (%s)" % (", ".join(infos),))
        else:
            self.stream.write("\n")
        return result
