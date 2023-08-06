
from honcho.manager import Manager
from honcho.process import Process
import signal

SIGNALS = {
    signal.SIGINT: {
        'name': 'SIGINT',
        'rc': 130,
    },
    signal.SIGTERM: {
        'name': 'SIGTERM',
        'rc': 143,
    },
}
SYSTEM_PRINTER_NAME = 'system'


class AllStopManager(Manager):

    def loop(self):
        """
        Start all the added processes and multiplex their output onto the bound
        printer (which by default will print to STDOUT).

        If one process terminates, all the others will be terminated by
        Honcho, and :func:`~honcho.manager.Manager.loop` will return.

        This method will block until all the processes have terminated.
        """
        def _terminate(signum, frame):
            self._system_print("%s received\n" % SIGNALS[signum]['name'])
            self.returncode = SIGNALS[signum]['rc']
            self.terminate()
        import signal
        from multiprocessing.queues import Empty
        import datetime
        KILL_WAIT = 5
        signal.signal(signal.SIGTERM, _terminate)
        signal.signal(signal.SIGINT, _terminate)


        self._start()

        exit = False
        exit_start = None

        while 1:
            try:
                msg = self.events.get(timeout=0.1)
            except Empty:
                if exit:
                    break
            else:
                if msg.type == 'line':
                    self._printer.write(msg)
                elif msg.type == 'start':
                    self._processes[msg.name]['pid'] = msg.data['pid']
                    self._system_print("%s started (pid=%s)\n"
                                       % (msg.name, msg.data['pid']))
                elif msg.type == 'stop':
                    self._processes[msg.name]['returncode'] = msg.data['returncode']
                    self._system_print("%s stopped (rc=%s)\n"
                                       % (msg.name, msg.data['returncode']))
                    if self.returncode is None:
                        self.returncode = msg.data['returncode']

            if self._all_started() and self._all_stopped():
                exit = True

            # if exit_start is None and self._all_started():
            #     # if self._any_stopped() and self.exit_on_any_stop:
            #     #     exit_start = self._env.now()
            #     #     self.terminate()
            #     if self._all_stopped():
            #         exit_start = self._env.now()
            #         self.terminate()

            # if exit_start is not None:
            #     # If we've been in this loop for more than KILL_WAIT seconds,
            #     # it's time to kill all remaining children.
            #     waiting = self._env.now() - exit_start
            #     if waiting > datetime.timedelta(seconds=KILL_WAIT):
            #         self.kill()
