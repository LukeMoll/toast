import ansible_runner

from .config import get_toastfile, config
from .action import update_repository

from .data import roles

import os, time

from threading import Thread, current_thread
from multiprocessing import Queue
from queue import Empty

from typing import Callable, Iterable, Mapping, Any, Optional

ROLES_DIR = os.path.normpath(os.path.dirname(roles.__file__))


def run_slice(s: dict):
    playbook = get_toastfile(s["path"])

    s_clone = dict(s)
    try:
        del s_clone["secret"]
    except KeyError:
        pass

    vars_dict = {"toast": {"slice": s_clone, "vars": config["toast"]["vars"]}}

    r = ansible_runner.run(
        playbook=playbook,
        inventory=[],
        roles_path=[ROLES_DIR],
        extravars=vars_dict,
    )


class AnsibleWorker(Thread):
    def __init__(
        self,
        group: None = None,
        target: Optional[Callable[..., Any]] = None,
        name: Optional[str] = None,
        args: Iterable[Any] = [],
        *,
        kwargs: Optional[Mapping[str, Any]] = None,
    ) -> None:
        super().__init__(
            group=group,
            target=target,
            name=name,
            args=args,
            kwargs=kwargs,
            daemon=True,
        )

        self._queue = Queue()

    def run(self) -> None:
        while True:
            t = current_thread()
            try:
                itm = self._queue.get(block=True, timeout=30)

                print(f"Processing slice {itm['upstream']}")
                print("Updating repository...")
                update_repository(itm)
                print("Running toastfile...")
                run_slice(itm)
            except Empty:
                time.sleep(1)

    def queue_slice(self, slice: dict):
        self._queue.put(slice)


worker = AnsibleWorker()
