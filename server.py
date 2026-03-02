class Server:
    def __init__(self, root, database):
        self._root = root
        self._database = database

        # waittime db update
        self._waittime_job = None

        self._schedule_waittime_update()

    def _schedule_waittime_update(self):
        if self._waittime_job is not None:
            self._root.after_cancel(self._waittime_job)
        self._waittime_job = self._root.after(30_000, self._update_waittimes_db)

    def _update_waittimes_db(self):
        self._database.decrease_waittime_for_all_orders()
        self._schedule_waittime_update()

    def cancel_waittime_update(self):
        if self._waittime_job:
            self._root.after_cancel(self._waittime_job)
            self._waittime_job = None