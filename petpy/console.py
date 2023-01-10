from petpy.base_task import TaskInfo
from petpy.rmi_proxy import RMIProxy, RMICallee, RMICaller


class Console:
    task_info_map: dict[str, TaskInfo] = {}
    local_caller, local_callee = RMIProxy.get_local_pair()

    def __init__(self) -> None:
        pass

    def start(self) -> None:
        pass

    def progress_new(self, task_id: str, init_total: int):
        pass

    def progress_set(self, task_id: str, step: int, total: int):
        pass

    def progress_add(self, task_id: str, exp_total: int):
        pass

    def progress_step(self, task_id: str, step: int):
        pass
