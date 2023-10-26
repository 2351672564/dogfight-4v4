import random
from enum import Enum
import pygame
import logging
from random import uniform
import harfang as hg

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class FSMStateEnum(Enum):
    init = 0
    sear = 1
    esca = 2
    att = 3
    rep = 4
    liftoff = 5
    des = 6


class FSMState:
    """
    有限状态机状态类
    """

    def __init__(self):
        self.controller = None
        self.machine = None
        self.extern_exit = True
        pass

    def enter(self):
        pass

    def event(self, dts):
        pass

    def exit(self):
        pass

    def getNextState(self):
        pass

    def OnMessage(self, msgID, data):
        pass

    def type(self):
        pass


class InitState(FSMState):

    def __init__(self, controller):
        super(InitState).__init__()
        self.name = 'init'
        self.controller = controller
        self.extern_exit = False

    # hansongde
    def event(self, dts):
        pass

    def exit(self):
        """
        结束索敌
        当锁定目标或者被目标锁定后，退出索敌状态
        :return:
        """
        logger.info("退出init状态")

    def type(self):
        return FSMStateEnum.init


class LiftoffState(FSMState):

    def __init__(self, controller):
        super(LiftoffState).__init__()
        self.name = 'sear'
        self.controller = controller
        self.extern_exit = False

    # hansongde
    def enter(self):
        """
        开始索敌
        :return:
        """
        logger.info("进入liftoff状态")
        """
        1. 获取最近目标：初次按概率，其他按距离
        2. 更新当前飞机的锁定目标
        """

    # hansongde
    def event(self, dts):
        """
        正在索敌，索敌方式为
        循环执行
        1. 计算和锁定目标的距离
        2. 向锁定目标匀速飞行
        3. 当接近目标至一定范围后，发射导弹（真实场景下，首先应该进行）
        4.
        :return:
        """
        self.controller.update_IA_liftoff_fsm(self.controller.machine, dts)

    def exit(self):
        """
        结束索敌
        当锁定目标或者被目标锁定后，退出索敌状态
        :return:
        """

        logger.info("退出liftoff状态")

    def getNextState(self):
        """
        判断是否进入下一状态
        :return:
        """

    def type(self):
        return FSMStateEnum.liftoff


class SearState(FSMState):

    def __init__(self, controller):
        super(SearState).__init__()
        self.name = 'sear'
        self.controller = controller
        self.extern_exit = True

        self.missile_freeze = 1
        self.missile_freeze_timer = 0

    # hansongde
    def enter(self):
        """
        开始索敌
        :return:
        """
        logger.info("进入sear状态")
        """
        1. 获取最近目标：初次按概率，其他按距离
        2. 更新当前飞机的锁定目标
        """
        td = self.controller.machine.get_device("TargettingDevice")
        if td is not None:
            pass
            #td.search_nearest_target()
            """
            3. 编写接口，向目标空中智能体对象通信，更新其已被锁定的flag（考虑在飞机类里面新增被锁定flag）
            target = search_nearest_target() 
            update_target_lock(self.controller.machine.plane_id, target)
            """

    # hansongde
    def event(self, dts):
        """
        正在索敌，索敌方式为
        循环执行
        1. 计算和锁定目标的距离
        2. 向锁定目标匀速飞行
        3. 当接近目标至一定范围后，发射导弹（真实场景下，首先应该进行）
        4.
        :return:
        """
        if self.missile_freeze_timer > 0:
            self.missile_freeze_timer -= dts
        self.controller.update_IA_fight_fsm(self.controller.machine, dts)  # 发射导弹的距离可通过self.controller.machine.set_fire_distance函数修改

        """
        
        dts = get_distance_3D(self.controller.machine, target)
        update_IA_Idle(self.controller.machine, dts)
        """

    def exit(self):
        """
        结束索敌
        当锁定目标或者被目标锁定后，退出索敌状态
        :return:
        """

        logger.info("退出sear状态")

    def getNextState(self):
        """
        判断是否进入下一状态
        :return:
        """

    def type(self):
        return FSMStateEnum.sear


class EscaState(FSMState):

    def __init__(self, controller):
        super(EscaState).__init__()
        self.name = 'esca'
        self.controller = controller
        self.timer = float()
        self.maneuver_interval = 1.0  # 机动间隔时间
        self.esca_state = 0  # 0为处于机动间隔，1为处于机动期间
        self.extern_exit = False

        self.time_limit = 10
        self.limit_timer = self.time_limit

    # songde
    def enter(self):
        """
        开始回避
        :return:
        """
        self.esca_state = 1
        self.choose_method()
        logger.info("进入esca状态")

    # songde
    def event(self, dts):
        """
        正在回避
        :param dts:
        :param entity:
        :return:
        """
        self.limit_timer -= dts
        if self.limit_timer <= 0:
            self.machine.trans_state(FSMStateEnum.sear)

        if self.esca_state == 0:
            self.controller.update_IA_escape_fsm(self.controller.machine, dts)
            self.timer -= dts
            if self.timer <= 0:
                self.esca_state = 1
                self.extern_exit = False
                self.choose_method()
        else:
            # 若不采取准备动作（先转到平稳飞行再开始机动），则在这里使用self.controller.machine.IA_flag_maneuver_prepared = True
            print(self.controller.IA_flag_maneuver_method)
            self.controller.update_IA_maneuver_fsm(self.controller.machine, dts)
            if self.controller.IA_flag_maneuver_finished:
                self.controller.IA_flag_maneuver_finished = False
                self.esca_state = 0
                self.extern_exit = True
                self.timer = self.maneuver_interval

    def choose_method(self):
        # 随机选择，但背对敌人时更倾向于英麦曼机动
        angle = self.controller.machine.get_device("TargettingDevice").target_heading - self.controller.machine.get_device("AutopilotControlDevice").autopilot_heading
        if angle < 0:
            angle *= -1
        facing_enemy = angle < 90 or angle > 270
        self.controller.IA_flag_maneuver_method = 2 if not facing_enemy and uniform(0, 1) < 0.5 \
                                                        else int(uniform(0, self.controller.IA_flag_maneuver_method_num - 0.1))

    def exit(self):
        """
        结束回避
        :param entity:
        :return:
        """

    def getNextState(self):
        """
        判断是否进入下一状态
        :return:
        """

    def type(self):
        return FSMStateEnum.esca


class AttState(FSMState):

    def __init__(self, controller):
        super(AttState).__init__()
        self.name = 'att'
        self.controller = controller
        self.extern_exit = True

    # hansongde
    def enter(self):
        """
        开始攻击
        :return:
        """

    # hansongde
    def event(self, dts):
        """
        正在攻击
        :param dts:
        :param entity:
        :return:
        """

    def exit(self):
        """
        结束攻击
        :param entity:
        :return:
        """

    def getNextState(self):
        """
        判断是否进入下一状态
        :return:
        """

    def type(self):
        return FSMStateEnum.att


class RepState(FSMState):

    def __init__(self, controller):
        super(RepState).__init__()
        self.name = 'rep'
        self.controller = controller
        self.extern_exit = False

        self.timer = float()
        self.interval = 1

    # hansongde
    def enter(self):
        """
        开始整备
        :return:
        """
        self.timer = self.interval
        logger.info("进入rep状态")

    # hansongde
    def event(self, dts):
        """
        正在整备
        :param entity:
        :return:
        """
        self.controller.update_IA_landing_fsm(self.controller.machine, dts)
        if not self.machine.flag_ready_landing:
            self.timer -= dts
            if self.timer <= 0:
                if self.controller.machine.targeted and random.uniform(0, 1) < 0.5:
                    self.machine.trans_state(FSMStateEnum.esca)
                else:
                    self.timer = self.interval

    def exit(self):
        """
        结束整备
        :param entity:
        :return:
        """

    def getNextState(self):
        """
        判断是否进入下一状态
        :return:
        """

    def type(self):
        return FSMStateEnum.rep


class DesState(FSMState):
    def __init__(self):
        super(DesState).__init__()
        self.name = 'des'
        self.extern_exit = True

    # hansongde
    def enter(self):
        """
        开始整备
        :return:
        """

    # hansongde
    def event(self):
        """
        正在整备
        :param entity:
        :return:
        """

    def exit(self):
        """
        结束整备
        :param entity:
        :return:
        """

    def getNextState(self):
        """
        判断是否进入下一状态
        :return:
        """

    def type(self):
        return FSMStateEnum.des
