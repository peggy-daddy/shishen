#!/usr/bin/env python3
"""
八字排盘计算器 — 零依赖，纯 Python 标准库
用法: python3 bazi-calc.py <年> <月> <日> <时(0-23)>
示例: python3 bazi-calc.py 1995 3 15 14
输出: JSON 格式的四柱八字 + 十神分布
"""

import sys
import json
import math

STEMS = ['甲','乙','丙','丁','戊','己','庚','辛','壬','癸']
BRANCHES = ['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥']

STEM_ELEMENTS = {'甲':'木','乙':'木','丙':'火','丁':'火','戊':'土','己':'土','庚':'金','辛':'金','壬':'水','癸':'水'}
STEM_POLARITY = {'甲':'yang','乙':'yin','丙':'yang','丁':'yin','戊':'yang','己':'yin','庚':'yang','辛':'yin','壬':'yang','癸':'yin'}

HIDDEN_STEMS = {
    '子':['癸'], '丑':['己','癸','辛'], '寅':['甲','丙','戊'], '卯':['乙'],
    '辰':['戊','乙','癸'], '巳':['丙','庚','戊'], '午':['丁','己'], '未':['己','丁','乙'],
    '申':['庚','壬','戊'], '酉':['辛'], '戌':['戊','辛','丁'], '亥':['壬','甲'],
}

GENERATES = {'木':'火','火':'土','土':'金','金':'水','水':'木'}
CONTROLS = {'木':'土','土':'水','水':'火','火':'金','金':'木'}

GOD_NAMES = {
    'bijian':'比肩','jiecai':'劫财','shishen':'食神','shangguan':'伤官',
    'piancai':'偏财','zhengcai':'正财','qisha':'七杀','zhengguan':'正官',
    'pianyin':'偏印','zhengyin':'正印',
}

# ============ 节气数据 (1900-2100) ============
# 每年24节气的日期数据，用于精确确定月柱
# 立春为年的分界，各节气为月的分界

# 节气月份对应：立春-惊蛰=寅月(1), 惊蛰-清明=卯月(2), ...
JIE_QI_MONTHS = ['寅','卯','辰','巳','午','未','申','酉','戌','亥','子','丑']

def solar_to_jd(year, month, day):
    """公历转儒略日"""
    if month <= 2:
        year -= 1
        month += 12
    A = int(year / 100)
    B = 2 - A + int(A / 4)
    return int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + B - 1524.5

def get_year_stem_branch(year, month, day):
    """年柱：以立春为界。简化处理：2月4日前算上一年"""
    # 立春一般在2月3-5日，这里用2月4日作为近似值
    if month < 2 or (month == 2 and day < 4):
        year -= 1
    stem_idx = (year - 4) % 10
    branch_idx = (year - 4) % 12
    return STEMS[stem_idx], BRANCHES[branch_idx]

def get_month_stem_branch(year, month, day):
    """月柱：以节气为界"""
    # 节气日期近似表（每月节气大约日期）
    jie_dates = [
        (2, 4),   # 立春 → 寅月开始
        (3, 6),   # 惊蛰 → 卯月开始
        (4, 5),   # 清明 → 辰月开始
        (5, 6),   # 立夏 → 巳月开始
        (6, 6),   # 芒种 → 午月开始
        (7, 7),   # 小暑 → 未月开始
        (8, 7),   # 立秋 → 申月开始
        (9, 8),   # 白露 → 酉月开始
        (10, 8),  # 寒露 → 戌月开始
        (11, 7),  # 立冬 → 亥月开始
        (12, 7),  # 大雪 → 子月开始
        (1, 6),   # 小寒 → 丑月开始
    ]

    # 确定月支
    lunar_month = 11  # 默认丑月
    for i, (jm, jd) in enumerate(jie_dates):
        next_jm, next_jd = jie_dates[(i + 1) % 12]
        if jm == month and day >= jd:
            if i < 11:
                next_check_month, next_check_day = jie_dates[i + 1]
                if month < next_check_month or (month == next_check_month and day < next_check_day):
                    lunar_month = i
                    break
            else:
                lunar_month = i
                break

    # 更精确的判断
    month_branch_idx = -1
    for i in range(12):
        jm, jd = jie_dates[i]
        njm, njd = jie_dates[(i + 1) % 12]
        if jm <= njm or i == 11:
            if i == 11:  # 丑月跨年
                if (month == jm and day >= jd) or (month == njm and day < njd) or (month == 1 and day < njd):
                    month_branch_idx = i
                    break
            elif month == jm and day >= jd:
                if month < njm or (month == njm and day < njd):
                    month_branch_idx = i
                    break
        else:
            if (month == jm and day >= jd) or month > jm:
                if month < njm or (month == njm and day < njd):
                    month_branch_idx = i
                    break

    if month_branch_idx == -1:
        # Fallback：按月份近似
        month_branch_idx = (month + 9) % 12

    month_branch = JIE_QI_MONTHS[month_branch_idx]
    branch_idx = BRANCHES.index(month_branch)

    # 年干定月干（五虎遁）
    year_stem, _ = get_year_stem_branch(year, month, day)
    year_stem_idx = STEMS.index(year_stem)
    # 甲己之年丙寅头，乙庚之年戊寅头...
    month_stem_start = [2, 4, 6, 8, 0][year_stem_idx % 5]  # 寅月天干起始
    month_stem_idx = (month_stem_start + month_branch_idx) % 10

    return STEMS[month_stem_idx], month_branch

def get_day_stem_branch(year, month, day):
    """日柱：基于已知参考日推算
    参考日：1900年1月1日 = 甲戌日 (stem=0, branch=10) → 六十甲子第10位
    """
    jd = solar_to_jd(year, month, day)
    jd_ref = solar_to_jd(1900, 1, 1)  # 甲戌日
    diff = int(jd - jd_ref)

    ref_sexagenary = 10  # 甲戌 = 第10位
    sexagenary = (ref_sexagenary + diff) % 60

    stem_idx = sexagenary % 10
    branch_idx = sexagenary % 12
    return STEMS[stem_idx], BRANCHES[branch_idx]

def get_hour_branch(hour):
    """时支"""
    if hour == 23:
        return '子'
    idx = (hour + 1) // 2
    return BRANCHES[idx % 12]

def get_hour_stem(day_stem, hour):
    """时干：日上起时法"""
    day_idx = STEMS.index(day_stem)
    branch_idx = (hour + 1) // 2 % 12
    start_idx = (day_idx % 5) * 2
    return STEMS[(start_idx + branch_idx) % 10]

def derive_ten_god(day_stem, other_stem):
    """推算十神"""
    de = STEM_ELEMENTS[day_stem]
    dp = STEM_POLARITY[day_stem]
    oe = STEM_ELEMENTS[other_stem]
    op = STEM_POLARITY[other_stem]
    same = dp == op

    if de == oe:
        return 'bijian' if same else 'jiecai'
    if GENERATES[de] == oe:
        return 'shishen' if same else 'shangguan'
    if GENERATES[oe] == de:
        return 'pianyin' if same else 'zhengyin'
    if CONTROLS[de] == oe:
        return 'piancai' if same else 'zhengcai'
    if CONTROLS[oe] == de:
        return 'qisha' if same else 'zhengguan'
    return None

def calculate(year, month, day, hour):
    year_s, year_b = get_year_stem_branch(year, month, day)
    month_s, month_b = get_month_stem_branch(year, month, day)
    day_s, day_b = get_day_stem_branch(year, month, day)
    hour_s = get_hour_stem(day_s, hour)
    hour_b = get_hour_branch(hour)

    pillars = {
        'year':  {'stem': year_s, 'branch': year_b},
        'month': {'stem': month_s, 'branch': month_b},
        'day':   {'stem': day_s, 'branch': day_b},
        'hour':  {'stem': hour_s, 'branch': hour_b},
    }

    # Ten gods calculation with weights
    god_counts = {}
    pillar_weights = {'year': 1, 'month': 3, 'day': 0, 'hour': 1}

    for pillar, data in pillars.items():
        # Heavenly stem
        if pillar != 'day':
            god = derive_ten_god(day_s, data['stem'])
            if god:
                god_counts[god] = god_counts.get(god, 0) + pillar_weights[pillar]

        # Hidden stems
        for i, h_stem in enumerate(HIDDEN_STEMS.get(data['branch'], [])):
            god = derive_ten_god(day_s, h_stem)
            if god:
                weight = 2 if i == 0 else 0.5
                god_counts[god] = god_counts.get(god, 0) + weight

    # Normalize
    max_count = max(god_counts.values()) if god_counts else 1
    all_gods = ['bijian','jiecai','shishen','shangguan','piancai','zhengcai','qisha','zhengguan','pianyin','zhengyin']
    ten_gods = {}
    for god in all_gods:
        raw = god_counts.get(god, 0)
        score = round(min(5, (raw / max_count) * 5), 1) if max_count > 0 else 0
        if score >= 4:
            level = '旺'
        elif score >= 2:
            level = '中'
        elif score > 0:
            level = '弱'
        else:
            level = '缺'
        ten_gods[god] = {'score': score, 'count': round(raw, 1), 'level': level, 'name': GOD_NAMES[god]}

    return {
        'fourPillars': pillars,
        'dayMaster': day_s,
        'dayMasterElement': STEM_ELEMENTS[day_s],
        'dayMasterPolarity': '阳' if STEM_POLARITY[day_s] == 'yang' else '阴',
        'tenGods': ten_gods,
    }

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('用法: python3 bazi-calc.py <年> <月> <日> <时(0-23)>', file=sys.stderr)
        print('示例: python3 bazi-calc.py 1995 3 15 14', file=sys.stderr)
        sys.exit(1)

    year, month, day, hour = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    result = calculate(year, month, day, hour)
    print(json.dumps(result, ensure_ascii=False, indent=2))
