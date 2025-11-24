import os
from typing import Dict, Any
from pathlib import Path
import yaml

class SDKConfig:
    """SDK configuration management"""
    
    DEFAULT_CONFIG = {
        "base_url": "http://localhost:8007",
        "timeout": 30,
        "retry_attempts": 3,
        "cache_enabled": True,
        "log_level": "INFO",
        "agents": {
            "threat_intel": "http://localhost:8001",
            "forecaster": "http://localhost:8008", 
            "reporter": "http://localhost:8009",
            "validator": "http://localhost:8002"
        }
    }
    
    def __init__(self, config_path: str = None):
        self.config = self.DEFAULT_CONFIG.copy()
        
        # Load from environment variables
        self._load_from_env()
        
        # Load from config file
        if config_path and Path(config_path).exists():
            self._load_from_file(config_path)
        else:
            # Try default locations
            default_paths = [
                "cyber_intel_config.yaml",
                "~/.cyber_intel/config.yaml",
                "/etc/cyber_intel/config.yaml"
            ]
            for path in default_paths:
                expanded_path = Path(path).expanduser()
                if expanded_path.exists():
                    self._load_from_file(expanded_path)
                    break
    
    def _load_from_env(self):
        """Load configuration from environment variables"""
        env_mappings = {
            'CYBER_INTEL_BASE_URL': 'base_url',
            'CYBER_INTEL_API_KEY': 'api_key', 
            'CYBER_INTEL_TIMEOUT': 'timeout',
            'CYBER_INTEL_LOG_LEVEL': 'log_level'
        }
        
        for env_var, config_key in env_mappings.items():
            if env_var in os.environ:
                self.config[config_key] = os.environ[env_var]
    
    def _load_from_file(self, config_path: Path):
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                file_config = yaml.safe_load(f) or {}
                self.config.update(file_config)
        except Exception as e:
            print(f"Warning: Failed to load config from {config_path}: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def get_agent_url(self, agent_name: str) -> str:
        """Get agent endpoint URL"""
        return self.config['agents'].get(agent_name)

# Global configuration instance
_config = None

def get_config(config_path: str = None) -> SDKConfig:
    """Get or create configuration instance"""
    global _config
    if _config is None:
        _config = SDKConfig(config_path)
    return _config
