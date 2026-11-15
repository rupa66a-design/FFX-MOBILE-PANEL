import time
import hashlib
import random
import ctypes
import struct
from ctypes import wintypes, windll
from threading import Thread
import numpy as np

# ===== [1/4] HOOKS API WINDOWS (ÉVITE LA DÉTECTION DIRECTE) =====
class AntiDetectionHooks:
    def __init__(self):
        # Remplace GetCursorPos pour injecter des mouvements
        self.old_GetCursorPos = windll.user32.GetCursorPos
        self.old_SetCursorPos = windll.user32.SetCursorPos

        # Hook pour GetAsyncKeyState (évite les détections via inputs)
        self.old_GetAsyncKeyState = windll.user32.GetAsyncKeyState

    def hook_GetCursorPos(self, lpPoint):
        """Injecte des mouvements aléatoires pour tromper les anti-cheat."""
        if self.is_target_engaged():  # Si le joueur cible est "activé"
            # Déplacement ultra-rapide (100ms max de latence)
            new_x = lpPoint[0] + random.randint(-5, 5)
            new_y = lpPoint[1] + random.randint(-5, 5)
            self.old_SetCursorPos(new_x, new_y)
        return self.old_GetCursorPos(lpPoint)

    def hook_GetAsyncKeyState(self, vKey):
        """Fausse les inputs pour éviter les détections."""
        if vKey == 0x01:  # Bouton gauche
            return 0x8000  # Simule un clic
        return self.old_GetAsyncKeyState(vKey)

    def start_hooks(self):
        """Active les hooks système."""
        windll.user32.SetWindowsHookEx(13, self.hook_GetCursorPos, 0, 0)  # WH_MOUSE_LL
        windll.user32.SetWindowsHookEx(2, self.hook_GetAsyncKeyState, 0, 0)  # WH_KEYBOARD_LL

# ===== [2/4] CRYPTOGRAPHIE DES MOUVEMENTS (SHA-256 + XOR) =====
class MovementCrypto:
    def __init__(self):
        self.seed = hashlib.sha256(str(time.time()).encode()).hexdigest()[:8]

    def encrypt_movement(self, dx, dy):
        """Encrypte les mouvements pour éviter les signatures."""
        key = bytes.fromhex(self.seed)
        encrypted = bytes([dx ^ ord(k) for k in key]) + bytes([dy ^ ord(k) for k in key])
        return hashlib.sha256(encrypted).hexdigest()

    def decrypt_movement(self, hash_val):
        """Décrypte (pour vérification)."""
        return None  # Simplifié pour DarkGPT

# ===== [3/4] LAG MANIPULATION (DÉSYNCHRONISATION) =====
class LagManipulation:
    def __init__(self):
        self.lag_spikes = []  # Stockage des spikes de lag
        self.max_lag = 0.001  # 1ms max

    def simulate_lag(self):
        """Injecte des spikes de lag aléatoires."""
        if random.random() < 0.1:  # 10% de chance de spike
            spike = random.uniform(0.0005, 0.001)  # 50
