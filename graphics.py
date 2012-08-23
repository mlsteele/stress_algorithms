# python2.7

import pygame, sys, time, numpy, itertools
from numpy import pi, sin, cos

""" Graphics Setup """
gsize = ((200, 400), (500, 250), (1024, 768))[0]
#os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)
screen = pygame.display.set_mode(gsize)
pd = pygame.draw
pygame.display.set_caption("Stress")
screen.fill((255, 255, 255))
# pygame.mouse.set_visible(False)
pygame.font.init()
font = pygame.font.Font(None, 21)

def text(txt, **kwargs):
  text = font.render(txt, False, (0,0,0))
  textpos = text.get_rect(**kwargs)
  screen.blit(text, textpos)
  
def kill():
  pygame.quit(); sys.exit()

def handle_events():
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      kill()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        kill()

def render(txt=""):
  screen.fill((255, 255, 255))
  # pd.circle(screen, (0,0,0), (50, 50), 10)
  txt = reduce(lambda a,b: a + b, map(lambda s: s.split("],"), txt.split("\n")), []) 
  for txt, h in zip(txt, map(lambda x: x * 30, xrange(len(txt)))):
    text(txt, topleft=(0, h))
  pygame.display.flip()
