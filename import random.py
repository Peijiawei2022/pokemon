import random
from collections import defaultdict

# -----------------------------
# 卡牌数据结构定义
# -----------------------------

class PokemonCard:
    def __init__(self, name, hp, attack_names, attack_damages, energy_required, is_basic=True, prize_count=1):
        # 卡牌名称，比如“皮卡丘”
        self.name = name
        # 宝可梦最大生命值
        self.hp = hp
        # 攻击名称列表，例如 ["打雷", "十万伏特"]
        self.attack_names = attack_names
        # 对应每个攻击的伤害值列表，例如 [10, 20]
        self.attack_damages = attack_damages
        # 对应每个攻击需要消耗的能量数量列表，例如 [1, 2]
        self.energy_required = energy_required
        # 是否为基础宝可梦，默认是True
        self.is_basic = is_basic
        # 击倒该宝可梦后，获得的奖赏卡数量，默认1张
        self.prize_count = prize_count
        # 当前生命值，初始化为最大生命值
        self.current_hp = hp
        # 当前附加的能量数量，初始化为0
        self.energy_attached = 0

    # 定义攻击方法，默认执行第一个攻击(attack_index=0)
    def attack(self, attack_index=0, opponent=None):
        # 判断当前附加能量是否满足该攻击的能量需求
        if self.energy_attached >= self.energy_required[attack_index]:
            # 获取对应攻击的伤害值
            damage = self.attack_damages[attack_index]
            # 如果有对手（对战对象）
            if opponent:
                # 对对手的当前生命值造成伤害
                opponent.current_hp -= damage
            # 打印攻击动作和伤害数值，方便调试和观察战斗过程
            print(f"{self.name} 使用 {self.attack_names[attack_index]}，造成了 {damage} 点伤害")

    def is_knocked_out(self):
        # 判断宝可梦是否被击倒
        return self.current_hp <= 0


class TrainerCard:
    # 定义训练家卡，包含名称和效果
    def __init__(self, name, effect):
        self.name = name  # 卡牌名称
        self.effect = effect  # 效果函数


class EnergyCard:
    # 定义能量卡，仅包含名称
    def __init__(self, name="Basic Energy"):
        self.name = name


# -----------------------------
# 卡牌库管理 + 遗传算法支持
# -----------------------------

class CardDatabase:
    # 管理卡牌库和卡组胜负记录，实现遗传算法选择与变异
    def __init__(self):
        self.pokemon_cards = []  # 所有宝可梦卡
        self.trainer_cards = []  # 所有训练家卡
        self.energy_cards = []  # 所有能量卡
        self.deck_records = defaultdict(lambda: {"wins": 0, "losses": 0})  # 卡组胜负记录

    def add_pokemon(self, card):
        # 添加宝可梦卡
        self.pokemon_cards.append(card)

    def add_trainer(self, card):
        # 添加训练家卡
        self.trainer_cards.append(card)

    def add_energy(self, card):
        # 添加能量卡
        self.energy_cards.append(card)


# -----------------------------
# 可以在这下面添加卡牌
# -----------------------------    
# 实例化卡牌库
db = CardDatabase()

# 创建皮卡丘卡牌
pikachu = PokemonCard(
    name="皮卡丘",
    hp=100,
    attack_names=["打雷", "十万伏特"],
    attack_damages=[10, 20],
    energy_required=[1, 2],
    is_basic=True
)

# 创建卡比兽卡牌，睡觉攻击不造成伤害但示例展示
snorlax = PokemonCard(
    name="卡比兽",
    hp=160,
    attack_names=["撞击", "睡觉"],
    attack_damages=[30, 0],       # 睡觉攻击暂不造成伤害
    energy_required=[2, 0],       # 睡觉不消耗能量
    is_basic=True
)

# 添加宝可梦卡牌进卡库
db.add_pokemon(pikachu)
db.add_pokemon(snorlax)

# 测试输出卡库内所有宝可梦卡牌信息
for card in db.pokemon_cards:
    print(f"卡牌名称: {card.name}, 血量: {card.hp}, 攻击技能: {card.attack_names}")
# -----------------------------
# 可以在这上面添加卡牌
# -----------------------------

    def generate_random_deck(self):
        # 随机生成一套卡组：20张宝可梦、20张训练家、20张能量卡
        return random.sample(self.pokemon_cards, 20) + \
               random.sample(self.trainer_cards, 20) + \
               random.sample(self.energy_cards, 20)

    def update_deck_stats(self, deck, win):
        # 根据对战结果更新卡组胜负记录
        key = str(sorted(card.name for card in deck))  # 以卡组名称列表为键
        if win:
            self.deck_records[key]["wins"] += 1  # 增加胜场
        else:
            self.deck_records[key]["losses"] += 1  # 增加败场

    def evaluate_decks(self):
        # 评估所有卡组，选出前10%的高胜率卡组作为遗传算法父代
        records = list(self.deck_records.items())  # 获取所有记录
        records.sort(key=lambda x: x[1]['wins'] / (x[1]['wins'] + x[1]['losses'] + 1e-5), reverse=True)  # 按胜率排序
        top = records[:max(1, len(records)//10)]  # 取前10%卡组
        parents = [eval(deck_repr) for deck_repr, _ in top] if top else [self.generate_random_deck()]  # 父代卡组
        return self.mutate_deck(random.choice(parents))  # 返回突变后的新卡组

    def mutate_deck(self, deck):
        # 对卡组进行轻微变异（突变）：随机替换5张卡牌
        new_deck = deck[:]  # 复制卡组
        for _ in range(5):  # 进行5次突变
            idx = random.randint(0, len(new_deck) - 1)  # 随机选择一张卡
            if isinstance(new_deck[idx], PokemonCard):
                new_deck[idx] = random.choice(self.pokemon_cards)  # 替换为随机宝可梦
            elif isinstance(new_deck[idx], TrainerCard):
                new_deck[idx] = random.choice(self.trainer_cards)  # 替换为随机训练家
            elif isinstance(new_deck[idx], EnergyCard):
                new_deck[idx] = random.choice(self.energy_cards)  # 替换为随机能量卡
        return new_deck


# -----------------------------
# 玩家定义
# -----------------------------

class Player:
    # 玩家类，管理卡组、手牌、场上宝可梦等
    def __init__(self, name, deck):
        self.name = name  # 玩家名称
        self.deck = deck[:]  # 初始卡组
        self.hand = []  # 手牌
        self.active_pokemon = None  # 场上宝可梦
        self.bench = []  # 替补席宝可梦
        self.prize_cards = []  # 奖赏卡
        self.discard_pile = []  # 弃牌堆

    def draw_cards(self, num):
        # 抽卡函数，从卡组中抽num张卡
        for _ in range(num):
            if self.deck:
                self.hand.append(self.deck.pop(0))

    def setup_game(self):
        # 游戏初始化：抽卡、选出基础宝可梦并设置奖赏卡
        self.draw_cards(7)  # 初始抽7张
        basics = [card for card in self.hand if isinstance(card, PokemonCard) and card.is_basic]  # 找出基础宝可梦
        if not basics:
            # 若无基础宝可梦，则重新洗牌并重新抽卡
            self.deck += self.hand
            random.shuffle(self.deck)
            self.hand.clear()
            self.setup_game()
        else:
            self.active_pokemon = basics[0]  # 选第一张为主动宝可梦
            self.hand.remove(self.active_pokemon)
            self.bench = basics[1:6]  # 其余为替补
            for p in self.bench:
                self.hand.remove(p)
            self.prize_cards = self.deck[:6]  # 前6张为奖赏卡
            self.deck = self.deck[6:]  # 更新卡组


# -----------------------------
# 对战逻辑
# -----------------------------

def take_turn(player, opponent):
    # 单个玩家回合操作：抽卡、附能量、攻击
    player.draw_cards(1)  # 抽1张牌
    for card in player.hand:
        # 尝试附加能量卡
        if isinstance(card, EnergyCard) and player.active_pokemon.energy_attached < player.active_pokemon.energy_required:
            player.active_pokemon.energy_attached += 1  # 附加能量
            player.hand.remove(card)
            break

    if player.active_pokemon.energy_attached >= player.active_pokemon.energy_required:
        # 若能量充足则攻击
        opponent.active_pokemon.current_hp -= player.active_pokemon.attack_damage  # 减少对方血量
        if opponent.active_pokemon.is_knocked_out():
            # 若对手被击倒
            opponent.discard_pile.append(opponent.active_pokemon)
            if player.prize_cards:
                player.prize_cards.pop()  # 获得一张奖赏卡
            if opponent.bench:
                opponent.active_pokemon = opponent.bench.pop(0)  # 从替补席换人
            else:
                opponent.active_pokemon = None  # 无人可替代


def check_victory(player1, player2):
    # 判断胜利条件：对手场上无宝可梦或已取得所有奖赏卡
    if not player2.active_pokemon:
        return player1
    if len(player1.prize_cards) == 0:
        return player1
    return None


# -----------------------------
# 主训练逻辑（带遗传算法）
# -----------------------------

if __name__ == "__main__":
    db = CardDatabase()  # 创建卡牌数据库

    # 添加卡牌数据：100张宝可梦，50张训练家，50张能量
    for i in range(100):
        db.add_pokemon(PokemonCard(f"宝可梦{i+1}", 60 + (i % 3) * 20, f"攻击{i+1}", 20 + (i % 4) * 10, (i % 3) + 1))
    for i in range(50):
        db.add_trainer(TrainerCard(f"训练家{i+1}", lambda x: None))
    for i in range(50):
        db.add_energy(EnergyCard(f"能量{i+1}"))

    # 模拟1000场AI自我对战
    for _ in range(1000):
        deck1 = db.evaluate_decks()  # 生成卡组1
        deck2 = db.evaluate_decks()  # 生成卡组2
        player1 = Player("AI玩家1", deck1)
        player2 = Player("AI玩家2", deck2)
        player1.setup_game()
        player2.setup_game()

        winner = None
        for _ in range(20):  # 最多打20回合
            take_turn(player1, player2)
            winner = check_victory(player1, player2)
            if winner:
                break
            take_turn(player2, player1)
            winner = check_victory(player2, player1)
            if winner:
                break

        if winner:
            db.update_deck_stats(winner.deck, True)  # 胜者加胜场
            loser = player1 if winner == player2 else player2
            db.update_deck_stats(loser.deck, False)  # 败者加败场

    # 输出当前胜率最高的卡组（示例前10张）
    top_deck = db.evaluate_decks()
    print("胜率最高卡组（示例10张）:")
    for card in top_deck[:10]:
        print(f"{card.name}")
