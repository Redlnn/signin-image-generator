#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from os.path import dirname, join
from pathlib import Path
from random import choices, randint
from typing import Optional
from uuid import uuid4

from model import Reward, UserInfo
from util import get_signin_img


def main():
    font_path = Path('fonts', 'OPPOSans-B.ttf')
    # 查询用户信息
    # result: Optional[tuple[UserInfo]] = await Database.select_first(select(UserInfo).where(UserInfo.qq == member.id))
    result: Optional[tuple[UserInfo]] = (UserInfo(qq='10086'),)
    user: UserInfo = UserInfo(qq=str(10086)) if result is None else result[0]
    # 判断时间戳是不是今天
    if time.localtime(user.last_signin_time).tm_yday == time.localtime().tm_yday:
        # await app.sendMessage(group, MessageChain.create(Plain(f'你今天已经签到过了哦~')), quote=source)
        return

    # 签到成功，总天数 +1
    user.total_signin_days += 1

    # 判断是否连签
    if user.total_signin_days <= 1 or time.time() - user.last_signin_time > 86400:
        is_signin_consecutively = False
        user.consecutive_signin_days = 0
    else:
        is_signin_consecutively = True
        user.consecutive_signin_days += 1

    # 计算经验及奖励增加数量
    added_coin = randint(3, 8)
    added_gold = choices([1, 2, 3], weights=[89, 10, 1])[0]
    added_exp = randint(2, 10)

    user.coin += added_coin
    user.gold += added_gold
    user.exp += added_exp
    user.last_signin_time = int(time.time())

    # 写回数据库
    # if not await Database.update_exist(user):
    #     await app.sendMessage(group, MessageChain.create(Plain('签到数据保存失败，请联系 Bot 主人')))
    #     return

    # Lv1 <500
    # Lv2 <1500
    # Lv3 <3000
    # Lv4 <5000
    # Lv5 <7500
    # Lv6 <10500
    levels = {
        0: 0,
        1: 500,
        2: 1500,
        3: 3000,
        4: 5000,
        5: 7500,
        6: 10500,
        7: 10500,
    }
    if user.exp >= 10500:
        level = 6
    elif user.exp >= 7500:
        level = 5
    elif user.exp >= 5000:
        level = 4
    elif user.exp >= 3000:
        level = 3
    elif user.exp >= 1500:
        level = 2
    elif user.exp >= 500:
        level = 1
    else:
        level = 0

    img_bytes = get_signin_img(
        qq=user.qq,
        name="群菜鸮",
        uuid=uuid4(),
        level=level,
        exp=(user.exp - levels[level], levels[level + 1]),
        total_days=user.total_signin_days,
        consecutive_days=user.consecutive_signin_days,
        is_signin_consecutively=is_signin_consecutively,
        rewards=[
            Reward(name='经验', num=added_exp),
            Reward(num=added_coin, ico=join(dirname(__file__), 'imgs', '原石.png')),
            Reward(num=added_gold, ico=join(dirname(__file__), 'imgs', '纠缠之缘.png')),
        ],
        font_path=str(font_path),
    )

    # 发送签到图片
    # await app.sendMessage(group, MessageChain.create(Image(data_bytes=img_bytes)))


if __name__ == '__main__':
    main()
