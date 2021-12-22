ENEMY_ROW = 5
ENEMY_COL = 8

MAX_PLAYER_BULLETS = 5
ADDED_BULLETS = 2

sprites = loadImage(sketchPath('Sprites/SpaceInvaders.png'))
# cut the ship sprite
spaceship = sprites.get(68,4,9,10)
# resize
spaceship.resize(18, 20)

class Game:
    def __init__(self):
        self.level = 1
        self.win = False
        self.score = 0
        self.aliens = []
        self.life = spaceship
        
    def start(self):
        self.player = Player()
        self.bg = Background()
        self.alien_bullet = Bullet(-1, -1, 'enemy')
        self.button = Button(width/2-50, height/2+20, 100, 40)
        self.gameOver = False
        self.pickups = []
        for i in range(ENEMY_ROW):
                self.aliens.append([])
                for j in range(ENEMY_COL):
                    self.aliens[i].append(Alien(i, j))
    
    def change_level(self):
        self.level = self.level + 1
        if(self.level == 5):
            self.gameOver = True
            # add a function to show that player has beaten the game
            # self.won()
        self.load_level(self.level)
    
    def load_level(self, level_number):
        if(level_number == 1):
            for i in range(ENEMY_ROW):
                self.aliens.append([])
                for j in range(ENEMY_COL):
                    self.aliens[i][j].clear_attributes(i, j)
        elif(level_number == 2):
            for i in range(ENEMY_ROW):
                for j in range(ENEMY_COL):
                    self.aliens[i][j].clear_attributes(i, j)
                    self.aliens[i][j].alive = True
                    self.aliens[i][j].speed = 0.5
                    self.aliens[i][j].dropPickups = True
    
    # check collision with enemy bullet
    def player_collision(self, object):
        rectOneRight = self.player.pos[0] + self.player.sprite.width
        rectOneLeft = self.player.pos[0]
        rectOneTop = self.player.pos[1]
        rectOneBottom = self.player.pos[1] + self.player.sprite.height
        
        rectTwoRight = object.pos[0] + object.sprite.width
        rectTwoLeft = object.pos[0]
        rectTwoTop = object.pos[1]
        rectTwoBottom = object.pos[1] + object.sprite.height
        
        if rectOneRight > rectTwoLeft and rectOneLeft < rectTwoRight and rectOneBottom > rectTwoTop and rectOneTop < rectTwoBottom:
            if object.type == 'enemy':    
                # if collided, remove the bullet and destroy ship
                object.pos = [-1, -1]
                self.player.hit()
            elif object.type == 'shield':
                # add health
                if(self.player.health < 3):
                    self.player.health += 1
                self.pickups.remove(object)
            elif object.type == 'laser':
                self.pickups.remove(object)
                self.player.laser = True
        
    # shoot a bullet from random alien
    def alien_shoot(self):
        if self.alien_bullet.pos[1] < height and self.alien_bullet.pos[1] > 0:
            return
        alive = []
        for row in self.aliens:
            for alien in row:
                if alien.alive:
                    alive.append(alien)
        if len(alive) == 0:
            self.change_level()
        else:
            alien = alive[int(random(len(alive)))]
            self.alien_bullet.pos = [alien.pos[0] + alien.sprites[0].width/2+1, alien.pos[1] + alien.sprites[0].height]
        
    # check alien collisions with bullet
    def alien_collision(self, bullets):
        for row in self.aliens:
            for alien in row:
                if alien.alive:
                    for bullet in bullets:
                        if bullet.pos[1] <= 0:
                            self.player.shots.remove(bullet)
                            self.player.bullet += 1
                            break
                        pickup = alien.collision(bullet)
                        if(pickup == True):
                            self.player.shots.remove(bullet)
                            self.player.bullet += 1
                        elif(pickup != None):
                            return pickup
        return None
        
    # check if aliens have reached the player or all players dead
    def check_gameover(self):
        for row in self.aliens:
            for alien in row:
                if alien.alive and alien.pos[1] >= 2*height/3:
                    self.player.destroy()
                    self.gameOver = True
    
    def update_aliens(self):
        onedge = False
        # move aliens
        for row in self.aliens:
            for alien in row:        
                # check if all aliens can move
                if alien.alive and not alien.can_move(alien.dir):
                        onedge = True                
        for row in self.aliens:
            for alien in row:
                # move if possible
                if not onedge:
                    alien.move(alien.dir)
                # else, move down and change direction
                else:
                    alien.dir *= -1
                    alien.move_down()
                                    
    def update(self):
        # clear screen
        fill(0x11000000)
        rect(0, 0, width, height)
        
        # check collisions
        self.player_collision(self.alien_bullet)
        pickup = self.alien_collision(self.player.shots)
        
        if pickup != None:
            self.pickups.append(pickup)
              
        if len(self.pickups) > 0:
            for pickup in self.pickups:
                pickup.update()
                self.player_collision(pickup)
                if pickup.pos[1] == height:
                    self.pickups.remove(pickup)    
        
        if self.player.alive:
            # update player
            self.player.update()
            # update aliens
            self.update_aliens()
            # check whether game is over
            self.check_gameover()
            # shoot alien bullet
            self.alien_shoot()
            # update bullet
            self.alien_bullet.update()
            
    def show_gameover(self):
        textFont(font, 24)
        fill(154, 217, 65)
        textAlign(CENTER)
        text("Game Over", width/2, height/2);
        self.button.draw(self.button.in_bounds(mouseX, mouseY))     
        
    def draw(self):
        # draw objects
        self.bg.draw()
        self.player.draw()
        self.alien_bullet.draw()
        for row in self.aliens:
            for alien in row:
                if alien.alive:
                    alien.draw()
        
        if len(self.pickups) > 0:
            for pickup in self.pickups:
                pickup.draw() 
        
        # draw ui
        textFont(font, 12)
        fill(154, 217, 65)
        s = "Score: " + str(self.score)
        textAlign(LEFT)
        text(s, 16, 32);
        l = "Level: " + str(game.level)
        textAlign(RIGHT)
        text(l, width - 16 , 32);
        
        spacing = self.life.width + 10
        for l in range(self.player.health):
            image(self.life, width/2 + 20 - spacing * (2-l) , 20)
        
        b = "Bullets: " + str(self.player.bullet)
        print(str(len(self.player.shots)) + " " + str(self.player.bullet))
        textAlign(RIGHT)
        text(b, width - 16 , 64);
    
# class for displaying the background
class Background:
     
    def __init__(self):
        # load the images
        self.stars = loadImage(sketchPath('Sprites/SpaceInvaders_Background.png'))
        self.floor = loadImage(sketchPath('Sprites/SpaceInvaders_BackgroundFloor.png'))
        self.building = loadImage(sketchPath('Sprites/SpaceInvaders_BackgroundBuildings.png'))
        pass
    
    
    def draw(self):
        # draw the background
        self.fill_screen(self.stars, 0)
        self.fill_screen(self.floor, 2*height/3)
        self.draw_strip(self.building, 2*height/3 - self.stars.height)
        pass
        
    
    def fill_screen(self, img, y):
        # fill the screen with img starting from a given y coordinate
        while y < height:
            self.draw_strip(img, y)
            y += img.height
            
        
    def draw_strip(self, img, y):
        # fill a row with img at y coordinate
        x = 0
        while x < width:
            image(img, x, y)
            x += img.width
    

# class for the Player Spaceship
class Player:
    
    def __init__(self):
        # load the image
        # print(sketchPath('Sprites/SpaceInvaders.png'))
        self.sprite = spaceship
        # set starting position
        self.pos = (width/2 - self.sprite.width/2, 2*height/3 + 32)
        self.shots = []
        # set health
        self.health = 3
        # set speed
        self.speed = 2
        self.bullet = 0
        # set direction
        self.isLeft = 0
        self.isRight = 0
        # additional booleans
        self.alive = True
        self.laser = False
        
    # set the direction of movement
    def setMove(self, code, val):
        if code == LEFT:
            self.isLeft = val
        elif code == RIGHT:
            self.isRight = val
            
    def update(self):
        if self.laser:
            self.laser = False
            if self.bullet <= MAX_PLAYER_BULLETS:
                self.bullet += ADDED_BULLETS
        
        if(len(self.shots)>0):
            for shot in self.shots:
                shot.update()
            
        self.move()
    
    # move the player
    def move(self):
        dir = (self.isRight - self.isLeft) * self.speed
        # check if in bounds
        if self.pos[0] + dir > width - self.sprite.width:
            return
        if self.pos[0] + dir < 0:
            return
        self.pos = (self.pos[0] + dir, self.pos[1])
    
    
    def shoot(self):
        # if player is alive
        if self.alive:        
            if self.bullet > 0:
                self.bullet -= 1
            elif(self.bullet == 0):
                self.bullet += 1
            
            if(len(self.shots)<self.bullet):
                shot = Bullet(self.pos[0], self.pos[1],'player')
                shot.speed = 5
                self.shots.append(shot)
            
    def draw(self):
        if self.alive:
            image(self.sprite, self.pos[0],self.pos[1])
        for shot in self.shots:
            shot.draw()
    
    # destroy the player
    def hit(self):
        self.health -= 1
        if self.health == 0:
            self.alive = False
            game.gameOver = True
    
    def destroy(self):
        self.alive = False
        game.gameOver = True
        
class Alien:
    def __init__(self, index, col):
        # set sprite size
        sprite_size = 24
        self.sprite_size = sprite_size
        # load the two frames of animation
        self.sprites = [sprites.get(0,16*index,16,16)]
        self.sprites.append(sprites.get(16,16*index,16,16))
        # resize the sprites
        self.sprites[0].resize(sprite_size, sprite_size)
        self.sprites[1].resize(sprite_size, sprite_size)
        self.clear_attributes(index, col)
        
    def clear_attributes(self, index, col):
        # set position
        y = 100 + self.sprite_size * index
        x = width/2 - 160 + self.sprite_size * col
        self.pos = (x, y)
        self.speed = 0.3
        self.alive = True
        self.dir = 1
        self.canmove =  True
        self.dropPickups = False   
                    
    def draw(self):
        # select frame of animation to draw
        frame = 1 if frameCount%60 > 30 else 0
        image(self.sprites[frame], self.pos[0],self.pos[1])    
        
    def can_move(self, dir):
        # check if movement is in screenbounds
        if self.pos[0] + dir > width - self.sprites[0].width:
            return False
        if self.pos[0] + dir < 0:
            return False
        return True

    # move the alien
    def move(self, dir):
        self.pos = (self.pos[0] + dir * self.speed, self.pos[1])
        
    # move the alien down one row
    def move_down(self):
        self.pos = (self.pos[0], self.pos[1] + self.sprite_size)
        self.speed += 0.1
        
    # check collision with bullet
    def collision(self, bullet):
        rectOneRight = self.pos[0] + self.sprites[0].width
        rectOneLeft = self.pos[0]
        rectOneTop = self.pos[1]
        rectOneBottom = self.pos[1] + self.sprites[0].height
        
        rectTwoRight = bullet.pos[0] + bullet.sprite.width
        rectTwoLeft = bullet.pos[0]
        rectTwoTop = bullet.pos[1]
        rectTwoBottom = bullet.pos[1] + bullet.sprite.height
        
        # if collided, remove the bullet and destroy alien
        if rectOneRight > rectTwoLeft and rectOneLeft < rectTwoRight and rectOneBottom > rectTwoTop and rectOneTop < rectTwoBottom:
            self.alive = False
            # increase score
            game.score += 20
            if self.dropPickups:
                ran = random(1)
                if (ran <= 0.25):
                    pickup = Pickups(self.pos[0], self.pos[1], "shield")
                    return pickup
                elif (ran > 0.25 and ran <= 0.5):
                    pickup = Pickups(self.pos[0], self.pos[1], "laser")
                    return pickup
            return True
        return None
 
class Pickups:
    def __init__(self, x, y, type):
        self.pos = [x, y]
        self.type = type
        self.speed = 2
        
        if self.type == "shield":
            self.sprite = sprites.get(48, 0, 16, 16)
            # resize
            self.sprite.resize(20, 20)
        elif self.type == "laser":
            self.sprite = sprites.get(32, 32, 16, 16)
            # resize
            self.sprite.resize(20, 20)
            
    def update(self):
        if self.pos[1] < height:
            self.pos[1] += self.speed
    
    def draw(self):
        image(self.sprite, self.pos[0], self.pos[1])
                                            
# class for the bullets
class Bullet:
    def __init__(self,x, y, type):
        self.type = type
        # select sprite based on either enemy or player
        if type == 'enemy':
            self.sprite = sprites.get(38,21,3,7)
            self.sprite.resize(5, 15)
            self.speed = 3
            self.dir = 1
        else:
            self.sprite = sprites.get(39,5,1,5)
            self.sprite.resize(2, 10)
            self.speed = 0
            self.dir = -1
            
        # set position
        self.pos = [x, y]    
        
    # move the bullet if it is on screen
    def update(self):
        if self.pos[1] < 0 or self.pos[1] > height:
            return
        self.pos = (self.pos[0], self.pos[1] + self.speed * self.dir)
               
    # draw the bullet if it is on screen
    def draw(self):
        if self.pos[1] < 0 or self.pos[1] > height:
            return
        image(self.sprite, self.pos[0],self.pos[1])


# class for the Restart Button
class Button:
    
    def __init__(self, x, y, w, h):        
        # store the x,y coordinates and width and height of the button
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def draw(self, hover):
        # if mouse is on button, use a darker color
        if hover:
            fill(96, 128, 87)
        else:
            fill(154, 217, 65)
        rect(self.x, self.y, self.w, self.h)
        fill(0xFFFFFFFF)
        textSize(12)
        text('RESTART', width/2, self.y + self.h/2 + 4)
        pass
    
    def in_bounds(self, x, y):
        # check if coordinates are inside button
        if not(x > self.x and x < self.x + self.w):
            return False
        if not(y > self.y and y < self.y + self.h):
            return False
        return True
   
# global variables
game = Game()
font = None

def setup():
    global font
    # initialize game window
    size(320, 600)
    noSmooth()
    noStroke()
    
    font = createFont("Retro Gaming.ttf", 32);

    game.start()
    # load level 1
    game.load_level(1)
    

def draw():
    if not game.gameOver:
        game.update()
        game.draw()
    else:
        game.show_gameover()        
            
def keyPressed():
    if key == ' ':
        game.player.shoot()
    else:        
        game.player.setMove(keyCode, 1)
  
def keyReleased():
    game.player.setMove(keyCode, 0)
        
def mousePressed():
    # mouse input
    global game
    if not game.player.alive or game.gameOver:
        if game.button.in_bounds(mouseX, mouseY):
            game = Game()
            game.start()
            game.load_level(1)
