import json
from datetime import datetime
from repository_monitoring import Observable

class Result:
    def __init__(self, plugin_name, severity, details):
        self.plugin_name = plugin_name
        self.severity = severity
        self.details = details
        self.timestamp = datetime.now().isoformat()

    def to_dict(self):
        return {
            "plugin_name": self.plugin_name,
            "severity": self.severity,
            "details": self.details,
            "timestamp": self.timestamp
        }

class ResultRepository(Observable):
    def __init__(self, storage_file='results.json'):
        super().__init__()
        self.storage_file = storage_file
        self.results = self.load_results()

    def load_results(self):
        try:
            with open(self.storage_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_results(self):
        with open(self.storage_file, 'w') as file:
            json.dump(self.results, file, indent=4)
        self.notify_observers()

    def add_result(self, result):
        self.results.append(result.to_dict())
        self.save_results()

    def get_results(self, severity_filter=None):
        if severity_filter:
            return [result for result in self.results if result['severity'] == severity_filter]
        return self.results

class ResultsDashboard:
    def __init__(self, result_repository):
        self.result_repository = result_repository
        self.result_repository.add_observer(self)

    def display(self, severity_filter=None):
        results = self.result_repository.get_results(severity_filter)
        if not results:
            print("No results found.")
            return

        print(f"{'Timestamp':<25} {'Plugin':<20} {'Severity':<10} {'Details':<30}")
        print("-" * 105)
        for result in results:
            print(f"{result['timestamp']:<25} {result['plugin_name']:<20} {result['severity']:<10} {result['details']:<30}")

