from plugin_manager import PluginManager
from results import ResultsDashboard, Result
from notification import NotificationSystem

class Kernel:
    def __init__(self, result_repository):
        self.plugin_manager = PluginManager()
        self.result_repository = result_repository
        self.results = []

    def initiate_testing(self, code_change):
        plugins = self.plugin_manager.load_plugins()
        for plugin in plugins:
            result = plugin.run_test(code_change)
            self.results.append(result)
            self.store_result(result)
        self.aggregate_results()

    def store_result(self, result):
        result_obj = Result(
            plugin_name=result['plugin_name'],
            severity=result['severity'],
            details=result['details']
        )
        self.result_repository.add_result(result_obj)

    def aggregate_results(self):
        aggregated_results = {}
        for result in self.results:
            if result['severity'] not in aggregated_results:
                aggregated_results[result['severity']] = []
            aggregated_results[result['severity']].append(result)
        self.report_results(aggregated_results)

    def report_results(self, aggregated_results):
        dashboard = ResultsDashboard(self.result_repository)
        dashboard.display()
        notifier = NotificationSystem(self.result_repository)
        notifier.send_alerts()

