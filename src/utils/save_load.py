import os
import pickle
import json
import copy
from src.core.config import SAVEGAME_PATH, RANKING_PATH


class SaveManager:
    @staticmethod
    def save_game(game):
        # 실행 중 필요한 정보 초기화
        game.inactivate_selected_tower()
        game.inactivate_selected_tower_btn()
        # pickle로 게임 정보 저장
        try:
            with open(SAVEGAME_PATH, "wb") as f:
                pickle.dump(game.before_game_state, f)
            print("게임이 성공적으로 저장되었습니다!")
        except Exception as e:
            print(f"게임 저장 중 오류 발생: {e}")

    @staticmethod
    def load_game(game):
        try:
            with open(SAVEGAME_PATH, "rb") as f:
                save_data = pickle.load(f)
            game.game_map = save_data.get("game_map", [])
            game.towers = save_data.get("towers", [])
            game.enemies = save_data.get("enemies", [])
            game.bullets = save_data.get("bullets", [])
            game.skills = save_data.get("skills", [])
            game.path = save_data.get("path", [])
            game.gold = save_data.get("gold", 100)
            game.hp = save_data.get("hp", 100)
            game.wave_data = save_data.get("wave_data", [])
            game.wave_index = save_data.get("wave_index", 0)
            game.current_message = save_data.get("current_message", None)
            game.update_before_game_state()
            game.wave_data_progressed = copy.deepcopy(game.wave_data)
            
            print(f"게임을 성공적으로 불러왔습니다! ({SAVEGAME_PATH})")
            return True
        except Exception as e:
            print(f"불러오기 중 오류 발생: {e}")
            return False

    @staticmethod
    def save_score(name, score):
        ranking = []

        if os.path.exists(RANKING_PATH):
            try:
                with open(RANKING_PATH, 'r', encoding='utf-8') as f:
                    ranking = json.load(f)
            except (json.JSONDecodeError, Exception):
                ranking = []
        
        new_entry = {
            "name": name,
            "score": score
        }
        ranking.append(new_entry)
        ranking.sort(key=lambda x: x.get("score", 0), reverse=True)

        try:
            with open(RANKING_PATH, "w", encoding="utf-8") as f:
                json.dump(ranking, f, ensure_ascii=False, indent=4)
                return True
        except:
            return False