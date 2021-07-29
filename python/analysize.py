import yaml

FILE = "/home/healer/Public/code/haskell/linux/syncDirectory.yaml"

with open(FILE, 'r') as f:
    file = yaml.safe_load(f)

print(file['userSetting'][0])