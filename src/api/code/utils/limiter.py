#api/utils/limiter.py


# Lib
from slowapi import Limiter
from slowapi.util import get_remote_address

from utils.common_functions import get_jwt_token
from utils.config import LIMITER_TYPE, DEFAULT_LIMITS_FOR_LIMITER

""""
Limiter definition
- key_func: Function to extract the client IP address
"""
if LIMITER_TYPE == "ip":
    function_to_use = get_remote_address
    default_limits = DEFAULT_LIMITS_FOR_LIMITER
elif LIMITER_TYPE == "user":
    function_to_use = get_jwt_token
    default_limits = []



limiter = Limiter(key_func = function_to_use, default_limits = default_limits)