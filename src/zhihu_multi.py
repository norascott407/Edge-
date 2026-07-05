"""
知乎多账号登录 - 关窗口即完成
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

print("知乎多账号登录工具")
print("每个账号只需登录一次，之后永久自动")
print()

for name, profile_dir in ACCOUNTS.items():
    print(f"\n[{name}]")

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            headless=False,
            channel="msedge",
            args=EDGE_FLAGS,
        )
        page = context.new_page()
        page.goto("https://www.zhihu.com/hot")
        time.sleep(3)

        if "signin" not in page.url:
            print("  ✓ 已登录，跳过")
            context.close()
            continue

        print("  → 请登录知乎")
        print("  → 登录后关掉浏览器窗口")
        print("  → 脚本会自动继续...")

        # 等待浏览器关闭（用户关掉窗口）
        try:
            while len(context.pages) > 0:
                time.sleep(1)
        except:
            pass

        print("  ✓ 完成")

    time.sleep(1)

print("\n" + "=" * 50)
print("全部完成！")
print("现在可以运行 zhihu_daily.py 自动拿数据")
print("=" * 50)
