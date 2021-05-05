#importing libraries
import time,os,random,math
import pygame
from pygame.locals import *
pygame.init()

#definingfunctions

def system():
	system=checkos()
	font = pygame.font.Font('freesansbold.ttf', 50) 
	text=font.render(system, True, (0,255,0),(0,0,0))
	text = pygame.transform.rotate(text, 270)
	textr=text.get_rect()
	c=(1400-textr.height)/2
	d=(700-textr.width)/2
	textr=textr.move([d,c])
	screen.blit(text,textr)
	pygame.display.update()
	time.sleep(3)
	return system

def checkos():
	mob=os.path.exists('/storage')
	if mob:
		return 'mobile'
	else:
		return 'pc'
	
def buildings(no):
	bg=pygame.image.load('buildings/building'+str(no)+'.jpg')
	bgr=bg.get_rect()
	c=(1400-bgr.height)/2
	bgr=bgr.move([0,c])
	screen.blit(bg,bgr)

def zoombuild(no):
	global c,d
	build=pygame.image.load('scope/building'+str(no)+'.jpg')
	buildr=build.get_rect()
	c=(1400-buildr.height)/2
	d=(700-buildr.width)/2
	buildr=buildr.move([c,d])
	screen.blit(build,buildr)
	return build,buildr
	
def gunfire(g):
	gf=pygame.image.load('gun/gun'+str(g)+'.png')
	gfr=gf.get_rect()
	return gf,gfr

def pregun(g,gf,gfr):
	c=(1500-gfr.height)/2
	gfr=gfr.move([0,c])
	screen.blit(gf,gfr)
	if g<7:
		g+=1
	else:
		g=1
	return g
	
def gunscope():
	scope=pygame.image.load('gun/scope.png')
	scoper=scope.get_rect()
	c=(1400-scoper.height)/2
	mopo=[0,c]
	scoper=scoper.move(mopo)
	return scope,scoper
	
def medikit():
	#medikit
	b=pygame.image.load('enemy/medikit.png')
	br=b.get_rect()
	screen.blit(b,[0,0])
	return br
	
def hplus(hp,med):
	if hp<200:
		hp+=50
		med-=1
	return hp,med
	
def enemy(econd,enem,hp):
	if econd==0:
		enemy=pygame.image.load('enemy/enemy1.png')
		econd=1
	elif econd==1:
		enemy=pygame.image.load('enemy/enemy2.png')
		sound=pygame.mixer.Sound('enemy/gunsound.mp3')
		sound.play()
		t=random.randint(0,3)
		if t==1:
			hp-=10
		econd=0
	enemyr=enemy.get_rect()
	enemyr.center = (screct.w/2,screct.h/2+enem)
	screen.blit(enemy,enemyr)
	return econd,hp

def enemymove(econd,mopo,mop,enem,hp,build,buildr):
	if econd==0:
		enemy=pygame.image.load('enemy/zoomedenemy1.png')
		econd=1
	elif econd==1:
		enemy=pygame.image.load('enemy/zoomedenemy2.png')
		sound=pygame.mixer.Sound('enemy/gunsound.mp3')
		sound.play()
		t=random.randint(0,3)
		if t==1:
			hp-=10
		econd=0
	enemyr=enemy.get_rect()
	enemyr.center = (screct.w/2-50,screct.h/2+enem*2)
	mopo=[mopo[0]+mop[0],mopo[1]+mop[1]]
	#screenlimit
	if mopo[0]<-325 and mop[0]<0:
		mopo[0]=-325
	if mopo[0]>325 and mop[0]>0:
		mopo[0]=325
	if mopo[1]>690 and mop[1]>0:
		mopo[1]=690
	if mopo[1]<-690 and mop[1]<0:
		mopo[1]=-690
	enemyr=enemyr.move(mopo)
	font = pygame.font.Font('freesansbold.ttf', 50)
	text=font.render(str(mopo), True, (200,0,0))
	text = pygame.transform.rotate(text, 270)
	textr=text.get_rect()
	textr.center=[screct.w/2,screct.h/2]
	buildr=buildr.move(mopo)
	screen.blit(build,buildr)
	screen.blit(enemy,enemyr)
	#screen.blit(text,textr)
	return econd,mopo,hp
	
def blood(n):
	for i in range(n):
		blo=pygame.image.load('blood/blood'+str(i+1)+'.png')
		blor=blo.get_rect()
		blor=blor.move([screct.w/2-225,screct.h/2-70])
		screen.blit(blo,blor)
			
def spl():
	spl=pygame.image.load('gun/gun.png')
	splr=spl.get_rect()
	c=(1800-splr.height)/2
	splr=splr.move([-100,c])
	screen.blit(spl,splr)

def health(hp):
	h=pygame.Rect((25, 500), (20,hp))
	screen.fill((255,255,255),h)

def restart(font):
	screen.fill((0,0,0))
	text=font.render('Restart', True, (200,0,0))
	text = pygame.transform.rotate(text, 270)
	textr=text.get_rect()
	textr.center=[screct.w/2,screct.h/2]
	screen.blit(text,textr)
	pygame.display.update()
	time.sleep(2)
	rungame()
	
def rungame():
	#gametime
	clock=pygame.time.Clock()
	#framerate
	fps=30
	#playercondition
	playeralive=True
	#enemycondition
	enemykill=False
	#buildingimageno.
	no=0
	#animationimageno.
	a=1
	#touchcondition
	touched=False
	#gunimageno.
	g=1
	#recoilofgun
	recoil=-100
	#looptime
	tim=-1
	#handscopecondition
	sco=0
	#scopeopeningcondition
	j=7
	#enemycondition
	econd=0
	#enemyposition
	enem=random.randint(-3,3)
	#healthofplayer
	hp=250
	#representingmedikit
	br=medikit()
	med=5
	while 1:
		touch=False
		#playercondition
		if playeralive:
			#eventloop
			for event in pygame.event.get():
				if event.type == MOUSEBUTTONDOWN:
					if br.collidepoint(event.pos):
						if med>0:
							hp,med=hplus(hp,med)
					elif tim == -1:
						touch=True
						sco=1
						
				if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
					enemykill=True
			screen.fill((0,0,0))
			if no<=4:
				buildings(no)
				econd,hp=enemy(econd,enem,hp)
			else:
				screen.fill((0,0,0))
				font = pygame.font.Font('freesansbold.ttf', 50)
				text=font.render('YOU WIN', True, (200,0,0))
				text = pygame.transform.rotate(text, 270)
				textr=text.get_rect()
				textr.center=[screct.w/2,screct.h/2]
				screen.blit(text,textr)
				pygame.display.update()
				time.sleep(3)
				restart(font)
			if enemykill:
				no+=1
				enemykill=False
			if sco==0:
				spl()
			if touch:
				tim=0
				touch=False
			for i in range(7):
				if g<=7 and tim==i:
					gf,gfr=gunfire(g)
					g=pregun(g,gf,gfr)
			#scopefunction
			if tim==7:
				mop=(0,0)
				touched=True
				build,buildr=zoombuild(no)
				buildr=buildr.move((350,-350))
				scope,scoper=gunscope()
				while touched:
					for event in pygame.event.get():
						if event.type == MOUSEBUTTONDOWN:
							mopo=pygame.mouse.get_rel()
						if event.type == MOUSEBUTTONUP:
							fire=pygame.mixer.Sound('sounds/kar98sound.mp3')
							fire.play()
							touched =False
					if touched:
						mopo=pygame.mouse.get_rel()
						screen.fill((0,0,0))
						mopo=[-mopo[0]*3,-mopo[1]*3]
						econd,mop,hp=enemymove(econd,mopo,mop,enem,hp,build,buildr)
						screen.blit(scope,scoper)
						if hp>0:
							health(hp)
						else:
							playeralive=False
							break
						pygame.display.update()
						clock.tick(12)
						pygame.display.flip()
				else:
					screen.fill((0,0,0))
					buildr=buildr.move((recoil,0))
					mopo=(recoil,0)
					econd,mop,hp=enemymove(econd,mopo,mop,enem,hp,build,buildr)
					if 81>mop[1]+(enem*2)>-36 and -335 <mop[0]<65:
						if mop[0]<-274:
							blood(7)
							enem=random.randint(-3,3)*100
							font = pygame.font.Font('freesansbold.ttf', 50) 
							text=font.render('1100', True, (200,0,0))
							text = pygame.transform.rotate(text, 270)
							textr=text.get_rect()
							textr=textr.move([100,700])
							screen.blit(text,textr)
							blo=pygame.image.load('blood/headshot.png')
							blor=blo.get_rect()
							blor=blor.move([screct.w/2,screct.h/2-40])
							screen.blit(blo,blor)
							
						elif mop[0]>-274:
							blood(4)
							enem=random.randint(-3,3)*100
							font = pygame.font.Font('freesansbold.ttf', 50) 
							text=font.render(' 500', True, (0,255,0))
							text = pygame.transform.rotate(text, 270)
							textr=text.get_rect()
							textr=textr.move([300,700])
							screen.blit(text,textr)
							blo=pygame.image.load('blood/bodyshot.png')
							blor=blo.get_rect()
							blor=blor.move([screct.w/2,screct.h/2-40])
							screen.blit(blo,blor)
						enemykill=True
					screen.blit(scope,scoper)
					clock.tick(3)
						
			for i in range(7):
				if j>0 and tim==8+i:
					gf,gfr=gunfire(j)
					pregun(j,gf,gfr)
					j-=1
			if -1< tim <14:
				tim+=1
			if tim==9:
				clock.tick(1)
			elif tim==14:
				tim=-1
				sco=0
				j=7
			if hp>0:
				health(hp)
			else:
				playeralive=False
			br=medikit()
			font = pygame.font.Font('freesansbold.ttf', 40) 
			text=font.render(str(med)+'         '+str(hp), True, (255,255,255))
			text = pygame.transform.rotate(text, 270)
			textr=text.get_rect()
			textr=textr.move([20,300])
			screen.blit(text,textr)
			pygame.display.update()
			clock.tick(fps)
			pygame.display.flip()
		else:
			screen.fill((0,0,0))
			font = pygame.font.Font('freesansbold.ttf', 50)
			text=font.render('GAME OVER', True, (200,0,0))
			text = pygame.transform.rotate(text, 270)
			textr=text.get_rect()
			textr.center=[screct.w/2,screct.h/2]
			screen.blit(text,textr)
			pygame.display.update()
			time.sleep(3)
			screen.fill((0,0,0))
			text=font.render('Restart', True, (200,0,0))
			text = pygame.transform.rotate(text, 270)
			textr=text.get_rect()
			textr.center=[screct.w/2,screct.h/2]
			screen.blit(text,textr)
			pygame.display.update()
			time.sleep(2)
			restart(font)

#----main----#
#screeninitiating
screen=pygame.display.set_mode((720,1372),pygame.FULLSCREEN | pygame.SCALED)
screct=screen.get_rect()
#systemchecking
system=system()
rungame()
pygame.quit()
	
	