# Edge 多账号自动化爬虫框架

基于 Playwright + Microsoft Edge 持久化上下文的多账号自动化框架。

## 核心原理

用 `launch_persistent_context()` + `channel="msedge"` + 独立 `user_data_dir`
将完整的浏览器上下文（Cookie + localStorage + 指纹信息）保存到硬盘。

**每次"唤醒"同一个浏览器目录，目标网站就认为你是同一个人，不需要重新登录。**

## 解决的问题

公寓 OTA 对账需要登录美团、携程、飞猪等平台拉数据。每次登录都有验证码/扫码，登一次管不了两天。16 个账号反复登录，每周浪费大量时间。

## 快速开始

### 环境要求
- 已安装 Edge 浏览器
- Python 3.8+
- `pip install playwright`
- `playwright install chromium`

### 核心代码

```python
from playwright.sync_api import sync_playwright

PROFILE_DIR = "./profiles/account_1"  # 每个账号独立目录
EDGE_FLAGS = ["--disable-sync", "--no-first-run"]

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=PROFILE_DIR,
        headless=True,
        channel="msedge",
        args=EDGE_FLAGS,
    )
    page = context.new_page()
    page.goto("https://target.com")
    # ... 取数据
    context.close()
```

### 首次登录

首次登录时用 `headless=False`，会弹出浏览器窗口让你手动登录。登录完成后关掉窗口，上下文自动保存。下次运行用 `headless=True` 即可。

## 多账号管理

```
profiles/
├── meituan_a/        ← 美团账号A登录态
├── meituan_b/        ← 美团账号B登录态
├── ctrip_a/          ← 携程账号A登录态
├── feizhu_a/         ← 飞猪账号A登录态
└── ...
```

遍历所有目录，逐个加载上下文获取数据。

## 关键参数

| 参数 | 作用 |
|------|------|
| `channel="msedge"` | 使用系统已安装的 Edge 浏览器 |
| `headless=True/False` | True=不弹窗(日常) / False=弹窗(首次登录) |
| `--disable-sync` | 禁止 Edge 同步，防止主浏览器污染独立账号目录 |
| `--no-first-run` | 跳过 Edge 首次运行向导 |

## 已知坑点

1. **Edge 同步污染**：新创建的 user_data_dir 必须加 `--disable-sync`，否则主浏览器的登录态会同步进去
2. **首次必须弹窗**：headless=True 无法扫码/验证码，首次必须用 headless=False
3. **Edge 必须关闭**：使用 `channel="msedge"` 时如果 Edge 正在运行，Playwright 无法访问用户数据目录

## 脚本说明

- `src/zhihu_multi.py` — 多账号首次登录工具（弹窗登录，关窗即完成）
- `src/zhihu_daily.py` — 多账号每日自动获取知乎热榜（headless）

## License

MIT
