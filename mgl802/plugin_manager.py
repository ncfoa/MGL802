import os
import json
import importlib
from Plugins.plugin import Plugin

class PluginFactory:
    @staticmethod
    def create_plugin(plugin_name, class_name):
        try:
            plugin_module = importlib.import_module(f'plugins.{plugin_name}')
            plugin_class = getattr(plugin_module, class_name)
            return plugin_class()
        except (ImportError, AttributeError) as e:
            print(f"Error loading plugin {plugin_name}: {e}")
            return None


class PluginManager:
    def __init__(self, plugin_dir='Plugins'):
        self.plugin_dir = plugin_dir
        self.plugins = []
        self.plugin_metadata = {}
        self.load_plugin_metadata()

    def load_plugin_metadata(self):
        metadata_file = os.path.join(self.plugin_dir, 'plugin_metadata.json')
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r') as file:
                self.plugin_metadata = json.load(file)
        else:
            self.plugin_metadata = {}
        print(f"Loaded plugin metadata: {self.plugin_metadata}")

    def save_plugin_metadata(self):
        metadata_file = os.path.join(self.plugin_dir, 'plugin_metadata.json')
        with open(metadata_file, 'w') as file:
            json.dump(self.plugin_metadata, file, indent=4)
        print(f"Saved plugin metadata: {self.plugin_metadata}")

    def load_plugins(self):
        self.plugins = []
        for plugin_name, metadata in self.plugin_metadata.items():
            if metadata['enabled']:
                try:
                    plugin_instance = PluginFactory.create_plugin(plugin_name, metadata['class_name'])
                    if plugin_instance:
                        self.validate_plugin(plugin_instance)
                        self.plugins.append(plugin_instance)
                        print(f"Loaded plugin: {plugin_name}")
                except (ImportError, AttributeError) as e:
                    print(f"Error loading plugin {plugin_name}: {e}")
        return self.plugins

    def update_plugins(self):
        # Example: Implement the plugin update logic here
        for plugin_name, metadata in self.plugin_metadata.items():
            if metadata['enabled']:
                print(f"Updating plugin: {plugin_name}")
                # Mock update process
                updated_version = metadata['version'] + 0.1
                self.plugin_metadata[plugin_name]['version'] = updated_version
        self.save_plugin_metadata()

    def validate_plugin(self, plugin):
        if not isinstance(plugin, Plugin):
            raise ValueError(f"{plugin} is not a valid plugin instance")

    def register_plugin(self, plugin_name, class_name, version, enabled=True):
        if plugin_name in self.plugin_metadata:
            raise ValueError(f"Plugin {plugin_name} is already registered")
        self.plugin_metadata[plugin_name] = {
            'class_name': class_name,
            'version': version,
            'enabled': enabled
        }
        self.save_plugin_metadata()
        print(f"Registered new plugin: {plugin_name}")
    def unregister_plugin(self, plugin_name):
        if plugin_name not in self.plugin_metadata:
            raise ValueError(f"Plugin {plugin_name} is not registered")
        del self.plugin_metadata[plugin_name]
        self.save_plugin_metadata()
        print(f"Unregistered plugin: {plugin_name}")

    def enable_plugin(self, plugin_name):
        if plugin_name in self.plugin_metadata:
            self.plugin_metadata[plugin_name]['enabled'] = True
            self.save_plugin_metadata()
            print(f"Enabled plugin: {plugin_name}")

    def disable_plugin(self, plugin_name):
        if plugin_name in self.plugin_metadata:
            self.plugin_metadata[plugin_name]['enabled'] = False
            self.save_plugin_metadata()
            print(f"Disabled plugin: {plugin_name}")

