# 知识图谱课程设计 - 电影知识图谱构建 - 第15组

## 使用方法

- 安装依赖

  - 所需依赖模块列于requirements.txt中

- 下载中文维基百科原始dump数据库文件保存至./data/wiki.xml

- 将繁体汉字转换为简体

  ```shell
  python convert.py
  rm ./data/wiki.xml
  ```

  - 生成的文件保存于./data/wiki_simple.xml

- 将原始dump文件切分为页面

  ```shell
  mv ./data/wiki.xml ./data/page.xml
  python XML_split.py ./data/page.xml page 1
  rm ./data/page.xml
  ```

  - 生成的文件保存于./data/page\*.xml

- 筛选电影相关页面（类别推断）

  ```shell
  python filter.py
  ```

  - 页面按类别保存于./filtered_data/actor/page\*.xml、./filtered_data/director/page\*.xml、./filtered_data/writer/page\*.xml

- 根据已有本体进行事实抽取

  ```shell
  python fact_extract.py
  ```

  - 得到的初步图谱数据保存于./graph/graph_base.csv

- 属性清洗

  ```shell
  python data_normalize.py
  ```

  - 得到的清洗后图谱数据保存于./graph/graph.csv

- 补全、可视化等

  - 将图谱csv文件导入至neo4j中进行后续操作（详见报告）
  - ./graph/graph.csv去除一些特殊字符后得到./graph/graph.csv
  - 运行neo4j服务器
  - 导入节点

  ```shell
  python visualize.py
  ```

