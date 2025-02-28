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
import sys
import zipfile

def load_config():
    config_path = 'config.yaml'
    default_config = {
        'backup_dir': './backups/',
        'db': 'sqlite.db',
        'max_backups': 5,
        'compression': -1,
        'silent': False
    }
    
    if not os.path.exists(config_path):
        with open(config_path, 'w') as file:
            yaml.dump(default_config, file)
    
    with open(config_path) as file:
        return yaml.safe_load(file) or default_config

def get_config(key: str, default=None):
    return CONFIG.get(key, default)

def log(*args):
    if not SILENT:
        print(*args)

def ensure_directory(path):
    try:
        os.makedirs(path, exist_ok=True)
    except Exception as e:
        log(f"Error creating directory {path}: {e}")
        sys.exit(1)

def backup_database():
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    unique_id = uuid.uuid4().hex
    backup_path = os.path.join(BACKUP_DIR, f"{timestamp}_{unique_id}")
    
    try:
        if COMPRESSION_LEVEL == -1:
            backup_file = f"{backup_path}{DB_EXTENSION}"
            shutil.copy(DB, backup_file)
        else:
            backup_file = f"{backup_path}.zip"
            compression = zipfile.ZIP_STORED if COMPRESSION_LEVEL == 0 else zipfile.ZIP_DEFLATED
            with zipfile.ZipFile(backup_file, 'w', compression=compression) as zipf:
                zipf.write(DB, os.path.basename(DB))
        
        log(f"Backup successful: {backup_file}")
    except Exception as e:
        log(f"Backup failed: {e}")
        sys.exit(1)
    
    if MAX_BACKUPS != -1:
        cleanup_old_backups()

def cleanup_old_backups():
    try:
        backups = sorted(
            [os.path.join(BACKUP_DIR, f) for f in os.listdir(BACKUP_DIR)],
            key=os.path.getctime, reverse=True
        )
        
        if len(backups) > MAX_BACKUPS:
            for old_backup in backups[MAX_BACKUPS:]:
                try:
                    os.remove(old_backup)
                    log(f"Deleted old backup: {old_backup}")
                except Exception as e:
                    log(f"Failed to delete {old_backup}: {e}")
    except Exception as e:
        log(f"Error during cleanup: {e}")

CONFIG = load_config()
BACKUP_DIR = get_config('backup_dir', './backups/')
DB = get_config('db', 'sqlite.db')
MAX_BACKUPS = get_config('max_backups', 5)
COMPRESSION_LEVEL = get_config('compression', -1)
SILENT = get_config('silent', False)
DB_EXTENSION = os.path.splitext(DB)[1]

ensure_directory(BACKUP_DIR)

if not os.path.exists(DB):
    log(f"Database file not found: {DB}")
    sys.exit(1)

backup_database()