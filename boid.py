import sys, pygame, random, math #ukljucivanje potrebnih biblioteka neophodnih za realizaciju boids algoritma

pygame.init() #inicijalizacija svih uvezenih biblioteka

size = width, height = 800, 600 #velicina prozora
black = 0, 0, 0 #boja pozadine prozora

maxVelocity = 5 #brzina kretanja boida
numBoids = 20 #broj boida
boids = []

class Boid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocityX = random.randint(1, 10) / 10.0
        self.velocityY = random.randint(1, 10) / 10.0

    "Ova funkcija vraca udaljenost izmedju dva boida"
    def distance(self, boid):
        distX = self.x - boid.x
        distY = self.y - boid.y        
        return math.sqrt(distX * distX + distY * distY)

    "Ova funkcija omogucava da se boid priblizi skupu boida"
    def moveCloser(self, boids):
        if len(boids) < 1: return
            
        # racunanje prosecne udaljenosti od ostalih boida
        avgX = 0
        avgY = 0
        for boid in boids:
            if boid.x == self.x and boid.y == self.y:
                continue
                
            avgX += (self.x - boid.x)
            avgY += (self.y - boid.y)

        avgX /= len(boids)
        avgY /= len(boids)

        # postavlja brzinu boida u odnosu na ostale boide
        distance = math.sqrt((avgX * avgX) + (avgY * avgY)) * -1.0
       
        self.velocityX -= (avgX / 100) 
        self.velocityY -= (avgY / 100) 
        
    "Ova funkcija omogucava kretanje jednog boida sa skupom boida"
    def moveWith(self, boids):
        if len(boids) < 1: return
        # racunanje prosecne brzine ostalih boida
        avgX = 0
        avgY = 0
                
        for boid in boids:
            avgX += boid.velocityX
            avgY += boid.velocityY

        avgX /= len(boids)
        avgY /= len(boids)

        # postavljanje brzine boida u odnosu na ostale boide
        self.velocityX += (avgX / 40)
        self.velocityY += (avgY / 40)
    
    "Ovom funkcijom se postize da se boid odmakne od skupa boida da bi se izbegla guzva"
    def moveAway(self, boids, minDistance):
        if len(boids) < 1: return
        
        distanceX = 0
        distanceY = 0
        numClose = 0

        for boid in boids:
            distance = self.distance(boid)
            if  distance < minDistance:
                numClose += 1
                xdiff = (self.x - boid.x) 
                ydiff = (self.y - boid.y) 
                
                if xdiff >= 0: xdiff = math.sqrt(minDistance) - xdiff
                elif xdiff < 0: xdiff = -math.sqrt(minDistance) - xdiff
                
                if ydiff >= 0: ydiff = math.sqrt(minDistance) - ydiff
                elif ydiff < 0: ydiff = -math.sqrt(minDistance) - ydiff

                distanceX += xdiff 
                distanceY += ydiff 
        
        if numClose == 0:
            return
            
        self.velocityX -= distanceX / 10
        self.velocityY -= distanceY / 10
        
    "Ova funkcija pomera boid na osnovu njegove brzine"
    def move(self):
        if abs(self.velocityX) > maxVelocity or abs(self.velocityY) > maxVelocity:
            scaleFactor = maxVelocity / max(abs(self.velocityX), abs(self.velocityY))
            self.velocityX *= scaleFactor
            self.velocityY *= scaleFactor
        
        self.x += self.velocityX
        self.y += self.velocityY

screen = pygame.display.set_mode(size)

ball = pygame.image.load("ball.png")
ballrect = ball.get_rect()

# postavljanje boida na slucajne polozaje
for i in range(numBoids):
    boids.append(Boid(random.randint(0, width), random.randint(0, height)))   

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    for boid in boids:
        closeBoids = []
        for otherBoid in boids:
            if otherBoid == boid: continue
            distance = boid.distance(otherBoid)
            if distance < 100:
                closeBoids.append(otherBoid)

        
        boid.moveCloser(closeBoids)
        boid.moveWith(closeBoids)  
        boid.moveAway(closeBoids, 20)  

        # osiguravanje da boidi ostanu u granicama ekrana
        # i ukoliko se predje granica dolazi do smanjenja brzine boida
        border = 25
        if boid.x < border and boid.velocityX < 0:
            boid.velocityX = -boid.velocityX * random.random()
        if boid.x > width - border and boid.velocityX > 0:
            boid.velocityX = -boid.velocityX * random.random()
        if boid.y < border and boid.velocityY < 0:
            boid.velocityY = -boid.velocityY * random.random()
        if boid.y > height - border and boid.velocityY > 0:
            boid.velocityY = -boid.velocityY * random.random()
            
        boid.move()
        
    screen.fill(black)
    for boid in boids:
        boidRect = pygame.Rect(ballrect)
        boidRect.x = boid.x
        boidRect.y = boid.y
        screen.blit(ball, boidRect)
    pygame.display.flip()
    pygame.time.delay(10)
