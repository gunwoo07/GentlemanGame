from src.core.config import TILE_SIZE


ARCHER_DATA = {
    1: {
            "damage": 15, "attack_range": 3.0*TILE_SIZE, "attack_speed": 0.50, "size_rate": 0.90, "cost": 50, "bullet_speed": 300, "color": (0, 255, 0), 
            "skill": {"cooltime": 4, "skill_name": "InfiniteArrow", "damage": 15, "bullet_speed": 300, "damage_range": 1.0*TILE_SIZE, "color": "blue"}
        },
    2: {
            "damage": 30, "attack_range": 3.5*TILE_SIZE, "attack_speed": 0.40, "size_rate": 0.95, "cost": 40, "bullet_speed": 310, "color": (0, 150, 0), 
            "skill": {"cooltime": 4, "skill_name": "InfiniteArrow","damage": 30, "bullet_speed": 310, "damage_range": 1.0*TILE_SIZE, "color": "blue"}
        },
    3: {
            "damage": 60, "attack_range": 4.0*TILE_SIZE, "attack_speed": 0.35, "size_rate": 1.00, "cost": 80, "bullet_speed": 320, "color": (0, 100, 0), 
            "skill": {"cooltime": 4, "skill_name": "InfiniteArrow","damage": 60, "bullet_speed": 320, "damage_range": 1.0*TILE_SIZE, "color": "blue"}
        }
}

CANNON_DATA = {
    1: {
            "damage": 40, "attack_range": 2.5*TILE_SIZE, "attack_speed": 0.70, "size_rate": 0.90, "cost": 80, "bullet_speed": 400, "color": (211, 211, 211),
            "skill": {"cooltime": 5, "skill_name": "Bomb", "damage": 40, "bullet_speed": 400, "damage_range": 2.0*TILE_SIZE, "color": "orange"}
        },
    2: {
            "damage": 80, "attack_range": 3.0*TILE_SIZE, "attack_speed": 0.75, "size_rate": 0.95, "cost": 60, "bullet_speed": 410, "color": (169, 169, 169),
            "skill": {"cooltime": 5, "skill_name": "Bomb", "damage": 80, "bullet_speed": 410, "damage_range": 2.0*TILE_SIZE, "color": "orange"}
        },
    3: {
            "damage": 160, "attack_range": 4.0*TILE_SIZE, "attack_speed": 0.80, "size_rate": 1.00, "cost": 130, "bullet_speed": 420, "color": (128, 128, 128),
            "skill": {"cooltime": 5, "skill_name": "Bomb", "damage": 160, "bullet_speed": 420, "damage_range": 2.0*TILE_SIZE, "color": "orange"}
        }
}

FROST_DATA = {
    1: {
            "damage": 5, "attack_range": 4.0*TILE_SIZE, "attack_speed": 0.60, "size_rate": 0.90, "cost": 40, "bullet_speed": 350, "color": (245, 254, 253),
            "skill": {"cooltime": 3, "skill_name": "Iceball", "damage": 5, "bullet_speed": 350, "slow_duration": 2.0, "slow_rate": 0.8, "color": (173, 216, 230)}
        },
    2: {
            "damage": 10, "attack_range": 4.5*TILE_SIZE, "attack_speed": 0.50, "size_rate": 0.95, "cost": 30, "bullet_speed": 400, "color": (248, 248, 255),
            "skill": {"cooltime": 3, "skill_name": "Iceball", "damage": 10, "bullet_speed": 400, "slow_duration": 2.5, "slow_rate": 0.7,  "color": (173, 216, 230)}
        },
    3: {
            "damage": 15, "attack_range": 4.7*TILE_SIZE, "attack_speed": 0.45, "size_rate": 1.00, "cost": 60, "bullet_speed": 420, "color": (255, 255, 255),
            "skill": {"cooltime": 3, "skill_name": "Iceball", "damage": 15, "bullet_speed": 420, "slow_duration": 3.0, "slow_rate": 0.6,  "color": (173, 216, 230)}
        }
}


TOWERS_DATA = {
    "archer": ARCHER_DATA,
    "cannon": CANNON_DATA,
    "frost": FROST_DATA
}