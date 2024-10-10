from gym.envs.registration import register
from .custom_env import Custom_Env

register(
    id='fiveg-v0',
    entry_point='ki_5g_env:Custom_Env'
)
