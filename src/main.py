import atexit
import bottle
import signal
import player
import log

def handle_termination_signal(signum: signal.Signals, frame):
    log.bottle.info(f'Received termination signal ({signum}). Exiting...')
    atexit._run_exitfuncs()
    exit()

if __name__ == '__main__':
    atexit.register(player.update_players_data)
    signal.signal(signal.SIGTERM, handle_termination_signal)
    signal.signal(signal.SIGINT, handle_termination_signal)
    bottle.run()