# 沪深300 指数数据服务

一个使用 FastAPI + SQLite 的小项目：
- 从网络获取沪深300（CSI 300）指数日线历史数据（基于 akshare）
- 将数据存储到本地 SQLite 数据库
- 使用 Chart.js 在网页中可视化价格曲线

## 环境准备

- 需要 Python 3.10+

## 安装依赖

```bash
pip install -r requirements.txt
```

## 初始化与更新数据（可选）

执行一次全量更新，抓取历史数据并写入数据库：

```bash
python -m app.cli
```

## 启动服务

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

打开浏览器访问 `http://localhost:8000` 查看图表。点击“更新数据”按钮可拉取并写入最新数据。

## 说明

- 数据来源：akshare（调用 `stock_zh_index_daily(symbol="sh000300")`）。
- 数据库存储路径：`/workspace/data/app.db`。
- 首次打开如数据为空，界面无曲线，可先点击“更新数据”或运行 CLI 进行初始化。