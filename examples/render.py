#!/usr/bin/env python

import gymnasium as gym
import gymnasium_csv

env = gym.make('gymnasium_csv-v0',
               render_mode='human',  # "human", "text", None
               inFileStr='../assets/map2.csv',
               initX=2,
               initY=2,
               goalX=11,
               goalY=9)
env.reset()
env.render()
