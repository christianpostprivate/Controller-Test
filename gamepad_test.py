import pygame as pg
import traceback
import math

offset_y = 64
WIDTH = 812
HEIGHT = 554 + offset_y

vec = pg.math.Vector2

# initialize pygame
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

pg.joystick.init()

    
deadzone_stick = 0.2
deadzone_trigger = 0.01


# load images and set positions
gamepad_bg = pg.image.load('gamepad.png')

button_a = pg.image.load('button_A.png')
button_b = pg.image.load('button_B.png')
button_x = pg.image.load('button_X.png')
button_y = pg.image.load('button_Y.png')
button_start = pg.image.load('button_start.png')

button_a_pos = (584, 201 + offset_y)
button_b_pos = (637, 148 + offset_y)
button_x_pos = (533, 149 + offset_y)
button_y_pos = (585, 96 + offset_y)

button_back_pos = (336, 159 + offset_y)
button_start_pos = (451, 159 + offset_y)

shoulder_l = pg.image.load('shoulderL.png')
shoulder_r = pg.image.load('shoulderR.png')

shoulder_l_pos = (123, 4 + offset_y)
shoulder_r_pos = (510, 4 + offset_y)

stick_l = vec(0, 0)
stick_r = vec(0, 0)

stick_l_center = vec(214, 175 + offset_y)
stick_r_center = vec(510, 294 + offset_y)

stick_radius = 30
stick_size = 20

dpad_up = pg.image.load('dpad_up.png')
dpad_down = pg.image.load('dpad_down.png')
dpad_left = pg.image.load('dpad_left.png')
dpad_right = pg.image.load('dpad_right.png')

dpad_pos = (262, 249 + offset_y)
dpad = vec(0, 0)

trigger_r = 0
trigger_l = 0

bar_width = 36
bar_height = 160
trigger_l_pos = (16, 16 + offset_y)
trigger_r_pos = (WIDTH - 16 - bar_width, 16 + offset_y)

slider_width = 200
slider_size = 20
slider_pos_start = (WIDTH // 2 - slider_width // 2, HEIGHT - 40)
slider_pos_end = (WIDTH // 2 + slider_width // 2, HEIGHT - 40)

slider_held = False


font = pg.font.SysFont('Arial', 24)


# game loop
running = True
try:
    while running:
        clock.tick(60)
    
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
    
        screen.fill((50, 50, 50))
        # draw the gamepad
        screen.blit(gamepad_bg, (0, offset_y))
        
        # detect gamepad
        gamepads = [pg.joystick.Joystick(x) for x in range(
                     pg.joystick.get_count())]
        if len(gamepads) > 0:
            gamepads[0].init()
            name = gamepads[0].get_name()
            buttons = gamepads[0].get_numbuttons()
            axes = gamepads[0].get_numaxes()
            dpads = gamepads[0].get_numhats()
    
            stick_l_pressed = False
            stick_r_pressed = False
        
            trigger_r = 0
            trigger_l = 0   
            
            text = "Device: " + name
            text_surf = font.render(text, False, (200, 200, 200))
            
            screen.blit(text_surf, (120, 16))
        
            # get gamepad inputs
            for i in range(buttons):
                if gamepads[0].get_button(i):
                    if i == 0:
                        screen.blit(button_a, button_a_pos)
                    elif i == 1:
                        screen.blit(button_b, button_b_pos)
                    elif i == 2:
                        screen.blit(button_x, button_x_pos)
                    elif i == 3:
                        screen.blit(button_y, button_y_pos)
                    elif i == 4:
                        screen.blit(shoulder_l, shoulder_l_pos)
                    elif i == 5:
                        screen.blit(shoulder_r, shoulder_r_pos)
                    elif i == 6:
                        screen.blit(button_start, button_back_pos)
                    elif i == 7:
                        screen.blit(button_start, button_start_pos)
                    elif i == 8:
                        stick_l_pressed = True
                    elif i == 9:
                        stick_r_pressed = True
            
            # get axes values
            for i in range(axes):
                axis = gamepads[0].get_axis(i)
                #if abs(axis) > deadzone:
                if i == 0:
                    stick_l.x = axis
                elif i == 1:
                    stick_l.y = axis
                elif i == 2:
                    if axis > deadzone_trigger:
                        trigger_l = axis
                        trigger_r = 0
                    elif abs(axis) > deadzone_trigger:
                        trigger_r = abs(axis)
                        trigger_l = 0
                elif i == 3:
                    stick_r.y = axis
                elif i == 4:
                    stick_r.x = axis
                    #print('axis', i, axis)
            
            # get dpad values
            for i in range(dpads):
                dpad.x, dpad.y = gamepads[0].get_hat(i)
                if dpad.y == 1:
                    screen.blit(dpad_up, dpad_pos)
                if dpad.y == -1:
                    screen.blit(dpad_down, dpad_pos)
                if dpad.x == 1:
                    screen.blit(dpad_right, dpad_pos)
                if dpad.x == -1:
                    screen.blit(dpad_left, dpad_pos)
                
                    
            # draw analog sticks
            # left stick
            if stick_l.length_squared() != 0:
                if stick_l.length() < deadzone_stick:
                    stick_l.scale_to_length(0)
                else:
                    stick_l /= math.sqrt(abs(stick_l.x) + abs(stick_l.y))
            vec_left = stick_l_center + stick_l * stick_radius
            if stick_l_pressed:
                color = (20, 20, 20)
            else:
                color = (200, 200, 200)
            pg.draw.circle(screen, color, (int(vec_left.x), int(vec_left.y)), 
                           stick_size)

            # right stick
            if stick_r.length_squared() != 0:
                if stick_r.length() < deadzone_stick:
                    stick_r.scale_to_length(0)
                else:
                    stick_r /= math.sqrt(abs(stick_r.x) + abs(stick_r.y))
            vec_right = stick_r_center + stick_r * stick_radius
            if stick_r_pressed:
                color = (20, 20, 20)
            else:
                color = (200, 200, 200)
            pg.draw.circle(screen, color, (int(vec_right.x), 
                                    int(vec_right.y)), stick_size)
            
            # draw shoulder triggers
            r_l = pg.Rect(trigger_l_pos, (bar_width, trigger_l * bar_height))         
            r_r = pg.Rect(trigger_r_pos, (bar_width, trigger_r * bar_height))
            pg.draw.rect(screen, (200, 200, 200), r_l)
            pg.draw.rect(screen, (200, 200, 200), r_r)
            
            
            # draw slider to adjust deadzone
            pg.draw.line(screen, (100, 100, 100), slider_pos_start,
                         slider_pos_end, 6)
            #get mouse position
            m_pos = vec(pg.mouse.get_pos())
            # calculate slider_pos
            slider_pos = vec(slider_pos_start[0] + int(deadzone_stick 
                          * slider_width), slider_pos_start[1])
            # check if mouse is within slider
            if (m_pos - slider_pos).length() < slider_size:
                color = (150, 150, 150)
                if pg.mouse.get_pressed()[0]:
                    slider_held = True
                else:
                    slider_held = False
            else:
                color = (200, 200, 200)
            
            if slider_held:
                slider_pos.x = m_pos.x
                slider_pos.x = max(slider_pos_start[0], min(slider_pos_end[0],
                                   slider_pos.x))
                deadzone_stick = ((slider_pos.x - slider_pos_start[0])
                                    / slider_width)

            pg.draw.circle(screen, color, (int(slider_pos.x), 
                                           int(slider_pos.y)), slider_size)
            
            text = "Analog stick dead zone: " + str(round(deadzone_stick, 2))
            text_surf = font.render(text, False, (200, 200, 200))
            
            screen.blit(text_surf, (slider_pos_start[0], +
                                    slider_pos_start[1] - 60))
        
        else:
            text = "No Device plugged in."
            text_surf = font.render(text, False, (200, 200, 200))
            screen.blit(text_surf, (120, 16))
    
        pg.display.update()
    
    pg.quit()
except Exception:
    traceback.print_exc()
    pg.quit()