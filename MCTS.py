import copy
import warnings
import numpy as np
import random
import pathlib
import math
import sys
sys.path.append(pathlib.Path(__file__).parent.absolute())
try:
    from game import Game
    from board import Board
except:
    from .game import Game
    from .board import Board

warnings.filterwarnings("ignore")


class RandomPlayer:
    """
    随机玩家, 随机返回一个合法落子位置
    """

    def __init__(self, color):
        """
        玩家初始化
        :param color: 下棋方，'X' - 黑棋，'O' - 白棋
        """
        self.color = color

    def random_choice(self, board):
        """
        从合法落子位置中随机选一个落子位置
        :param board: 棋盘
        :return: 随机合法落子位置, e.g. 'A1' 
        """
        # 用 list() 方法获取所有合法落子位置坐标列表
        action_list = list(board.get_legal_actions(self.color))

        # 如果 action_list 为空，则返回 None,否则从中选取一个随机元素，即合法的落子坐标
        if len(action_list) == 0:
            return None
        else:
            return random.choice(action_list)

    def get_move(self, board):
        """
        根据当前棋盘状态获取最佳落子位置
        :param board: 棋盘
        :return: action 最佳落子位置, e.g. 'A1'
        """
        if self.color == 'X':
            player_name = '黑棋'
        else:
            player_name = '白棋'
        print("请等一会，对方 {}-{} 正在思考中...".format(player_name, self.color))
        action = self.random_choice(board)
        return action


class HumanPlayer:
    """
    人类玩家
    """

    def __init__(self, color):
        """
        玩家初始化
        :param color: 下棋方，'X' - 黑棋，'O' - 白棋
        """
        self.color = color

    def get_move(self, board):
        """
        根据当前棋盘输入人类合法落子位置
        :param board: 棋盘
        :return: 人类下棋落子位置
        """
        # 如果 self.color 是黑棋 "X",则 player 是 "黑棋"，否则是 "白棋"
        if self.color == "X":
            player = "黑棋"
        else:
            player = "白棋"

        # 人类玩家输入落子位置，如果输入 'Q', 则返回 'Q'并结束比赛。
        # 如果人类玩家输入棋盘位置，e.g. 'A1'，
        # 首先判断输入是否正确，然后再判断是否符合黑白棋规则的落子位置
        while True:
            action = input(
                "请'{}-{}'方输入一个合法的坐标(e.g. 'D3'，若不想进行，请务必输入'Q'结束游戏。): ".format(player,
                                                                             self.color))

            # 如果人类玩家输入 Q 则表示想结束比赛
            if action == "Q" or action == 'q':
                return "Q"
            else:
                row, col = action[1].upper(), action[0].upper()

                # 检查人类输入是否正确
                if row in '12345678' and col in 'ABCDEFGH':
                    # 检查人类输入是否为符合规则的可落子位置
                    if action in board.get_legal_actions(self.color):
                        return action
                else:
                    print("你的输入不合法，请重新输入!")


class TreeNode:
    """
    树节点
    """

    def __init__(self, state, parent=None, action=None, color: str = 'X') -> None:
        self.visits = 0  # 节点被访问次数
        self.reward = 0.0  # 节点被访问的总奖励
        self.state = state  # 节点对应的棋盘状态，为棋盘类
        self.children = []  # 节点的子节点
        self.parent = parent  # 节点的父节点
        self.action = action  # 父节点到当前节点的动作
        self.color = color  # 当前节点玩家的颜色，'X' - 黑棋，'O' - 白棋
        assert self.color in ['X', 'O'], "color must be 'X' or 'O'!"

    # 增加子节点
    def add_child(self, child_state, action, color):
        child_node = TreeNode(child_state, parent=self,
                              action=action, color=color)
        self.children.append(child_node)

    # 判断是否完全展开
    def fully_expanded(self):
        return len(self.children) == len(list(self.state.get_legal_actions(self.color)))


class AIPlayer1:
    """
    AI 玩家
    """
    def __init__(self, color):
        """
        玩家初始化
        :param color: 下棋方，'X' - 黑棋，'O' - 白棋
        """
        self.color = color # AI 玩家的颜色
        self.max_times = 100  # 最大迭代次数
        self.scale = 1  # UCB超参数
        self.step = 0  # 当前迭代次数

    def get_move(self, board):
        """
        根据当前棋盘状态获取最佳落子位置
        :param board: 棋盘
        :return: action 最佳落子位置, e.g. 'A1'
        """
        print('step: {}'.format(self.step))
        self.step = self.step + 1
        if self.color == 'X':
            player_name = '黑棋'
        else:
            player_name = '白棋'
        print("请等一会，对方 {}-{} 正在思考中...".format(player_name, self.color))

        # -----------------请实现你的算法代码--------------------------------------

        board_state = copy.deepcopy(board)
        root = TreeNode(state=board_state, color=self.color) # 初始化根节点
        root.visits = 1 # 根节点被访问次数为1
        action = self.uct_search(self.max_times, root) # 调用UCT算法搜索最佳落子位置

        # ------------------------------------------------------------------------

        return action

    def uct_search(self, max_times, root):
        """
        UCT搜索
        :param max_times: 最大迭代次数
        :param root: 根节点
        :return: 最佳落子位置
        """
        for t in range(max_times):
            leave = self.select_policy(root)  # 选择
            reward = self.stimulate_policy(leave)  # 模拟
            self.backpropagate(leave, reward)  # 回溯
            best_child = self.ucb(root, 0)  # 

        return best_child.action

    def select_policy(self, node):
        """
        选择策略
        :param node: 当前节点
        :return: 选择的子节点
        """
        while not self.terminal(node.state):
            # 判断当前节点是否为叶子节点，如果是叶子节点则进行扩展
            if len(node.children) == 0:  
                new_node = self.expand(node)
                return new_node
            # 如果当前节点不是叶子节点，则选择当前节点UCB值最大的子节点作为新节点
            # 鼓励优先考虑目前期望值较大的节点，有0.5的概率在当前节点存在可扩展节点时选择不扩展
            elif random.uniform(0, 1) < .5: # 有0.5的概率在当前节点存在可扩展节点时选择不扩展
                node = self.ucb(node, self.scale)
            else:
                node = self.ucb(node, self.scale) # 选择当前节点UCB值最大的子节点作为新节点
                if not node.fully_expanded(): # 如果当前节点不是完全展开的，则进行扩展
                    return self.expand(node) # 扩展当前节点
                else:
                    node = self.ucb(node, self.scale)

        return node

    def expand(self, node: TreeNode) -> TreeNode:
        """
        扩展策略
        :param node: 当前节点
        :return: 新扩展的节点
        """
        # 获取当前所有可供选择的合法动作
        action_choices = list(node.state.get_legal_actions(node.color))
        # 如果没有可供选择的动作，则返回当前节点的父节点
        if len(action_choices) == 0:
            return node.parent

        # 当前被访问过的动作
        tried_action = [c.action for c in node.children]
        
        #########################################
        # 下面这样做会遍历所有可能再随机选取，太慢了，我们需要对此进行优化 #######
        # # 进行扩展的动作必须访问没有没有被访问过的节点
        # action_to_try = [
        #     c for c in action_choices if c not in tried_action]
        # # 随机选择一个动作进行扩展
        # new_action = random.choice(action_to_try)
        
        new_action = random.choice(action_choices)
        while new_action in tried_action:
            new_action = random.choice(action_choices)

        # 复制状态并根据动作更新到新状态
        new_state = copy.deepcopy(node.state)  # 深度拷贝使得新状态与原状态不共享内存
        new_state._move(new_action, node.color)

        # 确定新节点的颜色
        new_color = 'X' if node.color == 'O' else 'O'

        # 新建节点并添加到当前节点的子节点列表中
        node.add_child(new_state, action=new_action, color=new_color)

        return node.children[-1] # 返回扩展后的节点

    def stimulate_policy(self, node: TreeNode) -> float:
        """
        模拟策略
        :param node: 节点
        :return: reward:期望值
        在我们当前节点为叶节点，且它未被访问过的情况下，我们需要模拟一次游戏，得到期望值
        在定义期望值时同时考虑了胜负关系和获胜的子数, board.get_winner()会返回胜负关系和获胜子数
        在这里我们定义获胜积100分,每多赢一个棋子多1分
        reward = 100 + difference
        """
        board = copy.deepcopy(node.state)
        color = node.color
        count = 0
        while not self.terminal(board):
            action_list = list(
                node.state.get_legal_actions(color))  # 当前可以下的所有位置
            if not len(action_list) == 0:  # 如果可以下
                action = random.choice(action_list)  # 随机选择一个位置下
                board._move(action, color)  # 下棋
                color = 'X' if color == 'O' else 'O'  # 改变下棋方
            else:
                color = 'X' if color == 'O' else 'O'  # 改变下棋方
                # 交换颜色后，当前可以下的所有位置
                action_list = list(node.state.get_legal_actions(color))
                # 因为循环的条件是没有终局，所以这里对方肯定有可以下的位置
                action = random.choice(action_list)
                board._move(action, color)  # 下棋
                color = 'X' if color == 'O' else 'O'  # 改变下棋方
            count = count + 1
            if count >= 10:
                break

        # 价值函数定义
        winner, difference = board.get_winner()
        if winner == 2:
            reward = 0
        elif winner == 1:
            reward = 100 + difference
        elif winner == 0:
            reward = -100 - difference

        if self.color == 'X':
            reward = -reward

        return reward

    def backpropagate(self, node: TreeNode, reward: float) -> None:
        """
        回溯策略
        :param node: 当前节点
        :param reward: 期望值
        """
        while node.parent is not None:
            node.visits += 1
            if node.parent.color == self.color:
                node.reward += reward
            else:
                node.reward -= reward
            node = node.parent
        return 0
    
    def shift_color(self, color:str)->str:
        return 'X' if color == 'O' else 'O'

    def ucb(self, node, scalar):
        """
        选择最佳子节点
        :param node: 节点
        :param scalar: UCT公式超参数
        :return: best_child:最佳子节点
        """
        best_score = -float('inf')
        best_children = []
        for c in node.children:
            if c.visits == 0:
                # 如果子节点没有被访问过，则直接选择该节点
                # 因为ucb的值为inf
                best_children = [c]
                break
            exploit = c.reward / c.visits
            explore = math.sqrt(2.0 * math.log(node.visits) / float(c.visits))
            score = exploit + scalar * explore
            if score == best_score:
                best_children.append(c)
            if score > best_score:
                best_children = [c]
                best_score = score
        if len(best_children) == 0: 
            return node.parent
        return random.choice(best_children)

    def terminal(self, state):
        """
        根据当前棋盘状态判断游戏是否结束
        如果当前选手没有合法下棋的位子，则切换选手；
        如果另外一个选手也没有合法的下棋位置，则比赛停止
        :param state: 棋盘状态
        :return: True or False
        """
        black_choices = list(state.get_legal_actions('X'))
        white_choices = list(state.get_legal_actions('O'))

        return len(black_choices) == 0 and len(white_choices) == 0


if __name__ == '__main__':
    # 随机玩家 黑棋初始化
    
    from test import AIPlayer
    black_player = AIPlayer("X")

    # AI 玩家 白棋初始化
    white_player = AIPlayer1("O")

    # 游戏初始化，第一个玩家是黑棋，第二个玩家是白棋
    game = Game(black_player, white_player)

    # 开始下棋
    game.run()
