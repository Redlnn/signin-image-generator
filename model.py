#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from pydantic import BaseModel
from typing import Optional, Union


class UserInfo(BaseModel):
    qq: str
    exp: int = 0
    coin: int = 0
    gold: int = 0
    total_signin_days: int = 0
    consecutive_signin_days: int = 0
    last_signin_time: int = 0



class Reward(BaseModel):
    """奖励"""

    name: Optional[str] = None
    """奖励名称"""

    num: int
    """奖励数量"""

    ico: Optional[Union[str, Path]] = None
    """奖励图标"""

