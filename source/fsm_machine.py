import os
import random
import sys
from enum import Enum
import pygame as pg
#import constants as c
import logging

from fsm_state import FSMStateEnum
from fsm_state import FSMState
from fsm_state import InitState
from fsm_state import LiftoffState
from fsm_state import SearState
from fsm_state import EscaState
from fsm_state import AttState
from fsm_state import RepState
from fsm_state import AdjustState

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Entity:

    def __init__(self, entity):
        self.states: dict[FSMStateEnum, FSMState] = {}
        self.state: FSMState = None
        self.entity = entity #空中智能体的标识
        self.enemy: int = 1 #载D量
        self.preState: list = [] #历史状态，用于记录和回溯

        self.flag_missle_short = False
        self.flag_targeted = False

        self.debug = False
        self.replay = False
        self.replay_over = False
        self.replay_takeover = False

        #添加状态
        init_state = InitState(entity)
        self.add_state(init_state)

        sear_state = SearState(entity)
        self.add_state(sear_state)

        esca_state = EscaState(entity)
        self.add_state(esca_state)

        att_state = AttState(entity)
        self.add_state(att_state)

        rep_state = RepState(entity)
        self.add_state(rep_state)

        liftoff_state = LiftoffState(entity)
        self.add_state(liftoff_state)

        adjust_state = AdjustState(entity)
        self.add_state(adjust_state)

        self.set_state(FSMStateEnum.init)
        self.preState.append(self.states[FSMStateEnum.init])

    """
    @Author: Songde
    """
    def _update(self, dts: float):
        """
        :return:
        """
        if self.replay and self.replay_over:
            return
        self.state.event(dts)
        if self.state.extern_exit and not self.replay:
            new_state = self.event_handle()  # 监测并判断飞机应处的状态
            self.trans_state(new_state)

    def add_state(self, state: FSMState):
        key = state.type()
        self.states[key] = state

    def get_state(self):
        """
        获取当前状态
        :return: 依次返回当前状态，前一时刻状态和当前状态
        """
        return self.state

    def set_state(self, state: FSMStateEnum):
        """
        设置状态
        :param state: 新的状态
        :return:
        """
        if self.state is not None:
            self.state.exit()
        self.state = self.states[state] #设置新的状态
        self.state.machine = self
        self.state.enter() #进入新的状态

    def trans_state(self, goal_state: FSMStateEnum):
        """
        状态转换
        :param goal_state: 目标状态
        :return:
        """
        if goal_state == self.state.type():
            return
        self.flag_locked = False
        self.flag_missle_short = False
        self.preState.append(goal_state)
        if goal_state in self.states:
            self.set_state(goal_state)
            if goal_state != FSMStateEnum.sear:
                aircraft = self.entity.machine
                n = aircraft.get_machinegun_count()
                for i in range(n):
                    mgd = aircraft.get_device("MachineGunDevice_%02d" % i)
                    if mgd is not None and mgd.is_activated():
                        mgd.deactivate()


    def trans_state_by_name(self, goal_state: str):
        """
        状态转换
        :param goal_state: 目标状态
        :return:
        """
        gs = self.state
        if goal_state == "FSMStateEnum.init":
            gs = FSMStateEnum.init
        if goal_state == "FSMStateEnum.liftoff":
            gs = FSMStateEnum.liftoff
        if goal_state == "FSMStateEnum.sear":
            gs = FSMStateEnum.sear
        if goal_state == "FSMStateEnum.esca":
            gs = FSMStateEnum.esca
        if goal_state == "FSMStateEnum.rep":
            gs = FSMStateEnum.rep
        self.trans_state(gs)

    def destroy(self):
        """
        飞机被击毁，销毁对象
        :return:
        """
        #self.state.clear()
        logger.info(self.entity.machine.id + 'destroy……')

    """
    @Author: Songde
    """
    def event_handle(self) -> FSMStateEnum:
        """
        监听智能体状态，并针对DD和智能体的关系作出反应
        1.根据clock监听智能体状态
        2.if 当前智能体被锁定：
             进入回避状态
          elif 当前智能体DD数量不充足：
             进入休整状态
          elif 当前智能体未能锁定目标：
             (如果DD数量未达到最大值，按30%的概率进入休整状态)
             进入索敌状态，执行索敌动作
             如果攻击范围内有敌方单位，则锁定
             如果攻击范围没有敌方单位，则寻找敌方单位（接近敌方单位）
          else：
             当前智能体对锁定目标发动攻击
        :return:
        """
        if self.entity.machine.locked > 0 and not self.flag_locked:
            self.flag_locked = True
            if random.uniform(0, 1) < 0.5:
                return FSMStateEnum.esca
            else:
                return self.state.type()
        else:
            md = self.entity.machine.get_device("MissilesDevice")
            mnum: int = 0
            if md is not None:
                for missile in md.missiles:
                    if missile is not None:
                        mnum += 1
            if mnum < self.enemy:
                return FSMStateEnum.rep
            elif mnum < md.num_slots and not self.flag_missle_short:
                self.flag_missle_short = True
                if random.uniform(0, 1) < 0.3:
                    return FSMStateEnum.rep
                else:
                    return self.state.type()
            else:
                return FSMStateEnum.sear
