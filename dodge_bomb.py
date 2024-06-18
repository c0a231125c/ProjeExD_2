import os
import sys
import pygame as pg
import random

WIDTH, HEIGHT = 1600, 900
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue，画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right: #横方向判定
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom: #縦方向判定
        tate = False
    return yoko, tate

def direction(move):
            return kk_direction[move]

kk_direction = {(-5, 0):pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2),
                     (-5, 5):pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 2),
                     (0, 5):pg.transform.rotozoom(pg.image.load("fig/3.png"), 90, 2),
                     (5, 5):pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 2),
                     (5, 0):pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2),
                     (5, -5):pg.transform.rotozoom(pg.image.load("fig/3.png"), -45, 2),
                     (0, -5):pg.transform.rotozoom(pg.image.load("fig/3.png"), 270, 2),
                     (-5, -5):pg.transform.rotozoom(pg.image.load("fig/3.png"), 315, 2),
                     (0, 0):pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2)}

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bomb_x = random.uniform(0, WIDTH)
    bomb_y = random.uniform(0, HEIGHT)
    vx = 5
    vy = 5
    bomb = pg.Surface((20, 20))
    pg.draw.circle(bomb, (255, 0, 0), (10, 10), 10)
    bomb.set_colorkey((0, 0, 0))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bomb_rct = bomb.get_rect()
    bomb_rct.center = bomb_x, bomb_y

    clock = pg.time.Clock()
    tmr = 0

    move = {pg.K_UP:(0, -5), pg.K_DOWN:(0, 5), pg.K_LEFT:(-5, 0), pg.K_RIGHT:(5, 0)}

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])
        
        
        key_lst = pg.key.get_pressed()        
        sum_mv = [0, 0]
        for key in move:
            if key_lst[key]:
                tpl = move[key]
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)
        check_kk = check_bound(kk_rct)
        if check_kk[0] == False or check_kk[1] == False:
            sum_mv[0] =- sum_mv[0]
            sum_mv[1] =- sum_mv[1] 
            kk_rct.move_ip(sum_mv)

        
        if sum_mv == [0, -5] or sum_mv == [0, 5] or sum_mv == [5, 0] or sum_mv == [5, 5] or sum_mv == [5, -5]:
            kk_img = direction(tuple(sum_mv))
            kk_img = pg.transform.flip(kk_img, True, False)
        else:
            kk_img = direction(tuple(sum_mv))
        screen.blit(kk_img, kk_rct)

        


        bomb_rct.move_ip(vx, vy)
        check_bomb = check_bound(bomb_rct)
        if check_bomb[0] == False:
            vx *= -1
            bomb_rct.move_ip(vx, 0)
        if check_bomb[1] == False:
            vy *= -1
            bomb_rct.move_ip(0, vy)
        screen.blit(bomb, bomb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)

        if kk_rct.colliderect(bomb_rct):
            break



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
