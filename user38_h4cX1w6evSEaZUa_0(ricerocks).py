# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 0
time = 0.5
count = 0


class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.s2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


    


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def inc_angular_velocity(self, vel):
        self.angle_vel += vel
    
    def dec_angular_velocity(self, vel):
        self.angle_vel -= vel    
        
    def is_thrust(self, thrust):
        self.thrust = thrust
        if self.thrust:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()
        
        
    def shoot(self):
        global a_missile, missile_group, forward
        forward_shot = angle_to_vector(self.angle)
        
        pos = [self.pos[0] + 45 * forward_shot[0] , self.pos[1] + 45 * forward_shot[1]]
        vel = [self.vel[0] + 10 * forward_shot[0],self.vel[1] +  10 *forward_shot[1]]
        a_missile = Sprite(pos, vel, self.angle, 0, missile_image, missile_info, missile_sound)
        
        missile_group.add(a_missile)
        
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size , self.pos,self.image_size,self.angle)
        if self.thrust:
                canvas.draw_image(ship_image,[135, 45],[90,90], self.pos,self.image_size,self.angle)
                
    def get_radius(self):
        return self.radius
    
    def get_position(self):
        return self.pos
        
    
            
    def update(self):
        
        self.vel[0] *= (1-0.125)
        self.vel[1] *= (1-0.125)
        
        
        # positional update
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        if  self.pos[0] > WIDTH or self.pos[0] < 0 :
            self.pos[0] =  self.pos[0] % WIDTH
        elif self.pos[1] > HEIGHT or self.pos[1] < 0:
            self.pos[1] = self.pos[1] % HEIGHT
        
        # Angular velocity update
        self.angle += self.angle_vel 
        forward = angle_to_vector(self.angle)
         
        if self.thrust:
            self.vel[0] += forward[0] 
            self.vel[1] += forward[1] 
            
        
    
    
        

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.age = self.age + 1
        
        
        
        self.angle += self.angle_vel  
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        if self.pos[0] > WIDTH or self.pos[0] < 0:
            self.pos[0] = self.pos[0] % WIDTH
            
        elif self.pos[1] > HEIGHT or self.pos[1] < 0:
            self.pos[1] = self.pos[1] % HEIGHT
            
        if self.age <= self.lifespan and self.lifespan:
            return False
        else:
            return True  
            
    def collide(self, another_object):
        d = dist(self.pos, another_object.get_position())
        if d <= self.radius + another_object.get_radius() :
            return True
        else:
            return False

       
    def get_radius(self):
        return self.radius
    
    def get_position(self):
        return self.pos
    
def group_collide(group, other_object):
           
       is_colliding	= False
       rs = set([])
       global count
       for element in group:
                if element.collide(other_object):
                    rs.add(element)
                    is_colliding = True
                   
       group.difference_update(rs)  
       if is_colliding:
                  return True
                    
       else:
                  return False
                    
def group_group_collide(group, other_group):
    collision = 0
    for sprite in set(group):
        if group_collide(other_group, sprite):
            group.discard(sprite)
            collision += 1
    return collision
             
                 
    
    
           
def draw(canvas):
    global time,lives,score
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.update()
    my_ship.draw(canvas)
    
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    
    
    # update ship and sprites
    
    #a_rock.update()
    
    
    canvas.draw_text('Lives = ' + str(lives), [50,40], 30, 'white', 'sans-serif')
    canvas.draw_text('Score = ' + str(score), [640,40], 30, 'white', 'sans-serif')
    
    if group_collide(rock_group, my_ship) and lives > 0:
        lives -= 1
    if lives == 0:
        soundtrack.play()
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], splash_info.get_size())
        
    score += group_group_collide(missile_group, rock_group) 
    
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [0, 0], 0, 0, asteroid_image, asteroid_info)    
rock_group = set([])
missile_group = set([])

# timer handler that spawns a rock    
def rock_spawner():
    if len(rock_group) < 13:
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        if dist(rock_pos, my_ship.pos) > my_ship.radius + 10:
            rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
            rock_avel = random.random() * .2 - .1
            a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)
            rock_group.add(a_rock)
                           
        if lives == 0:
         for rock in set(rock_group):
            rock_group.discard(rock)
                   

def process_sprite_group(group, canvas):
    for sprite in set(group):
        if sprite.update():
             group.remove(sprite)
        sprite.draw(canvas)        
    
def mouse_handler(pos):
    global score, lives
    score = 0
    lives = 3
    soundtrack.rewind()
    soundtrack.play()
    
    
    
         
#               
    
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two spritesframe.set_keydown_handler(key_handler)
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

a_missile = Sprite([WIDTH / 2 + ship_info.get_radius(), HEIGHT / 2 + ship_info.get_radius()], [0, 0], 0, 0, missile_image, missile_info, missile_sound)

def key_down(key):
            if key == simplegui.KEY_MAP['left']:
                my_ship.inc_angular_velocity(-0.05)
            if key == simplegui.KEY_MAP['right']:
                my_ship.inc_angular_velocity(0.05)
            if key == simplegui.KEY_MAP['up']:
                my_ship.is_thrust(True)
            if key == simplegui.KEY_MAP['space']:
                my_ship.shoot()
                
def key_up(key):
            if key == simplegui.KEY_MAP['left']:
                my_ship.dec_angular_velocity(-0.05)
            if key == simplegui.KEY_MAP['right']:
                my_ship.dec_angular_velocity(0.05)
            if key == simplegui.KEY_MAP['up']:
                my_ship.is_thrust(False)
                #ship_thrust_sound.rewind()

                     
                    
            
# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)
frame.set_mouseclick_handler(mouse_handler)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()

