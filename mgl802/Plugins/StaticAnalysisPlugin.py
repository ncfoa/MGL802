from .plugin import Plugin

class StaticAnalysisPlugin(Plugin):
    def run_test(self, code_change):
        # Mock static analysis test
        return {"plugin_name": "StaticAnalysis", "severity": "High", "details": "SQL Injection"}
