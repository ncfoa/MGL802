import argparse
from results import ResultRepository
from repository_monitoring import RepositoryMonitor
from notification import NotificationSystem
from results import ResultsDashboard
from kernel import Kernel


def main():    
    parser = argparse.ArgumentParser(description='Automate software security testing.')
    parser.add_argument('-rp', '--register-plugin', nargs=3, metavar=('plugin_name', 'class_name', 'version'), help='Register a new plugin')
    parser.add_argument('-up', '--unregister-plugin', metavar='plugin_name', help='Unregister an existing plugin')
    parser.add_argument('-ep', '--enable-plugin', metavar='plugin_name', help='Enable a plugin')
    parser.add_argument('-dp', '--disable-plugin', metavar='plugin_name', help='Disable a plugin')
    parser.add_argument('-t', '--test', action='store_true', help='Initiate security tests')
    parser.add_argument('-m', '--monitor', metavar='repo_path', help='Monitor a repository for changes')
    parser.add_argument('-d', '--display', action='store_true', help='Display results')
    parser.add_argument('-a', '--alert', action='store_true', help='Send alerts based on results')

    args = parser.parse_args()

    result_repo = ResultRepository()
    kernel = Kernel(result_repo)
    plugin_manager = kernel.plugin_manager

    if args.register_plugin:
        plugin_name, class_name, version = args.register_plugin
        plugin_manager.register_plugin(plugin_name, class_name, float(version))

    if args.unregister_plugin:
        plugin_manager.unregister_plugin(args.unregister_plugin)

    if args.enable_plugin:
        plugin_manager.enable_plugin(args.enable_plugin)

    if args.disable_plugin:
        plugin_manager.disable_plugin(args.disable_plugin)

    if args.test:
        # Example code change for testing
        code_change = {
            "branch": "main",
            "commit_id": "abc123",
            "changed_files": ["file1.py", "file2.py"],
            "diff": "diff details here"
        }
        kernel.initiate_testing(code_change)

    if args.monitor:
        monitor = RepositoryMonitor(args.monitor, kernel)
        monitor.start()

    if args.display:
        dashboard = ResultsDashboard(result_repo)
        dashboard.display()

    if args.alert:
        notifier = NotificationSystem(result_repo)
        notifier.send_alerts()

if __name__ == '__main__':
    main()