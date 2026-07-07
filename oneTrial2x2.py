import pygame
import sys
import math
import time
from subprocess import Popen, PIPE
import random


pygame.init()
pygame.font.init()
screenWidth = 800
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Skinner Box (2x2)")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 22)


# creating 2x2 grid
rectWidth = 600
rectHeight = 400
rectX = (screenWidth - rectWidth) // 2
rectY = (screenHeight - rectHeight) // 2
halfWidth = rectWidth // 2
halfHeight = rectHeight // 2

# finding center of each tile for mouse
topLeftCenter = (
    rectX + halfWidth // 2,
    rectY + halfHeight // 2
)
topRightCenter = (
    rectX + halfWidth + halfWidth // 2,
    rectY + halfHeight // 2
)
bottomLeftCenter = (
    rectX + halfWidth // 2,
    rectY + halfHeight + halfHeight // 2
)
bottomRightCenter = (
    rectX + halfWidth + halfWidth // 2,
    rectY + halfHeight + halfHeight // 2
)

# lever inside bottom-right tile against the east (right) wall
leverWidth = 60
leverLength = 120
leverX = rectX + rectWidth - leverWidth
leverY = rectY + halfHeight + (halfHeight - leverLength) // 2
lever = pygame.Rect(leverX, leverY, leverWidth, leverLength)

# loc 1 = top-left chamber
# loc 2 = top-right chamber
# loc 3 = bottom-left chamber
# loc 4 = bottom-right chamber
# Direction angles: N=270, E=0, S=90, W=180  (pygame y-axis is flipped)
locationPixels = {
    1: topLeftCenter,
    2: topRightCenter,
    3: bottomLeftCenter,
    4: bottomRightCenter,
}
directionAngles = {
    1: 0,
    2: 90,
    3: 180,
    4: 270
}
directions  = {1: "N",   2: "E",  3: "S",  4: "W"}

# Which (loc, direction) pairs let  mouse cross into an adjacent tile, which chamber it lands in
transitions = {
    (1, 2): 2,  # top-left moving E -> top-right
    (2, 4): 1,  # top-right moving W -> top-left
    (3, 2): 4,  # bottom-left moving E -> bottom-right
    (4, 4): 3,  # bottom-right moving W -> bottom-left
    (1, 3): 3,  # top-left moving S -> bottom-left
    (3, 1): 1,  # bottom-left moving N -> top-left
    (2, 3): 4,  # top-right moving S -> bottom-right
    (4, 1): 2,  # bottom-right moving N -> top-right
}

mouseSize  = 15
delay  = 0.25   # seconds between steps (lower = faster replay)

white  = (255, 255, 255)
black  = (0,   0,   0)
red    = (200, 50,  50)
green  = (50,  180, 50)
yellow = (240, 200, 0)
grey   = (180, 180, 180)
blue   = (50,  100, 220)

def trianglePoints(center, angle_deg):
    cx, cy = center
    pts = []

    for i in [0, 120, 240]:
        rad = math.radians(angle_deg + i - 90)
        dist = 40 if i == 0 else 40 / 1.5
        pts.append((
            cx + dist * math.cos(rad),
            cy + dist * math.sin(rad)
        ))

    return pts


def drawFrame(loc, direction, trial_idx, step, hit):

    screen.fill(white)

    # kkinner box outer border
    pygame.draw.rect(screen, black, (rectX, rectY, rectWidth, rectHeight), 3)

    # line down the middle & one line across to make the grid
    pygame.draw.line(screen, black,
                      (rectX + halfWidth, rectY),
                      (rectX + halfWidth, rectY + rectHeight), 3)
    pygame.draw.line(screen, black,
                      (rectX, rectY + halfHeight),
                      (rectX + rectWidth, rectY + halfHeight), 3)

    # lever
    leverColor = yellow if hit else red
    pygame.draw.rect(screen, leverColor, (leverX, leverY, leverWidth, leverLength))

    # mouse
    center = locationPixels[loc]
    pts = trianglePoints(center, directionAngles[direction])
    pygame.draw.polygon(screen, green, pts)

    # displays trial number & number of steps in top left corner
    label = font.render(f"Trial {trial_idx + 1}    Step {step}", True, black)
    screen.blit(label, (10, 10))

    pygame.display.flip()

# the skip doesn't totally work i dont think ._.
def eventKeys():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return 'quit'
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_q, pygame.K_ESCAPE):
                return 'quit'
            if event.key == pygame.K_n:
                return 'skip'
    return 'ok'

# iterate thru one trial at a time
def runTrial(trial_idx, loc, direction, pid):

    reached = False
    steps = 0

    for j in range(50):
        drawFrame(loc, direction, trial_idx, j, reached)

        clock.tick(60)
        time.sleep(delay)

        ev = eventKeys()
        if ev == 'quit':
            return j, False, 'quit'
        if ev == 'skip':
            return j, False, 'skip'

        pid.stdin.write((str(((loc - 1) * 4 + direction) % 11) + '/1\n').encode('utf-8'))
        x = pid.stdout.readline()

        if x[0:1] == b'1':
            direction -= 1
            if direction == 0:
                direction = 4
        elif x[0:1] == b'2':
            direction += 1
            if direction > 4:
                direction = 1
        elif x[0:1] == b'3':
            loc = transitions.get((loc, direction), loc)
        elif x[0:1] == b'4':
            if loc == 4 and direction == 2:
                # lever pressed, send reward signal
                pid.stdin.write(b"9/1\n")
                pid.stdout.readline()
                reached = True
                steps = j + 1

                # flash lever pressed state
                for _ in range(20):
                    drawFrame(loc, direction, trial_idx, steps, reached)
                    clock.tick(60)
                    ev = eventKeys()
                    if ev == 'quit':
                        return steps, True, 'quit'
                    if ev == 'skip':
                        return steps, True, 'skip'
                break

        steps = j + 1

    return steps, reached, 'ok'


def main():
    random.seed()
    numTrials = 300

    pid = Popen(["/Users/lenas/Desktop/ca", "/Users/lenas/Desktop/STAR Scholars/skinnerVision.cfg"], stdin=PIPE, stdout=PIPE, bufsize=0)

    print(f"{'Trial':>6}  {'Steps':>6}  {'Reached?'}")
    print("-" * 30)

    for i in range(numTrials):
        loc = random.choice([1, 2, 3, 4])
        d   = random.random()
        if   d > 0.75: direction = 1
        elif d > 0.50: direction = 2
        elif d > 0.25: direction = 3
        else:          direction = 4

        steps, reached, signal = runTrial(i, loc, direction, pid)

        pid.stdin.write(b"0/1\n")
        pid.stdout.readline()

        print(f"{i + 1:>6}  {steps:>6}  {'YES' if reached else 'no'}")

        if signal == 'quit':
            break
        # 'skip' or 'ok' both just continue to the next trial immediately --> need to fix this so that skip actually skips the trial and goes to the next one

    pid.terminate()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()