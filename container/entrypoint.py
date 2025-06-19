import os
import subprocess
import json
import time
import signal
import requests 
import sys
import pytest

class ResultCollector:
    def __init__(self):
        self.results = {}

    def pytest_runtest_logreport(self, report):
        if report.when == "call":  # Only care about actual test run (not setup/teardown)
            entry = {
                "status": report.outcome,  # 'passed', 'failed', 'skipped'
                "output": ""
            }
            if report.outcome == "failed":
                # Capture the long representation (e.g., traceback)
                entry["output"] = str(report.longrepr)
            self.results[report.nodeid] = entry

def run_pytest_and_collect():
    collector = ResultCollector()
    pytest.main(["tests.py", "-q"], plugins=[collector])
    return collector.results

print(sys.argv)
user_challenge_repo = sys.argv[1]
startup_command = sys.argv[2]
runner_url = sys.argv[3]
task_id = sys.argv[4]
secret = sys.argv[5]

subprocess.run(["git", "clone", user_challenge_repo, "/runner/app"], check=True)

if startup_command != "None":
    bg_process = subprocess.Popen(startup_command, shell=True, preexec_fn=os.setsid, env={**os.environ, "SECRET": ""}, cwd="/runner/app")
    time.sleep(5)

result = run_pytest_and_collect()

os.system("ls -l **")

requests.post(f"{runner_url}/result/{task_id}/{secret}", json=result)

os.killpg(os.getpgid(bg_process.pid), signal.SIGTERM)
bg_process.wait()