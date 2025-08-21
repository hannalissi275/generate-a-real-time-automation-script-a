import pandas as pd
import re
from collections import defaultdict

class AutomationScriptAnalyzer:
    def __init__(self):
        self.script = ''
        self.commands = []
        self.variables = defaultdict(list)
        self.errors = []

    def load_script(self, script_path):
        with open(script_path, 'r') as f:
            self.script = f.read()

    def parse_script(self):
        lines = self.script.splitlines()
        for line in lines:
            if line.startswith('#'):  # skip comments
                continue
            match = re.match(r'(\w+)\s*(.*)', line)
            if match:
                command, args = match.groups()
                self.commands.append({'command': command, 'args': args})
            else:
                self.errors.append(f'Invalid command: {line}')

    def analyze_variables(self):
        for command in self.commands:
            if command['command'] == 'set':
                var_name, value = command['args'].split('=')
                self.variables[var_name].append(value)
            elif command['command'] == 'use':
                var_name = command['args']
                if var_name not in self.variables:
                    self.errors.append(f'Undefined variable: {var_name}')

    def generate_report(self):
        report = 'Automation Script Analysis Report\n'
        report += '-------------------------------\n'
        report += 'Commands:\n'
        for command in self.commands:
            report += f'  {command["command"]}: {command["args"]}\n'
        report += '\nVariables:\n'
        for var, values in self.variables.items():
            report += f'  {var}: {", ".join(values)}\n'
        if self.errors:
            report += '\nErrors:\n'
            for error in self.errors:
                report += f'  {error}\n'
        return report

analyzer = AutomationScriptAnalyzer()
analyzer.load_script('script.txt')
analyzer.parse_script()
analyzer.analyze_variables()
print(analyzer.generate_report())