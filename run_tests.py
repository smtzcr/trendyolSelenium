#!/usr/bin/env python3
"""
Main test runner for Trendyol automation tests
Supports both web and mobile tests with comprehensive reporting
"""

import sys
import os
import unittest
import argparse
import json
from datetime import datetime
import logging

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.test_result_reporter import TestResultReporter, CustomTestResult, export_metrics_for_grafana


class TrendyolTestRunner:
    def __init__(self):
        self.reporter = TestResultReporter()
        self.setup_logging()

    def setup_logging(self):
        """Setup logging configuration"""
        if not os.path.exists('logs'):
            os.makedirs('logs')

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'logs/test_runner_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def discover_tests(self, test_path, pattern="test_*.py"):
        """Discover test cases in the given path"""
        loader = unittest.TestLoader()
        if os.path.isfile(test_path):
            # Single test file
            suite = loader.loadTestsFromName(test_path.replace('/', '.').replace('.py', ''))
        else:
            # Directory of tests
            suite = loader.discover(test_path, pattern=pattern)
        return suite

    def run_web_tests(self):
        """Run web automation tests"""
        self.logger.info("Starting web tests...")

        # Discover web tests
        web_test_suite = self.discover_tests('tests')

        # Run tests with custom result handler
        runner = unittest.TextTestRunner(
            resultclass=lambda: CustomTestResult(self.reporter),
            verbosity=2,
            stream=sys.stdout
        )

        result = runner.run(web_test_suite)

        self.logger.info(f"Web tests completed. Tests run: {result.testsRun}, "
                         f"Failures: {len(result.failures)}, Errors: {len(result.errors)}")

        return result

    def run_mobile_tests(self):
        """Run mobile automation tests"""
        self.logger.info("Starting mobile tests...")

        try:
            # Check if Appium server is running
            import requests
            response = requests.get("http://localhost:4723/wd/hub/status", timeout=5)
            if response.status_code != 200:
                self.logger.error("Appium server is not running. Please start Appium server first.")
                return None
        except Exception as e:
            self.logger.error(f"Cannot connect to Appium server: {e}")
            return None

        # Discover mobile tests
        mobile_test_suite = self.discover_tests('mobile/tests')

        # Run tests with custom result handler
        runner = unittest.TextTestRunner(
            resultclass=lambda: CustomTestResult(self.reporter),
            verbosity=2,
            stream=sys.stdout
        )

        result = runner.run(mobile_test_suite)

        self.logger.info(f"Mobile tests completed. Tests run: {result.testsRun}, "
                         f"Failures: {len(result.failures)}, Errors: {len(result.errors)}")

        return result

    def run_specific_test(self, test_path):
        """Run a specific test file or test case"""
        self.logger.info(f"Running specific test: {test_path}")

        test_suite = self.discover_tests(test_path)

        runner = unittest.TextTestRunner(
            resultclass=lambda: CustomTestResult(self.reporter),
            verbosity=2,
            stream=sys.stdout
        )

        result = runner.run(test_suite)
        return result

    def generate_html_report(self):
        """Generate HTML report from test results"""
        try:
            if not os.path.exists('reports'):
                os.makedirs('reports')

            # Read latest test results
            if os.path.exists('reports/latest_test_results.json'):
                with open('reports/latest_test_results.json', 'r') as f:
                    data = json.load(f)
            else:
                self.logger.warning("No test results found for HTML report generation")
                return

            # Generate HTML report
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Trendyol Test Automation Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; }}
        .summary {{ display: flex; gap: 20px; margin: 20px 0; }}
        .metric {{ background-color: #e9ecef; padding: 15px; border-radius: 5px; text-align: center; flex: 1; }}
        .metric.success {{ background-color: #d1eddc; }}
        .metric.warning {{ background-color: #fff3cd; }}
        .metric.danger {{ background-color: #f8d7da; }}
        .test-results {{ margin: 20px 0; }}
        .test-item {{ padding: 10px; margin: 5px 0; border-radius: 3px; }}
        .test-pass {{ background-color: #d1eddc; }}
        .test-fail {{ background-color: #f8d7da; }}
        .test-skip {{ background-color: #e2e3e5; }}
        .timestamp {{ color: #6c757d; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Trendyol Test Automation Report</h1>
        <p class="timestamp">Generated: {data.get('timestamp', 'N/A')}</p>
    </div>

    <div class="summary">
        <div class="metric {'success' if data.get('success_rate', 0) >= 90 else 'warning' if data.get('success_rate', 0) >= 70 else 'danger'}">
            <h3>Success Rate</h3>
            <p style="font-size: 2em; margin: 0;">{data.get('success_rate', 0):.1f}%</p>
        </div>
        <div class="metric">
            <h3>Total Tests</h3>
            <p style="font-size: 2em; margin: 0;">{data.get('total_tests', 0)}</p>
        </div>
        <div class="metric success">
            <h3>Passed</h3>
            <p style="font-size: 2em; margin: 0;">{data.get('passed_tests', 0)}</p>
        </div>
        <div class="metric danger">
            <h3>Failed</h3>
            <p style="font-size: 2em; margin: 0;">{data.get('failed_tests', 0)}</p>
        </div>
    </div>

    <div class="test-results">
        <h2>Test Results</h2>
        {self._generate_test_items_html(data.get('test_results', []))}
    </div>

    <div style="margin-top: 40px; color: #6c757d; font-size: 0.9em;">
        <p>Report generated by Trendyol Test Automation Framework</p>
    </div>
</body>
</html>
"""

            with open('reports/test_report.html', 'w') as f:
                f.write(html_content)

            self.logger.info("HTML report generated: reports/test_report.html")

        except Exception as e:
            self.logger.error(f"Failed to generate HTML report: {e}")

    def _generate_test_items_html(self, test_results):
        """Generate HTML for individual test items"""
        html = ""
        for test in test_results:
            status_class = f"test-{test.get('status', 'unknown').lower()}"
            html += f"""
        <div class="test-item {status_class}">
            <strong>{test.get('test_name', 'Unknown Test')}</strong>
            <span style="float: right;">{test.get('status', 'UNKNOWN')} ({test.get('duration_seconds', 0):.2f}s)</span>
            {f'<br><small>Error: {test.get("error_message", "")}</small>' if test.get('error_message') else ''}
        </div>
"""
        return html

    def cleanup_old_reports(self, days=7):
        """Clean up old reports and screenshots"""
        try:
            import time
            current_time = time.time()

            for directory in ['reports', 'screenshots', 'logs']:
                if os.path.exists(directory):
                    for filename in os.listdir(directory):
                        if filename == 'latest_test_results.json':
                            continue  # Keep latest results

                        file_path = os.path.join(directory, filename)
                        if os.path.isfile(file_path):
                            file_age = current_time - os.path.getctime(file_path)
                            if file_age > (days * 24 * 60 * 60):  # older than specified days
                                os.remove(file_path)
                                self.logger.info(f"Cleaned up old file: {file_path}")
        except Exception as e:
            self.logger.warning(f"Failed to cleanup old reports: {e}")


def main():
    parser = argparse.ArgumentParser(description='Trendyol Test Automation Runner')
    parser.add_argument('--web', action='store_true', help='Run web tests only')
    parser.add_argument('--mobile', action='store_true', help='Run mobile tests only')
    parser.add_argument('--test', type=str, help='Run specific test file')
    parser.add_argument('--cleanup', action='store_true', help='Cleanup old reports before running')
    parser.add_argument('--report-only', action='store_true', help='Generate reports only (no test execution)')

    args = parser.parse_args()

    # Create test runner
    runner = TrendyolTestRunner()

    # Cleanup if requested
    if args.cleanup:
        runner.cleanup_old_reports()

    # Handle report-only mode
    if args.report_only:
        runner.generate_html_report()
        export_metrics_for_grafana()
        return 0

    # Start test execution
    runner.reporter.start_test_run()

    try:
        if args.test:
            # Run specific test
            result = runner.run_specific_test(args.test)
            success = result and (len(result.failures) + len(result.errors)) == 0
        elif args.web:
            # Run web tests only
            result = runner.run_web_tests()
            success = result and (len(result.failures) + len(result.errors)) == 0
        elif args.mobile:
            # Run mobile tests only
            result = runner.run_mobile_tests()
            success = result and (len(result.failures) + len(result.errors)) == 0
        else:
            # Run both web and mobile tests
            web_result = runner.run_web_tests()
            mobile_result = runner.run_mobile_tests()

            web_success = web_result and (len(web_result.failures) + len(web_result.errors)) == 0
            mobile_success = mobile_result and (len(mobile_result.failures) + len(mobile_result.errors)) == 0

            success = web_success and mobile_success

        # Generate final reports
        summary = runner.reporter.end_test_run()
        runner.generate_html_report()
        export_metrics_for_grafana()

        # Print summary
        print("\n" + "=" * 50)
        print("TEST EXECUTION SUMMARY")
        print("=" * 50)
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['passed_tests']}")
        print(f"Failed: {summary['failed_tests']}")
        print(f"Success Rate: {summary['success_rate']:.2f}%")
        print(f"Duration: {summary['total_duration_seconds']:.2f} seconds")
        print("=" * 50)

        # Return appropriate exit code
        return 0 if success else 1

    except KeyboardInterrupt:
        runner.logger.info("Test execution interrupted by user")
        return 1
    except Exception as e:
        runner.logger.error(f"Test execution failed: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)