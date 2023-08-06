#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from base import ApolloClientBase
from util import get_value_from_dict, no_key_cache_key


class ApolloClient(ApolloClientBase):

    def get_value(self, key, default_val=None, namespace='application'):
        try:
            # 读取内存配置
            namespace_cache = self._cache.get(namespace)
            val = get_value_from_dict(namespace_cache, key)
            if val is not None:
                return val

            no_key = no_key_cache_key(namespace, key)
            if no_key in self._no_key:
                return default_val

            # 读取网络配置
            namespace_data = self.get_json_from_net(namespace)
            val = get_value_from_dict(namespace_data, key)
            if val is not None:
                self._update_cache_and_file(namespace_data, namespace)
                return val

            # 读取文件配置
            namespace_cache = self._get_local_cache(namespace)
            val = get_value_from_dict(namespace_cache, key)
            if val is not None:
                self._update_cache_and_file(namespace_cache, namespace)
                return val

            # 如果全部没有获取，则把默认值返回，设置本地缓存为None
            self._set_local_cache_none(namespace, key)
            return default_val
        except Exception as e:
            self.logger.error(
                "get_value has error, [key is %s], [namespace is %s], [error is %s], ",key, namespace, e
            )
            return default_val

    def get_debug(self, key='DEBUG', default_val=None, **kwargs):
        debug_v = self.get_value(key=key, default_val=default_val, **kwargs)
        if debug_v in ('on', True, 1, '1'):
            debug_v = True
        else:
            debug_v = False
        return debug_v

    def get_json(self, key, default_val=None, namespace='application'):
        """将数据解析成JSON"""
        value = self.get_value(key=key, default_val=default_val, namespace=namespace)
        try:
            value = json.loads(value)
        except Exception as e:
            pass
        return value
