"""
知乎多账号 - 每日自动拿数据
不弹窗，不登录，直接出结果
"""
import sys, io, os, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ACCOUNTS = {
    "QQ登录": BASE_DIR + "/zhihu_qq",
    "微信登录": BASE_DIR + "/zhihu_wechat",
}

EDGE_FLAGS = ["--disable-sync", "--no-first-run"]

print("知乎热榜 - 每日自动获取")
print()

all_results = {}

for name, profile_dir in ACCOUNTS.items():
    if not os.path.exists(profile_dir + "/Default"):
        print(f"  [{name}] 未登录，请先运行 zhihu_multi.py 登录此账号")
        continue

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            headless=True,
            channel="msedge",
            args=EDGE_FLAGS,
        )
        page = context.new_page()

        page.goto("https://www.zhihu.com/hot")
        time.sleep(4)

        if "signin" in page.url:
            print(f"  [{name}] 登录已过期，请重新运行 zhihu_multi.py 登录")
            context.close()
            continue

        try:
            items = page.query_selector_all(".HotList-item")
            if not items:
                items = page.query_selector_all("h2")

            titles = []
            for item in items:
                text = item.inner_text().strip()
                if text:
                    titles.append(text)

            all_results[name] = titles
            print(f"  [{name}] ✅ {len(titles)} 条热榜")

        except Exception as e:
            print(f"  [{name}] ❌ 出错: {e}")

        context.close()

print()
print("=" * 60)
for name, titles in all_results.items():
    print(f"\n{name}:")
    for i, t in enumerate(titles[:10]):
        print(f"  #{i+1} {t[:50]}")
print("=" * 60)

# 保存到文件
with open("知乎热榜_多账号.txt", "w", encoding="utf-8") as f:
    for name, titles in all_results.items():
        f.write(f"\n=== {name} ===\n")
        for i, t in enumerate(titles):
            f.write(f"#{i+1} {t}\n")

print(f"\n已保存到 知乎热榜_多账号.txt")
