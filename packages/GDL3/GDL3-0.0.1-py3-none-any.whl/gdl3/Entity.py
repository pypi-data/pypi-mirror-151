import pygame

class Entity:

    """
        __init__() method  - will take in
        the args:
            mandatory - x,y,width,height,img
            optional - vel
    """

    def __init__(self,x,y,width,height,img,vel=0):
        self.x,self.y,self.width,self.height = x,y,width,height
        self.vel = vel
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img,(self.width,self.height))
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)

    """
        draw function will 
        draw the img to
        the pygame window using pygames
        blit function
    """

    def draw(self, win):
        win.blit(self.img,(self.x,self.y))
    
    """
        will move the
        player using the arrow keys on
        the keyboard
    """
    
    def Move_arrow_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel
        
        if keys[pygame.K_DOWN]:
            self.y += self.vel
        
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)

    """
        will move the
        player using the w,s,a,d keys on
        the keyboard
    """
    def Move_with_wsad(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.x += self.vel

        if keys[pygame.K_a]:
            self.x -= self.vel

        if keys[pygame.K_w]:
            self.y -= self.vel
        
        if keys[pygame.K_s]:
            self.y += self.vel

        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)

    """
        will move the entity's x,y
        to a specific location 
        on the game window
    """
    def Move_towards(self,x,y, diagonal=True):
        if diagonal:
            if x > self.x:
                self.x += self.vel
            
            if x < self.x:
                self.x -= self.vel
            
            if y > self.y:
                self.y += self.vel
            
            if y < self.y:
                self.y -= self.vel

            self.rect = pygame.Rect(self.x,self.y,self.width,self.height)

        elif not diagonal:
            if x > self.x:
                self.x += self.vel
            
            elif x < self.x:
                self.x -= self.vel
            
            elif y > self.y:
                self.y += self.vel
            
            elif y < self.y:
                self.y -= self.vel
            
            self.rect = pygame.Rect(self.x,self.y,self.width,self.height)


    def draw_rect(self,win, borders=False):
        if not borders:
            pygame.draw.rect(win, "red", self.rect)
        else:
            pygame.draw.rect(win, "red", self.rect,2)

    def check_Collision(self,rect):
        if self.rect.colliderect(rect):
            return True
        
        return False
    
    """
        drawing text on the pygame window!
    """
    def draw_text(self,win,text,font,size,color):
        font = pygame.font.SysFont(font,size)
        txt = font.render(text,1,color)
        win.blit(txt,(self.x,self.y))
