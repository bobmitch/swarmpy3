
try:
	pass
	#import psyco
	#from psyco.classes import *
except:
	# no psyco - hope you have a nice cpu ;)
	print "No psyco..."


#psyco.full()

from heapq import heappush, heappop
import math
import operator
import pyglet
import sys
pyglet.options['debug_gl'] = False	# TURN ON FOR DEBUGGIN GL!!!
import random
from pyglet.window import key
from pyglet.window import mouse
from pyglet import resource
from pyglet.gl import *
from pyglet import clock
import copy

#FONT_NAME = 'Saved By Zero'
FONT_NAME = 'Arial'


#window.set_minimum_size (width=1024, height=768)

#
#	LOAD TEXTURES
#

def tex_border (tex):
	""" takes a pyglet texture/region and insets the texture coordinates by half a texel
		allowing for sub-pixel blitting without interpolation with nearby regions within 
		same texture atlas """
	coord_width = tex.tex_coords[3] - tex.tex_coords[0]
	coord_height = tex.tex_coords[4] - tex.tex_coords[1]
	x_adjust = (coord_width / tex.width) / 2.0	# get tex coord half texel width
	y_adjust = (coord_height / tex.height) / 2.0	# get tex coord half texel width
	# create new 12-tuple texture coordinate
	tex.tex_coords = ( 	tex.tex_coords[0]+x_adjust, tex.tex_coords[1]+y_adjust, 0,
						tex.tex_coords[3]-x_adjust, tex.tex_coords[4]+y_adjust, 0,
						tex.tex_coords[6]-x_adjust, tex.tex_coords[7]-y_adjust, 0,
						tex.tex_coords[9]+x_adjust, tex.tex_coords[10]-y_adjust, 0)
						
resource.path.append('res')
resource.reindex()

sprite_atlas = pyglet.image.atlas.TextureAtlas (width=1024, height=1024)

batch = pyglet.graphics.Batch()

pointer_image = resource.image('pointer.png')
pointer_image.anchor_x = pointer_image.width // 2
pointer_image.anchor_y = pointer_image.height // 2
pointer_image_flip = resource.image('pointer.png', flip_x=True)

small_red_bug_pic = pyglet.image.load('roomba_medium.png')
small_red_bug_tex = sprite_atlas.add (small_red_bug_pic)
small_red_bug_tex.anchor_x = small_red_bug_pic.width / 2
small_red_bug_tex.anchor_y = small_red_bug_pic.height / 2
tex_border (small_red_bug_tex)

fast_pic = pyglet.image.load('fast.png')
fast_tex = sprite_atlas.add (fast_pic)
fast_tex.anchor_x = fast_pic.width / 2
fast_tex.anchor_y = fast_pic.height / 2
tex_border (fast_tex)

valid_placement_pic = pyglet.image.load('valid_placement.png')
valid_placement_tex = sprite_atlas.add (valid_placement_pic)

selected_pic = pyglet.image.load('selected.png')
selected_tex = sprite_atlas.add (selected_pic)

money_pic = pyglet.image.load('money.png')
money_tex = sprite_atlas.add (money_pic)
money_tex.anchor_x = money_pic.width / 2
money_tex.anchor_y = money_pic.width / 2

invalid_placement_pic = pyglet.image.load('invalid_placement.png')
invalid_placement_tex = sprite_atlas.add (invalid_placement_pic)
invalid_placement_tex.anchor_x = invalid_placement_pic.width / 2
invalid_placement_tex.anchor_y = invalid_placement_pic.width / 2


cannon_1_base_pic = pyglet.image.load('cannon_1_base.png')
cannon_1_base_sprite = sprite_atlas.add (cannon_1_base_pic)

cannon_1_turret_pic = pyglet.image.load('cannon_1_turret.png')
cannon_1_turret_sprite = sprite_atlas.add (cannon_1_turret_pic)
cannon_1_turret_sprite.anchor_x = cannon_1_turret_pic.width / 2
cannon_1_turret_sprite.anchor_y = cannon_1_turret_pic.width / 2
tex_border (cannon_1_turret_sprite)

cannon_2_turret_pic = pyglet.image.load('cannon_2_turret.png')
cannon_2_turret_sprite = sprite_atlas.add (cannon_2_turret_pic)
cannon_2_turret_sprite.anchor_x = cannon_2_turret_pic.width / 2
cannon_2_turret_sprite.anchor_y = cannon_2_turret_pic.width / 2
tex_border (cannon_2_turret_sprite)

cannon_2_base_pic = pyglet.image.load('cannon_2_base.png')
cannon_2_base_sprite = sprite_atlas.add (cannon_2_base_pic)

cannon_3_turret_pic = pyglet.image.load('cannon_3_turret.png')
cannon_3_turret_sprite = sprite_atlas.add (cannon_3_turret_pic)
cannon_3_turret_sprite.anchor_x = cannon_3_turret_pic.width / 2
cannon_3_turret_sprite.anchor_y = cannon_3_turret_pic.width / 2
tex_border (cannon_3_turret_sprite)

cannon_3_base_pic = pyglet.image.load('cannon_3_base.png')
cannon_3_base_sprite = sprite_atlas.add (cannon_3_base_pic)

berserker_1_turret_pic = pyglet.image.load('berserker_1_turret.png')
berserker_1_turret_sprite = sprite_atlas.add (berserker_1_turret_pic)
berserker_1_turret_sprite.anchor_x = berserker_1_turret_pic.width / 2
berserker_1_turret_sprite.anchor_y = berserker_1_turret_pic.width / 2
tex_border (berserker_1_turret_sprite)

sell_outline_pic = pyglet.image.load ('sell_outline.png')
sell_outline_sprite = sprite_atlas.add (sell_outline_pic)

bullet_1_pic = pyglet.image.load('bullet_1.png')
bullet_1_sprite = sprite_atlas.add (bullet_1_pic)
bullet_1_sprite.anchor_x = bullet_1_pic.width / 2
bullet_1_sprite.anchor_y = bullet_1_pic.height / 2

bullet_2_pic = pyglet.image.load('bullet_2.png')
bullet_2_sprite = sprite_atlas.add (bullet_2_pic)
bullet_2_sprite.anchor_x = bullet_2_pic.width / 2
bullet_2_sprite.anchor_y = bullet_2_pic.height / 2

bullet_3_pic = pyglet.image.load('bullet_3.png')
bullet_3_sprite = sprite_atlas.add (bullet_3_pic)
bullet_3_sprite.anchor_x = bullet_3_pic.width / 2
bullet_3_sprite.anchor_y = bullet_3_pic.height / 2

rail_1_pic = pyglet.image.load('rail_1.png')
rail_1_sprite = sprite_atlas.add (rail_1_pic)
rail_1_sprite.anchor_x = rail_1_pic.width / 2
rail_1_sprite.anchor_y = rail_1_pic.height / 2

rail_2_pic = pyglet.image.load('rail_2.png')
rail_2_sprite = sprite_atlas.add (rail_2_pic)
rail_2_sprite.anchor_x = rail_2_pic.width / 2
rail_2_sprite.anchor_y = rail_2_pic.height / 2

rail_3_pic = pyglet.image.load('rail_3.png')
rail_3_sprite = sprite_atlas.add (rail_3_pic)
rail_3_sprite.anchor_x = rail_3_pic.width / 2
rail_3_sprite.anchor_y = rail_3_pic.height / 2

spark_pic = pyglet.image.load('spark.png')
spark_sprite = sprite_atlas.add (spark_pic)
spark_sprite.anchor_x = spark_pic.width / 2
spark_sprite.anchor_y = spark_pic.height / 2

blue_particle_pic = pyglet.image.load('blue_particle.png')
blue_particle_sprite = sprite_atlas.add (blue_particle_pic)
blue_particle_sprite.anchor_x = blue_particle_pic.width / 2
blue_particle_sprite.anchor_y = blue_particle_pic.height / 2

white_particle_pic = pyglet.image.load('white_particle.png')
white_particle_sprite = sprite_atlas.add (white_particle_pic)
white_particle_sprite.anchor_x = white_particle_pic.width / 2
white_particle_sprite.anchor_y = white_particle_pic.height / 2

spark_big_pic = pyglet.image.load('spark_big.png')
spark_big_sprite = sprite_atlas.add (spark_big_pic)
spark_big_sprite.anchor_x = spark_big_pic.width / 2
spark_big_sprite.anchor_y = spark_big_pic.height / 2

mote_pic = pyglet.image.load('mote.png')
mote_sprite = sprite_atlas.add (mote_pic)
mote_sprite.anchor_x = mote_pic.width / 2
mote_sprite.anchor_y = mote_pic.height / 2



range_pic = pyglet.image.load('range.png')
range_sprite = sprite_atlas.add (range_pic)


frame_test_pic = pyglet.image.load ('frame_test.png')

button_ai_weak_off_pic = pyglet.image.load ('ai_weak_off.png')
button_ai_weak_on_pic = pyglet.image.load ('ai_weak_on.png')
button_ai_strong_off_pic = pyglet.image.load ('ai_strong_off.png')
button_ai_strong_on_pic = pyglet.image.load ('ai_strong_on.png')
button_ai_slow_off_pic = pyglet.image.load ('ai_slow_off.png')
button_ai_slow_on_pic = pyglet.image.load ('ai_slow_on.png')
button_ai_fast_off_pic = pyglet.image.load ('ai_fast_off.png')
button_ai_fast_on_pic = pyglet.image.load ('ai_fast_on.png')
button_ai_near_off_pic = pyglet.image.load ('ai_near_off.png')
button_ai_near_on_pic = pyglet.image.load ('ai_near_on.png')
button_ai_far_off_pic = pyglet.image.load ('ai_far_off.png')
button_ai_far_on_pic = pyglet.image.load ('ai_far_on.png')

button_cannon_tower_pic = pyglet.image.load ('cannon.png')
button_cannon_tower_mouseover_pic = pyglet.image.load ('cannon_mouseover.png')
button_cannon_tower_selected_pic = pyglet.image.load ('cannon_selected.png')

button_berserker_tower_mouseover_pic = pyglet.image.load ('berserker_mouseover.png')
button_berserker_tower_selected_pic = pyglet.image.load ('berserker_selected.png')

button_start_pic = pyglet.image.load ('start.png')
button_pause_pic = pyglet.image.load ('pause.png')

upgrade_pic = pyglet.image.load('upgrade.png')
sell_pic = pyglet.image.load('sell_ok.png')

map_bg = resource.image ('wp.jpg')

title_background = resource.image('SWARM.jpg')
pause_background = resource.image('SWARM.png')




#
#	END OF LOAD TEXTURES
#	



#
#	LOAD AUDIO
#

#title_music =  resource.media('yarp.mp3')
#title_music.play()

audio_menu_over =  pyglet.media.StaticSource (resource.media('audio_menu_over.wav'))
audio_menu_ok =  pyglet.media.StaticSource (resource.media('audio_menu_ok.wav'))
audio_menu_escape =  pyglet.media.StaticSource (resource.media('audio_menu_escape.wav'))
audio_menu_click =  pyglet.media.StaticSource (resource.media('audio_menu_click.wav'))

audio_cannon_1_fire = pyglet.media.StaticSource (resource.media('audio_cannon_1_fire.wav'))
audio_cannon_2_fire = pyglet.media.StaticSource (resource.media('audio_cannon_2_fire.wav'))

audio_rail_1_fire = pyglet.media.StaticSource (resource.media('audio_rail_1_fire.wav'))

audio_hit =  pyglet.media.StaticSource (resource.media('hit3.wav'))
audio_explode = pyglet.media.StaticSource (resource.media('explode.mp3'))

audio_upgrade = pyglet.media.StaticSource (resource.media('upgrade.wav'))

#
#	END OF LOAD AUDIO - SET UP WINDOW
#


window = pyglet.window.Window(1024, 768,"SWARM",True)
window.set_vsync (False)
window.set_fullscreen (False)
window.clear()

# over ride default escape key behaviour
def on_key_press(symbol, modifiers):
	if symbol == key.ESCAPE:
		if game.state & game.states['ingame']:
			game.state = game.state ^ game.states['paused']
			set_overlay ( PauseMenu() )
		return True
window.push_handlers(on_key_press)

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glEnable (GL_TEXTURE_2D)	



#
#	MENU CLASSES
#

class Overlay(object):
    def update(self, dt):
        pass

    def draw(self):
        pass

class Menu(Overlay):
	def __init__ (self, title, background=None):
		self.title_text = pyglet.text.Label(title, 
                                            font_name=FONT_NAME,
                                            font_size=36,
                                            x=window.width // 2, 
                                            y=340,
                                            anchor_x='center',
                                            anchor_y='center')
		self.items = []
		self.background=background
		
	def reset(self):
		# assumes items have been added - to be called usually after menu has been setup with items.  if no items - use a banner instead :)
		self.selected_index = 0
		self.items[self.selected_index].selected = True
	
	def on_mouse_motion(self, x, y, dx, dy):
		for item in self.items:
			item.on_mouse_motion(x,y,dx,dy)
			
	def on_mouse_release(self, x, y, buttons, modifiers):
		for item in self.items:
			item.on_mouse_release(x,y,buttons,modifiers)
		
	def on_key_press(self, symbol, modifiers):
		if symbol == key.DOWN:
			self.selected_index += 1
			audio_menu_over.play()
		elif symbol == key.UP:
			self.selected_index -= 1
			audio_menu_over.play()
		else:
			self.items[self.selected_index].on_key_press(symbol, modifiers)
		self.selected_index = min(max(self.selected_index, 0), len(self.items) - 1)

		if symbol in (key.DOWN, key.UP) and game.sound_enabled:
			bullet_sound.play()
			
		if symbol == key.ESCAPE:
		# esc pressed while in a menu
			audio_menu_escape.play()
			if self.title_text.text=='Main Menu':
				# main menu esc pressed
				quit_option()
			elif self.title_text.text=='Pause':
				# in game pause menu esc pressed
				unpause()
				return pyglet.event.EVENT_HANDLED
			elif self.title_text.text=='Options':
				# options menu esc pressed, go back to main
				goto_main_menu()
			else:
				pass	# do nothing
				

	def draw(self):
		if self.background:
			self.background.blit (0,0,width=window.width, height=window.height)
		self.title_text.draw()
		
		# now check if mouse is over any of the items, if it is make sure this is the selected item
		for i, item in enumerate(self.items):
			if item.mouseover:
				if self.selected_index <> i:
					# new item, play over sound
					audio_menu_over.play()
				self.selected_index = i
				
		
		# now draw item, sending flag of true as parameter if this is selected - this will trigger the pointer drawing routine on this item
		for i, item in enumerate(self.items):
			item.draw(i == self.selected_index)
	

class MenuItem(object):
	pointer_color = (.46, 0, 1.)
	inverted_pointers = False
	
	def __init__(self, label, y, activate_func):
		self.y = y
		self.text = pyglet.text.Label(label,
                                      font_name=FONT_NAME,
                                      font_size=24,
                                      x=window.width // 2, 
                                      y=y,
                                      anchor_x='center',
                                      anchor_y='center')
		self.activate_func = activate_func
		self.mouseover=False

	def draw_pointer(self, x, y, color, flip=False):
		# Tint the pointer image to a color
		glPushAttrib(GL_CURRENT_BIT)
		glColor3f(*color)
		if flip:
			pointer_image_flip.blit(x, y)
		else:
			pointer_image.blit(x, y)
		glPopAttrib()

	def draw(self, selected):
		self.text.draw()

		if selected:
			self.draw_pointer(
                self.text.x - self.text.content_width / 2 - 
                    pointer_image.width / 2,
                self.y, 
                self.pointer_color,
                self.inverted_pointers)
			self.draw_pointer(
                self.text.x + self.text.content_width / 2 + 
                    pointer_image.width / 2,
                self.y,
                self.pointer_color,
                not self.inverted_pointers)

	def on_key_press(self, symbol, modifiers):
		if symbol == key.ENTER and self.activate_func:
			audio_menu_click.play()
			self.activate_func()
			
	def on_mouse_motion(self, x, y, dx, dy):
		if (y>self.text.y-(self.text.font_size//2) and y<self.text.y+(self.text.font_size//2)):
			self.mouseover=True
		else:
			self.mouseover=False
			
	def on_mouse_release(self, x, y, buttons, modifiers):
		if self.mouseover and buttons & mouse.LEFT:
			audio_menu_click.play()
			self.activate_func()


class ToggleMenuItem(MenuItem):
	pointer_color = (.27, .82, .25)
	inverted_pointers = True

	def __init__(self, label, value, y, toggle_func):
		self.value = value
		self.label = label
		self.toggle_func = toggle_func
		super(ToggleMenuItem, self).__init__(self.get_label(), y, None)

	def get_label(self):
		return self.label + (self.value and ': ON' or ': OFF')

	def on_key_press(self, symbol, modifiers):
		if symbol == key.LEFT or symbol == key.RIGHT:
			self.value = not self.value
			self.text.text = self.get_label()
			self.toggle_func(self.value)
			audio_menu_ok.play()	

	def on_mouse_release(self, x, y, buttons, modifiers):
	# overrides menuitem mouse release funtion
		if self.mouseover and buttons & mouse.LEFT:
			self.value = not self.value
			self.text.text = self.get_label()
			self.toggle_func(self.value)
			audio_menu_ok.play()	
			
			
	
class MainMenu(Menu):
	def __init__(self):
		super(MainMenu, self).__init__('Main Menu',background=title_background)
		self.items.append(MenuItem('Start', 280, begin_option))
		self.items.append(MenuItem('Options',250, options_option))
		self.items.append(MenuItem('Quit', 100, quit_option))
		self.reset()
		
class PauseMenu(Menu):
	def __init__(self):
		super(PauseMenu, self).__init__('Pause',background=pause_background)
		self.items.append(MenuItem('Continue',280,unpause))
		self.items.append(MenuItem('Main Menu',250,end_game))
		self.items.append(MenuItem('Game Options',220,ingame_options_option))
		self.items.append(MenuItem('Restart',160,begin_option))
		self.items.append(MenuItem('Quit',100,quit_option))
		self.reset()
		
	

class OptionsMenu(Menu):
	def __init__(self):
		super(OptionsMenu, self).__init__('Options',background=title_background)
		self.items.append(ToggleMenuItem('Fullscreen', window.fullscreen, 280, toggle_fullscreen_options_menu))
		self.items.append(ToggleMenuItem('Vsync', window.vsync, 250, window.set_vsync))
		self.items.append(MenuItem('Done', 190, end_game))
		self.reset()
		
class IngameOptionsMenu(Menu):
	def __init__(self):
		super(IngameOptionsMenu, self).__init__('Options',background=pause_background)
		self.items.append(ToggleMenuItem('Fullscreen', window.fullscreen, 280, toggle_fullscreen_ingameoptions_menu))
		self.items.append(ToggleMenuItem('Vsync', window.vsync, 250, window.set_vsync))
		self.items.append(MenuItem('Done', 190, pause))
		self.reset()
		
class GameOver (Menu):
	def __init__(self):
		super(GameOver, self).__init__('Game Over!',background=pause_background)
		self.items.append(MenuItem('Retry',280, begin_option))
		self.items.append(MenuItem('Main Menu',250,goto_main_menu))
		self.items.append(MenuItem('Quit',100,quit_option))
		self.reset()
		
# menu option functions

def toggle_fullscreen_options_menu(value):
	window.set_fullscreen(value)
	set_overlay (None)
	set_overlay (OptionsMenu())

def toggle_fullscreen_ingameoptions_menu(value):
	window.set_fullscreen(value)
	set_overlay (None)
	set_overlay (IngameOptionsMenu())
	
def pause():
	set_overlay ( PauseMenu() )

def unpause():
	game.state = game.state ^ game.states['paused']
	set_overlay ( None )

def ingame_options_option():
	set_overlay ( IngameOptionsMenu() )
	
def options_option():
	set_overlay ( OptionsMenu() )
	
def end_game ():
	# remove handlers of all objects
	for tower in game.towers:
		window.remove_handlers(tower)
	# reset game state and overlay
	game.state = game.states['menu']
	set_overlay ( MainMenu() )
	
def goto_main_menu():
	game.state = game.states['menu']
	set_overlay ( MainMenu() )

def begin_option ():
	# remove handlers of any towers left over from previous game (this could be from 'retry' option at gameover...
	for tower in game.towers:
		window.remove_handlers(tower)
	set_overlay(None)
	game.reset()
	if start_button not in gui.widgets:
		gui.widgets.append (start_button)
	game.state =  game.states['pregame'] | game.states['ingame']
	
def quit_option ():
	sys.exit()
	
def set_overlay(new_overlay):
	if game.overlay:
		window.remove_handlers(game.overlay)
	game.overlay = new_overlay
	if game.overlay:
		window.push_handlers(game.overlay)
		
		
		
		
		
#
#	END OF MENU CLASSES / FUNCTIONS
#	
	
	
	
	
def draw_circle (x, y, r,i):
	""" r = radius, i = steps"""
	angle=0
	r*=game.map.cellsize
	glLineWidth (2)
	glColor4f (1,0.5,0.5,0.5)
	glDisable (GL_TEXTURE_2D)
	glPushMatrix()
	glTranslatef (x,y,0)
	glBegin (GL_LINE_STRIP)
	while angle<=i+(math.pi*2):
		glVertex2f (math.cos(angle)*r, math.sin(angle)*r)
		angle+=i
	glEnd()
	glPopMatrix()
	glEnable (GL_TEXTURE_2D)
	glColor4f(1,1,1,1)
	

class amouse(object):
	def __init__ (self):
		self.x = 0
		self.y = 0
		self.mapx = 0
		self.mapy = 0
		self.dx = 0	# deploy x and y - used rather than mapx and mapy to give more natural feel to deploying towers
		self.dy = 0
		self.overmap = False
		self.lmb_clicked=False
		self.rmb_clicked=False
		self.tex = None
		
	def update_pos (self,x,y):
		self.x = x
		self.y = y
		
	def draw (self):
		if game.state & game.states['ingame'] and not game.state & game.states['paused'] and self.tex:
			if self.tex is valid_placement_tex:
				glColor4f (1,1,1,0.3)
				self.tex.blit (self.x-game.map.cellsize, self.y-game.map.cellsize)
				glColor4f (1,1,1,1)
				self.tex.blit (game.map.llx + (self.dx*game.map.cellsize), game.map.lly + (self.dy*game.map.cellsize) )
				draw_circle (self.x, self.y, game.deploying.range_sq, 0.15)
			else:
				self.tex.blit (self.x, self.y)
		
		
	def update (self):
		# get map coords and display appropraite mouse icons
		if game.state & game.states['ingame']:
			if self.x > game.map.llx and self.x < game.map.llx + game.map.width_pixels and self.y > game.map.lly and self.y < game.map.lly + game.map.height_pixels:
				self.overmap = True
				self.mapx = (self.x - game.map.llx ) / game.map.cellsize
				self.mapy = (self.y - game.map.lly ) / game.map.cellsize
				#if game.deploying and game.map.placement_valid (self.mapx, self.mapy):
				if game.deploying:
					self.dx = int( ((self.x - game.map.llx )-(game.map.cellsize*0.5)) / game.map.cellsize)
					self.dy = int( ((self.y - game.map.lly )-(game.map.cellsize*0.5)) / game.map.cellsize)
					if game.credits >= game.deploying.cost:
						if game.map.placement_valid (self.dx, self.dy):
							self.tex = valid_placement_tex
						else:
							self.tex = invalid_placement_tex
					else:
						self.tex = money_tex
				
			else:
				self.overmap = False
				self.tex = None
				self.mapx = -1
				self.mapy = -1
		# reset mouse clicks from last frame and handle mouse clicks made 
		if self.lmb_clicked:
			self.lmb_clicked=False
			if game.state & game.states['ingame']:
				if self.tex is valid_placement_tex and game.deploying:
					if game.deploying.deploy():
						audio_menu_ok.play()
						game.credits-=game.deploying.cost
						credits_label.text = 'Credits: '+str(game.credits)
						game.deploying=copy.copy(game.deploying)	# ready to deploy next tower of same type
					else:
						pass # could not deploy for whatever reason
					
					
				if (self.tex is invalid_placement_tex or self.tex is money_tex) and game.deploying:
					# handle playing of error noise or something
					audio_menu_escape.play()
					pass
		if self.rmb_clicked:
			game.deploying=None
			self.tex = None
			game.selected=None
			audio_menu_escape.play()
			self.rmb_clicked=False
			
		
			

			
		
	def over (self, ll, tr):
		if self.x >= ll[0] and self.x <= tr[0] and self.y >= ll[1] and self.y <=tr[1]:
			return True
		else:
			return False

class GUI(object):
	""" gui contains widgets or frames, which contain all widgets """
	def __init__ (self):
		# get coords of corners
		self.ll = (0,0)
		self.lr = (window.width,0)
		self.tr = (window.width,window.height)
		self.tl = (0,window.height)
		self.widgets=[]
		self.enabled = True # always true
		
	def update (self,dt):
		for frame in self.widgets:
			frame.update(dt)
			
	def draw (self):
		for frame in self.widgets:
			frame.draw()
		
class Frame(object):
	""" a widget container """
	def __init__ (self, pos=(250,250), width=100, height=100, scale=False, border=None, background=None, background_colour=None):
		self.pos=pos
		self.scale=scale
		self.enabled = True
		self.visible = True
		
		# if background texture supplied, use that to determine area of frame, unless scale is True
		if background and not scale:
			self.width = background.width
			self.height = background.height
		else:
			self.width=width
			self.height=height
		
		# get coords of corners
		self.ll = (pos[0],pos[1]-self.height)
		self.lr = (pos[0]+self.width,pos[1]-self.height)
		self.tr = (pos[0]+self.width,pos[1])
		self.tl = (pos[0], pos[1])
			
		self.widgets=[]
		self.background = background
		
		# if no background colour given, then make it opaqe if texture given, otherwise make it almost black
		if background_colour is None:
			if background:
				self.background_colour = (1,1,1,1)
			else:
				self.background_colour = (1,1,1,0.1)
		else:
			self.background_colour = background_colour
		self.border = border
		
		# logic
		self.mouseover = False
		
		# callbacks
		self.on_mouseover = None
		
		# add self to gui
		gui.widgets.append (self)
		
	def update(self,dt):
		if self.visible:
			if mymouse.over ( self.ll , self.tr ):
				self.mouseover = True
			else:
				self.mouseover = False
				
			# update widgets in frame
			for widget in self.widgets:
				widget.update(dt)
		
			
	def draw (self):
		if self.enabled:
			if self.background:
				if self.scale:
					glColor4f (*self.background_colour)
					self.background.blit (self.ll[0], self.ll[1], width=self.width, height=self.height)
					glColor4f (1,1,1,1)
				else:
					glColor4f (*self.background_colour)
					self.background.blit (self.ll[0], self.ll[1])
					glColor4f (1,1,1,1)
			else:
				glColor4f (*self.background_colour)
				glDisable (GL_TEXTURE_2D)
				pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (	self.ll[0], self.ll[1],
																		self.lr[0], self.lr[1],
																		self.tr[0], self.tr[1],
																		self.tl[0], self.tl[1])))
				glEnable (GL_TEXTURE_2D)
				glColor4f (1,1,1,1)
			for widget in self.widgets:
				widget.draw()

class Button(object):
	""" a button widget """
	def __init__ (self, parent, pos=(10, 10), width=10, height=10, scale=False, rmb_clears=True, background=None, background_colour=None, background_selected=None, background_mouseover=None):
		self.parent=parent # pointer to parent frame
	
		self.pos=(parent.tl[0]+pos[0], parent.tl[1]-pos[1])	# relative to parent top left
		self.scale=scale
		self.enabled=True
		self.visible=True
		self.rmb_clears=rmb_clears
		
		
		# if background texture supplied, use that to determine area of frame
		if background and not scale:
			self.width = background.width
			self.height = background.height
		else:
			self.width=width
			self.height=height
		
		# get coords of corners
		self.ll = (self.pos[0],				self.pos[1]-self.height)
		self.lr = (self.pos[0]+self.width,	self.pos[1]-self.height)
		self.tr = (self.pos[0]+self.width,	self.pos[1])
		self.tl = (self.pos[0], 			self.pos[1])
			
		self.background = background
		self.background_mouseover = background_mouseover
		
		self.background_selected = background_selected
		
		# if no background colour given, then make it opaqe if texture given, otherwise make it almost black
		if background_colour is None:
			if background:
				self.background_colour = (1,1,1,1)
			else:
				self.background_colour = (1,1,1,0.1)
		else:
			self.background_colour = background_colour
		
		# logic
		self.mouseover = False
		self.click = False
		self.selected = False
		
		# callbacks
		self.on_mouseover = None
		self.on_click = None
		self.on_right_click = None
		
		# add self to parent frame
		parent.widgets.append (self)
		
		# push handlers
		window.push_handlers(self)
		
	def update(self,dt):
		if self.enabled:
			pass
			
	def draw (self):
		if self.visible:
			if not self.enabled:
				glColor4f (1,1,1,0.6)
				self.background.blit (self.ll[0], self.ll[1])
				glColor4f (1,1,1,1)
				return
			if self.selected:
				glColor4f (*self.background_colour)
				self.background_selected.blit (self.ll[0], self.ll[1])
				glColor4f (1,1,1,1)
			else:
				if self.mouseover and self.background_mouseover:
					glColor4f (*self.background_colour)
					self.background_mouseover.blit (self.ll[0], self.ll[1])
					glColor4f (1,1,1,1)
				elif self.mouseover:
					self.background.blit (self.ll[0], self.ll[1])
				else:
					glColor4f (1,1,1,0.75)
					self.background.blit (self.ll[0], self.ll[1])
					glColor4f (1,1,1,1)
					
		
	def on_mouse_motion(self, x, y, dx, dy):
		if (x>self.ll[0] and x<self.tr[0] and y>self.ll[1] and y<self.tl[1]):
			if not self.mouseover:
				#audio_menu_over.play()
				self.mouseover=True
		else:
			self.mouseover=False
			
	def on_mouse_release(self, x, y, buttons, modifiers):
		if self.mouseover and buttons & mouse.LEFT  and self.visible and self.parent.enabled:
			if self.on_click:
				#audio_menu_click.play()
				self.on_click(self)
		if buttons & mouse.RIGHT and self.rmb_clears:
			self.selected = False
		

		
class anUpgrade(object):
	def __init__ (self, x, y, time, next_tower, oldai=0):
		self.x = copy.copy(x)
		self.y = copy.copy(y)
		self.screenx = game.map.llx + x*game.map.cellsize
		self.screeny = game.map.lly + y*game.map.cellsize
		self.time=time
		self.time_alive=0
		self.scale = 1.0 / time
		self.next_tower = next_tower
		self.oldai=oldai
		
	def update(self,dt):
		self.time_alive+=dt
		if self.time_alive>self.time:
			# upgrade complete
			print "Updgrade complete, putting tower at ", self.next_tower.pos
			self.next_tower.deploy_fast ()	# tells itself to deploy quickly with no map recalcs, and push its handlers itself
			# give upgraded tower same ai as old one - if applicable
			if self.oldai:
				self.next_tower.target_mode = self.oldai
			game.towers.remove (self)	# remove upgrade tower no longer needed
			
	def draw_selection (self):
		# no need for mouse detection - but function required
		pass
			
	def draw(self):
		glColor4f (1,1,0.5, (self.time_alive * self.scale))
		glDisable (GL_TEXTURE_2D)
		pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (	self.screenx, self.screeny,
																self.screenx+game.cw*2, self.screeny,
																self.screenx+game.cw*2, self.screeny+game.cw*2,
																self.screenx, self.screeny+game.cw*2)))
		glEnable (GL_TEXTURE_2D)
		glColor4f (1,1,1,1)
		sell_outline_sprite.blit (self.screenx, self.screeny)
		
		
		

class aSell(object):
	def __init__ (self, x, y, time):
		self.x = copy.copy(x)
		self.y = copy.copy(y)
		self.screenx = game.map.llx + x*game.map.cellsize
		self.screeny = game.map.lly + y*game.map.cellsize
		self.time=time
		self.time_alive=0
		self.scale = 1.0 / time
		
	def update(self,dt):
		self.time_alive+=dt
		if self.time_alive>self.time:
			# sale complete - update map and recalc routes
			game.towers.remove (self)
			game.map.cell[self.x][self.y].passable=True
			game.map.cell[self.x+1][self.y].passable=True
			game.map.cell[self.x+1][self.y+1].passable=True
			game.map.cell[self.x][self.y+1].passable=True
			game.map.recalc_routes()
			
	def draw_selection (self):
		# no need 
		pass
			
	def draw(self):
		glColor4f (1,1,0.5, 1-(self.time_alive * self.scale))
		glDisable (GL_TEXTURE_2D)
		pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (	self.screenx, self.screeny,
																self.screenx+game.cw*2, self.screeny,
																self.screenx+game.cw*2, self.screeny+game.cw*2,
																self.screenx, self.screeny+game.cw*2)))
		glEnable (GL_TEXTURE_2D)
		glColor4f (1,1,1,1)
		sell_outline_sprite.blit (self.screenx, self.screeny)
		
		
		
class aCell(object):
	def __init__ (self):
		self.passable=True
		self.tower = None
		

class aSwarm(object):
	def __init__(self, type=0, no=10, health=100, time=60, credits=10):
		""" create a swarm """
		
		self.type=type
		self.no=no
		self.count=0
		self.health=health
		self.credits=credits
		self.time=time
		if type==0:
			self.time_between_spawns = 0.8
		elif type==1:
			self.time_between_spawns = 1.0
		elif type==2:
			self.time_between_spawns = 0.05
		self.time_since_last_spawn=0
		
	def update (self, tick):
		self.time -= tick
		self.time_since_last_spawn+=tick
		if self.count < self.no and self.time_since_last_spawn > self.time_between_spawns:
			if self.type == 0:
				# create critter type 0 at start of routes
				for route in game.map.routes:
					yadda = normalEnemy(route, self.health, self.credits )
					yadda.health=self.health
					game.enemies.append ( yadda )
					self.count+=1
					self.time_since_last_spawn=0
			if self.type == 1:
				# create critter type 1 at start of routes
				for route in game.map.routes:
					yadda = fastEnemy(route, self.health, self.credits )
					yadda.health=self.health
					game.enemies.append ( yadda )
					self.count+=1
					self.time_since_last_spawn=0
			if self.type == 2:
				# create critter type 2 at start of routes
				for route in game.map.routes:
					yadda = normalEnemy(route, self.health, self.credits )
					yadda.health=self.health
					game.enemies.append ( yadda )
					self.count+=1
					self.time_since_last_spawn=0
		if self.time < 0:
			# do next wave
			if game.map.swarms and len(game.map.active_swarms)==1:
				# if this is only current swarm, and still have swarms left, pop next from list onto actives
				game.map.active_swarms.append ( game.map.swarms.pop(0) )
			# remove self from active swarm list
			game.map.active_swarms.remove (self)
			
			
		# else do nothing

class aNode(object):
	def __init__ (self,pos):
		self.pos=pos
		self.next=None
		self.distance=99999
	
	#for heapq
	#def __cmp__(self, other): return cmp(self.distance, other.distance)
	
	#def __eq__ (self, other): return self is other
	def __eq__ (self, other): return self.distance == other.distance
	def __ne__ (self, other): return self.distance <> other.distance
	def __lt__ (self, other): return self.distance < other.distance
	def __gt__ (self, other): return self.distance > other.distance
	def __le__ (self, other): return self.distance <= other.distance
	def __ge__ (self, other): return self.distance >= other.distance
	
	#def __hash__ (self): return (100*self.pos[0] + self.pos[0])
	#def __hash__ (self): return id(self)
			
class aRoute(object):
	def __init__ (self, start, end, map):
		""" route class - takes start, end tuples of (x,y), and the map it belongs to """
		self.map = map
		self.start=start
		self.end=end
		self.route={}
		for a in xrange(0,self.map.width):
			for b in xrange(0,self.map.height):
				self.route[(a,b)]=aNode((a,b))
				
	
	def reset (self):
		for a in xrange(0,self.map.width):
			for b in xrange(0,self.map.height):
				self.route[(a,b)].next=None
				self.route[(a,b)].distance=99999
			


	def recalc (self):
		"""	dijkstra algorithm - works from exit to start fills all reachable nodes in map """
		path_found = False
		self.reset()
		Q = []
		visited = {}
		self.route[(self.end[0],self.end[1])].next=None
		self.route[(self.end[0],self.end[1])].distance=0	# dist to exit (end) node is going to be zero
		# create starting set Q, (binary heap) containing all nodes with exit node set to 0
		heappush (Q, self.route[(self.end[0],self.end[1])] )
		map = self.map
		nb = self.map.get_neighbours
		distance = 1	# default distance - changed to 1.4 for diagonals
		start=self.start		# set up local for speed
		self_route=self.route	# set up local for speed
		hpop = heappop			# set up local for speed
		hpush = heappush		# set up local for speed
		while Q:
			curnode = hpop (Q)	# pop next nearest node off top of binary heap
			if curnode.pos not in visited:
				curnode_pos = curnode.pos	# remove dot for speed
				visited[curnode_pos]=True
				neighbours = nb (curnode_pos)
				for pos in neighbours:
					if pos == start:
						path_found = True
					neighbour_node = self_route [(pos[0],pos[1])]
					if pos[0]<>curnode_pos[0] and pos[1]<>curnode_pos[1]:
						distance = 1.4
					else:
						distance = 1
					newdist = curnode.distance+distance
					if neighbour_node.distance > newdist:
						neighbour_node.next = curnode
						neighbour_node.distance = newdist
					if neighbour_node.pos not in visited:
						# if neighbour node not already fully processed, stick on priority queue for consideration
						hpush (Q, neighbour_node)
		return path_found
		
	
	
	
	
	def recalc_no_priority (self):
		"""	dijkstra algorithm - works from exit to start fills all reachable nodes in map 
			no priority queue - so produces not so great paths - but very fast """
		path_found = False
		self.reset()
		Q = []
		visited = {}
		self.route[(self.end[0],self.end[1])].next=None
		self.route[(self.end[0],self.end[1])].distance=0	# dist to exit (end) node is going to be zero
		# create starting set Q, (binary heap) containing all nodes with exit node set to 0
		Q.append (self.route[(self.end[0],self.end[1])] )
		map = self.map
		nb = self.map.get_neighbours
		distance = 1	# default distance - changed to 1.4 for diagonals
		start=self.start	# set up local for speed
		while Q:
			curnode = Q.pop()	# pop next nearest node off top of binary heap
			if curnode.pos not in visited:
				visited[curnode.pos]=True
				neighbours = nb (curnode.pos)
				for pos in neighbours:
					if pos == start:
						path_found = True
					neighbour_node = self.route[(pos[0],pos[1])]
					if pos[0]<>curnode.pos[0] and pos[1]<>curnode.pos[1]:
						distance = 1.4
					else:
						distance = 1
					if neighbour_node.distance > curnode.distance+distance:
						neighbour_node.next = curnode
						neighbour_node.distance = curnode.distance+distance
					if neighbour_node.pos not in visited:
						# if neighbour node not already fully processed, stick on priority queue for consideration
						Q.append (neighbour_node)
		return path_found
		

		
		
		
class aMap(object):
	def __init__ (self, width=28, height=24, cellsize=24, llx=148, lly=148):
		""" aMap - takes width, height, cellsize and llx and lly for offset of lower left hand corner from screen edges """
		# create 2d array of Cells
		self.cell = []
		self.width = width
		self.height = height
		self.width_pixels = width * cellsize
		self.height_pixels = height * cellsize
		self.current_swarm=0
		self.llx = llx
		self.lly = lly
		self.cellsize=cellsize
		self.sell_time = 2
		self.sell_time_multiplier = 1.05
		
		
		self.active_swarms = []
		self.swarms = []	# type, number of critters, health of each critter, time till next swarm, credits per kill
		self.swarms.append ( aSwarm (0, 5, 10, 10, 1) )
		self.swarms.append ( aSwarm (0, 10, 15, 10, 1) )
		self.swarms.append ( aSwarm (1, 15, 15, 20, 2) )
		self.swarms.append ( aSwarm (2, 20, 20, 20, 2) )
		self.swarms.append ( aSwarm (1, 25, 40, 20, 3) )
		self.swarms.append ( aSwarm (0, 20, 80, 30, 3) )
		self.swarms.append ( aSwarm (1, 20, 110, 30, 3) )
		self.swarms.append ( aSwarm (2, 30, 140, 30, 4) )
		self.swarms.append ( aSwarm (1, 30, 200, 40, 4) )
		self.swarms.append ( aSwarm (2, 30, 300, 40, 5) )
		self.swarms.append ( aSwarm (1, 40, 300, 50, 5) )		
		
		self.routes=[]
		self.routes.append ( aRoute( (0,height/2), (width-1,height/2), self) )
		self.routes.append ( aRoute( (width/2,height-1), (width/2,0), self) )
		
		
		# create map
		for a in xrange(0,width):
			row=[]
			for b in xrange(0,height):
				row.append ( aCell() )
			self.cell.append ( row )
			
		
			
		# TEMPORARY WALLS - TODO: implement custom map loading
		for a in range(width):
			if a < (width/2)-4 or a > (width/2)+3:
				self.cell[a][0].passable = False
				self.cell[a][height-1].passable = False
		for a in range(height):
			if a < (height/2)-3 or a > (height/2)+2:
				self.cell[0][a].passable = False
				self.cell[width-1][a].passable = False
		
		self.create_display_list()
		
	def swarm_update (self, tick):
		if self.active_swarms:
			for swarm in self.active_swarms:
				swarm.update(tick)
			
	def create_display_list (self):
		glNewList(1,GL_COMPILE)
		
		# draw map background here if needed
		map_bg.blit (self.llx, self.lly, width=(self.width*self.cellsize), height=(self.height*self.cellsize))
		
		glDisable (GL_TEXTURE_2D)
		
		# GRID
		glColor4f (0.7,0.7,1,0.05)
		glLineWidth(1)
		glBegin (GL_LINES)
		for x in range (0,self.width+1):
			glVertex2f (self.llx + (x*self.cellsize), self.lly)
			glVertex2f (self.llx + (x*self.cellsize), self.lly + (self.height * self.cellsize))
		for y in range (0,self.height+1):
			glVertex2f (self.llx, self.lly + (y*self.cellsize))
			glVertex2f (self.llx + (self.width * self.cellsize), self.lly + (y*self.cellsize))
		glEnd()
		
		# WALLS
		glColor4f (1,1,1,0.2)
		glBegin (GL_QUADS)
		for x in range (0,self.width):
			for y in range (0,self.height):
				if self.cell[x][y].passable != True:
					glVertex2f ( (x*self.cellsize)+self.llx, (y*self.cellsize)+self.lly)
					glVertex2f ((x*self.cellsize)+self.llx, (y*self.cellsize)+self.lly+self.cellsize)
					glVertex2f ((x*self.cellsize)+self.llx+self.cellsize, (y*self.cellsize)+self.lly+self.cellsize)
					glVertex2f ((x*self.cellsize)+self.llx+self.cellsize, (y*self.cellsize)+self.lly)
		glEnd()
		glColor4f (1,1,1,1)
		
		glEnable (GL_TEXTURE_2D)
		
		glEndList()
		
	def draw (self):
		pass
		glCallList(1)
		
	def draw_selection (self):
		pass
		
	def debug_check_cells (self):
		for x in range(self.width):
			for y in range(self.height):
				print "Cell ",x,",",y," is passable? ", self.cell[x][y].passable
				
	def recalc_routes (self):
		valid = True
		for route in self.routes:
			#if not route.recalc_no_priority():
			if not route.recalc():
				valid = False
		return valid
		

		
	def get_neighbours (self, pos):
		""" for pos (tuple of x,y) returns passable neightbours in map as a list of coordinate tuples - empty list if none """
		l=[]
		px=pos[0]
		py=pos[1]
		# create local for speed
		c = self.cell
		for x in xrange (pos[0]-1, pos[0]+2):
			for y in xrange (pos[1]-1,pos[1]+2):
				if x is not -1 and y is not -1 and x is not self.width and y is not self.height:
					# in bounds
					#print "debug: getting neighbours for cell at ",x,",",y
					if c[x][y].passable:
						corner_walkable=True
						if x == px-1:
							if y == py-1:
								if c[px-1][py].passable is False or c[px][py-1].passable is False:
									corner_walkable=False
							elif y == py+1:
								if c[px-1][py].passable is False or c[px][py+1].passable is False:
									corner_walkable=False
						elif x == px+1:
							if y == py-1:
								if c[px][py-1].passable is False or c[px+1][py].passable is False:
									corner_walkable=False
							elif y == py+1:
								if c[px+1][py].passable is False or c[px][py+1].passable is False:
									corner_walkable=False
						if corner_walkable:
							l.append ( (x,y) )
		return l
		
	def placement_valid (self, x, y):
		""" takes map x and y and determines if 2x2 placement is valid """
		# check against map itself
		if x<0 or y<0 or x>self.width-2 or y>self.height-2:
			return False
		if not self.cell[x][y].passable or not self.cell[x+1][y].passable or not self.cell[x+1][y+1].passable or not self.cell[x][y+1].passable:
			return False
		# map is ok, check against all beasties
		for enemy in game.enemies:
			if int(enemy.pos[0]) == x or int(enemy.pos[0]) == x+1:
				if int(enemy.pos[1]) == y or int(enemy.pos[1]) == y+1:
					return False
		return True
	



class normalEnemy(object):
	""" normal enemy class.  takes:  route, health, credits """
	def __init__ (self, route=None, health = 10, credits = 5):
		self.map = game.map
		self.pos=[0,0]
		self.pos[0]=route.start[0]+0.5
		self.pos[1]=route.start[1]+0.5
		
		self.route = route
		self.diag = False
		self.health = health
		self.credits = credits
		self.alive = True
		self.dir = None
		self.target_dir = None
		self.speed = 1.8
		
		self.next_position = copy.copy(self.route.route[(int(self.pos[0]),int(self.pos[1]))].next.pos)
		self.next_position = (self.next_position[0]+0.5,self.next_position[1]+0.5)
		self.previous_position = self.next_position
		
		# offset start and randomize a bit
		if route.start[0]==0:
			self.pos[0]-=4
			yrand=-2+(int(random.random()*4))
			self.pos[1]+=yrand
			self.next_position = (self.next_position[0]-1, self.pos[1])
		if route.start[1]==game.map.height-1:
			self.pos[1]+=4
			xrand=-2+(int(random.random()*4))
			self.pos[0]+=xrand
			self.next_position = (self.pos[0], self.next_position[1]+1)
		
		if abs(self.pos[0]-self.next_position[0]) > 0.6 and abs(self.pos[1]-self.next_position[1]) > 0.6:
			self.diag = True
		else:
			self.diag = False
		# make sure initial direction is facing intital target path
		self.set_target_dir()
		self.dir = copy.copy (self.target_dir)
		
		
	def draw (self):
		glPushMatrix()
		x = self.map.llx + (self.pos[0]*self.map.cellsize)
		y = self.map.lly + (self.pos[1]*self.map.cellsize)
		glTranslatef (x, y, 0)
		glRotatef (self.dir, 0, 0, 1)
		small_red_bug_tex.blit (0, 0)
		glPopMatrix()
		
	def set_target_dir (self):
		if int(self.next_position[0]) > int(self.pos[0]):
			# right
			if int(self.next_position[1]) > int(self.pos[1]):
				# up right
				self.target_dir = 315
			elif int(self.next_position[1]) == int(self.pos[1]):
				# right
				self.target_dir = 270
			else:
				#down right
				self.target_dir = 225
		elif int(self.next_position[0]) < int(self.pos[0]):
			# left
			if int(self.next_position[1]) > int(self.pos[1]):
				# up left
				self.target_dir = 45
			elif int(self.next_position[1]) == int(self.pos[1]):
				# left
				self.target_dir = 90
			else:
				#down left
				self.target_dir = 135
		else:
			# straight up or down
			if int(self.next_position[1]) > int(self.pos[1]):
				# up
				self.target_dir = 0
			else:
				#down
				self.target_dir = 180
			
	
	def get_current_grid_pos (self):
		return [ int(self.pos[0]), int(self.pos[1]) ]
		
	def get_path_distance_left (self):
		if self.pos[0]<0 or self.pos[1]>game.map.height-2:	# maybe should be just -1?
			return 99
		#gridpos = self.get_current_grid_pos ()
		return self.route.route[ (int(self.pos[0]), int(self.pos[1]) ) ].distance

	def update (self, tick):
		if self.health<0:
			# I`m dead
			audio_explode.play()
			# do other cleanup jobs and spawn whatever necessary particles
			game.particles.append (particle_explosion(copy.copy(self.pos), int(0.4/tick)))
			self.alive = False
			game.score += self.credits*3
			game.credits += self.credits
			credits_label.text = "Credits: " + str(game.credits)
			score_label.text = "Score: " +str(game.score)
			game.enemies.remove (self)
			return 0
				
		# check still on path
		# make locals for speed
		sp0 = self.pos[0]
		sp1 = self.pos[1]
		np0 = self.next_position[0]
		np1 = self.next_position[1]
		if abs(sp0-np0) < 0.1 and abs(sp1-np1) < 0.1:
			# get next path position
			if self.route.route[(int(sp0),int(sp1))].next:
				self.previous_position = copy.copy(self.next_position)
				self.next_position = copy.copy(self.route.route[(int(sp0),int(sp1))].next.pos)
				self.next_position = (self.next_position[0]+0.5, self.next_position[1]+0.5)
				
				if abs(sp0-self.next_position[0]) > 0.6 and abs(sp1-self.next_position[1]) > 0.6:
					self.diag = True
				else:
					self.diag = False
				self.set_target_dir()	# set new target direction according to new next position
				
			else:
				# might be end of path - check
				if self.route.route[(int(sp0),int(sp1))].pos == self.route.end:
					# end of path!
					# job done - update all
					self.alive = False
					game.enemies.remove (self)
					game.lives -= 1
					lives_label.text = "Lives: " +str(game.lives)
					# check if game over now...
					if game.lives<1:
						set_overlay (GameOver())
						game.state=game.states['menu']
				else:
					#else not end of path, go back to where we were :)
					self.next_position = self.previous_position
		
		# rotate if necessary to face direction of travel
		if self.dir <> self.target_dir:
			if self.dir < self.target_dir:
				self.dir += 9	# must be a divisor of 45 for rotations to work properly ie. 3, 5, 9, 15, 45
			else:
				self.dir -= 9	# must be a divisor of 45 for rotations to work properly
		
		# reaffirm local next position for speed (it may have changed above)
		np0 = self.next_position[0]
		np1 = self.next_position[1]
		
		if self.diag:
			speed = self.speed * 0.7
			if sp0 > np0 +0.1:
				self.pos[0] -= tick * speed
			elif sp0 < np0-0.1:
				self.pos[0] += tick * speed
			if sp1 > np1 + 0.1:
				self.pos[1] -= tick *speed
			elif sp1 < np1 -0.1:
				self.pos[1] += tick *speed
		else:
			if sp0 > np0+0.1:
				self.pos[0] -= tick * self.speed
			elif sp0 < np0-0.1:
				self.pos[0] += tick * self.speed
			if sp1 > np1+0.1:
				self.pos[1] -= tick * self.speed
			elif sp1 < np1-0.1:
				self.pos[1] += tick * self.speed	
				
				
				

class fastEnemy(object):
	""" normal enemy class.  takes:  route, health, credits """
	def __init__ (self, route=None, health = 10, credits = 5):
		self.map = game.map
		self.pos=[0,0]
		self.pos[0]=route.start[0]+0.5
		self.pos[1]=route.start[1]+0.5
		
		self.route = route
		self.diag = False
		self.health = health
		self.credits = credits
		self.alive = True
		self.dir = None
		self.target_dir = None
		self.speed = 2.8
		
		self.next_position = copy.copy(self.route.route[(int(self.pos[0]),int(self.pos[1]))].next.pos)
		self.next_position = (self.next_position[0]+0.5,self.next_position[1]+0.5)
		self.previous_position = self.next_position
		
		# offset start and randomize a bit
		if route.start[0]==0:
			self.pos[0]-=4
			yrand=-2+(int(random.random()*4))
			self.pos[1]+=yrand
			self.next_position = (self.next_position[0]-1, self.pos[1])
		if route.start[1]==game.map.height-1:
			self.pos[1]+=4
			xrand=-2+(int(random.random()*4))
			self.pos[0]+=xrand
			self.next_position = (self.pos[0], self.next_position[1]+1)
		
		if abs(self.pos[0]-self.next_position[0]) > 0.6 and abs(self.pos[1]-self.next_position[1]) > 0.6:
			self.diag = True
		else:
			self.diag = False
		# make sure initial direction is facing intital target path
		self.set_target_dir()
		self.dir = copy.copy (self.target_dir)
		
		
	def draw (self):
		glPushMatrix()
		x = self.map.llx + (self.pos[0]*self.map.cellsize)
		y = self.map.lly + (self.pos[1]*self.map.cellsize)
		glTranslatef (x, y, 0)
		glRotatef (self.dir, 0, 0, 1)
		fast_tex.blit (0, 0)
		glPopMatrix()
		
	def set_target_dir (self):
		if int(self.next_position[0]) > int(self.pos[0]):
			# right
			if int(self.next_position[1]) > int(self.pos[1]):
				# up right
				self.target_dir = 315
			elif int(self.next_position[1]) == int(self.pos[1]):
				# right
				self.target_dir = 270
			else:
				#down right
				self.target_dir = 225
		elif int(self.next_position[0]) < int(self.pos[0]):
			# left
			if int(self.next_position[1]) > int(self.pos[1]):
				# up left
				self.target_dir = 45
			elif int(self.next_position[1]) == int(self.pos[1]):
				# left
				self.target_dir = 90
			else:
				#down left
				self.target_dir = 135
		else:
			# straight up or down
			if int(self.next_position[1]) > int(self.pos[1]):
				# up
				self.target_dir = 0
			else:
				#down
				self.target_dir = 180
			
	
	def get_current_grid_pos (self):
		return [ int(self.pos[0]), int(self.pos[1]) ]
		
	def get_path_distance_left (self):
		if self.pos[0]<0 or self.pos[1]>game.map.height-2:	# maybe should be just -1?
			return 99
		#gridpos = self.get_current_grid_pos ()
		return self.route.route[ (int(self.pos[0]), int(self.pos[1]) ) ].distance

	def update (self, tick):
		if self.health<0:
			# I`m dead
			audio_explode.play()
			# do other cleanup jobs and spawn whatever necessary particles
			game.particles.append (particle_explosion(copy.copy(self.pos), int(0.4/tick)))
			self.alive = False
			game.score += self.credits*3
			game.credits += self.credits
			credits_label.text = "Credits: " + str(game.credits)
			score_label.text = "Score: " +str(game.score)
			game.enemies.remove (self)
			return 0
				
		# check still on path
		# make locals for speed
		sp0 = self.pos[0]
		sp1 = self.pos[1]
		np0 = self.next_position[0]
		np1 = self.next_position[1]
		if abs(sp0-np0) < 0.1 and abs(sp1-np1) < 0.1 and sp1<game.map.height:	# added 3rd clause because sometimes dict check 2 lines below messed up
			# get next path position
			if self.route.route[(int(sp0),int(sp1))].next:
				self.previous_position = copy.copy(self.next_position)
				self.next_position = copy.copy(self.route.route[(int(sp0),int(sp1))].next.pos)
				self.next_position = (self.next_position[0]+0.5, self.next_position[1]+0.5)
				
				if abs(sp0-self.next_position[0]) > 0.6 and abs(sp1-self.next_position[1]) > 0.6:
					self.diag = True
				else:
					self.diag = False
				self.set_target_dir()	# set new target direction according to new next position
				
			else:
				# might be end of path - check
				if self.route.route[(int(sp0),int(sp1))].pos == self.route.end:
					# end of path!
					# job done - update all
					self.alive = False
					game.enemies.remove (self)
					game.lives -= 1
					lives_label.text = "Lives: " +str(game.lives)
					# check if game over now...
					if game.lives<1:
						set_overlay (GameOver())
						game.state=game.states['menu']
				else:
					#else not end of path, go back to where we were :)
					self.next_position = self.previous_position
		
		# rotate if necessary to face direction of travel
		if self.dir <> self.target_dir:
			if self.dir < self.target_dir:
				self.dir += 9	# must be a divisor of 45 for rotations to work properly ie. 3, 5, 9, 15, 45
			else:
				self.dir -= 9	# must be a divisor of 45 for rotations to work properly
		
		# reaffirm local next position for speed (it may have changed above)
		np0 = self.next_position[0]
		np1 = self.next_position[1]
		
		if self.diag:
			speed = self.speed * 0.7
			if sp0 > np0 +0.1:
				self.pos[0] -= tick * speed
			elif sp0 < np0-0.1:
				self.pos[0] += tick * speed
			if sp1 > np1 + 0.1:
				self.pos[1] -= tick *speed
			elif sp1 < np1 -0.1:
				self.pos[1] += tick *speed
		else:
			if sp0 > np0+0.1:
				self.pos[0] -= tick * self.speed
			elif sp0 < np0-0.1:
				self.pos[0] += tick * self.speed
			if sp1 > np1+0.1:
				self.pos[1] -= tick * self.speed
			elif sp1 < np1-0.1:
				self.pos[1] += tick * self.speed	
				
				
				
				
				
				
				
				
				
				
				
				
				
				
		
class Bullet_1(object):
	def __init__ (self, pos, target, damage):
		self.pos=pos
		self.target=target
		self.damage=damage
		self.speed = 8
		dx = target.pos[0]-pos[0]
		dy = target.pos[1]-pos[1]
		length = math.sqrt (dx**2 + dy**2)
		if dx==0:
			self.direction=[0,self.speed*dy]
		elif dy==0:
			self.direction=[self.speed*dx,0]
		else:
			self.direction = [ self.speed*(dx/length), self.speed*(dy/length) ]
		
	def draw (self):
		bullet_1_sprite.blit (game.map.llx + (game.map.cellsize * self.pos[0]) , game.map.lly + (game.map.cellsize * self.pos[1]) )
		
	def update (self, tick):
		if self.target.alive:
			dx = self.target.pos[0]-self.pos[0]
			dy = self.target.pos[1]-self.pos[1]
			if abs(dx) < 0.5 and abs(dy) < 0.5:
				# HIT TARGET
				audio_hit.play()
				# Spawn hit particles
				# get screen coords
				sx = game.map.llx + (game.map.cellsize * self.pos[0])
				sy = game.map.lly + (game.map.cellsize * self.pos[1])
				
				# create some particles - TODO: check fps is high enough
				#game.particles.append (particle_small_hit ([sx,sy]))
				#game.particles.append (particle_small_hit ([sx,sy]))
				#game.particles.append (particle_small_hit ([sx,sy]))
				
				self.target.health -= self.damage
				game.projectiles.remove (self)
			else:
				speed = self.speed * tick
				if dx==0:
					self.direction=[0,speed*dy]
				elif dy==0:
					self.direction=[speed*dx,0]
				else:
					length = math.sqrt (dx**2 + dy**2)
					self.direction = [ speed*(dx/length), speed*(dy/length) ]
					self.pos[0] += self.direction[0]
					self.pos[1] += self.direction[1]
		else:
			# target gone - just remove projectile once out of range / off map
			if self.pos[0]<0 or self.pos[0]>game.map.width or self.pos[1]<0 or self.pos[1]>game.map.height:
				game.projectiles.remove (self)
				return 1
			self.pos[0] += self.direction[0]
			self.pos[1] += self.direction[1]
			

class Bullet_2(object):
	def __init__ (self, pos, target, damage):
		self.pos=pos
		self.target=target
		self.damage=damage
		self.speed = 10
		self.dir=0
		dx = target.pos[0]-pos[0]
		dy = target.pos[1]-pos[1]
		length = math.sqrt (dx**2 + dy**2)
		if dx==0:
			self.direction=[0,self.speed*dy]
		elif dy==0:
			self.direction=[self.speed*dx,0]
		else:
			self.direction = [ self.speed*(dx/length), self.speed*(dy/length) ]
		
	def draw (self):
		glPushMatrix()
		glTranslatef (game.map.llx + (game.map.cellsize * self.pos[0]),  game.map.lly + (game.map.cellsize * self.pos[1]), 0)
		glRotatef (self.dir, 0, 0, 1)
		#bullet_2_sprite.blit (game.map.llx + (game.map.cellsize * self.pos[0]) , game.map.lly + (game.map.cellsize * self.pos[1]) )
		bullet_2_sprite.blit (0,0)
		glPopMatrix()
		
		
	def update (self, tick):
		self.dir+=700*tick

		if self.target.alive:
			dx = self.target.pos[0]-self.pos[0]
			dy = self.target.pos[1]-self.pos[1]
			if abs(dx) < 0.5 and abs(dy) < 0.5:
				# HIT TARGET
				self.target.health -= self.damage
				audio_hit.play()
				
				if self.target.health>0:
					# Spawn hit particles
					# set up locals
					g=game.particles.append
					# get screen coords
					sx = game.map.llx + (game.map.cellsize * self.pos[0])
					sy = game.map.lly + (game.map.cellsize * self.pos[1])
					g (particle_small_hit ([sx,sy]))
					g (particle_small_hit ([sx,sy]))
					g (particle_small_hit ([sx,sy]))
					g (particle_small_hit ([sx,sy]))
					g (particle_small_hit ([sx,sy]))
					g (particle_small_hit ([sx,sy]))

				game.projectiles.remove (self)
			else:
				speed = self.speed * tick
				if dx==0:
					self.direction=[0,speed*dy]
				elif dy==0:
					self.direction=[speed*dx,0]
				else:
					length = math.sqrt (dx**2 + dy**2)
					self.direction = [ speed*(dx/length), speed*(dy/length) ]
					self.pos[0] += self.direction[0]
					self.pos[1] += self.direction[1]
		else:
			# target gone - just remove projectile once out of range / off map
			if self.pos[0]<0 or self.pos[0]>game.map.width or self.pos[1]<0 or self.pos[1]>game.map.height:
				game.projectiles.remove (self)
				return 1
			self.pos[0] += self.direction[0]
			self.pos[1] += self.direction[1]
			
			
			
class Bullet_3(object):
	def __init__ (self, pos, target, damage):
		self.pos=pos
		self.target=target
		self.damage=damage
		self.speed = 8
		self.dir=0
		dx = target.pos[0]-pos[0]
		dy = target.pos[1]-pos[1]
		length = math.sqrt (dx**2 + dy**2)
		if dx==0:
			self.direction=[0,self.speed*dy]
		elif dy==0:
			self.direction=[self.speed*dx,0]
		else:
			self.direction = [ self.speed*(dx/length), self.speed*(dy/length) ]
		
	def draw (self):
		glPushMatrix()
		glTranslatef (game.map.llx + (game.map.cellsize * self.pos[0]),  game.map.lly + (game.map.cellsize * self.pos[1]), 0)
		glRotatef (self.dir, 0, 0, 1)
		#bullet_2_sprite.blit (game.map.llx + (game.map.cellsize * self.pos[0]) , game.map.lly + (game.map.cellsize * self.pos[1]) )
		bullet_3_sprite.blit (0,0)
		glPopMatrix()
		
		
	def update (self, tick):
		self.dir+=1200*tick
		
		# do glowing blue trail
		game.particles.append (particle_blue_trail (self.pos))
			
		if self.target.alive:
			dx = self.target.pos[0]-self.pos[0]
			dy = self.target.pos[1]-self.pos[1]
			if abs(dx) < 0.5 and abs(dy) < 0.5:
				# HIT TARGET
				audio_hit.play()
				
				self.target.health -= self.damage
				game.projectiles.remove (self)
			else:
				speed = self.speed * tick
				if dx==0:
					self.direction=[0,speed*dy]
				elif dy==0:
					self.direction=[speed*dx,0]
				else:
					length = math.sqrt (dx**2 + dy**2)
					self.direction = [ speed*(dx/length), speed*(dy/length) ]
					self.pos[0] += self.direction[0]
					self.pos[1] += self.direction[1]
		else:
			# target gone - just remove projectile once out of range / off map
			if self.pos[0]<0 or self.pos[0]>game.map.width or self.pos[1]<0 or self.pos[1]>game.map.height:
				game.projectiles.remove (self)
				return 1
			self.pos[0] += self.direction[0]
			self.pos[1] += self.direction[1]
			
			

class Rail_1(object):
	def __init__ (self, pos, target, damage):
		# dir set at init phase - determined by angle to target
		self.pos=pos
		self.target=target
		self.damage=damage
		self.speed = 24
		self.dir=0
		dx = target.pos[0]-pos[0]
		dy = target.pos[1]-pos[1]
		self.dir = math.atan2 (dy, dx) * 57.2957795 + 90
		length = math.sqrt (dx**2 + dy**2)
		if dx==0:
			self.direction=[0,self.speed*dy]
		elif dy==0:
			self.direction=[self.speed*dx,0]
		else:
			self.direction = [ self.speed*(dx/length), self.speed*(dy/length) ]
		
	def draw (self):
		glPushMatrix()
		glTranslatef (game.map.llx + (game.map.cellsize * self.pos[0]),  game.map.lly + (game.map.cellsize * self.pos[1]), 0)
		glRotatef (self.dir, 0, 0, 1)
		rail_1_sprite.blit (0,0)
		glPopMatrix()
		
		
	def update (self, tick):
		
		# add particle fx here
		#game.particles.append (particle_small_hit( [ game.map.llx + (game.map.cellsize * self.pos[0]), game.map.lly + (game.map.cellsize * self.pos[1])]     ))
			
		if self.target.alive:
			dx = self.target.pos[0]-self.pos[0]
			dy = self.target.pos[1]-self.pos[1]
			if abs(dx) < 0.5 and abs(dy) < 0.5:
				# HIT TARGET
				audio_hit.play()
				# Spawn hit particles - removed for now - the rail hits a lot of times per sec, so leave them out
				# get screen coords
				#sx = game.map.llx + (game.map.cellsize * self.pos[0])
				#sy = game.map.lly + (game.map.cellsize * self.pos[1])
				#for x in xrange(6):
				#	game.particles.append (particle_small_hit ([sx,sy]))
				self.target.health -= self.damage
				game.projectiles.remove (self)
			else:
				speed = self.speed * tick
				if dx==0:
					self.direction=[0,speed*dy]
				elif dy==0:
					self.direction=[speed*dx,0]
				else:
					length = math.sqrt (dx**2 + dy**2)
					self.direction = [ speed*(dx/length), speed*(dy/length) ]
					self.pos[0] += self.direction[0]
					self.pos[1] += self.direction[1]
		else:
			# target gone - just remove projectile once out of range / off map
			if self.pos[0]<0 or self.pos[0]>game.map.width or self.pos[1]<0 or self.pos[1]>game.map.height:
				game.projectiles.remove (self)
				return 1
			self.pos[0] += self.direction[0]
			self.pos[1] += self.direction[1]
			
			
			
class Rail_2(object):
	def __init__ (self, pos, target, damage):
		# dir set at init phase - determined by angle to target
		self.pos=pos
		self.target=target
		self.damage=damage
		self.speed = 24
		self.dir=0
		dx = target.pos[0]-pos[0]
		dy = target.pos[1]-pos[1]
		self.dir = math.atan2 (dy, dx) * 57.2957795 + 90
		length = math.sqrt (dx**2 + dy**2)
		if dx==0:
			self.direction=[0,self.speed*dy]
		elif dy==0:
			self.direction=[self.speed*dx,0]
		else:
			self.direction = [ self.speed*(dx/length), self.speed*(dy/length) ]
		
	def draw (self):
		glPushMatrix()
		glTranslatef (game.map.llx + (game.map.cellsize * self.pos[0]),  game.map.lly + (game.map.cellsize * self.pos[1]), 0)
		glRotatef (self.dir, 0, 0, 1)
		rail_2_sprite.blit (0,0)
		glPopMatrix()
		
		
	def update (self, tick):
		
		# add particle fx here
		#game.particles.append (particle_small_hit( [ game.map.llx + (game.map.cellsize * self.pos[0]), game.map.lly + (game.map.cellsize * self.pos[1])]     ))
			
		if self.target.alive:
			dx = self.target.pos[0]-self.pos[0]
			dy = self.target.pos[1]-self.pos[1]
			if abs(dx) < 0.5 and abs(dy) < 0.5:
				# HIT TARGET
				audio_hit.play()
				# Spawn hit particles - removed for now - the rail hits a lot of times per sec, so leave them out
				# get screen coords
				#sx = game.map.llx + (game.map.cellsize * self.pos[0])
				#sy = game.map.lly + (game.map.cellsize * self.pos[1])
				#for x in xrange(6):
				#	game.particles.append (particle_small_hit ([sx,sy]))
				self.target.health -= self.damage
				game.projectiles.remove (self)
			else:
				speed = self.speed * tick
				if dx==0:
					self.direction=[0,speed*dy]
				elif dy==0:
					self.direction=[speed*dx,0]
				else:
					length = math.sqrt (dx**2 + dy**2)
					self.direction = [ speed*(dx/length), speed*(dy/length) ]
					self.pos[0] += self.direction[0]
					self.pos[1] += self.direction[1]
		else:
			# target gone - just remove projectile once out of range / off map
			if self.pos[0]<0 or self.pos[0]>game.map.width or self.pos[1]<0 or self.pos[1]>game.map.height:
				game.projectiles.remove (self)
				return 1
			self.pos[0] += self.direction[0]
			self.pos[1] += self.direction[1]
			



class Rail_3(object):
	def __init__ (self, pos, target, damage):
		# dir set at init phase - determined by angle to target
		self.pos=pos
		self.target=target
		self.damage=damage
		self.speed = 24
		self.dir=0
		dx = target.pos[0]-pos[0]
		dy = target.pos[1]-pos[1]
		self.dir = math.atan2 (dy, dx) * 57.2957795 + 90
		length = math.sqrt (dx**2 + dy**2)
		if dx==0:
			self.direction=[0,self.speed*dy]
		elif dy==0:
			self.direction=[self.speed*dx,0]
		else:
			self.direction = [ self.speed*(dx/length), self.speed*(dy/length) ]
		
	def draw (self):
		glPushMatrix()
		glTranslatef (game.map.llx + (game.map.cellsize * self.pos[0]),  game.map.lly + (game.map.cellsize * self.pos[1]), 0)
		glRotatef (self.dir, 0, 0, 1)
		rail_3_sprite.blit (0,0)
		glPopMatrix()
		
		
		
		
	def update (self, tick):
		
		# add particle fx here
		# do white trail
		game.particles.append (particle_white_trail (self.pos))
		
		if self.target.alive:
			dx = self.target.pos[0]-self.pos[0]
			dy = self.target.pos[1]-self.pos[1]
			if abs(dx) < 0.5 and abs(dy) < 0.5:
				# HIT TARGET
				audio_hit.play()
				# Spawn hit particles - removed for now - the rail hits a lot of times per sec, so leave them out
				# get screen coords
				#sx = game.map.llx + (game.map.cellsize * self.pos[0])
				#sy = game.map.lly + (game.map.cellsize * self.pos[1])
				#for x in xrange(6):
				#	game.particles.append (particle_small_hit ([sx,sy]))
				self.target.health -= self.damage
				game.projectiles.remove (self)
			else:
				speed = self.speed * tick
				if dx==0:
					self.direction=[0,speed*dy]
				elif dy==0:
					self.direction=[speed*dx,0]
				else:
					length = math.sqrt (dx**2 + dy**2)
					self.direction = [ speed*(dx/length), speed*(dy/length) ]
					self.pos[0] += self.direction[0]
					self.pos[1] += self.direction[1]
		else:
			# target gone - just remove projectile once out of range / off map
			if self.pos[0]<0 or self.pos[0]>game.map.width or self.pos[1]<0 or self.pos[1]>game.map.height:
				game.projectiles.remove (self)
				return 1
			self.pos[0] += self.direction[0]
			self.pos[1] += self.direction[1]


			


		
			
			
			
			


class Berserker_1 (object):
	def __init__ (self, position=(0,0)):
		self.label = "BERSERKER - LVL 1"
		self.highlight = False
		self.pos = position
		self.center = (position[0]+1, position[1]+1)
		# screen coords
		self.llx = 0
		self.lly = 0
		self.urx = 0
		self.ury = 0
		self.cx = 0
		self.cy = 0
		
		self.active = False
		self.target = None
		self.cost = 15
		self.range_sq = 5
		self.range = self.range_sq * self.range_sq
		
		self.spin_accel = 0.1
		self.max_spin_speed = 5
		self.spin_speed = 0
		self.dir = 0
		
		self.upgrade_cost = 65
		self.upgrade_time = 3
		self.damage_per_shot = 3
		self.sell_price = 3
		self.time_between_shots = 0.45
		self.time_since_last_shot = 3
		self.target_mode = 0	# 0 - none, 1 strong 2 weak 3 fast 4 slow 5 near 6 end of path
		self.upgradeable = True
		self.info_headings = "Range:\nDamage:\nRate:\n\nUpgrade for:\nSell for:"
		self.info = str(self.range_sq) + "\n" + str(self.damage_per_shot) + "\n" + str(self.time_between_shots) + "\n\n" + str(self.upgrade_cost) + "\n" + str(self.sell_price)
		
		self.mouse_over = False
	
	def deploy (self):
		# make map squares impassable
		game.map.cell[mymouse.dx][mymouse.dy].passable=False
		game.map.cell[mymouse.dx+1][mymouse.dy].passable=False
		game.map.cell[mymouse.dx+1][mymouse.dy+1].passable=False
		game.map.cell[mymouse.dx][mymouse.dy+1].passable=False
		# put pointer to tower in map cells
		game.map.cell[mymouse.dx][mymouse.dy].tower=self
		game.map.cell[mymouse.dx+1][mymouse.dy].tower=self
		game.map.cell[mymouse.dx+1][mymouse.dy+1].tower=self
		game.map.cell[mymouse.dx][mymouse.dy+1].tower=self
		self.pos = (mymouse.dx, mymouse.dy)
		self.center = (self.pos[0]+1, self.pos[1]+1)
		# get screen coord area
		self.llx = game.map.llx + self.pos[0] * game.map.cellsize
		self.lly = game.map.lly + self.pos[1] * game.map.cellsize
		self.urx = game.map.llx + (self.pos[0]+2) * game.map.cellsize
		self.ury = game.map.lly + (self.pos[1]+2) * game.map.cellsize
		self.cx = game.map.llx + self.center[0] * game.map.cellsize
		self.cy = game.map.lly + self.center[1] * game.map.cellsize
		
		if game.map.recalc_routes():	# recalc routes
			game.towers.append ( self )
			window.push_handlers(self)
			return True
		else:
			# make routes passable again
			game.map.cell[mymouse.dx][mymouse.dy].passable=True
			game.map.cell[mymouse.dx+1][mymouse.dy].passable=True
			game.map.cell[mymouse.dx+1][mymouse.dy+1].passable=True
			game.map.cell[mymouse.dx][mymouse.dy+1].passable=True
			# remove pointers to tower in cells
			game.map.cell[mymouse.dx][mymouse.dy].tower=None
			game.map.cell[mymouse.dx+1][mymouse.dy].tower=None
			game.map.cell[mymouse.dx+1][mymouse.dy+1].tower=None
			game.map.cell[mymouse.dx][mymouse.dy+1].tower=None
			game.map.recalc_routes()	# recalc original routes
			return False	# tell calling function that deploy failed
		
	def deploy_fast (self):	# used when re-checking of paths is not needed - ie. for an upgrade
		# get screen coord area
		self.llx = game.map.llx + self.pos[0] * game.map.cellsize
		self.lly = game.map.lly + self.pos[1] * game.map.cellsize
		self.urx = game.map.llx + (self.pos[0]+2) * game.map.cellsize
		self.ury = game.map.lly + (self.pos[1]+2) * game.map.cellsize
		self.cx = game.map.llx + self.center[0] * game.map.cellsize
		self.cy = game.map.lly + self.center[1] * game.map.cellsize
		game.towers.append ( self )
		window.push_handlers(self)

	
	def sell (self):
		window.remove_handlers(self)
		self.mouse_over = False # BUGFIX: range still drawn when S key used to sell and mouse over spot where tower was
		game.towers.remove(self)
		game.selected = None
		if game.state & game.states['pregame']:
			# take no time
			game.towers.append ( aSell (self.pos[0],self.pos[1], 0.01) )
			# and free
			game.credits += self.cost
		else:
			game.towers.append ( aSell (self.pos[0],self.pos[1], game.map.sell_time) )
			game.credits += self.sell_price
			game.map.sell_time *= game.map.sell_time_multiplier

		
	def upgrade (self):
		print "DOING UPGRADE!"
		
		self.mouse_over = False
		pos=copy.copy(self.pos)
		upgrade_to = self.get_upgrade()
		if game.state & game.states['pregame']:
			self.upgrade_time = 0.01
		game.towers.append ( anUpgrade (pos[0], pos[1], self.upgrade_time, upgrade_to , copy.copy(self.target_mode) ))
		window.remove_handlers(self)
		game.towers.remove( self )
		game.selected=None

	
	def get_upgrade(self):
		return Berserker_2 (copy.copy(self.pos))
		
	def update (self,dt):
	
		self.dir += self.spin_speed 
	
		if self.spin_speed > 0 and self.target is None:
				self.spin_speed-=self.spin_accel
				if self.spin_speed < 0:
					self.spin_speed = 0
			
		self.time_since_last_shot+=dt
		if self.time_since_last_shot > self.time_between_shots:
			# find a new target
			nearby_enemies=[]
			# create locals for speed
			cx=self.center[0]
			cy=self.center[1]
			for enemy in game.enemies:
				# get squared distance
				sd = (cx-enemy.pos[0])**2 + (cy-enemy.pos[1])**2
				if sd < self.range:
					nearby_enemies.append (enemy)	
			if nearby_enemies:
				# this is berserker, so just pick random targets
				n = len(nearby_enemies)
				self.target = nearby_enemies[ int(random.random()* n) ]
			else:
				self.target = None
				self.target2 = None
				return 0
					
		if self.target and self.target.alive:
			# if target also still alive
			# check target is still in range
			sd = (self.center[0]-self.target.pos[0])**2 + (self.center[1]-self.target.pos[1])**2
			if sd < self.range:
				# have target, can we fire?
				# spin up in anticipation
				self.spin_speed+=self.spin_accel
				if self.spin_speed>self.max_spin_speed:
					self.spin_speed=self.max_spin_speed
				if self.time_since_last_shot > self.time_between_shots:
					# yes we can
					#print "BANG!"
					audio_rail_1_fire.play()
					game.projectiles.append (Rail_1 ( [self.pos[0]+1, self.pos[1]+1], self.target, self.damage_per_shot))
					
					self.time_since_last_shot=0
					self.time_between_shots = random.random() + 0.1
				
			else:
				# old target left range
				self.target2 = None
				self.target = None
			
		
			
		
		
		
	def draw (self, alpha=1):
		# base
		#cannon_1_base_sprite.blit (game.map.llx + (game.map.cellsize * self.pos[0]) , game.map.lly + (game.map.cellsize * self.pos[1]) )
		cannon_1_base_sprite.blit (self.llx, self.lly)
		# turret
		glPushMatrix()
		#glTranslatef (game.map.llx + (game.map.cellsize * self.center[0]),game.map.llx + (game.map.cellsize * self.center[1]),0)
		glTranslatef (self.cx, self.cy, 0)
		glRotatef (-self.dir, 0, 0, 1)
		berserker_1_turret_sprite.blit (0,0)
		glPopMatrix()
		
		
	def draw_highlight (self):
		width = self.range_sq * game.map.cellsize * 2
		offset = width * 0.5
		#range_sprite.blit ( -offset + game.map.llx + (game.map.cellsize * self.center[0]), -offset + game.map.lly + (game.map.cellsize * self.center[1]), width=width, height=width)
		range_sprite.blit ( -offset + self.cx, -offset + self.cy, width=width, height=width)
		
		# NO AI PANEL
		ai_frame.enabled=False

		
	def draw_selection (self):
		selected_tex.blit (self.llx, self.lly)
		
		
	def on_mouse_motion(self, x, y, dx, dy):
		if (x>self.llx and x<self.urx and y>self.lly and y<self.ury) and not game.state & game.states['paused']:
			self.mouse_over=True
			game.highlighted=self
		else:
			self.mouse_over=False
			
	def on_mouse_release(self, x, y, buttons, modifiers):
		if self.mouse_over and buttons & mouse.LEFT and not game.state & game.states['paused']:
			game.selected=self
			
			
		


class Berserker_2 (object):
	def __init__ (self, position=(0,0)):
		self.label = "BERSERKER - LVL 2 "
		self.highlight = False
		self.pos = position
		self.center = (position[0]+1, position[1]+1)
		# screen coords
		self.llx = 0
		self.lly = 0
		self.urx = 0
		self.ury = 0
		self.cx = 0
		self.cy = 0
		
		self.active = False
		self.target = None
		self.cost = 75
		self.range_sq = 6.5
		self.range = self.range_sq * self.range_sq
		
		self.spin_accel = 0.1
		self.max_spin_speed = 12
		self.spin_speed = 0
		self.dir = 0
		
		self.upgrade_cost = 165
		self.upgrade_time = 12
		self.damage_per_shot = 20
		self.sell_price = 60
		self.time_between_shots = 0.32
		self.time_since_last_shot = 3
		self.target_mode = 0	# 0 - none, 1 strong 2 weak 3 fast 4 slow 5 near 6 end of path
		self.upgradeable = True
		self.info_headings = "Range:\nDamage:\nRate:\n\nUpgrade for:\nSell for:"
		self.info = str(self.range_sq) + "\n" + str(self.damage_per_shot) + "\n" + str(self.time_between_shots) + "\n\n" + str(self.upgrade_cost) + "\n" + str(self.sell_price)
		
		self.mouse_over = False
	
	def deploy (self):
		# make map squares impassable
		game.map.cell[mymouse.dx][mymouse.dy].passable=False
		game.map.cell[mymouse.dx+1][mymouse.dy].passable=False
		game.map.cell[mymouse.dx+1][mymouse.dy+1].passable=False
		game.map.cell[mymouse.dx][mymouse.dy+1].passable=False
		# put pointer to tower in map cells
		game.map.cell[mymouse.dx][mymouse.dy].tower=self
		game.map.cell[mymouse.dx+1][mymouse.dy].tower=self
		game.map.cell[mymouse.dx+1][mymouse.dy+1].tower=self
		game.map.cell[mymouse.dx][mymouse.dy+1].tower=self
		self.pos = (mymouse.dx, mymouse.dy)
		self.center = (self.pos[0]+1, self.pos[1]+1)
		# get screen coord area
		self.llx = game.map.llx + self.pos[0] * game.map.cellsize
		self.lly = game.map.lly + self.pos[1] * game.map.cellsize
		self.urx = game.map.llx + (self.pos[0]+2) * game.map.cellsize
		self.ury = game.map.lly + (self.pos[1]+2) * game.map.cellsize
		self.cx = game.map.llx + self.center[0] * game.map.cellsize
		self.cy = game.map.lly + self.center[1] * game.map.cellsize
		
		if game.map.recalc_routes():	# recalc routes
			game.towers.append ( self )
			window.push_handlers(self)
			return True
		else:
			# make routes passable again
			game.map.cell[mymouse.dx][mymouse.dy].passable=True
			game.map.cell[mymouse.dx+1][mymouse.dy].passable=True
			game.map.cell[mymouse.dx+1][mymouse.dy+1].passable=True
			game.map.cell[mymouse.dx][mymouse.dy+1].passable=True
			# remove pointers to tower in cells
			game.map.cell[mymouse.dx][mymouse.dy].tower=None
			game.map.cell[mymouse.dx+1][mymouse.dy].tower=None
			game.map.cell[mymouse.dx+1][mymouse.dy+1].tower=None
			game.map.cell[mymouse.dx][mymouse.dy+1].tower=None
			game.map.recalc_routes()	# recalc original routes
			return False	# tell calling function that deploy failed
		
	def deploy_fast (self):	# used when re-checking of paths is not needed - ie. for an upgrade
		# get screen coord area
		self.llx = game.map.llx + self.pos[0] * game.map.cellsize
		self.lly = game.map.lly + self.pos[1] * game.map.cellsize
		self.urx = game.map.llx + (self.pos[0]+2) * game.map.cellsize
		self.ury = game.map.lly + (self.pos[1]+2) * game.map.cellsize
		self.cx = game.map.llx + self.center[0] * game.map.cellsize
		self.cy = game.map.lly + self.center[1] * game.map.cellsize
		game.towers.append ( self )
		window.push_handlers(self)

	
	def sell (self):
		window.remove_handlers(self)
		self.mouse_over = False # BUGFIX: range still drawn when S key used to sell and mouse over spot where tower was
		game.towers.remove(self)
		game.selected = None
		if game.state & game.states['pregame']:
			# take no time
			game.towers.append ( aSell (self.pos[0],self.pos[1], 0.01) )
			# and free
			game.credits += self.cost
		else:
			game.towers.append ( aSell (self.pos[0],self.pos[1], game.map.sell_time) )
			game.credits += self.sell_price
			game.map.sell_time *= game.map.sell_time_multiplier

		
	def upgrade (self):
		print "DOING UPGRADE!"
		
		self.mouse_over = False
		pos=copy.copy(self.pos)
		upgrade_to = self.get_upgrade()
		if game.state & game.states['pregame']:
			self.upgrade_time = 0.01
		game.towers.append ( anUpgrade (pos[0], pos[1], self.upgrade_time, upgrade_to , copy.copy(self.target_mode) ))
		window.remove_handlers(self)
		game.towers.remove( self )
		game.selected=None

	
	def get_upgrade(self):
		return Berserker_3 (copy.copy(self.pos))
		
	def update (self,dt):
	
		self.dir += self.spin_speed 
	
		if self.spin_speed > 0 and self.target is None:
				self.spin_speed*=0.99
				if self.spin_speed < 0:
					self.spin_speed = 0
			
		self.time_since_last_shot+=dt
		if self.time_since_last_shot > self.time_between_shots:
			# find a new target
			nearby_enemies=[]
			# create locals for speed
			cx=self.center[0]
			cy=self.center[1]
			for enemy in game.enemies:
				# get squared distance
				sd = (cx-enemy.pos[0])**2 + (cy-enemy.pos[1])**2
				if sd < self.range:
					nearby_enemies.append (enemy)	
			if nearby_enemies:
				# this is berserker, so just pick random targets
				n = len(nearby_enemies)
				self.target = nearby_enemies[ int(random.random()* n) ]
			else:
				self.target = None
				return 0
					
		if self.target and self.target.alive:
			# if target also still alive
			# check target is still in range
			sd = (self.center[0]-self.target.pos[0])**2 + (self.center[1]-self.target.pos[1])**2
			if sd < self.range:
				# have target, can we fire?
				# spin up in anticipation
				self.spin_speed+=self.spin_accel
				if self.spin_speed>self.max_spin_speed:
					self.spin_speed=self.max_spin_speed
				if self.time_since_last_shot > self.time_between_shots:
					# yes we can
					#print "BANG!"
					audio_rail_1_fire.play()
					game.projectiles.append (Rail_2 ( [self.pos[0]+1, self.pos[1]+1], self.target, self.damage_per_shot))
					
					self.time_since_last_shot=0
				
			else:
				# old target left range
				self.target = None
			
		
			
		
		
		
	def draw (self, alpha=1):
		# base
		#cannon_1_base_sprite.blit (game.map.llx + (game.map.cellsize * self.pos[0]) , game.map.lly + (game.map.cellsize * self.pos[1]) )
		cannon_2_base_sprite.blit (self.llx, self.lly)
		# turret
		glPushMatrix()
		#glTranslatef (game.map.llx + (game.map.cellsize * self.center[0]),game.map.llx + (game.map.cellsize * self.center[1]),0)
		glTranslatef (self.cx, self.cy, 0)
		glRotatef (-self.dir, 0, 0, 1)
		berserker_1_turret_sprite.blit (0,0)
		glPopMatrix()
		
		
	def draw_highlight (self):
		width = self.range_sq * game.map.cellsize * 2
		offset = width * 0.5
		#range_sprite.blit ( -offset + game.map.llx + (game.map.cellsize * self.center[0]), -offset + game.map.lly + (game.map.cellsize * self.center[1]), width=width, height=width)
		range_sprite.blit ( -offset + self.cx, -offset + self.cy, width=width, height=width)
		
		# NO AI PANEL
		ai_frame.enabled=False

		
	def draw_selection (self):
		selected_tex.blit (self.llx, self.lly)
		
		
	def on_mouse_motion(self, x, y, dx, dy):
		if (x>self.llx and x<self.urx and y>self.lly and y<self.ury) and not game.state & game.states['paused']:
			self.mouse_over=True
			game.highlighted=self
		else:
			self.mouse_over=False
			
	def on_mouse_release(self, x, y, buttons, modifiers):
		if self.mouse_over and buttons & mouse.LEFT and not game.state & game.states['paused']:
			game.selected=self




			
			
class Berserker_3 (object):
	def __init__ (self, position=(0,0)):
		self.label = "BERSERKER - LVL 2 "
		self.highlight = False
		self.pos = position
		self.center = (position[0]+1, position[1]+1)
		# screen coords
		self.llx = 0
		self.lly = 0
		self.urx = 0
		self.ury = 0
		self.cx = 0
		self.cy = 0
		
		self.active = False
		self.target = None
		self.cost = 135
		self.range_sq = 7
		self.range = self.range_sq * self.range_sq
		
		self.spin_accel = 0.1
		self.max_spin_speed = 18
		self.spin_speed = 0
		self.dir = 0
		
		self.upgrade_cost = 135
		self.upgrade_time = 8
		self.damage_per_shot = 55
		self.sell_price = 110
		self.time_between_shots = 0.22
		self.time_since_last_shot = 3
		self.target_mode = 0	# 0 - none, 1 strong 2 weak 3 fast 4 slow 5 near 6 end of path
		self.upgradeable = False
		self.info_headings = "Range:\nDamage:\nRate:\n\nUpgrade for:\nSell for:"
		self.info = str(self.range_sq) + "\n" + str(self.damage_per_shot) + "\n" + str(self.time_between_shots) + "\n\n" + str(self.upgrade_cost) + "\n" + str(self.sell_price)
		
		self.mouse_over = False
	
	def deploy (self):
		# make map squares impassable
		game.map.cell[mymouse.dx][mymouse.dy].passable=False
		game.map.cell[mymouse.dx+1][mymouse.dy].passable=False
		game.map.cell[mymouse.dx+1][mymouse.dy+1].passable=False
		game.map.cell[mymouse.dx][mymouse.dy+1].passable=False
		# put pointer to tower in map cells
		game.map.cell[mymouse.dx][mymouse.dy].tower=self
		game.map.cell[mymouse.dx+1][mymouse.dy].tower=self
		game.map.cell[mymouse.dx+1][mymouse.dy+1].tower=self
		game.map.cell[mymouse.dx][mymouse.dy+1].tower=self
		self.pos = (mymouse.dx, mymouse.dy)
		self.center = (self.pos[0]+1, self.pos[1]+1)
		# get screen coord area
		self.llx = game.map.llx + self.pos[0] * game.map.cellsize
		self.lly = game.map.lly + self.pos[1] * game.map.cellsize
		self.urx = game.map.llx + (self.pos[0]+2) * game.map.cellsize
		self.ury = game.map.lly + (self.pos[1]+2) * game.map.cellsize
		self.cx = game.map.llx + self.center[0] * game.map.cellsize
		self.cy = game.map.lly + self.center[1] * game.map.cellsize
		
		if game.map.recalc_routes():	# recalc routes
			game.towers.append ( self )
			window.push_handlers(self)
			return True
		else:
			# make routes passable again
			game.map.cell[mymouse.dx][mymouse.dy].passable=True
			game.map.cell[mymouse.dx+1][mymouse.dy].passable=True
			game.map.cell[mymouse.dx+1][mymouse.dy+1].passable=True
			game.map.cell[mymouse.dx][mymouse.dy+1].passable=True
			# remove pointers to tower in cells
			game.map.cell[mymouse.dx][mymouse.dy].tower=None
			game.map.cell[mymouse.dx+1][mymouse.dy].tower=None
			game.map.cell[mymouse.dx+1][mymouse.dy+1].tower=None
			game.map.cell[mymouse.dx][mymouse.dy+1].tower=None
			game.map.recalc_routes()	# recalc original routes
			return False	# tell calling function that deploy failed
		
	def deploy_fast (self):	# used when re-checking of paths is not needed - ie. for an upgrade
		# get screen coord area
		self.llx = game.map.llx + self.pos[0] * game.map.cellsize
		self.lly = game.map.lly + self.pos[1] * game.map.cellsize
		self.urx = game.map.llx + (self.pos[0]+2) * game.map.cellsize
		self.ury = game.map.lly + (self.pos[1]+2) * game.map.cellsize
		self.cx = game.map.llx + self.center[0] * game.map.cellsize
		self.cy = game.map.lly + self.center[1] * game.map.cellsize
		game.towers.append ( self )
		window.push_handlers(self)

	
	def sell (self):
		window.remove_handlers(self)
		self.mouse_over = False # BUGFIX: range still drawn when S key used to sell and mouse over spot where tower was
		game.towers.remove(self)
		game.selected = None
		if game.state & game.states['pregame']:
			# take no time
			game.towers.append ( aSell (self.pos[0],self.pos[1], 0.01) )
			# and free
			game.credits += self.cost
		else:
			game.towers.append ( aSell (self.pos[0],self.pos[1], game.map.sell_time) )
			game.credits += self.sell_price
			game.map.sell_time *= game.map.sell_time_multiplier

		
	def upgrade (self):
		print "DOING UPGRADE!"
		
		self.mouse_over = False
		pos=copy.copy(self.pos)
		upgrade_to = self.get_upgrade()
		if game.state & game.states['pregame']:
			self.upgrade_time = 0.01
		game.towers.append ( anUpgrade (pos[0], pos[1], self.upgrade_time, upgrade_to , copy.copy(self.target_mode) ))
		window.remove_handlers(self)
		game.towers.remove( self )
		game.selected=None

	
	def get_upgrade(self):
		return Berserker_2 (copy.copy(self.pos))
		
	def update (self,dt):
	
		self.dir += self.spin_speed 
	
		if self.spin_speed > 0 and self.target is None:
				self.spin_speed*=0.99
				if self.spin_speed < 0:
					self.spin_speed = 0
			
		self.time_since_last_shot+=dt
		if self.time_since_last_shot > self.time_between_shots:
			# find a new target
			nearby_enemies=[]
			# create locals for speed
			cx=self.center[0]
			cy=self.center[1]
			for enemy in game.enemies:
				# get squared distance
				sd = (cx-enemy.pos[0])**2 + (cy-enemy.pos[1])**2
				if sd < self.range:
					nearby_enemies.append (enemy)	
			if nearby_enemies:
				# this is berserker, so just pick random targets
				n = len(nearby_enemies)
				self.target = nearby_enemies[ int(random.random()* n) ]
			else:
				self.target = None
				return 0
					
		if self.target and self.target.alive:
			# if target also still alive
			# check target is still in range
			sd = (self.center[0]-self.target.pos[0])**2 + (self.center[1]-self.target.pos[1])**2
			if sd < self.range:
				# have target, can we fire?
				# spin up in anticipation
				self.spin_speed+=self.spin_accel
				if self.spin_speed>self.max_spin_speed:
					self.spin_speed=self.max_spin_speed
				if self.time_since_last_shot > self.time_between_shots:
					# yes we can
					#print "BANG!"
					audio_rail_1_fire.play()
					game.projectiles.append (Rail_3 ( [self.pos[0]+1, self.pos[1]+1], self.target, self.damage_per_shot))
					
					self.time_since_last_shot=0
				
			else:
				# old target left range
				self.target = None
			
		
			
		
		
		
	def draw (self, alpha=1):
		# base
		#cannon_1_base_sprite.blit (game.map.llx + (game.map.cellsize * self.pos[0]) , game.map.lly + (game.map.cellsize * self.pos[1]) )
		cannon_3_base_sprite.blit (self.llx, self.lly)
		# turret
		glPushMatrix()
		#glTranslatef (game.map.llx + (game.map.cellsize * self.center[0]),game.map.llx + (game.map.cellsize * self.center[1]),0)
		glTranslatef (self.cx, self.cy, 0)
		glRotatef (-self.dir, 0, 0, 1)
		berserker_1_turret_sprite.blit (0,0)
		glPopMatrix()
		
		
	def draw_highlight (self):
		width = self.range_sq * game.map.cellsize * 2
		offset = width * 0.5
		#range_sprite.blit ( -offset + game.map.llx + (game.map.cellsize * self.center[0]), -offset + game.map.lly + (game.map.cellsize * self.center[1]), width=width, height=width)
		range_sprite.blit ( -offset + self.cx, -offset + self.cy, width=width, height=width)
		
		# NO AI PANEL
		ai_frame.enabled=False

		
	def draw_selection (self):
		selected_tex.blit (self.llx, self.lly)
		
		
	def on_mouse_motion(self, x, y, dx, dy):
		if (x>self.llx and x<self.urx and y>self.lly and y<self.ury) and not game.state & game.states['paused']:
			self.mouse_over=True
			game.highlighted=self
			ai_frame.enabled=False
		else:
			self.mouse_over=False
			
	def on_mouse_release(self, x, y, buttons, modifiers):
		if self.mouse_over and buttons & mouse.LEFT and not game.state & game.states['paused']:
			game.selected=self

			
			
			
			
			
			
			
			
class Tower (object):
	""" Tower Base Class """
	def __init__ (self, position=(0,0)):
		self.highlight=False
		
			
			

class Cannon_1 (object):
	def __init__ (self, position=(0,0)):
		self.label = "CANNON - LVL 1"
		self.highlight = False
		self.pos = position
		self.center = (position[0]+1, position[1]+1)
		# screen coords
		self.llx = 0
		self.lly = 0
		self.urx = 0
		self.ury = 0
		self.cx = 0
		self.cy = 0
		
		self.direction = 0
		self.active = False
		self.target = None
		self.cost = 5
		self.range_sq = 4
		self.range = self.range_sq * self.range_sq
		
		self.upgrade_cost = 40
		self.upgrade_time = 2
		self.damage_per_shot = 3
		self.sell_price = 3
		self.time_between_shots = 1.2
		self.time_since_last_shot = 3
		self.target_mode = 0	# 0 - none, 1 strong 2 weak 3 fast 4 slow 5 near 6 end of path
		self.upgradeable = True
		self.info_headings = "Range:\nDamage:\nRate:\n\nUpgrade for:\nSell for:"
		self.info = str(self.range_sq) + "\n" + str(self.damage_per_shot) + "\n" + str(self.time_between_shots) + "\n\n" + str(self.upgrade_cost) + "\n" + str(self.sell_price)
		
		self.mouse_over = False
	
	def deploy (self):
		# make map squares impassable
		game.map.cell[mymouse.dx][mymouse.dy].passable=False
		game.map.cell[mymouse.dx+1][mymouse.dy].passable=False
		game.map.cell[mymouse.dx+1][mymouse.dy+1].passable=False
		game.map.cell[mymouse.dx][mymouse.dy+1].passable=False
		# put pointer to tower in map cells
		game.map.cell[mymouse.dx][mymouse.dy].tower=self
		game.map.cell[mymouse.dx+1][mymouse.dy].tower=self
		game.map.cell[mymouse.dx+1][mymouse.dy+1].tower=self
		game.map.cell[mymouse.dx][mymouse.dy+1].tower=self
		self.pos = (mymouse.dx, mymouse.dy)
		self.center = (self.pos[0]+1, self.pos[1]+1)
		# get screen coord area
		self.llx = game.map.llx + self.pos[0] * game.map.cellsize
		self.lly = game.map.lly + self.pos[1] * game.map.cellsize
		self.urx = game.map.llx + (self.pos[0]+2) * game.map.cellsize
		self.ury = game.map.lly + (self.pos[1]+2) * game.map.cellsize
		self.cx = game.map.llx + self.center[0] * game.map.cellsize
		self.cy = game.map.lly + self.center[1] * game.map.cellsize
		
		if game.map.recalc_routes():	# recalc routes
			game.towers.append ( self )
			window.push_handlers(self)
			return True
		else:
			# make routes passable again
			game.map.cell[mymouse.dx][mymouse.dy].passable=True
			game.map.cell[mymouse.dx+1][mymouse.dy].passable=True
			game.map.cell[mymouse.dx+1][mymouse.dy+1].passable=True
			game.map.cell[mymouse.dx][mymouse.dy+1].passable=True
			# remove pointers to tower in cells
			game.map.cell[mymouse.dx][mymouse.dy].tower=None
			game.map.cell[mymouse.dx+1][mymouse.dy].tower=None
			game.map.cell[mymouse.dx+1][mymouse.dy+1].tower=None
			game.map.cell[mymouse.dx][mymouse.dy+1].tower=None
			game.map.recalc_routes()	# recalc original routes
			return False	# tell calling function that deploy failed
		
	def deploy_fast (self):	# used when re-checking of paths is not needed - ie. for an upgrade
		# get screen coord area
		self.llx = game.map.llx + self.pos[0] * game.map.cellsize
		self.lly = game.map.lly + self.pos[1] * game.map.cellsize
		self.urx = game.map.llx + (self.pos[0]+2) * game.map.cellsize
		self.ury = game.map.lly + (self.pos[1]+2) * game.map.cellsize
		self.cx = game.map.llx + self.center[0] * game.map.cellsize
		self.cy = game.map.lly + self.center[1] * game.map.cellsize
		game.towers.append ( self )
		window.push_handlers(self)

	
	def sell (self):
		window.remove_handlers(self)
		self.mouse_over = False # BUGFIX: range still drawn when S key used to sell and mouse over spot where tower was
		game.towers.remove(self)
		game.selected = None
		if game.state & game.states['pregame']:
			# take no time
			game.towers.append ( aSell (self.pos[0],self.pos[1], 0.01) )
			# and free
			game.credits += self.cost
		else:
			game.towers.append ( aSell (self.pos[0],self.pos[1], game.map.sell_time) )
			game.credits += self.sell_price
			game.map.sell_time *= game.map.sell_time_multiplier

		
	def upgrade (self):
		print "DOING UPGRADE!"
		
		self.mouse_over = False
		pos=copy.copy(self.pos)
		upgrade_to = self.get_upgrade()
		if game.state & game.states['pregame']:
			self.upgrade_time = 0.01
		game.towers.append ( anUpgrade (pos[0], pos[1], self.upgrade_time, upgrade_to , copy.copy(self.target_mode) ))
		window.remove_handlers(self)
		game.towers.remove( self )
		game.selected=None

	
	def get_upgrade(self):
		return Cannon_2 (copy.copy(self.pos))
		
	def update (self,dt):
		self.time_since_last_shot+=dt
		if self.time_since_last_shot > self.time_between_shots and self.target is None:
			# find a new target
			nearby_enemies=[]
			# create locals for speed
			cx=self.center[0]
			cy=self.center[1]
			for enemy in game.enemies:
				# get squared distance
				sd = (cx-enemy.pos[0])**2 + (cy-enemy.pos[1])**2
				if sd < self.range:
					self.target = enemy
					return 0
			else:
				self.target = None
				return 0
					
		if self.target and self.target.alive:
			# if target also still alive
			# check target is still in range
			sd = (self.center[0]-self.target.pos[0])**2 + (self.center[1]-self.target.pos[1])**2
			if sd < self.range:
				# have target, can we fire?
				if self.time_since_last_shot > self.time_between_shots:
					# yes we can
					#print "BANG!"
					audio_cannon_1_fire.play()
					game.projectiles.append (Bullet_1 ( [self.pos[0]+1, self.pos[1]+1], self.target, self.damage_per_shot))
					self.time_since_last_shot=0
				# turn turret to face target
				# get angle in degrees from turret to target
				dx = self.center[0] - self.target.pos[0]
				dy = self.center[1] - self.target.pos[1]
				self.direction = math.atan2 (dy, -dx) * 57.2957795 + 90
			else:
				# old target left range
				self.target = None
		else:
			self.target = None
			
		
		
		
	def draw (self, alpha=1):
		# base
		#cannon_1_base_sprite.blit (game.map.llx + (game.map.cellsize * self.pos[0]) , game.map.lly + (game.map.cellsize * self.pos[1]) )
		cannon_1_base_sprite.blit (self.llx, self.lly)
		# turret
		glPushMatrix()
		#glTranslatef (game.map.llx + (game.map.cellsize * self.center[0]),game.map.llx + (game.map.cellsize * self.center[1]),0)
		glTranslatef (self.cx, self.cy, 0)
		glRotatef (-self.direction, 0, 0, 1)
		cannon_1_turret_sprite.blit (0,0)
		glPopMatrix()
		
		
	def draw_highlight (self):
		width = self.range_sq * game.map.cellsize * 2
		offset = width * 0.5
		#range_sprite.blit ( -offset + game.map.llx + (game.map.cellsize * self.center[0]), -offset + game.map.lly + (game.map.cellsize * self.center[1]), width=width, height=width)
		range_sprite.blit ( -offset + self.cx, -offset + self.cy, width=width, height=width)
	
		
	def draw_selection (self):
		selected_tex.blit (self.llx, self.lly)
		
		
	def on_mouse_motion(self, x, y, dx, dy):
		if (x>self.llx and x<self.urx and y>self.lly and y<self.ury) and not game.state & game.states['paused']:
			self.mouse_over=True
			game.highlighted=self
		else:
			self.mouse_over=False
			
	def on_mouse_release(self, x, y, buttons, modifiers):
		if self.mouse_over and buttons & mouse.LEFT and not game.state & game.states['paused'] and not game.deploying:
			game.selected=self


class Cannon_2 (object):
	def __init__ (self, position=(0,0)):
		self.label = "CANNON - LVL 2"
		self.highlight = False
		self.pos = position
		self.center = (position[0]+1, position[1]+1)
		# screen coords
		self.llx = 0
		self.lly = 0
		self.urx = 0
		self.ury = 0
		self.cx = 0
		self.cy = 0
		
		self.direction = 0
		self.active = False
		self.target = None
		self.cost = 40
		self.range_sq = 5
		self.range = self.range_sq * self.range_sq
		
		self.upgrade_cost = 100
		self.upgrade_time = 10
		self.damage_per_shot = 20
		self.sell_price = 25
		self.time_between_shots = 1.4
		self.time_since_last_shot = 3
		self.target_mode = 6	# 0 - none, 1 strong 2 weak 3 fast 4 slow 5 near 6 end of path
		self.upgradeable = True
		self.info_headings = "Range:\nDamage:\nRate:\n\nUpgrade for:\nSell for:"
		self.info = str(self.range_sq) + "\n" + str(self.damage_per_shot) + "\n" + str(self.time_between_shots) + "\n\n" + str(self.upgrade_cost) + "\n" + str(self.sell_price)
		
		self.mouse_over = False
	
	def deploy (self):
		# make map squares impassable
		game.map.cell[mymouse.dx][mymouse.dy].passable=False
		game.map.cell[mymouse.dx+1][mymouse.dy].passable=False
		game.map.cell[mymouse.dx+1][mymouse.dy+1].passable=False
		game.map.cell[mymouse.dx][mymouse.dy+1].passable=False
		# put pointer to tower in map cells
		game.map.cell[mymouse.dx][mymouse.dy].tower=self
		game.map.cell[mymouse.dx+1][mymouse.dy].tower=self
		game.map.cell[mymouse.dx+1][mymouse.dy+1].tower=self
		game.map.cell[mymouse.dx][mymouse.dy+1].tower=self
		self.pos = (mymouse.dx, mymouse.dy)
		self.center = (self.pos[0]+1, self.pos[1]+1)
		# get screen coord area
		self.llx = game.map.llx + self.pos[0] * game.map.cellsize
		self.lly = game.map.lly + self.pos[1] * game.map.cellsize
		self.urx = game.map.llx + (self.pos[0]+2) * game.map.cellsize
		self.ury = game.map.lly + (self.pos[1]+2) * game.map.cellsize
		self.cx = game.map.llx + self.center[0] * game.map.cellsize
		self.cy = game.map.lly + self.center[1] * game.map.cellsize
		
		if game.map.recalc_routes():	# recalc routes
			game.towers.append ( self )
			window.push_handlers(self)
			return True
		else:
			# make routes passable again
			game.map.cell[mymouse.dx][mymouse.dy].passable=True
			game.map.cell[mymouse.dx+1][mymouse.dy].passable=True
			game.map.cell[mymouse.dx+1][mymouse.dy+1].passable=True
			game.map.cell[mymouse.dx][mymouse.dy+1].passable=True
			# remove pointers to tower in cells
			game.map.cell[mymouse.dx][mymouse.dy].tower=None
			game.map.cell[mymouse.dx+1][mymouse.dy].tower=None
			game.map.cell[mymouse.dx+1][mymouse.dy+1].tower=None
			game.map.cell[mymouse.dx][mymouse.dy+1].tower=None
			game.map.recalc_routes()	# recalc original routes
			return False	# tell calling function that deploy failed
		
	def deploy_fast (self):	# used when re-checking of paths is not needed - ie. for an upgrade
		# get screen coord area
		self.llx = game.map.llx + self.pos[0] * game.map.cellsize
		self.lly = game.map.lly + self.pos[1] * game.map.cellsize
		self.urx = game.map.llx + (self.pos[0]+2) * game.map.cellsize
		self.ury = game.map.lly + (self.pos[1]+2) * game.map.cellsize
		self.cx = game.map.llx + self.center[0] * game.map.cellsize
		self.cy = game.map.lly + self.center[1] * game.map.cellsize
		game.towers.append ( self )
		window.push_handlers(self)

	
	def sell (self):
		window.remove_handlers(self)
		self.mouse_over = False # BUGFIX: range still drawn when S key used to sell and mouse over spot where tower was
		game.towers.remove(self)
		game.selected = None
		if game.state & game.states['pregame']:
			# take no time
			game.towers.append ( aSell (self.pos[0],self.pos[1], 0.01) )
			# and free
			game.credits += self.cost
		else:
			game.towers.append ( aSell (self.pos[0],self.pos[1], game.map.sell_time) )
			game.credits += self.sell_price
			game.map.sell_time *= game.map.sell_time_multiplier

		
	def upgrade (self):
		self.mouse_over = False
		pos=copy.copy(self.pos)
		upgrade_to = self.get_upgrade()
		if game.state & game.states['pregame']:
			self.upgrade_time = 0.01
		game.towers.append ( anUpgrade (pos[0], pos[1], self.upgrade_time, upgrade_to , copy.copy(self.target_mode) ))
		window.remove_handlers(self)
		game.towers.remove( self )
		game.selected=None

	
	def get_upgrade(self):
		return Cannon_3 (copy.copy(self.pos))
		
	def update (self,dt):
		self.time_since_last_shot+=dt
		if self.time_since_last_shot > self.time_between_shots:
			# find a new target
			nearby_enemies=[]
			# create locals for speed
			cx=self.center[0]
			cy=self.center[1]
			for enemy in game.enemies:
				# get squared distance
				sd = (cx-enemy.pos[0])**2 + (cy-enemy.pos[1])**2
				if sd < self.range:
					nearby_enemies.append ((enemy, sd, enemy.get_path_distance_left() ))	# create list of enemy, dist, and path length remaining
			if nearby_enemies:
				if self.target_mode == 6:	# nearest to end of path
					enemy_path_left=99999
					for near_enemy in nearby_enemies:
						if near_enemy[2] < enemy_path_left:
							enemy_path_left=near_enemy[2]
							self.target = near_enemy[0]	
				elif self.target_mode == 5:	# nearest to tower
					closest=99999
					for near_enemy in nearby_enemies:
						if near_enemy[1] < closest:
							closest = near_enemy[1]
							self.target = near_enemy[0]
				elif self.target_mode == 1:	# strongest
					strongest=-1
					for near_enemy in nearby_enemies:
						if near_enemy[0].health > strongest:
							strongest = near_enemy[0].health
							self.target = near_enemy[0]
				elif self.target_mode == 2:	# weakest
					strongest=99999
					for near_enemy in nearby_enemies:
						if near_enemy[0].health < strongest:
							strongest = near_enemy[0].health
							self.target = near_enemy[0]
				elif self.target_mode == 3:	# fastest
					fastest=0
					for near_enemy in nearby_enemies:
						if near_enemy[0].speed > fastest:
							fastest = near_enemy[0].speed
							self.target = near_enemy[0]
				elif self.target_mode == 4:	# slowest
					fastest=99999
					for near_enemy in nearby_enemies:
						if near_enemy[0].speed < fastest:
							fastest = near_enemy[0].speed
							self.target = near_enemy[0]
			else:
				self.target = None
				return 0
					
		if self.target and self.target.alive:
			# if target also still alive
			# check target is still in range
			sd = (self.center[0]-self.target.pos[0])**2 + (self.center[1]-self.target.pos[1])**2
			if sd < self.range:
				# have target, can we fire?
				if self.time_since_last_shot > self.time_between_shots:
					# yes we can
					#print "BANG!"
					audio_cannon_2_fire.play()
					game.projectiles.append (Bullet_2 ( [self.pos[0]+1, self.pos[1]+1], self.target, self.damage_per_shot))
					self.time_since_last_shot=0
				# turn turret to face target
				# get angle in degrees from turret to target
				dx = self.center[0] - self.target.pos[0]
				dy = self.center[1] - self.target.pos[1]
				self.direction = math.atan2 (dy, -dx) * 57.2957795 + 90
			else:
				# old target left range
				self.target = None
		else:
			self.target = None
			
		
		
		
	def draw (self, alpha=1):
		# base
		#cannon_1_base_sprite.blit (game.map.llx + (game.map.cellsize * self.pos[0]) , game.map.lly + (game.map.cellsize * self.pos[1]) )
		cannon_2_base_sprite.blit (self.llx, self.lly)
		# turret
		glPushMatrix()
		#glTranslatef (game.map.llx + (game.map.cellsize * self.center[0]),game.map.llx + (game.map.cellsize * self.center[1]),0)
		glTranslatef (self.cx, self.cy, 0)
		glRotatef (-self.direction, 0, 0, 1)
		cannon_2_turret_sprite.blit (0,0)
		glPopMatrix()
		
		
	def draw_highlight (self):
		width = self.range_sq * game.map.cellsize * 2
		offset = width * 0.5
		#range_sprite.blit ( -offset + game.map.llx + (game.map.cellsize * self.center[0]), -offset + game.map.lly + (game.map.cellsize * self.center[1]), width=width, height=width)
		range_sprite.blit ( -offset + self.cx, -offset + self.cy, width=width, height=width)
		
		# draw ai panel with appropriate button selected
		ai_frame.enabled=True
		for ai_button in ai_frame.widgets:
			if ai_frame.widgets.index(ai_button)==self.target_mode-1:
				ai_button.selected=True
			else:
				ai_button.selected=False

		
	def draw_selection (self):
		selected_tex.blit (self.llx, self.lly)
		
		
	def on_mouse_motion(self, x, y, dx, dy):
		if (x>self.llx and x<self.urx and y>self.lly and y<self.ury) and not game.state & game.states['paused']:
			self.mouse_over=True
			game.highlighted=self
		else:
			self.mouse_over=False
			
	def on_mouse_release(self, x, y, buttons, modifiers):
		if self.mouse_over and buttons & mouse.LEFT and not game.state & game.states['paused']:
			game.selected=self



			
class Cannon_3 (object):
	def __init__ (self, position=(0,0)):
		self.label = "CANNON - LVL 3"
		self.highlight = False
		self.pos = position
		self.center = (position[0]+1, position[1]+1)
		# screen coords
		self.llx = 0
		self.lly = 0
		self.urx = 0
		self.ury = 0
		self.cx = 0
		self.cy = 0
		
		self.direction = 0
		self.active = False
		self.target = None
		self.cost = 100
		self.range_sq = 5
		self.range = self.range_sq * self.range_sq
		
		self.upgrade_cost = 250
		self.upgrade_time = 20
		self.damage_per_shot = 50
		self.sell_price = 80
		self.time_between_shots = 1.6
		self.time_since_last_shot = 3
		self.target_mode = 6	# 0 - none, 1 strong 2 weak 3 fast 4 slow 5 near 6 end of path
		self.upgradeable = True
		self.info_headings = "Range:\nDamage:\nRate:\n\nUpgrade for:\nSell for:"
		self.info = str(self.range_sq) + "\n" + str(self.damage_per_shot) + "\n" + str(self.time_between_shots) + "\n\n" + str(self.upgrade_cost) + "\n" + str(self.sell_price)
		
		self.mouse_over = False
	
	def deploy (self):
		# make map squares impassable
		game.map.cell[mymouse.dx][mymouse.dy].passable=False
		game.map.cell[mymouse.dx+1][mymouse.dy].passable=False
		game.map.cell[mymouse.dx+1][mymouse.dy+1].passable=False
		game.map.cell[mymouse.dx][mymouse.dy+1].passable=False
		# put pointer to tower in map cells
		game.map.cell[mymouse.dx][mymouse.dy].tower=self
		game.map.cell[mymouse.dx+1][mymouse.dy].tower=self
		game.map.cell[mymouse.dx+1][mymouse.dy+1].tower=self
		game.map.cell[mymouse.dx][mymouse.dy+1].tower=self
		self.pos = (mymouse.dx, mymouse.dy)
		self.center = (self.pos[0]+1, self.pos[1]+1)
		# get screen coord area
		self.llx = game.map.llx + self.pos[0] * game.map.cellsize
		self.lly = game.map.lly + self.pos[1] * game.map.cellsize
		self.urx = game.map.llx + (self.pos[0]+2) * game.map.cellsize
		self.ury = game.map.lly + (self.pos[1]+2) * game.map.cellsize
		self.cx = game.map.llx + self.center[0] * game.map.cellsize
		self.cy = game.map.lly + self.center[1] * game.map.cellsize
		
		if game.map.recalc_routes():	# recalc routes
			game.towers.append ( self )
			window.push_handlers(self)
			return True
		else:
			# make routes passable again
			game.map.cell[mymouse.dx][mymouse.dy].passable=True
			game.map.cell[mymouse.dx+1][mymouse.dy].passable=True
			game.map.cell[mymouse.dx+1][mymouse.dy+1].passable=True
			game.map.cell[mymouse.dx][mymouse.dy+1].passable=True
			# remove pointers to tower in cells
			game.map.cell[mymouse.dx][mymouse.dy].tower=None
			game.map.cell[mymouse.dx+1][mymouse.dy].tower=None
			game.map.cell[mymouse.dx+1][mymouse.dy+1].tower=None
			game.map.cell[mymouse.dx][mymouse.dy+1].tower=None
			game.map.recalc_routes()	# recalc original routes
			return False	# tell calling function that deploy failed
		
	def deploy_fast (self):	# used when re-checking of paths is not needed - ie. for an upgrade
		# get screen coord area
		self.llx = game.map.llx + self.pos[0] * game.map.cellsize
		self.lly = game.map.lly + self.pos[1] * game.map.cellsize
		self.urx = game.map.llx + (self.pos[0]+2) * game.map.cellsize
		self.ury = game.map.lly + (self.pos[1]+2) * game.map.cellsize
		self.cx = game.map.llx + self.center[0] * game.map.cellsize
		self.cy = game.map.lly + self.center[1] * game.map.cellsize
		game.towers.append ( self )
		window.push_handlers(self)

	
	def sell (self):
		window.remove_handlers(self)
		self.mouse_over = False # BUGFIX: range still drawn when S key used to sell and mouse over spot where tower was
		game.towers.remove(self)
		game.selected = None
		if game.state & game.states['pregame']:
			# take no time
			game.towers.append ( aSell (self.pos[0],self.pos[1], 0.01) )
			# and free
			game.credits += self.cost
		else:
			game.towers.append ( aSell (self.pos[0],self.pos[1], game.map.sell_time) )
			game.credits += self.sell_price
			game.map.sell_time *= game.map.sell_time_multiplier

		
	def upgrade (self):
		self.mouse_over = False
		pos=copy.copy(self.pos)
		upgrade_to = self.get_upgrade()
		if game.state & game.states['pregame']:
			self.upgrade_time = 0.01
		game.towers.append ( anUpgrade (pos[0], pos[1], self.upgrade_time, upgrade_to , copy.copy(self.target_mode) ))
		window.remove_handlers(self)
		game.towers.remove( self )
		game.selected=None

	
	def get_upgrade(self):
		return Cannon_1 (copy.copy(self.pos))
		
	def update (self,dt):
		self.time_since_last_shot+=dt
		if self.time_since_last_shot > self.time_between_shots:
			# find a new target
			nearby_enemies=[]
			# create locals for speed
			cx=self.center[0]
			cy=self.center[1]
			for enemy in game.enemies:
				# get squared distance
				sd = (cx-enemy.pos[0])**2 + (cy-enemy.pos[1])**2
				if sd < self.range:
					nearby_enemies.append ((enemy, sd, enemy.get_path_distance_left() ))	# create list of enemy, dist, and path length remaining
			if nearby_enemies:
				if self.target_mode == 6:	# nearest to end of path
					enemy_path_left=99999
					for near_enemy in nearby_enemies:
						if near_enemy[2] < enemy_path_left:
							enemy_path_left=near_enemy[2]
							self.target = near_enemy[0]	
				elif self.target_mode == 5:	# nearest to tower
					closest=99999
					for near_enemy in nearby_enemies:
						if near_enemy[1] < closest:
							closest = near_enemy[1]
							self.target = near_enemy[0]
				elif self.target_mode == 1:	# strongest
					strongest=-1
					for near_enemy in nearby_enemies:
						if near_enemy[0].health > strongest:
							strongest = near_enemy[0].health
							self.target = near_enemy[0]
				elif self.target_mode == 2:	# weakest
					strongest=99999
					for near_enemy in nearby_enemies:
						if near_enemy[0].health < strongest:
							strongest = near_enemy[0].health
							self.target = near_enemy[0]
				elif self.target_mode == 3:	# fastest
					fastest=0
					for near_enemy in nearby_enemies:
						if near_enemy[0].speed > fastest:
							fastest = near_enemy[0].speed
							self.target = near_enemy[0]
				elif self.target_mode == 4:	# slowest
					fastest=99999
					for near_enemy in nearby_enemies:
						if near_enemy[0].speed < fastest:
							fastest = near_enemy[0].speed
							self.target = near_enemy[0]
			else:
				self.target = None
				return 0
					
		if self.target and self.target.alive:
			# if target also still alive
			# check target is still in range
			sd = (self.center[0]-self.target.pos[0])**2 + (self.center[1]-self.target.pos[1])**2
			if sd < self.range:
				# have target, can we fire?
				if self.time_since_last_shot > self.time_between_shots:
					# yes we can
					#print "BANG!"
					audio_cannon_2_fire.play()
					game.projectiles.append (Bullet_3 ( [self.pos[0]+1, self.pos[1]+1], self.target, self.damage_per_shot))
					self.time_since_last_shot=0
				# turn turret to face target
				# get angle in degrees from turret to target
				dx = self.center[0] - self.target.pos[0]
				dy = self.center[1] - self.target.pos[1]
				self.direction = math.atan2 (dy, -dx) * 57.2957795 + 90
			else:
				# old target left range
				self.target = None
		else:
			self.target = None
			
		
		
		
	def draw (self, alpha=1):
		# base
		#cannon_1_base_sprite.blit (game.map.llx + (game.map.cellsize * self.pos[0]) , game.map.lly + (game.map.cellsize * self.pos[1]) )
		cannon_3_base_sprite.blit (self.llx, self.lly)
		# turret
		glPushMatrix()
		#glTranslatef (game.map.llx + (game.map.cellsize * self.center[0]),game.map.llx + (game.map.cellsize * self.center[1]),0)
		glTranslatef (self.cx, self.cy, 0)
		glRotatef (-self.direction, 0, 0, 1)
		cannon_3_turret_sprite.blit (0,0)
		glPopMatrix()
		
		
	def draw_highlight (self):
		width = self.range_sq * game.map.cellsize * 2
		offset = width * 0.5
		#range_sprite.blit ( -offset + game.map.llx + (game.map.cellsize * self.center[0]), -offset + game.map.lly + (game.map.cellsize * self.center[1]), width=width, height=width)
		range_sprite.blit ( -offset + self.cx, -offset + self.cy, width=width, height=width)
		
		# draw ai panel with appropriate button selected
		ai_frame.enabled=True
		for ai_button in ai_frame.widgets:
			if ai_frame.widgets.index(ai_button)==self.target_mode-1:
				ai_button.selected=True
			else:
				ai_button.selected=False

		
	def draw_selection (self):
		selected_tex.blit (self.llx, self.lly)
		
		
	def on_mouse_motion(self, x, y, dx, dy):
		if (x>self.llx and x<self.urx and y>self.lly and y<self.ury) and not game.state & game.states['paused']:
			self.mouse_over=True
			game.highlighted=self
		else:
			self.mouse_over=False
			
	def on_mouse_release(self, x, y, buttons, modifiers):
		if self.mouse_over and buttons & mouse.LEFT and not game.state & game.states['paused']:
			game.selected=self
			
			
			
			

		
class particle_small_hit(object):
	def __init__ (self, pos):
		self.duration = random.random()*0.8
		self.time_alive = 0
		self.xdir = 33-(random.random()*66)
		self.ydir = 33-(random.random()*66)
		#self.pos=[ game.map.llx + (game.map.cellsize * pos[0]) , game.map.lly + (game.map.cellsize * pos[1]) ]
		self.pos = pos
		self.alpha_scale = 1.0 / self.duration
		
	def draw (self):
		x = 1-self.time_alive * self.alpha_scale
		glColor4f (1,x,x,x)
		mote_sprite.blit ( self.pos[0] , self.pos[1] )
		glColor4f (1,1,1,1)
	
	def update (self, tick):
		self.time_alive += tick
		if self.time_alive < self.duration:
			self.pos[0]+=self.xdir * tick
			self.pos[1]+=self.ydir * tick
		else:
			game.particles.remove (self)
			
			
class particle_blue_trail(object):
	def __init__ (self, pos):
		#self.duration = random.random()*0.8
		self.duration = 0.4
		self.time_alive = 0
		self.pos=[ game.map.llx + (game.map.cellsize * pos[0]) , game.map.lly + (game.map.cellsize * pos[1]) ]
		self.alpha_scale = 1.0 / self.duration
		
	def draw (self):
		x = 1-self.time_alive * self.alpha_scale
		glColor4f (1,1,1,x)
		blue_particle_sprite.blit ( self.pos[0], self.pos[1])
		glColor4f (1,1,1,1)
	
	def update (self, tick):
		self.time_alive += tick
		if self.time_alive > self.duration:
			game.particles.remove (self)
			
			
class particle_white_trail(object):
	def __init__ (self, pos):
		#self.duration = random.random()*0.8
		self.duration = 0.4
		self.time_alive = 0
		self.pos=[ game.map.llx + (game.map.cellsize * pos[0]) , game.map.lly + (game.map.cellsize * pos[1]) ]
		self.alpha_scale = 1.0 / self.duration
		
	def draw (self):
		x = 1-self.time_alive * self.alpha_scale
		glColor4f (x,x,1,x)
		white_particle_sprite.blit ( self.pos[0], self.pos[1])
		glColor4f (1,1,1,1)
	
	def update (self, tick):
		self.time_alive += tick
		if self.time_alive > self.duration:
			game.particles.remove (self)
			
class particle_explosion(object):
	def __init__ (self, pos, count=50):
		self.duration = 1.1
		self.time_alive = 0
		self.particle_count = count
		self.dir=[]
		self.curpos=[]
		self.sprites=[]
		screenx=game.map.llx + (game.map.cellsize * pos[0])
		screeny=game.map.lly + (game.map.cellsize * pos[1])
		for i in xrange (0,self.particle_count):
			x = -333+random.random()*666
			y = -333+random.random()*666
			self.dir.append ([x,y])
			#b=copy.copy(pos)
			#self.curpos.append ([copy.copy(self.screenx),copy.copy(self.screeny)])
			self.curpos.append ([screenx,screeny])
			self.sprites.append ( pyglet.sprite.Sprite(spark_pic, copy.copy(screenx), copy.copy(screeny), batch=batch) )
		self.alpha_scale = 1.0 / self.duration
		

		
	def draw (self):
		x = 1 - self.time_alive * self.alpha_scale
		glColor4f (1,1,1, x)
		t = 0
		# set up local variables for speed
		curpos=self.curpos
		s0=spark_big_sprite
		s1=spark_sprite
		s2=mote_sprite
		for i in xrange (0,self.particle_count):
			if t==0:
				s0.blit (curpos[i][0] , curpos[i][1] )
			elif t==1:
				s1.blit (curpos[i][0] , curpos[i][1] )
			else:
				s2.blit (curpos[i][0] , curpos[i][1] )
			t+=1
			if t>2: t=0
		glColor4f (1,1,1,1)
		
		
	
	def update (self, tick):
		self.time_alive += tick
		if self.time_alive < self.duration:
			omt = (1.0-tick*2.0)	# scaling factor for deceleration
			curpos=self.curpos
			dir=self.dir
			for i in xrange (0,self.particle_count):
				curpos[i][0]+=dir[i][0]*tick
				curpos[i][1]+=dir[i][1]*tick
				dir[i][0]*= omt 	# slows particles due to air density
				dir[i][1]*= omt 	# slows particles due to air density
		else:
			game.particles.remove (self)
		
		
		
class aGame(object):
	def __init__ (self, cellwidth=24):
		self.cw=cellwidth
		self.states={'paused':1, 'pregame':2, 'ingame':4, 'menu':8}
		self.state=self.states['menu'] | self.states['pregame']
		self.map = None
		self.towers=[]
		self.enemies=[]
		self.projectiles=[]
		self.particles=[]
		self.score = 0
		self.bonus = 0
		self.credits = 595
		self.lives = 20
		self.create_level()
		self.selected = None
		self.highlighted = None
		self.deploying = None
		self.overlay = None	# menu, banner etc...
		self.sound_enabled = False
		
	def reset (self):
		self.towers=[]
		self.enemies=[]
		self.projectiles=[]
		self.particles=[]
		self.score=0
		score_label.text = "Score: 0"
		self.bonus=0
		self.lives=20
		self.credits = 90
		self.selected=None
		self.deploying=None
		self.highlighted=None
		self.state = self.state | self.states['pregame']
		self.create_level()
		global mymouse
		mymouse=amouse()
		
		
	def create_level (self):
		self.map = aMap(cellsize=self.cw, llx=self.cw * 2, lly=self.cw * 4)
		for route in self.map.routes:
			route.recalc()

			

@window.event
def on_key_release (symbol, modifiers):
	if game.state & game.states['ingame']:
		if game.selected and symbol==key.S:
			game.selected.sell()
		if symbol==key._1:
			cannon_tower_button.on_click(cannon_tower_button)
	
			
@window.event
def on_deactivate():
	# lost focus - pause if ingame
	if game.state & game.states['ingame'] and not game.state & game.states['paused']:
		game.state = game.state | game.states['paused']
		set_overlay ( PauseMenu() )
			
@window.event
def on_mouse_release (x,y,buttons,modifiers):
	if buttons & mouse.RIGHT:
		mymouse.rmb_clicked=True
	if buttons & mouse.LEFT:
		mymouse.lmb_clicked=True
	if buttons & mouse.MIDDLE:
		if game.state & game.states['ingame']:
			px=(x-game.map.llx)/float(game.map.cellsize)
			py=(y-game.map.lly)/float(game.map.cellsize)
			game.particles.append (particle_explosion( (px,py) ))
		
		
@window.event
def on_mouse_motion (x,y,dx,dy):
	mymouse.update_pos (x,y)
	#print x,y
	

	
@window.event
def on_draw():

	window.clear()
	#background_image.blit(0,0)

	if game.state & game.states['ingame']:
		# draw in height order, far to near
		game.map.draw()
		# draw appropriate ingame stuff
		
		# do info panels
		if game.deploying:
			type=game.deploying.__class__.__name__
			if type=="Cannon_1":
				cannon_info_label.draw()
			elif type=="Berserker_1":
				berserker_info_label.draw()
				
		
		for tower in game.towers:
			tower.draw()
		if game.selected:
			#game.selected.draw_highlight()
			game.selected.draw()
			game.selected.draw_selection()
			# draw info panel
			type=game.selected.__class__.__name__
			if type=="Cannon_1":
				cannon_1_info_label.draw()
			elif type=="Cannon_2":
				cannon_2_info_label.draw()
			elif type=="Cannon_3":
				cannon_3_info_label.draw()
			elif type=="Berserker_1":
				berserker_1_info_label.draw()
			elif type=="Berserker_2":
				berserker_2_info_label.draw()
			elif type=="Berserker_3":
				berserker_3_info_label.draw()
		
		for enemy in game.enemies:
			enemy.draw()
			
		if game.highlighted and game.highlighted.mouse_over and not game.deploying and not game.selected:
			# draw range highlight etc..
			game.highlighted.draw_highlight()
			# also draw info panel
			type=game.highlighted.__class__.__name__
			if type=="Cannon_1":
				cannon_1_info_label.draw()
			elif type=="Cannon_2":
				cannon_2_info_label.draw()
			elif type=="Cannon_3":
				cannon_3_info_label.draw()
			elif type=="Berserker_1":
				berserker_1_info_label.draw()
			elif type=="Berserker_2":
				berserker_2_info_label.draw()
			elif type=="Berserker_3":
				berserker_3_info_label.draw()
			
		
		for particle in game.particles:
			particle.draw()
			
		for proj in game.projectiles:
			proj.draw()
			

		credits_label.text = "Credits: " + str(game.credits)
		credits_label.draw()
		lives_label.draw()
		score_label.draw()
		
		# draw gui
		gui.draw()
	
	
	if game.overlay:
		game.overlay.draw()
			
	# draw mouse
	mymouse.draw()
	
	
	
def update(dt):
	dt * 0.5
	if game.state & game.states['ingame']:
		# while ingame...
		# update gui
		gui.update(dt)
		
		ai_frame.enabled=False	# make sure ai frame doesnt get stuck
		
		if game.selected:
			selected_frame.enabled = True
			if game.selected.target_mode:
				# has an ai - show frame, and show the correct one selected
				ai_frame.enabled=True
				for ai_button in ai_frame.widgets:
					if ai_frame.widgets.index(ai_button)==game.selected.target_mode-1:
						ai_button.selected=True
					else:
						ai_button.selected=False
			if game.selected.upgradeable and game.credits >= game.selected.upgrade_cost:
				upgrade_button.visible = True
			else:
				upgrade_button.visible = False
		else:
			selected_frame.enabled = False
			ai_frame.enabled=False
		
		if not game.state & game.states['paused']:

			if not game.state & game.states['pregame']:
				# make sure swarms dont kick off until pregame is unset
				game.map.swarm_update (dt)
		
			#for proj in game.projectiles:
			#	proj.update (dt)
			map ( lambda i:i.update (dt), game.projectiles )
		
			#for enemy in game.enemies:
			#	enemy.update(dt)
			map ( lambda i:i.update (dt), game.enemies )
			
			#for tower in game.towers:
			#	tower.update (dt)
			map ( lambda i:i.update (dt), game.towers )
				
			#for particle in game.particles:
			#	particle.update (dt)
			map ( lambda i:i.update (dt), game.particles )
				
	mymouse.update()

	
	
	
# global instances of classes declared above

# create game singleton
game=aGame(24)

score_label = pyglet.text.Label ('Score: '+str(game.score),
						font_name=FONT_NAME, 
                          font_size=18,
						  width=window.width/2,
						  height=200,
						  multiline=True,
                          x=60, y=window.height-27,
                          anchor_x='left', anchor_y='top')

credits_label = pyglet.text.Label ('Credits: '+str(game.credits),
						font_name=FONT_NAME, 
                          font_size=18,
						  width=window.width/2,
						  height=200,
						  multiline=True,
                          x=560, y=window.height-27,
                          anchor_x='left', anchor_y='top')
						  
lives_label = pyglet.text.Label ('Lives: '+str(game.lives),
						font_name=FONT_NAME, 
                          font_size=18,
						  width=window.width/2,
						  height=200,
						  multiline=True,
                          x=360, y=window.height-27,
                          anchor_x='left', anchor_y='top')
						  
cannon_info_label = pyglet.text.HTMLLabel 	('<center><font size=5 color=white>Photon Cannon</font></center>'
											+'<font size=4 color=#ffff00>Cost: 5</font><br>'
											+'<font size=4 color=#5566ff>Range: 4</font><br>'
											+'<font size=4 color=#ff4455>Damage: 6</font><br><br>'
											+'<font size=4 color=white>A slow firing, but medium damage tower.  '
											+'Cheap to build, useful for shepherding enemies towards more powerful towers.<br><br>'
											+'Upgrades: Range, Damage - and at levels > 1 targetting AI.</font>' ,
						  width=240,
						  height=400,
						  multiline=True,
                          x=760, y=440,
                          anchor_x='left', anchor_y='top')
cannon_info_label.font_name=FONT_NAME

cannon_1_info_label = pyglet.text.HTMLLabel ('<center><font size=5 color=white>Photon Cannon<br>Level 1</font></center>'
											+'<font size=4 color=#5566ff>Range: 4</font><br>'
											+'<font size=4 color=#ff4455>Damage: 3</font><br><br>'
											+'<font size=4 color=#aaffaa><u>Upgrade Info</u></font><br><br>'
											+'<font size=4 color=#ffff00>Cost: 40</font><br>'
											+'<font size=4 color=#5566ff>Range: 5      (+1)</font><br>'
											+'<font size=4 color=#ff4455>Damage: 15   (+120%)</font>' ,
						  width=240,
						  height=400,
						  multiline=True,
                          x=760, y=440,
                          anchor_x='left', anchor_y='top')
cannon_1_info_label.font_name=FONT_NAME

cannon_2_info_label = pyglet.text.HTMLLabel ('<center><font size=5 color=white>Photon Cannon<br>Level 2</font></center>'
											+'<font size=4 color=#5566ff>Range: 5</font><br>'
											+'<font size=4 color=#ff4455>Damage: 15</font><br><br>'
											+'<font size=4 color=#aaffaa><u>Upgrade Info</u></font><br><br>'
											+'<font size=4 color=#ffff00>Cost: 100</font><br>'
											+'<font size=4 color=#5566ff>Range: 5     (no change)</font><br>'
											+'<font size=4 color=#ff4455>Damage: 50   (+333%)</font>' ,
						  width=240,
						  height=400,
						  multiline=True,
                          x=760, y=440,
                          anchor_x='left', anchor_y='top')
cannon_2_info_label.font_name=FONT_NAME

cannon_3_info_label = pyglet.text.HTMLLabel ('<center><font size=5 color=white>Photon Cannon<br>Level 3</font></center>'
											+'<font size=4 color=#5566ff>Range: 5</font><br>'
											+'<font size=4 color=#ff4455>Damage: 50</font><br><br>'
											+'<font size=4 color=#aaffaa><u>Upgrade Info</u></font><br><br>'
											+'<font size=4 color=#ffff00>Cost: na</font><br>'
											+'<font size=4 color=#5566ff>Range: na    </font><br>'
											+'<font size=4 color=#ff4455>Damage: na   </font>' ,
						  width=240,
						  height=400,
						  multiline=True,
                          x=760, y=440,
                          anchor_x='left', anchor_y='top')
cannon_3_info_label.font_name=FONT_NAME





berserker_info_label = pyglet.text.HTMLLabel 	('<center><font size=5 color=white>Berserker Tower</font></center>'
											+'<font size=4 color=#ffff00>Cost: 15</font><br>'
											+'<font size=4 color=#5566ff>Range: 4.5</font><br>'
											+'<font size=4 color=#ff4455>Damage: 3</font><br><br>'
											+'<font size=4 color=white>A rapid firing, indiscriminate rail gun with no AI.<br>'
											+'Low damage per hit is offset by rate of fire and range.'
											+'<br><br>Upgrades: Damage and Rate of Fire, and later massive Range increase.</font>' ,
						  width=240,
						  height=400,
						  multiline=True,
                          x=760, y=440,
                          anchor_x='left', anchor_y='top')
berserker_info_label.font_name=FONT_NAME	


berserker_1_info_label = pyglet.text.HTMLLabel ('<center><font size=5 color=white>Berserker Tower<br>Level 1</font></center>'
											+'<font size=4 color=#5566ff>Range: 4.5</font><br>'
											+'<font size=4 color=#ff4455>Damage: 3</font><br><br>'
											+'<font size=4 color=#aaffaa><u>Upgrade Info</u></font><br><br>'
											+'<font size=4 color=#ffff00>Cost: 65</font><br>'
											+'<font size=4 color=#5566ff>Range: 5      (+1)</font><br>'
											+'<font size=4 color=#ff4455>Damage: 15   (+33%)</font><br>'
											+'<font size=4 color=#7788ff>Rate of fire +50%</font>',
						  width=240,
						  height=400,
						  multiline=True,
                          x=760, y=440,
                          anchor_x='left', anchor_y='top')
berserker_1_info_label.font_name=FONT_NAME

berserker_2_info_label = pyglet.text.HTMLLabel ('<center><font size=5 color=white>Berserker Tower<br>Level 2</font></center>'
											+'<font size=4 color=#5566ff>Range: 5</font><br>'
											+'<font size=4 color=#ff4455>Damage: 15</font><br><br>'
											+'<font size=4 color=#aaffaa><u>Upgrade Info</u></font><br><br>'
											+'<font size=4 color=#ffff00>Cost: 165</font><br>'
											+'<font size=4 color=#5566ff>Range: 5      (+1)</font><br>'
											+'<font size=4 color=#ff4455>Damage: 40   (+285%)</font><br>'
											+'<font size=4 color=#7788ff>Rate of fire +20%</font>',
						  width=240,
						  height=400,
						  multiline=True,
                          x=760, y=440,
                          anchor_x='left', anchor_y='top')
berserker_2_info_label.font_name=FONT_NAME

berserker_3_info_label = pyglet.text.HTMLLabel ('<center><font size=5 color=white>Berserker Tower<br>Level 3</font></center>'
											+'<font size=4 color=#5566ff>Range: 5</font><br>'
											+'<font size=4 color=#ff4455>Damage: 40</font><br><br>'
											+'<font size=4 color=#aaffaa><u>Upgrade Info</u></font><br><br>'
											+'<font size=4 color=#ffff00>Cost: na</font><br>'
											+'<font size=4 color=#5566ff>Range: na      (+1)</font><br>'
											+'<font size=4 color=#ff4455>Damage: na   (+285%)</font><br>'
											+'<font size=4 color=#7788ff>Rate of fire +na%</font>',
						  width=240,
						  height=400,
						  multiline=True,
                          x=760, y=440,
                          anchor_x='left', anchor_y='top')
berserker_3_info_label.font_name=FONT_NAME


			

						
def cannon_button_on_click (button):
	# unselect all buttons in same frame
	for widget in button.parent.widgets:
		widget.selected=False
	# select button clicked
	button.selected=True
	# update game selected - which in turn drives the mouse draw icon
	game.deploying = Cannon_1 ()
	# make sure nothing selected
	if game.selected:
		game.selected=None
	
def berserker_button_on_click (button):
	# unselect all buttons in same frame
	for widget in button.parent.widgets:
		widget.selected=False
	# select button clicked
	button.selected=True
	# update game selected - which in turn drives the mouse draw icon
	game.deploying = Berserker_1 ()
	# make sure nothing selected
	if game.selected:
		game.selected=None
	
def start_button_on_click (button):
	# disable start button
	gui.widgets.remove(button)
	# flip pregame state
	game.state = game.state ^ game.states['pregame']
	# start swarms
	game.map.active_swarms.append (game.map.swarms.pop(0))
	
	
def sell_button_on_click (button):
	if game.selected:
		game.selected.sell()
		
def pause_button_on_click (button):
	game.state = game.state ^ game.states['paused'] #flip paused flag
	set_overlay ( PauseMenu() )	# overlay paused menu
	
def ai_button_on_click (button):
	for b in button.parent.widgets:
		# for all other ai buttons in frame
		if b is not button:
			b.selected=False
		button.selected=True
	game.selected.target_mode = button.parent.widgets.index(button)+1
	
	
def upgrade_button_on_click (button):
	if game.selected.upgradeable and game.credits>= game.selected.upgrade_cost:
		audio_upgrade.play()
		game.credits -= game.selected.upgrade_cost
		credits_label.text = "Credits: " + str(game.credits)
		game.selected.upgrade()
	else:
		pass


#window = pyglet.window.Window(800, 600,"test",True, style='borderless')

	
		

		
mymouse=amouse()
gui=GUI()

start_button = Button (gui, pos=(850,24), rmb_clears=False, background=button_start_pic)
start_button.on_click = start_button_on_click

pause_button = Button (gui, pos=(930, 24), rmb_clears=False, background=button_pause_pic)
pause_button.on_click = pause_button_on_click 

selected_frame = Frame ( pos=(game.cw*3+(game.map.width*game.cw), game.cw*4 + 32) , width = 300, height = 300, background_colour=(0,0,0,0))
upgrade_button = Button (selected_frame, pos=(0,0), background=upgrade_pic)
sell_button = Button (selected_frame, pos=(141, 0), background=sell_pic)
sell_button.on_click = sell_button_on_click 
upgrade_button.on_click = upgrade_button_on_click
selected_frame.enabled=False

pixels_between_ai_buttons = 44
ai_frame = Frame ( pos=(game.cw*3+(game.map.width*game.cw), game.cw*8-16), width = 300, height=300, background_colour=(0,0,0,0))
x=0
ai_strong_button=Button (ai_frame, pos=(x,0), rmb_clears=False, background=button_ai_strong_off_pic, background_selected=button_ai_strong_on_pic)
ai_strong_button.on_click = ai_button_on_click
x+=pixels_between_ai_buttons
ai_weak_button=Button (ai_frame, pos=(x,0), rmb_clears=False, background=button_ai_weak_off_pic, background_selected=button_ai_weak_on_pic)
ai_weak_button.on_click = ai_button_on_click
x+=pixels_between_ai_buttons
ai_fast_button=Button (ai_frame, pos=(x,0), rmb_clears=False, background=button_ai_fast_off_pic, background_selected=button_ai_fast_on_pic)
ai_fast_button.on_click = ai_button_on_click
x+=pixels_between_ai_buttons
ai_slow_button=Button (ai_frame, pos=(x,0), rmb_clears=False, background=button_ai_slow_off_pic, background_selected=button_ai_slow_on_pic)
ai_slow_button.on_click = ai_button_on_click
x+=pixels_between_ai_buttons
ai_near_button=Button (ai_frame, pos=(x,0), rmb_clears=False, background=button_ai_near_off_pic, background_selected=button_ai_near_on_pic)
ai_near_button.on_click = ai_button_on_click
x+=pixels_between_ai_buttons
ai_far_button=Button (ai_frame, pos=(x,0), rmb_clears=False, background=button_ai_far_off_pic, background_selected=button_ai_far_on_pic)
ai_far_button.on_click = ai_button_on_click
ai_frame.enabled=False

tower_frame = Frame ( pos=(60+(game.map.width*game.map.cellsize),600), width=250, height=150, background_colour=(0,0,0,0) )
cannon_tower_button = Button (tower_frame, pos=(10,10), background=button_cannon_tower_pic, background_selected=button_cannon_tower_selected_pic, background_mouseover=button_cannon_tower_mouseover_pic)
cannon_tower_button.on_click = cannon_button_on_click
berserker_tower_button = Button (tower_frame, pos=(80,10), background=berserker_1_turret_pic, background_selected=button_berserker_tower_selected_pic, background_mouseover=button_berserker_tower_mouseover_pic)
berserker_tower_button.on_click = berserker_button_on_click


set_overlay(MainMenu())


#pyglet.clock.schedule(update)
pyglet.clock.schedule_interval(update,1/120.)	
pyglet.app.run()
