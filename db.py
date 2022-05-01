import yaml, os


class Data:
    def __init__(self, data):
        self.data = str(data)

    def __enter__(self):
        if not os.path.exists(f'db/{self.data}.yaml'):
            with open(f'db/{self.data}.yaml', 'w') as f: f.write('')
        self.json = yaml.safe_load(open(f'db/{self.data}.yaml')) or {}
        self.json = {
            'lang': self.json.get('lang', 'en')
        }
        return self.json

    def __exit__(self, exc_type, exc_val, exc_tb):
        yaml.safe_dump(self.json, open(f'db/{self.data}.yaml', 'w'))