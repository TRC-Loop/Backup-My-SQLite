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
        'databases': ['sqlite.db'],
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

def backup_database(db_path):
    if not os.path.exists(db_path):
        log(f"Database file not found: {db_path}")
        return
    
    db_name = os.path.basename(db_path)
    db_ext = os.path.splitext(db_name)[1]
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    unique_id = uuid.uuid4().hex
    db_backup_dir = os.path.join(BACKUP_DIR, db_name)
    ensure_directory(db_backup_dir)
    
    backup_filename = f"{db_name}_{timestamp}_{unique_id}{db_ext if COMPRESSION_LEVEL == -1 else '.zip'}"
    backup_path = os.path.join(db_backup_dir, backup_filename)
    
    try:
        if COMPRESSION_LEVEL == -1:
            shutil.copy(db_path, backup_path)
        else:
            compression = zipfile.ZIP_STORED if COMPRESSION_LEVEL == 0 else zipfile.ZIP_DEFLATED
            with zipfile.ZipFile(backup_path, 'w', compression=compression) as zipf:
                zipf.write(db_path, db_name)
        log(f"Backup successful: {backup_path}")
    except Exception as e:
        log(f"Backup failed for {db_name}: {e}")
        return
    
    if MAX_BACKUPS != -1:
        cleanup_old_backups(db_backup_dir)

def cleanup_old_backups(db_backup_dir):
    try:
        backups = sorted(
            [os.path.join(db_backup_dir, f) for f in os.listdir(db_backup_dir)],
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
DATABASES = get_config('databases', ['sqlite.db'])
MAX_BACKUPS = get_config('max_backups', 5)
COMPRESSION_LEVEL = get_config('compression', -1)
SILENT = get_config('silent', False)

ensure_directory(BACKUP_DIR)

for db in DATABASES:
    backup_database(db)
