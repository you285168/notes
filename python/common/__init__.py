from .log import init_log
from .mysql import create_pool, execute
from .orm import Model

class mysql:
    create_pool = create_pool
    execute = execute
    Model = Model

(init_log, mysql)