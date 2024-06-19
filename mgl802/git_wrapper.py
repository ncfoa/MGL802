import os
import subprocess
import sys
from kernel import Kernel
from plugin_manager import PluginManager
from repository_monitoring import RepositoryMonitor
from results import Result
from notification import Notification

def run_command(command):
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Command failed: {command}")
        sys.exit(result.returncode)

def run_security_tests():
    # Initialize kernel
    kernel = Kernel()
    
    # Load plugins
    plugin_manager = PluginManager(kernel)
    plugin_manager.load_plugins()

    # Monitor repository
    repo_monitor = RepositoryMonitor(kernel)
    vulnerabilities = repo_monitor.scan_repository()

    # Generate results
    results = Result(vulnerabilities)
    results.generate_report()

    # Notify if vulnerabilities are found
    if vulnerabilities:
        notifier = Notification()
        notifier.send_alert(vulnerabilities)
        print("Security vulnerabilities detected. Operation aborted.")
        sys.exit(1)  # Indicate failure

def custom_add(files):
    run_command(f"git add {files}")

def custom_commit(message):
    run_command(f'git commit -m "{message}"')

def custom_push():
    # Run security tests before pushing
    run_security_tests()
    run_command("git push")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python git_wrapper.py <command> [<args>]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Usage: python git_wrapper.py add <files>")
            sys.exit(1)
        files = sys.argv[2]
        custom_add(files)

    elif command == "commit":
        if len(sys.argv) < 3:
            print("Usage: python git_wrapper.py commit <message>")
            sys.exit(1)
        message = sys.argv[2]
        custom_commit(message)

    elif command == "push":
        custom_push()

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
