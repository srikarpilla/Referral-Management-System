import json



def convert_natural_language_to_rule(prompt):
    
    rule_json = json.dumps({
        'conditions': [
            {'key': 'referrer_is_paid', 'op': '==', 'value': True},
            {'key': 'referred_subscribes', 'op': '==', 'value': True}
        ],
        'actions': [
            {'type': 'reward_voucher', 'value': 500}
        ]
    })
    return rule_json

# Test
prompt = "IF referrer is a paid user AND referred user subscribes → reward ₹500 voucher"
rule = convert_natural_language_to_rule(prompt)
print(rule)

# Auto-generate nodes 
def auto_generate_nodes(rule_json):
    rule = json.loads(rule_json)
    print("Generating nodes:")
    for cond in rule['conditions']:
        print(f"Condition node: {cond}")
    for action in rule['actions']:
        print(f"Action node: {action}")

auto_generate_nodes(rule)