from .plugin import Plugin

class DependencyCheckPlugin(Plugin):
    def run_test(self, code_change):
        # Mock dependency check test
        return {"plugin_name": "DependencyCheck", "severity": "Medium", "details": "Outdated Library"}
