"""
 * author: AK
 * created on 28-02-2025-16h-25m
 * github: https://github.com/TRC-Loop
 * email: ak@stellar-code.com
 * copyright 2025
"""

import yaml
import os
import shutil
import datetime
import uuid

def load_config():
    if not os.path.exists('config.yaml'):
        with open('config.yaml', 'w') as file:
            yaml.dump({
                'backup_dir': './backups/',
                'db': 'sqlite.db',
                'max_backups': 5
            }, file)
    with open('config.yaml') as file:
        return yaml.load(file, Loader=yaml.SafeLoader)

CONFIG = load_config()

def get_config(key: str, default=None):
    global CONFIG
    return CONFIG[key] if key in CONFIG else default



BACKUP_DIR = get_config('backup_dir', './backups/')
DB_DIR = get_config('db', 'sqlite.db')
MAX_BACKUPS = get_config('max_backups', 5)