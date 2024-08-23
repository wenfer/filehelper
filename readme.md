### 文件助手

> 自动监听目标文件，并对文件按照配置的规则进行移动归类

#### 演示规则文件
config.yaml
```yaml
name: "test"
dirs: # 监听目录
  - "${HOME}/Documents"
rules:
  - name: "movie"
    move_to: "${HOME}/Videos"
    rm_dir_if_empty: true #如果所在目录为空，则删除该目录
    rm_ignore: # 删除目录判空时，忽略名称包含以下字符的文件或文件夹
      - ".torrent"
    recursion: false
    extensions:  # 后缀名匹配
      - ".mp4"
      - ".mkv"
    regulars: # 正则匹配
      - 'org'
    rename: # 重命名规则（正则）
      - ori: "电影天堂" # 这里可以写正则
        new: "" # 匹配到的字符串会被替换为这个字段
    overwrite: false # 覆盖同名文件，false则递增文件名
```

#### 打包（pyinstaller）
```shell
pip install pyinstaller
pyinstaller -F main.spec
```

#### 运行
可执行文件同目录下放一个config.yaml文件
```shell
./filehelper
```
