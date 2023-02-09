import yaml


class Config:
    def __init__(self):
        with open('config.yaml', 'r') as f:
            self.config = yaml.safe_load(f)

        for i in self.config.get('database'):
            setattr(self, i, self.config['database'][i])


# TODO: 文件化数据库创建
# class Tables:
#     def __init__(self):
#         with open('../init.json', 'r') as f:
#             self.list = json.load(f)


config = Config()

if __name__ == '__main__':
    print(config)
    pass
