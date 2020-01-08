import players
import pong
import threading

if __name__ == "__main__":
    player = players.Player()
    player.connect_to_server()
    game_thread = threading.Thread(target=pong.run_game)
    peer_thread = threading.Thread(target=player.run)
    game_thread.start()
    peer_thread.start()
