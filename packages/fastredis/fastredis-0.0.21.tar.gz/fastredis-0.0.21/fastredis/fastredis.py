#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
from .basic import Basics
import showlog
import envx

default_db = 0  # 默认数据库
default_env_file_name = 'local.redis.env'  # 默认链接信息文件


def make_con_info(
        env_file_name: str = default_env_file_name
):
    # ---------------- 固定设置 ----------------
    inner_env = envx.read(file_name=env_file_name)
    if inner_env is None or len(inner_env) == 0:
        showlog.warning('[%s]文件不存在或文件填写错误！' % env_file_name)
        exit()
    else:
        max_connections = inner_env.get('max_connections')
        if max_connections is not None:
            try:
                max_connections = int(max_connections)
            except:
                showlog.warning('max_connections必须是数字！')
        else:
            max_connections = None
        con_info = {
            "host": inner_env.get('host', 'localhost'),
            "port": int(inner_env.get('port', '6379')),
            "password": inner_env.get('password'),
            "max_connections": max_connections,
        }
        return con_info


def delete_key(
        key,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name,
        auto_reconnect: bool = True,  # 自动重连
        reconnect_delay: int = 1  # 重连延时，单位为秒
) -> dict:
    """
    删除 key
    """
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.delete_key(
        key=key,
        auto_reconnect=auto_reconnect,
        reconnect_delay=reconnect_delay
    )


def list_add_r(
        key,
        value,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name
):
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    else:
        pass
    if db is None:
        db = 0
    else:
        pass
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.list_add_r(
        key=key,
        value=value
    )


def list_pop_l(
        key,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name
):
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    else:
        pass
    if db is None:
        db = 0
    else:
        pass
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.list_pop_l(
        key=key
    )


def read_list_key_values(
        key,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name
):
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    else:
        pass
    if db is None:
        db = 0
    else:
        pass
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.read_list_key_values_all(
        key=key
    )


def keys(
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name
):
    """
    获取键列表
    """
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    else:
        pass
    if db is None:
        db = 0
    else:
        pass
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.get_db_key_list()


def read_list_first_value(
        key,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name
):
    # 获取列表的第一个元素
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    else:
        pass
    if db is None:
        db = 0
    else:
        pass
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.read_list_first_value(
        key=key
    )


def read_list_last_value(
        key,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name
):
    # 获取列表的最后一个元素
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    else:
        pass
    if db is None:
        db = 0
    else:
        pass
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.read_list_last_value(
        key=key
    )


def count_set(
        key,
        value,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name
):
    # 键 计数 设定值
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    else:
        pass
    if db is None:
        db = 0
    else:
        pass
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.count_set(
        key=key,
        value=value
    )


def count_add(
        key,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name
):
    # 键 计数 增加1
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    else:
        pass
    if db is None:
        db = 0
    else:
        pass
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.count_add(
        key=key
    )


def count_reduce(
        key,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name
):
    # 键 计数 减少1
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    else:
        pass
    if db is None:
        db = 0
    else:
        pass
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.count_reduce(
        key=key
    )


def count_get(
        key,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name
):
    # 键 计数 获取值
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    else:
        pass
    if db is None:
        db = 0
    else:
        pass
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.count_get(
        key=key
    )


def read_list_key_values_length(
        key,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name
):
    # 键 获取列表元素数量
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    else:
        pass
    if db is None:
        db = 0
    else:
        pass
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.get_list_key_values_count(
        key=key
    )


# -------------------- hash --------------------


def hash_set(
        name,
        key,
        value,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name
):
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    else:
        pass
    if db is None:
        db = 0
    else:
        pass
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.hash_set(
        name=name,
        key=key,
        value=value,
    )


def hash_keys(
        name,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name
):
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    else:
        pass
    if db is None:
        db = 0
    else:
        pass
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.hash_keys(
        name=name
    )


def hash_get(
        name,
        key,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name
):
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    else:
        pass
    if db is None:
        db = 0
    else:
        pass
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.hash_get(
        name=name,
        key=key
    )


def hash_get_many(
        name,
        key_list: list,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name
):
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    else:
        pass
    if db is None:
        db = 0
    else:
        pass
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.hash_get_many(
        name=name,
        key_list=key_list
    )


def hash_get_all(
        name,
        db: int = default_db,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name,
        auto_reconnect: bool = True,  # 自动重连
        decode: bool = True
) -> dict:
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    else:
        pass
    if db is None:
        db = 0
    else:
        pass
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.hash_get_all(
        name=name,
        auto_reconnect=auto_reconnect,
        decode=decode
    )
