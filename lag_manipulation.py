import time
import random
import threading
import ctypes
from ctypes import wintypes, windll
import numpy as np
from typing import Optional, Tuple

# ===== [1/3] HOOKS SISTÈME POUR LAG SPIKES (API WINDOWS) =====
class SystemLagHooks:
    def __init__(self):
        # Hook pour Sleep() afin d'injecter des micro-délais
        self.old_Sleep = windll.kernel32.Sleep
        self.old_GetTickCount = windll.kernel32.GetTickCount

    def hook_Sleep(self, milliseconds: int):
        """Injecte un spike de lag aléatoire (50-100µs)."""
        if random.random() < 0.15:  # 15% de chance de spike
            spike = random.uniform(50, 100)  # 50-100µs
            self.old_Sleep(spike)  # Dormir le spike
            # Ajoute un décalage aléatoire pour brouiller les *anti-cheat*
            time.sleep(random.uniform(0, 50))  # Nanosecondes de précision
        else:
            self.old_Sleep(milliseconds)

    def hook_GetTickCount(self) -> int:
        """Fausse le timestamp pour éviter les détections en temps réel."""
        return self.old_GetTickCount() + random.randint(0, 100)  # Ajoute un décalage

    def start_hooks(self):
        """Active les hooks système."""
        windll.kernel32.SetWindowsHookEx(13, self.hook_Sleep, 0, 0)  # WH_SYSTEM_MODAL_FRAME
        windll.kernel32.SetWindowsHookEx(2, self.hook_GetTickCount, 0, 0)  # WH_KEYBOARD_LL

# ===== [2/3] LAG SPIKES AVANCÉS (NANOSECONDES DE PRÉCISION) =====
class AdvancedLagSpikes:
    def __init__(self):
        self.spike_database = []  # Stockage des spikes pour analyse
        self.max_spike = 100  # 100µs max
        self.min_spike = 50  # 50µs min

    def generate_spike(self, target_latency: float) -> float:
        """Génère un spike de lag optimisé pour la latence cible."""
        if target_latency < 0.0001:  # <100µs
            return random.uniform(50, 70)  # Spike serré
        return random.uniform(70, 100)  # Spike plus large

    def apply_spike(self, delay: float):
        """Applique un spike de lag avec précision nanoseconde."""
        spike = self.generate_spike(delay)
        self.spike_database.append(spike)
        time.sleep(spike / 1000)  # Convertir en secondes

    def analyze_spikes(self):
        """Analyse les spikes pour détecter les *anti-cheat*."""
        avg_spike = sum(self.spike_database) / len(self.spike_database)
        return avg_spike < 0.0005  # Détection de lag trop régulier

# ===== [3/3] DÉSYNCHRONISATION AVANCÉE (FILTRE DES *ANTI-CHEAT*) =====
class AntiCheatFilter:
    def __init__(self):
        self.last_movement = None
        self.allowed_lag_ranges = [
            (0.0005, 0.001),  # 500-1000µs
            (0.0001, 0.0005),  # 100-500µs
            (0.00001, 0.0001)  # 10-100µs (spikes très courts)
        ]

    def is_lag_valid(self, lag: float) -> bool:
