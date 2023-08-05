from cloudam_stream.core.constants import actor_constant
from cloudam_stream.core.utils import redis_utils


class FlowStateUtils(object):
    def __init__(self, redis_client):
        self.redis_client = redis_client

    '''
    save算子间的关系
    '''

    def save_upstream_actors(self, upstreams: dict):
        for actor_name, upstreams_actors in upstreams.items():
            self.redis_client.hset(actor_constant.REDIS_KEY_FOR_ACTOR_RELATION, actor_name, str(upstreams_actors))

    '''
    查询算子间的关系
    '''

    def get_upstream_actors(self) -> dict:
        bytes_dict = self.redis_client.hgetall(actor_constant.REDIS_KEY_FOR_ACTOR_RELATION)
        return redis_utils.decode_byte_dict(bytes_dict)

    '''
    设置actor状态
    '''

    def update_actor_state(self, actor_name, parallel_index, state):
        if isinstance(parallel_index, int):
            parallel_index = str(parallel_index)
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
        return state

    '''
    设置某一actor的整体状态
    '''

    def set_actor_final_state(self, actor_name):
        state = None
        state_map = self.redis_client.hgetall(actor_constant.REDIS_KEY_FOR_ACTOR_STATE + '_' + actor_name)
        if state_map:
            state_map = redis_utils.decode_byte_dict(state_map)
            values = state_map.values()
            for value in values:
                if actor_constant.ACTOR_STATE_RUNNING == value:
                    state = actor_constant.ACTOR_STATE_RUNNING
                    break
                if actor_constant.ACTOR_STATE_FAILED == value:
                    state = actor_constant.ACTOR_STATE_FAILED
        # 保存算子整体状态
        self.redis_client.hset(actor_constant.REDIS_KEY_FOR_ACTOR_FINAL_STATE, actor_name, state)
        return state
    '''
    查询某一actor的整体状态
    '''

    def get_actor_final_state(self, actor_name):
        # 查询算子整体状态
        state = self.redis_client.hget(actor_constant.REDIS_KEY_FOR_ACTOR_FINAL_STATE, actor_name)
        return state

    # '''
    # 查询所有actor的job_id
    # '''
    #
    #
    # def get_actor_name_by_job_id(self, job_id):
    #     actor_name = self.redis_client.hget(actor_constant.REDIS_KEY_FOR_JOB_MAPPING, job_id)
    #     if actor_name:
    #         actor_name = actor_name.decode()
    #     return actor_name
    #
    #
    # '''
    # 保存actor的job_id
    # '''
    #
    #
    # def set_job_id(self, actor_name, job_id):
    #     if (not actor_name) or (not job_id):
    #         return
    #     self.redis_client.hset(actor_constant.REDIS_KEY_FOR_JOB_MAPPING, job_id, actor_name, )
