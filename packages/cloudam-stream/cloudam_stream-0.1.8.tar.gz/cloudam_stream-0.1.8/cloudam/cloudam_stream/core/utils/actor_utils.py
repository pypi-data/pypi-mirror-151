from loguru import logger

from core.constants import actor_constant


class FlowStateUtils(object):
    def __init__(self, redis_client):
        self.redis_client = redis_client

    '''
    设置actor状态
    '''

    def update_actor_state(self, actor_name, parallel_index, state):
        if isinstance(parallel_index, int):
            parallel_index = str(parallel_index)
        logger.info('【update_actor_state】actor_name:{},parallel_index:{}------>state:{}', actor_name, parallel_index,
                    state)
        self.redis_client.hset(actor_constant.REDIS_KEY_FOR_ACTOR_STATE + '_' + actor_name, parallel_index, state)

    '''
    查询actor在某一job下的状态
    '''

    def get_actor_state(self, actor_name, parallel_index):
        if isinstance(parallel_index, int):
            parallel_index = str(parallel_index)
        state = self.redis_client.hget(actor_constant.REDIS_KEY_FOR_ACTOR_STATE + '_' + actor_name, parallel_index)
        if state:
            state = state.decode()
        logger.info('【get_actor_state】actor_name:{},parallel_index:{}------>state:{}', actor_name, parallel_index,
                    state)
        return state

    '''
    查询某一actor的整体状态
    '''

    def get_actor_final_state(self, actor_name):
        # 查询算子整体状态
        state = self.redis_client.hget(actor_constant.REDIS_KEY_FOR_ACTOR_FINAL_STATE, actor_name)
        logger.info('【get_actor_final_state】actor_name:{}------>state:{}', actor_name, state)
        return state
