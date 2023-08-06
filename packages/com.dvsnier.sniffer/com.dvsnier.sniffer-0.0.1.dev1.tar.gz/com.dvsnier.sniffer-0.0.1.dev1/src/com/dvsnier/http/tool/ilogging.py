# -*- coding:utf-8 -*-

import logging

from com.dvsnier.config.journal.common_config import config


class ILogging(object):
    '''the Template class'''
    def __init__(self):
        super(ILogging, self).__init__()

    def set_logging(self, _on_callback=None):
        '''
            the set method

            the default set params that is above:

            {
                'output_dir_name': 'http',
                'file_name': 'log',
                'level': logging.DEBUG
            }
        '''
        kwargs = {'output_dir_name': 'http', 'file_name': 'log', 'level': logging.DEBUG}
        if _on_callback:
            kwargs = _on_callback()
        config(kwargs)
