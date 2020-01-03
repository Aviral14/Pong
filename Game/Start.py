import players
import Pong
import threading

if __name__ == "__main__":
    player = players.Player()
    player.connect_to_server()
    game_thread = threading.Thread(target=Pong.run_game)
    peer_thread = threading.Thread(target=player.run)
    game_thread.start()
    peer_thread.start()
