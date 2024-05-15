import threading


class MasterReplicaRouter:
    def __init__(self):
        self.read_counter = threading.local()

    def db_for_read(self, model, **hints):
        if not hasattr(self.read_counter, 'value'):
            self.read_counter.value = 0

        # Update round-robin algorithm for three replicas
        self.read_counter.value = (self.read_counter.value + 1) % 3
        if self.read_counter.value == 0:
            return 'replica1'
        elif self.read_counter.value == 1:
            return 'replica2'
        else:
            return 'replica3'

    def db_for_write(self, model, **hints):
        return 'master'

    # The rest of the router class remains unchanged


class PrimaryReplicaRouter:
    def db_for_read(self, model, **hints):
        return 'default' if hints.get('instance') else 'replica_1'

    def db_for_write(self, model, **hints):
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == 'default'
