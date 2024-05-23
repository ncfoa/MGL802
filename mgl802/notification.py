class NotificationSystem:
    def __init__(self, result_repository):
        self.result_repository = result_repository
        self.result_repository.add_observer(self)

    def send_alerts(self, severity_filter=None):
        results = self.result_repository.get_results(severity_filter)
        if not results:
            print("No alerts to send.")
            return

        for result in results:
            self.send_alert(result)

    def send_alert(self, result):
        # Logic to send alert (e.g., email, Slack)
        print(f"Sending alert: {result['plugin_name']} - {result['severity']} - {result['details']}")

