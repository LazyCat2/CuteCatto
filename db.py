import yaml, os


class Data:
    def __init__(self, data):
        self.data = str(data)

    def __enter__(self):
        if not os.path.exists(f'db/{self.data}.yaml'):
            with open(f'db/{self.data}.yaml', 'w') as f: f.write('')
        self.json = yaml.safe_load(open(f'db/{self.data}.yaml')) or {}
        self.json = {
            'lang': self.json.get('lang', 'en'),

            'wlcm_enb': self.json.get('wlcm_enb', False),
            'wlcm_text': self.json.get('wlcm_text', ''),
            'wlcm_cnl': self.json.get('wlcm_cnl'),

            'min_join_age': self.json.get('min_join_age', 0),
            'kick_new': self.json.get('kick_new', False),
        }
        return self.json

    def __exit__(self, exc_type, exc_val, exc_tb):
        yaml.safe_dump(self.json, open(f'db/{self.data}.yaml', 'w'))


class User:
    def __init__(self, data):
        self.data = str(data)

    def __enter__(self):
        if not os.path.exists(f'db/{self.data}.yaml'):
            with open(f'db/{self.data}.yaml', 'w') as f: f.write('')
        self.json = yaml.safe_load(open(f'db/{self.data}.yaml')) or {}
        self.json = {
            'ping': self.json.get('ping', True),
            'screenshot': self.json.get('screenshot', True),
        }
        return self.json

    def __exit__(self, exc_type, exc_val, exc_tb):
        yaml.safe_dump(self.json, open(f'db/{self.data}.yaml', 'w'))
