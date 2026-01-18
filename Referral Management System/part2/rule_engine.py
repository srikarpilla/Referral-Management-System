import json

class RuleEngine:
    def __init__(self, rule_json):
        self.rule = json.loads(rule_json)

    def evaluate(self, context):
        for cond in self.rule['conditions']:
            if context.get(cond['key']) != cond['value']:
                return False

        for action in self.rule['actions']:
            self.execute(action)

        return True

    def execute(self, action):
        print(f"Executing action: {action['type']} → {action['value']}")
