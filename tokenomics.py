# tokenomics.py
import random

COLORS = ["Red", "Orange", "Yellow", "Green", "Blue", "Indigo", "Violet"]

class Tokenomics:
    def __init__(self):
        self.reset(1000.0, 0.0, 10.0, 10.0)

    def reset(self, token, xtoken, egg_emission, decay):
        self.week = 0
        self.token = token
        self.xtoken = xtoken
        self.eggs = []
        self.hatcher = []
        self.initial_egg_emission = egg_emission
        self.current_egg_emission = egg_emission
        self.decay_rate = decay

    def get_balances(self):
        return {
            "Token": self.token,
            "XToken": self.xtoken,
            "Eggs (Unhatched)": len([e for e in self.eggs if not e['hatched'] and not e['rotted']]),
            "Eggs (Hatched)": len([e for e in self.eggs if e['hatched']]),
            "Eggs (Rotted)": len([e for e in self.eggs if e['rotted']])
        }

    def lock_tokens(self, amt):
        if self.token >= amt:
            self.token -= amt
            self.xtoken += amt

    def speed_exit(self, amt):
        if self.xtoken >= amt:
            self.xtoken -= amt
            returned = amt * 0.5
            self.token += returned
            # other 50% burned

    def advance_week(self):
        self.week += 1
        self.emit_eggs()
        self.update_eggs()
        self.update_hatcher()

    def emit_eggs(self):
        color = COLORS[self.week % 7]
        for _ in range(int(self.current_egg_emission)):
            self.eggs.append({
                "color": color,
                "born": self.week,
                "rot_start": self.week + 1,
                "hatched": False,
                "rotted": False,
                "rot_percent": 0.0
            })
        self.current_egg_emission *= (1 - self.decay_rate / 100.0)

    def update_eggs(self):
        for egg in self.eggs:
            if not egg['hatched'] and not egg['rotted']:
                weeks_since_rot = self.week - egg['rot_start']
                if weeks_since_rot >= 0:
                    egg['rot_percent'] = min(1.0, weeks_since_rot / 6.0)
                    if egg['rot_percent'] >= 1.0:
                        egg['rotted'] = True

    def stake_to_hatch(self, egg, use_xtoken=True):
        if egg['hatched'] or egg['rotted']:
            return
        if use_xtoken:
            if self.xtoken >= 1:
                self.xtoken -= 1
                self.hatcher.append({"egg": egg, "weeks_left": 5, "type": "xtoken"})
        else:
            if self.token >= 0.5:
                self.token -= 0.5
                self.hatcher.append({"egg": egg, "weeks_left": 5, "type": "token"})

    def update_hatcher(self):
        for stake in self.hatcher[:]:
            stake['weeks_left'] -= 1
            if stake['weeks_left'] <= 0:
                stake['egg']['hatched'] = True
                self.xtoken += 1
                self.hatcher.remove(stake)
