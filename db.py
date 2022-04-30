import yaml, os


class Data:
    def __init__(self, data):
        self.data = str(data)

    def __enter__(self):
        if not os.path.exists(f'db/{self.data}.yaml'):
            with open(f'db/{self.data}.yaml', 'w') as f: f.write('')
        self.json = yaml.safe_load(open(f'db/{self.data}.yaml')) or {}
        self.json = {
            'users': self.json.get('users', []),
            'roles': self.json.get('roles', []),
            'verify': self.json.get('verify', False),
            'verify-role': self.json.get('verify-role', None),
            'items': self.json.get('items', {}),
            'reports': self.json.get('reports', {
                'enb': False,
                'channel': None
            }),
            'lang': 'en',
            'adm-req': self.json.get('adm-req', {
                'enb': False,
                'form': [],
                'cnl': 0,
                'sent': []
            })
        }
        return self.json

    def __exit__(self, exc_type, exc_val, exc_tb):
        yaml.safe_dump(self.json, open(f'db/{self.data}.yaml', 'w'))
