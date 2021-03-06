# Copyright 2020 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ament_index_python import get_resource, get_resources, has_resource
from ros2component.api import ComponentSearcher
try:
    from importlib.metadata import entry_points
except ImportError:
    from importlib_metadata import entry_points


class PyEntryPointComponentSearcher(ComponentSearcher):
    def __init__(self, component_resource_type='rclpy_components'):
        if component_resource_type != 'rclpy_components':
            raise ValueError('component resource type should be "rclpy_components" for '
                             'PythonEntryPointComponentLoader instances')

        self.component_resource_type = 'rclpy_components'

    def get_component_types(self):
        component_entry_points = entry_points().get(self.component_resource_type, None)
        if not component_entry_points:
            return []

        # key: component_type, value: component entry point values
        components = {}
        for entry_point in component_entry_points:
            component_type = str.split(entry_point.name, '::')[0].strip()
            if component_type not in components:
                components[component_type] = [entry_point.name]
            else:
                components[component_type].append(entry_point.name)

        return [('{}/{}'.format(self.component_resource_type, package_name), values)
                for package_name, values in components.items()]

    def get_package_component_types(self, package_name):
        component_entry_points = entry_points().get(self.component_resource_type, None)
        if not component_entry_points:
            return []
        return [ep.name for ep in component_entry_points if str.split(ep.name, '::')[0] == package_name]


class AmentResourceComponentSearcher(ComponentSearcher):

    def get_package_names_with_component_types(self):
        """Get the names of all packages that register component types in the ament index."""
        return list(get_resources(self.component_resource_type).keys())

    def get_package_component_types(self, package_name=None):
        """
        Get all component types registered in the ament index for the given package.

        :param package_name: whose component types are to be retrieved.
        :return: a list of component type names.
        """
        if not has_resource(self.component_resource_type, package_name):
            return []
        component_registry, _ = get_resource(self.component_resource_type, package_name)
        return [line.split(';')[0] for line in component_registry.splitlines()]

    def get_component_types(self):
        return [
            ('{}/{}'.format(self.component_resource_type, package_name),
             self.get_package_component_types(package_name=package_name))
            for package_name in self.get_package_names_with_component_types()
        ]
