import time
import random
import sys
import json
import os
import signal
import argparse

# ========================
# ANSI 颜色代码
# ========================
COLOR_RED = "\033[91m"
COLOR_YELLOW = "\033[93m"
COLOR_GREEN = "\033[92m"
COLOR_RESET = "\033[0m"

def print_red(text):
    print(f"{COLOR_RED}{text}{COLOR_RESET}")
    sys.stdout.flush()

def print_yellow(text):
    print(f"{COLOR_YELLOW}{text}{COLOR_RESET}")
    sys.stdout.flush()

def fast_print(text):
    print(text)
    sys.stdout.flush()

# ========================
# 全局变量（将在 main 中初始化）
# ========================
SAVE_FILE = None  # 将在程序启动时设置
SPEED_FACTOR = 1.0  # 速度控制

def sleep(seconds):
    time.sleep(seconds * SPEED_FACTOR)

def print_progress_bar(percentage, bar_length=50, prefix="演算进度: "):
    filled = int(bar_length * percentage / 100)
    bar = '█' * filled + '-' * (bar_length - filled)
    percent_str = f"{percentage:.1f}%"
    stage = "(阶段一：无机推演)" if percentage <= 100 else "(阶段二：追踪实体)"
    print(f"{prefix}|{bar}| {percent_str} {stage}", end='\r')

def loading_animation(text="载入中...", cycles=3):
    for _ in range(cycles):
        for c in ['/', '-', '\\', '|']:
            sys.stdout.write(f"\r{COLOR_YELLOW}{text} {c}{COLOR_RESET}")
            sys.stdout.flush()
            sleep(0.05)
    print()

# ========================
# 随机实体名称生成
# ========================
prefixes = ['Helios', 'Erebus', 'Hemera', 'Tartarus', 'Gaea', 'Phoebe', 'Rhea', 'Theia', 'Iapetus', 'Krios',
            'Hyperion', 'Chronos', 'Mnemosyne', 'Astraeus', 'Aether', 'Okeanos', 'Pontus', 'Thalassa',
            'Nyx', 'Eos', 'Selene', 'Hypnos', 'Thanatos', 'Ananke', 'Metis', 'Pallas', 'Perses', 'Echidna',
            'Typhon', 'Aion', 'Neikos', 'Leto', 'Tethys', 'Nesoi', 'Uranus', 'Chaos', 'Asteria', 'Lans']

suffixes = ['Krios', 'Uranus', 'Phoebe', 'Gaea', 'Helios', 'Astraeus', 'Leto', 'Tartarus', 'Okeanos', 'Echidna',
            'Typhon', 'Pontus', 'Thalassa', 'Nesoi', 'Hemera', 'Selene', 'Hypnos', 'Aether', 'Mnemosyne',
            'Nyx', 'Eos', 'Theia', 'Rhea', 'Iapetus', 'Chronos', 'Ananke', 'Metis', 'Pallas', 'Perses',
            'Aion', 'Neikos', 'Leto', 'Tethys', 'Uranus', 'Chaos', 'Asteria', 'Lans', 'Erebus', 'Hyperion']

def generate_entity():
    prefix = random.choice(prefixes)
    suffix = random.choice(suffixes)
    code = random.randint(1000, 9999)
    return f"{prefix}{suffix}-{code}"

# ========================
# 泰坦命途
# ========================
titan_forms = [
    '天空', '大地', '海洋', '浪漫', '负世', '理性', '诡计', '纷争', '死亡', '岁月', '律法', '门径'
]

# ========================
# 读取/保存/删除存档
# ========================
def load_save():
    if not os.path.exists(SAVE_FILE):
        return None
    try:
        with open(SAVE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if 'cycle' in data and 'destruction_score' in data:
            return data
    except Exception as e:
        print_yellow(f"[警告] 无法读取存档文件 '{SAVE_FILE}'：{e}")
    return None

def save_game(cycle, destruction_score, total_duration):
    data = {
        "cycle": cycle,
        "destruction_score": destruction_score,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_duration": round(total_duration, 2)
    }
    try:
        # 确保存档目录存在
        save_dir = os.path.dirname(SAVE_FILE)
        if save_dir and not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)
        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print_yellow(f"[系统] 进度已保存到 '{SAVE_FILE}'")
    except Exception as e:
        print_red(f"[错误] 无法保存存档: {e}")

def delete_save():
    if os.path.exists(SAVE_FILE):
        try:
            os.remove(SAVE_FILE)
            print_yellow(f"[系统] 已删除存档文件: {SAVE_FILE}")
        except Exception as e:
            print_red(f"[错误] 无法删除存档文件: {e}")

# ========================
# 暂停菜单（不退出）
# ========================
def pause_menu(current_cycle, destruction_score, start_time):
    """显示暂停菜单，等待用户选择"""
    total_duration = time.time() - start_time
    h, m, s = int(total_duration // 3600), int((total_duration % 3600) // 60), total_duration % 60

    while True:
        print("=" * 70)
        print_red("程序已暂停（Ctrl+C 捕获）")
        print_red(f"当前轮回: 第 {current_cycle} 轮")
        print_red(f"毁灭倾向评分: {destruction_score:.2f}")
        print_red(f"运行时间: {h:02d}:{m:02d}:{s:05.2f}")
        print()
        print("请选择操作：")
        print("  [1] 继续运行")
        print("  [2] 退出程序")
        print("=" * 70)

        choice = input("请输入选项 (1/2) > ").strip()
        if choice == '1':
            print_yellow("继续运行‘永劫轮回’协议...")
            return True  # 继续
        elif choice == '2':
            print_red("正在保存进度并退出...")
            save_game(current_cycle, destruction_score, total_duration)
            print_red("翁法罗斯协议已安全终止。")
            print_red("窗口将在您按下回车后关闭。")
            input()  # 等待用户按回车再关闭
            sys.exit(0)
        else:
            print_red("无效输入，请输入 1 或 2。")

# ========================
# 主程序
# ========================
def main():
    global SAVE_FILE

    # 设置默认存档路径：与 main.py 同目录下的 savegame.json
    script_dir = os.path.dirname(os.path.abspath(__file__))
    DEFAULT_SAVE_PATH = os.path.join(script_dir, "savegame.json")

    # 解析命令行参数
    parser = argparse.ArgumentParser(description="翁法罗斯协议 - 永劫轮回模拟器")
    parser.add_argument(
        '--save-path',
        default=DEFAULT_SAVE_PATH,
        help='指定存档文件的保存路径（默认: 与 main.py 同目录下的 savegame.json）'
    )
    args = parser.parse_args()

    # 设置保存路径（转换为绝对路径）
    SAVE_FILE = os.path.abspath(args.save_path)

    # 确保目录存在
    save_dir = os.path.dirname(SAVE_FILE)
    if save_dir and not os.path.exists(save_dir):
        try:
            os.makedirs(save_dir, exist_ok=True)
            print_yellow(f"[系统] 已自动创建存档目录: {save_dir}")
        except Exception as e:
            print_red(f"[错误] 无法创建存档目录 '{save_dir}': {e}")
            sys.exit(1)
    if save_dir and not os.access(save_dir, os.W_OK):
        print_red(f"[错误] 存档目录 '{save_dir}' 没有写入权限。")
        sys.exit(1)

    # 加载存档
    save_data = load_save()
    if save_data:
        print_yellow("检测到上次未完成的演算进程...")
        start_cycle = save_data['cycle'] + 1
        destruction_score = save_data['destruction_score']
        print(f"继续从第 {start_cycle} 轮开始")
        print(f"当前毁灭倾向评分: {destruction_score:.2f}")
        fast_print("")
    else:
        start_cycle = 1
        destruction_score = 144.65
        print("未检测到存档，开始新的‘永劫轮回’协议...")
        fast_print("")

    max_cycles = 33550336
    cycle_count = start_cycle - 1
    start_time = time.time()

    # 是否跳过第一阶段
    if start_cycle == 1:
        # ===== 第一阶段：启动与演算（不可中断）=====
        fast_print("=== 翁法罗斯 v10.3 (Dev) 启动 (简单模式) ===")
        sleep(0.3)
        fast_print("")
        fast_print("=== 进入无机实体培养阶段 ===")
        fast_print("...正在演化纯粹的“活性”与“稳定性”概念...")
        sleep(0.5)

        for i in range(0, 101, 5):
            print_progress_bar(i)
            sleep(0.05)
        print()

        print_red(">>> 原型验证完成! 发现高活性实体 (ID: 3455)! <<<")
        sleep(0.2)
        print_red(">>> 数据: 活性=15.54, 稳定性=11.78")
        sleep(0.2)
        print_red(">>> 基于原型，已将目标平均分调整为: 50.00 <<<")
        sleep(0.3)

        fast_print("")
        print_yellow(">>> 正式演算开始... <<<")
        sleep(0.2)
        fast_print("思潮更新: 当前时代的主流是 '毁灭' (权重: 0.010)")
        sleep(0.3)

        generations = 14
        records = [3.88, 4.05, 4.22, 4.44, 4.44, 4.58, 5.86]
        record_idx = 0
        strongest_entities = [
            "[HeliosKrios-4364] <'智识'的追随者>(评分:6.50|纯:0.21|最强命途:智识:0.21)",
            "[HypnosAstraeus-9963] <'记忆'的追随者>(评分:6.94|纯:0.21|最强命途:记忆:0.21)",
            "[RheaLeto-4626] <'毁灭'的追随者>(评分:7.09|纯:0.27|最强命途:毁灭:0.27)",
            "[IapetusUranus-4776] <'记忆'的追随者>(评分:6.52|纯:0.20|最强命途:记忆:0.20)",
            "[EosAstraeus-7050] <'毁灭'的追随者>(评分:7.36|纯:0.28|最强命途:毁灭:0.28)",
            "[EosAstraeus-7050] <'毁灭'的追随者>(评分:6.90|纯:0.28|最强命途:毁灭:0.28)",
            "[EosAstraeus-7050] <'毁灭'的追随者>(评分:7.54|纯:0.25|最强命途:毁灭:0.25)",
            "[AionNeikos-3870] <卡厄斯兰那>(评分:7.97|纯:0.33|最强命途:毁灭:0.33)",
            "[AionNeikos-3870] <卡厄斯兰那>(评分:8.49|纯:0.39|最强命途:毁灭:0.39)",
            "[AionNeikos-3870] <卡厄斯兰那>(评分:9.01|纯:0.41|最强命途:毁灭:0.41)",
            "[AionNeikos-3870] <卡厄斯兰那>(评分:9.17|纯:0.43|最强命途:毁灭:0.43)",
            "[AionNeikos-3870] <卡厄斯兰那>(评分:9.67|纯:0.45|最强命途:毁灭:0.45)",
            "[AionNeikos-3870] <卡厄斯兰那>(评分:10.86|纯:0.52|最强命途:毁灭:0.52)",
            "[AionNeikos-3870] <卡厄斯兰那>(评分:10.81|纯:0.47|最强命途:毁灭:0.47)"
        ]

        for gen in range(1, generations + 1):
            entity_count = random.randint(200, 400)
            golden_count = 12
            eliminations = random.randint(0, 200) if gen % 2 == 0 else random.randint(0, 10)

            fast_print(f"--- 世代 {gen}/33550336 | 实体数目:{entity_count} | 黄金裔:{golden_count} ---")
            sleep(0.1)

            if 2 <= gen <= 10:
                defeats = random.randint(1, 5)
                for _ in range(defeats):
                    enemy = generate_entity()
                    fast_print(f"对决: 卡厄斯兰那在其命途 '毁灭' 上遭遇敌人 {enemy}，并将其击败！")
                    sleep(0.1)

            fast_print(f"世代 {gen} 演算结束。")
            if eliminations > 0:
                fast_print(f"动态淘汰了 {eliminations} 个实体.")
            elif gen == 14:
                fast_print("【翁法罗斯事件: 泰坦回响】泰坦 '律法' 的概念浸染了所有实体！")

            if gen in [1, 2, 4, 6, 10, 12, 14] and record_idx < len(records):
                avg_score = records[record_idx]
                print_red(f"新纪录！平均分达到: {avg_score:.2f}")
                record_idx += 1

            if gen == 10:
                fast_print("思潮更新: 当前时代的主流是 '毁灭' (权重: 0.049)")
                fast_print("宏观调控: 命途能量上限调整为 14279.15 (当前均: 4.42 / 目标: 50.00)")
                fast_print("引导网络学习中... 损失: 1.6013, 奖励(分/多): 0.00/0.00")

            dominant_path = random.choice(titan_forms)
            fast_print(f"引导网络更新蓝图: 主导方向 '{dominant_path}'。")
            fast_print(f"当前最强者: {strongest_entities[gen-1]}")
            print_progress_bar(0, prefix="演算进度: ")
            fast_print("")
            sleep(0.2)

        print("=" * 70)
        print_red("      警告：侦测到突破框架的异常实体，演算异常！      ")
        print("=" * 70)
        sleep(0.3)
        print_red("实体分析:")
        print_red("  - 识别代号: 卡厄斯兰那 (AionNeikos-3870)")
        print_red("  - 状态: 已确认为当前最强个体，电信号异常活跃！")
        print_red("  - 核心倾向: 对 毁灭 命途的亲和度超出安全阈值。")
        sleep(0.3)
        print_red("")
        print_red("结论：该实体的存在已成为驱动翁法罗斯演化的核心变量。")
        print_red("      原有演化协议已失效，正在载入下一阶段...")
        fast_print("")
        print_yellow("警告：侦测异常反应... 原有进程已中断... 正在启动备用协议...")
        loading_animation("载入中...", cycles=2)
        fast_print("")
    else:
        print_yellow(f"跳过启动阶段，直接进入‘永劫轮回’第 {start_cycle} 轮...")
        fast_print("")

    # ========================
    # 第二阶段：永劫轮回（可暂停）
    # ========================
    try:
        for cycle in range(start_cycle, max_cycles + 1):
            cycle_count = cycle

            print_yellow(f"--- 永劫轮回 第 {cycle} 轮 开始 ---")
            fast_print("卡厄斯兰那将开始夺取创世火种。")
            sleep(0.1)

            titans = [generate_entity() for _ in titan_forms]
            for i, form in enumerate(titan_forms):
                fast_print(f"实体 {titans[i]} 已化身为 [{form}] 泰坦。")

            actions = ['谈判', '击杀']
            for titan in titans:
                action = random.choice(actions)
                fast_print(f"决策: 卡厄斯兰那对 {titan} 发起了 [{action}]...")
                sleep(0.05)
                if action == '谈判':
                    fast_print(f"...谈判成功! AionNeikos-3870 夺取了所有火种!")
                else:
                    fast_print(f"...AionNeikos-3870 夺取了所有火种!")

            dominant_path = random.choice(titan_forms)
            fast_print(f"引导网络更新蓝图: 主导方向 '{dominant_path}'。")

            memory_score = destruction_score * 0.14
            pure = destruction_score * 0.006
            strongest = f"[PallasAstraeus-2812] <'记忆'的追随者>(评分:{memory_score:.2f}|纯:{pure:.2f}|最强命途:记忆:{pure:.2f})"
            fast_print(f"当前最强者: {strongest}")
            fast_print("(阶段三：永劫轮回)")

            extra_kills = random.randint(5, 20)
            for _ in range(extra_kills):
                victim = generate_entity()
                fast_print(f"决策: 卡厄斯兰那对 {victim} 执行了 [击杀]!")
                sleep(0.02)

            print("=" * 70)
            print_red(f"卡厄斯兰那集齐了所有 12 个火种！第 {cycle} 轮轮回结束！")
            print_red(f"本轮毁灭倾向评分: {destruction_score:.2f}")
            print("=" * 70)

            inheritor_form = random.choice(titans)
            inheritor = inheritor_form.split('-')[0] + "-{:04d}".format(random.randint(1, 9999))
            fast_print("一个新的轮回即将开始...卡厄斯兰那的意志将作为新轮回的蓝图...")
            fast_print(f"在黄金裔中，{inheritor_form} 是这个轮回的白厄，开始数据继承...")
            print_yellow(f"数据继承成功！新的卡厄斯兰那为: {inheritor}。")
            fast_print("旧的实体已消逝，基于卡厄斯兰那的意志，新的生命正在诞生...")

            destruction_score += random.uniform(0.1, 1.5)

            if cycle % 100 == 0:
                print(f"[系统] 已完成 {cycle} 轮永劫轮回...", file=sys.stderr)
                sleep(0.05)

        # 全部完成
        end_time = time.time()
        duration = end_time - start_time
        mins, secs = divmod(duration, 60)
        hours, mins = divmod(mins, 60)
        print_red("=== 永劫轮回已达成最大次数，协议圆满完成。 ===")
        print_yellow(f"总耗时: {int(hours):02d}:{int(mins):02d}:{secs:05.2f}")
        delete_save()

    except KeyboardInterrupt:
        total_duration = time.time() - start_time
        save_game(cycle_count, destruction_score, total_duration)
        # 进入暂停菜单（不退出）
        should_continue = pause_menu(cycle_count, destruction_score, start_time)
        if should_continue:
            # 继续循环
            try:
                for cycle in range(cycle_count + 1, max_cycles + 1):
                    cycle_count = cycle
                    print_yellow(f"--- 永劫轮回 第 {cycle} 轮 开始 ---")
                    fast_print("卡厄斯兰那将开始夺取创世火种。")
                    sleep(0.1)

                    titans = [generate_entity() for _ in titan_forms]
                    for i, form in enumerate(titan_forms):
                        fast_print(f"实体 {titans[i]} 已化身为 [{form}] 泰坦。")

                    actions = ['谈判', '击杀']
                    for titan in titans:
                        action = random.choice(actions)
                        fast_print(f"决策: 卡厄斯兰那对 {titan} 发起了 [{action}]...")
                        sleep(0.05)
                        if action == '谈判':
                            fast_print(f"...谈判成功! AionNeikos-3870 夺取了所有火种!")
                        else:
                            fast_print(f"...AionNeikos-3870 夺取了所有火种!")

                    dominant_path = random.choice(titan_forms)
                    fast_print(f"引导网络更新蓝图: 主导方向 '{dominant_path}'。")

                    memory_score = destruction_score * 0.14
                    pure = destruction_score * 0.006
                    strongest = f"[PallasAstraeus-2812] <'记忆'的追随者>(评分:{memory_score:.2f}|纯:{pure:.2f}|最强命途:记忆:{pure:.2f})"
                    fast_print(f"当前最强者: {strongest}")
                    fast_print("(阶段三：永劫轮回)")

                    extra_kills = random.randint(5, 20)
                    for _ in range(extra_kills):
                        victim = generate_entity()
                        fast_print(f"决策: 卡厄斯兰那对 {victim} 执行了 [击杀]!")
                        sleep(0.02)

                    print("=" * 70)
                    print_red(f"卡厄斯兰那集齐了所有 12 个火种！第 {cycle} 轮轮回结束！")
                    print_red(f"本轮毁灭倾向评分: {destruction_score:.2f}")
                    print("=" * 70)

                    inheritor_form = random.choice(titans)
                    inheritor = inheritor_form.split('-')[0] + "-{:04d}".format(random.randint(1, 9999))
                    fast_print("一个新的轮回即将开始...卡厄斯兰那的意志将作为新轮回的蓝图...")
                    fast_print(f"在黄金裔中，{inheritor_form} 是这个轮回的白厄，开始数据继承...")
                    print_yellow(f"数据继承成功！新的卡厄斯兰那为: {inheritor}。")
                    fast_print("旧的实体已消逝，基于卡厄斯兰那的意志，新的生命正在诞生...")

                    destruction_score += random.uniform(0.1, 1.5)

                    if cycle % 100 == 0:
                        print(f"[系统] 已完成 {cycle} 轮永劫轮回...", file=sys.stderr)
                        sleep(0.05)
            except KeyboardInterrupt:
                save_game(cycle, destruction_score, time.time() - start_time)
                if not pause_menu(cycle, destruction_score, time.time() - start_time):
                    sys.exit(0)
        else:
            sys.exit(0)


if __name__ == "__main__":
    main()