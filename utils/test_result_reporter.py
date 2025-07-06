import json
import os
import time
from datetime import datetime
import unittest
import sys


class TestResultReporter:
    def __init__(self):
        self.test_results = []
        self.start_time = None
        self.end_time = None

        # Create reports directory if it doesn't exist
        if not os.path.exists('reports'):
            os.makedirs('reports')

    def start_test_run(self):
        """Mark the start of test execution"""
        self.start_time = datetime.now()
        print(f"Test execution started at: {self.start_time}")

    def end_test_run(self):
        """Mark the end of test execution and generate report"""
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()

        # Generate summary
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['status'] == 'PASS'])
        failed_tests = len([r for r in self.test_results if r['status'] == 'FAIL'])

        summary = {
            'timestamp': self.end_time.isoformat(),
            'total_duration_seconds': duration,
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            'test_results': self.test_results
        }

        # Save to JSON file for Grafana
        report_file = f'reports/test_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(report_file, 'w') as f:
            json.dump(summary, f, indent=2)

        # Also save latest results for Grafana dashboard
        with open('reports/latest_test_results.json', 'w') as f:
            json.dump(summary, f, indent=2)

        print(f"\nTest Results Summary:")
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {summary['success_rate']:.2f}%")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Report saved to: {report_file}")

        return summary

    def add_test_result(self, test_name, status, duration, error_message=None, screenshot_path=None):
        """Add a test result to the collection"""
        result = {
            'test_name': test_name,
            'status': status,  # PASS, FAIL, SKIP
            'duration_seconds': duration,
            'timestamp': datetime.now().isoformat(),
            'error_message': error_message,
            'screenshot_path': screenshot_path
        }
        self.test_results.append(result)


class CustomTestResult(unittest.TestResult):
    def __init__(self, reporter):
        super().__init__()
        self.reporter = reporter
        self.test_start_times = {}

    def startTest(self, test):
        super().startTest(test)
        self.test_start_times[test] = time.time()

    def addSuccess(self, test):
        super().addSuccess(test)
        duration = time.time() - self.test_start_times[test]
        self.reporter.add_test_result(
            test_name=str(test),
            status='PASS',
            duration=duration
        )

    def addError(self, test, err):
        super().addError(test, err)