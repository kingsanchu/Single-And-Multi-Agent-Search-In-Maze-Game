import random
import datetime
import csv
import os
from tkinter import *
from mazeGame import COLOR, textLabel
from enum import Enum
from collections import deque
class Agent:

    def __init__(self, parentMaze, x=None, y=None, shape='square', goal=None, filled=False, footprints=False, color: COLOR = COLOR.blue):

        self._parentMaze = parentMaze
        self.color = color
        if (isinstance(color, str)):
            if (color in COLOR.__members__):
                self.color = COLOR[color]
            else:
                raise ValueError(f'{color} is not a valid COLOR!')
        self.filled = filled
        self.shape = shape
        self._orient = 0
        if x is None:
            x = parentMaze.rows
        if y is None:
            y = parentMaze.cols
        self.x = x
        self.y = y
        self.footprints = footprints
        self._parentMaze._agents.append(self)
        if goal == None:
            self.goal = self._parentMaze._goal
        else:
            self.goal = goal
        self._body = []
        self.position = (self.x, self.y)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, newX):
        self._x = newX

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, newY):
        self._y = newY
        w = self._parentMaze._cell_width
        x = self.x*w-w+self._parentMaze._LabWidth
        y = self.y*w-w+self._parentMaze._LabWidth
        if self.shape == 'square':
            if self.filled:
                self._coord = (y, x, y + w, x + w)
            else:
                self._coord = (y + w/2.5, x + w/2.5, y +
                               w/2.5 + w/4, x + w/2.5 + w/4)
        else:
            self._coord = (y + w/2, x + 3*w/9, y + w/2, x + 3*w/9+w/4)

        if (hasattr(self, '_head')):
            if self.footprints is False:
                self._parentMaze._canvas.delete(self._head)
            else:
                if self.shape == 'square':
                    self._parentMaze._canvas.itemconfig(
                        self._head, fill=self.color.value[1], outline="")
                    self._parentMaze._canvas.tag_raise(self._head)
                    try:
                        self._parentMaze._canvas.tag_lower(self._head, 'ov')
                    except:
                        pass
                    if self.filled:
                        cell_coordinates = self._parentMaze._canvas.coords(
                            self._head)
                        old_cell = (round(((cell_coordinates[1]-26)/self._parentMaze._cell_width)+1), round(
                            ((cell_coordinates[0]-26)/self._parentMaze._cell_width)+1))
                        self._parentMaze._redrawCell(
                            *old_cell, self._parentMaze.theme)
                else:
                    self._parentMaze._canvas.itemconfig(
                        self._head, fill=self.color.value[1])  # ,outline='gray70')
                    self._parentMaze._canvas.tag_raise(self._head)
                    try:
                        self._parentMaze._canvas.tag_lower(self._head, 'ov')
                    except:
                        pass
                self._body.append(self._head)
            if not self.filled or self.shape == 'arrow':
                if self.shape == 'square':
                    self._head = self._parentMaze._canvas.create_rectangle(
                        *self._coord, fill=self.color.value[0], outline='')  # stipple='gray75'
                    try:
                        self._parentMaze._canvas.tag_lower(self._head, 'ov')
                    except:
                        pass
                else:
                    self._head = self._parentMaze._canvas.create_line(
                        *self._coord, fill=self.color.value[0], arrow=FIRST, arrowshape=(3/10*w, 4/10*w, 4/10*w))  # ,outline=self.color.name)
                    try:
                        self._parentMaze._canvas.tag_lower(self._head, 'ov')
                    except:
                        pass
                    orientation = self._orient % 4
                    if orientation == 1:
                        self.rotate_clockwise()
                        self._orient -= 1
                    elif orientation == 3:
                        self.rotate_counter_clockwise()
                        self._orient += 1
                    elif orientation == 2:
                        self.rotate_counter_clockwise()
                        self.rotate_counter_clockwise()
                        self._orient += 2
            else:
                self._head = self._parentMaze._canvas.create_rectangle(
                    *self._coord, fill=self.color.value[0], outline='')  # stipple='gray75'
                try:
                    self._parentMaze._canvas.tag_lower(self._head, 'ov')
                except:
                    pass
                self._parentMaze._redrawCell(
                    self.x, self.y, theme=self._parentMaze.theme)
        else:
            self._head = self._parentMaze._canvas.create_rectangle(
                *self._coord, fill=self.color.value[0], outline='')  # stipple='gray75'
            try:
                self._parentMaze._canvas.tag_lower(self._head, 'ov')
            except:
                pass
            self._parentMaze._redrawCell(
                self.x, self.y, theme=self._parentMaze.theme)

    @property
    def position(self):
        return (self.x, self.y)

    @position.setter
    def position(self, newpos):
        self.x = newpos[0]
        self.y = newpos[1]
        self._position = newpos

    def rotate_counter_clockwise(self):
        '''
        To Rotate the agent in Counter Clock Wise direction
        '''
        def pointNew(p, newOrigin):
            return (p[0]-newOrigin[0], p[1]-newOrigin[1])
        cell_width = self._parentMaze._cell_width
        x = self.x*cell_width-cell_width+self._parentMaze._LabWidth
        y = self.y*cell_width-cell_width+self._parentMaze._LabWidth
        center = (y+cell_width/2, x+cell_width/2)
        p1 = pointNew((self._coord[0], self._coord[1]), center)
        p2 = pointNew((self._coord[2], self._coord[3]), center)
        p1_cw = (p1[1], -p1[0])
        p2_cw = (p2[1], -p2[0])
        p1 = p1_cw[0]+center[0], p1_cw[1]+center[1]
        p2 = p2_cw[0]+center[0], p2_cw[1]+center[1]
        self._coord = (*p1, *p2)
        self._parentMaze._canvas.coords(self._head, *self._coord)
        self._orient = (self._orient-1) % 4

    def rotate_clockwise(self):
        '''
        To Rotate the agent in Clock Wise direction
        '''
        def pointNew(p, newOrigin):
            return (p[0]-newOrigin[0], p[1]-newOrigin[1])
        cell_width = self._parentMaze._cell_width
        x = self.x*cell_width-cell_width+self._parentMaze._LabWidth
        y = self.y*cell_width-cell_width+self._parentMaze._LabWidth
        center = (y+cell_width/2, x+cell_width/2)
        p1 = pointNew((self._coord[0], self._coord[1]), center)
        p2 = pointNew((self._coord[2], self._coord[3]), center)
        p1_cw = (-p1[1], p1[0])
        p2_cw = (-p2[1], p2[0])
        p1 = p1_cw[0]+center[0], p1_cw[1]+center[1]
        p2 = p2_cw[0]+center[0], p2_cw[1]+center[1]
        self._coord = (*p1, *p2)
        self._parentMaze._canvas.coords(self._head, *self._coord)
        self._orient = (self._orient+1) % 4

    def moveRight(self, event):
        if self._parentMaze.maze_map[self.x, self.y]['E'] == True:
            self.y = self.y+1

    def moveLeft(self, event):
        if self._parentMaze.maze_map[self.x, self.y]['W'] == True:
            self.y = self.y-1

    def moveUp(self, event):
        if self._parentMaze.maze_map[self.x, self.y]['N'] == True:
            self.x = self.x-1
            self.y = self.y

    def moveDown(self, event):
        if self._parentMaze.maze_map[self.x, self.y]['S'] == True:
            self.x = self.x+1
            self.y = self.y
