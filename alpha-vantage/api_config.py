"""
API Configuration for multiple APIs with parameter definitions and values.
Designed for dynamic URL construction.
"""
import requests
import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path
import sys



API_CONFIGS = {
    "alpha_vantage": {
        "base_url": "https://www.alphavantage.co/query",
        "functions": {
            "NEWS_SENTIMENT": {
                "required": ["function", "apikey"],
                "optional": ["tickers", "topics", "time_from", "time_to", "sort", "limit"],
                "defaults": {
                    "sort": "LATEST",
                    "limit": 50
                },
                "current_values": {
                    "function": "NEWS_SENTIMENT",
                    "topics": "technology,retail_wholesale,real_estate",
                    "tickers": "NVDA,AAPL,MSFT",
                    "time_from": "20250101T0000",
                    "time_to": "20250630T2359",
                    "limit": 100
                }
            },
            "TIME_SERIES_DAILY_ADJUSTED": {
                "required": ["function", "symbol", "apikey"],
                "optional": ["outputsize", "datatype"],
                "defaults": {
                    "outputsize": "compact",
                    "datatype": "json"
                },
                "current_values": {
                    "function": "TIME_SERIES_DAILY_ADJUSTED",
                    "symbol": "NVDA",
                    "outputsize": "full",
                    "datatype": "csv"
                }
            },
            "GLOBAL_QUOTE": {
                "required": ["function", "symbol", "apikey"],
                "optional": ["datatype"],
                "defaults": {
                    "datatype": "json"
                },
                "current_values": {
                    "function": "GLOBAL_QUOTE",
                    "symbol": "NVDA"
                }
            },
            "SYMBOL_SEARCH": {
                "required": ["function", "keywords", "apikey"],
                "optional": ["datatype"],
                "defaults": {
                    "datatype": "json"
                },
                "current_values": {
                    "function": "SYMBOL_SEARCH",
                    "keywords": "nvidia"
                }
            }
        }
    },
    # Future APIs can be added here
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "functions": {
            "chat_completions": {
                "required": ["model", "messages"],
                "optional": ["temperature", "max_tokens", "top_p"],
                "defaults": {
                    "temperature": 0.7,
                    "max_tokens": 1000
                },
                "current_values": {
                    "model": "gpt-4",
                    "temperature": 0.5
                }
            }
        }
    }
}

def build_url(api_name, function_name, api_key, **override_params):
    """
    Build API URL using configuration and current values.
    
    Args:
        api_name: e.g., "alpha_vantage"
        function_name: e.g., "NEWS_SENTIMENT"
        api_key: API key to use
        **override_params: Any parameters to override current_values
    
    Returns:
        Complete URL string ready for requests
    """
    if api_name not in API_CONFIGS:
        raise ValueError(f"Unknown API: {api_name}")
    
    api_config = API_CONFIGS[api_name]
    
    if function_name not in api_config["functions"]:
        raise ValueError(f"Unknown function: {function_name} for API: {api_name}")
    
    func_config = api_config["functions"][function_name]
    
    # Start with defaults
    params = func_config["defaults"].copy()
    
    # Add current values
    params.update(func_config["current_values"])
    
    # Add API key
    params["apikey"] = api_key
    
    # Override with any provided parameters
    params.update(override_params)
    
    # Validate required parameters
    missing_required = []
    for req_param in func_config["required"]:
        if req_param not in params:
            missing_required.append(req_param)
    
    if missing_required:
        raise ValueError(f"Missing required parameters: {missing_required}")
    
    # Build URL
    base_url = api_config["base_url"]
    param_string = "&".join([f"{key}={value}" for key, value in params.items()])
    
    return f"{base_url}?{param_string}"

def update_current_values(api_name, function_name, **new_values):
    """
    Update the current_values for a specific API function.
    
    Args:
        api_name: e.g., "alpha_vantage"
        function_name: e.g., "NEWS_SENTIMENT"
        **new_values: Parameters to update
    """
    if api_name in API_CONFIGS and function_name in API_CONFIGS[api_name]["functions"]:
        API_CONFIGS[api_name]["functions"][function_name]["current_values"].update(new_values)
    else:
        raise ValueError(f"Invalid API ({api_name}) or function ({function_name})")

def get_current_values(api_name, function_name):
    """Get current parameter values for a function."""
    return API_CONFIGS[api_name]["functions"][function_name]["current_values"].copy()

