import math

import pygame

pygame.init()

background_img = pygame.image.load('image/background_img.png')

cookie_img = pygame.image.load('image/cookie.png')

wooden_bar = pygame.image.load('image/wooden_bar.png')
upgrades_wooden_bar = pygame.image.load('image/upgrades_wooden_bar.png')
buildings_wooden_bar = pygame.image.load('image/buildings_wooden_bar.png')
building_display_background = pygame.image.load('image/building_display_background.png')
wooden_background = pygame.image.load('image/wooden_background.png')

cursor_img = pygame.image.load('image/cursor_img.png')
grandma_img = pygame.image.load('image/grandma_img.png')
farm_img = pygame.image.load('image/farm_img.png')
mine_img = pygame.image.load('image/mine_img.png')
factory_img = pygame.image.load('image/factory_img.png')
bank_img = pygame.image.load('image/bank_img.png')
temple_img = pygame.image.load('image/temple_img.png')
wizard_tower_img = pygame.image.load('image/wizard_tower_img.png')

cursor_icon = pygame.image.load('image/icons/cursor_icon.png')
grandma_icon = pygame.image.load('image/icons/grandma_icon.png')
farm_icon = pygame.image.load('image/icons/farm_icon.png')
mine_icon = pygame.image.load('image/icons/mine_icon.png')
factory_icon = pygame.image.load('image/icons/factory_icon.png')
bank_icon = pygame.image.load('image/icons/bank_icon.png')
temple_icon = pygame.image.load('image/icons/temple_icon.png')
wizard_tower_icon = pygame.image.load('image/icons/wizard_tower_icon.png')

upgrade_background_frame = pygame.image.load('image/upgrades/upgrade_background_frame.png')
cursor_upgrade_img = pygame.image.load('image/upgrades/cursor_upgrade_img_1.png')
grandma_upgrade_img = pygame.image.load('image/upgrades/grandma_upgrade_img_1.png')
farm_upgrade_img = pygame.image.load('image/upgrades/farm_upgrade_img_1.png')
mine_upgrade_img = pygame.image.load('image/upgrades/mine_upgrade_img_1.png')
factory_upgrade_img = pygame.image.load('image/upgrades/factory_upgrade_img_1.png')
bank_upgrade_img = pygame.image.load('image/upgrades/bank_upgrade_img_1.png')
temple_upgrade_img = pygame.image.load('image/upgrades/temple_upgrade_img_1.png')
wizard_tower_upgrade_img = pygame.image.load('image/upgrades/wizard_tower_upgrade_img_1.png')
mouse_upgrade_img = pygame.image.load('image/upgrades/mouse_upgrade_img_1.png')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (155, 155, 155)
LIGHT_GREEN = (0, 255, 0)
DARK_BLUE = (51, 90, 114)


class MainCookie:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = 250
        self.height = 250
        self.animation_state = 0

    def draw(self):
        if self.animation_state > 0:
            cookie_img_scaled = pygame.transform.scale(cookie_img, (int(0.9 * self.length), int(0.9 * self.height)))
            window.blit(cookie_img_scaled,
                        (cookie_img_scaled.get_rect(
                            center=(int(self.x + self.length / 2), int(self.y + self.height / 2)))))
            self.animation_state -= 1
        else:
            window.blit(cookie_img,
                        (cookie_img.get_rect(center=(int(self.x + self.length / 2), int(self.y + self.height / 2)))))

    def collidepoint(self, mouse_pos):
        return pygame.Rect(self.x, self.y, self.length, self.height).collidepoint(mouse_pos)


class ScoreDisplay():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = 100
        self.height = 100

    def draw(self):
        font = pygame.font.Font('Font/ChelseaMarket-Regular.ttf', 24)
        small_font = pygame.font.Font('Font/ChelseaMarket-Regular.ttf', 24)

        SCORE = font.render('{} cookies'.format(int(user.score)), True, WHITE)
        CPS = font.render('per second: {}'.format(int(user.cps)), True, WHITE)
        window.blit(SCORE,
                    (SCORE.get_rect(center=(int(self.x + self.length / 2), int(self.y + self.height / 2)))))
        window.blit(CPS,
                    (CPS.get_rect(center=(int(self.x + self.length / 2), int(self.y + self.height / 2) + 20))))


class Building:
    def __init__(self, name, x, y, image, icon, base_cost, increase_per_purchase, cps):
        self.base_cost = base_cost
        self.name = name
        self.x = x
        self.y = y
        self.length = 300
        self.height = 64

        self.image = image
        self.icon = icon  # да пзцд хули с тобой нахуй не так
        self.increase_per_purchase = increase_per_purchase
        self.cps = cps
        self.quantity = 0
        self.created = 0

    def collidepoint(self, mouse_pos):
        return pygame.Rect(self.x, self.y, self.length, self.height).collidepoint(mouse_pos)

    def getTotalCost(self):
        return self.base_cost * self.increase_per_purchase ** self.quantity

    def draw(self, solid=True):
        store_cost_font = pygame.font.Font('Font/ChelseaMarket-Regular.ttf', 17)
        store_quantity_font = pygame.font.Font('Font/ChelseaMarket-Regular.ttf', 36)

        icon = self.image
        cost = store_cost_font.render('{}'.format(format_number(int(self.getTotalCost()))), True, LIGHT_GREEN)
        quatity = store_quantity_font.render('{}'.format(self.quantity), True, GRAY)
        if not solid:  # типо не знаю, так можно или нет, кароч в душе не ебу
            icon.set_alpha(100)
        else:
            icon.set_alpha(225)
        window.blit(icon, (self.x, self.y))
        window.blit(cost, (self.x + 85, self.y + self.height - 30))
        window.blit(quatity, (self.x + self.length - 40, self.y + 10))

    def drawDisplayBox(self):
        building_font = pygame.font.Font('Font/ChelseaMarket-Regular.ttf', 20)
        building_title = building_font.render('{}'.format(self.name), True, WHITE)

        description_font = pygame.font.Font('Font/ChelseaMarket-Regular.ttf', 12)
        production = description_font.render('Each {} produces {:.1f} cookies per second'.format(self.name, self.cps),
                                             True, WHITE)
        quantity = description_font.render('You have {} {}s producing {:.1f} cookies per second'.format(self.quantity,
                                                                                                        self.name,
                                                                                                        self.cps *
                                                                                                        self.quantity),
                                           True, WHITE)
        created = description_font.render('{}s have created {} cookies so far'.format(self.name,
                                                                                      math.floor(self.created)),
                                          True, WHITE)

        x_pos = self.x - 380
        y_pos = pygame.mouse.get_pos()[1] - 72
        window.blit(building_display_background, (x_pos, y_pos))
        window.blit(self.icon, (x_pos + 3, y_pos + 3))
        window.blit(building_title, (x_pos + 43, y_pos + 3))

        space_between_lines = 16
        window.blit(production, (x_pos + 18, y_pos + 50))
        window.blit(quantity, (x_pos + 18, y_pos + 50 + space_between_lines))
        window.blit(created, (x_pos + 18, y_pos + 50 + space_between_lines * 2))

    def addUpgrade(self):
        I = 0
        II = 9
        if self.name == 'Cursor':
            if self.quantity == I:
                list_of_upgrades.append(Upgrade('Reinforced Index Finger I', cost=(self.getTotalCost() * 10),
                                                upgrade=self.name))
                list_of_upgrades.append(Upgrade('Double Click', cost=1000, upgrade='Mouse'))

            elif self.quantity == II:
                list_of_upgrades.append(Upgrade('Arthritis Prevention Cream', cost=self.getTotalCost() * 10,
                                                upgrade=self.name))
                list_of_upgrades.append(Upgrade('Double Click II', cost=2000, upgrade='Mouse'))
        elif self.name == 'Grandma':
            if self.quantity == I:
                list_of_upgrades.append(Upgrade('Forwards from Grandma', cost=self.getTotalCost() * 10,
                                                upgrade=self.name))
            elif self.quantity == II:
                list_of_upgrades.append(Upgrade('Steel-plated rolling pins', cost=self.getTotalCost() * 10,
                                                upgrade=self.name))


class Upgrade:
    def __init__(self, name, cost, upgrade):
        self.name = name
        self.cost = cost
        self.upgrade = upgrade
        self.x = 700
        self.y = 16

        self.length = 60
        self.height = 60

        if upgrade == 'Mouse':
            self.image = mouse_upgrade_img
        elif upgrade == 'Cursor':
            self.image = cursor_upgrade_img
        elif upgrade == 'Grandma':
            self.image = grandma_upgrade_img
        elif upgrade == 'Farm':
            self.image = farm_upgrade_img
        elif upgrade == 'Mine':
            self.image = mine_upgrade_img
        elif upgrade == 'Factory':
            self.image = factory_upgrade_img
        elif upgrade == 'Bank':
            self.image = bank_upgrade_img
        elif upgrade == 'Wizard Tower':
            self.image = wizard_tower_upgrade_img

    def collidepoint(self, mouse_pos):
        return pygame.Rect(self.x, self.y, self.length, self.height).collidepoint(mouse_pos)

    def draw(self, solid=True):
        icon = self.image
        frame = upgrade_background_frame
        if not solid:
            icon.set_alpha(100)
            frame.set_alpha(100)
        else:
            icon.set_alpha(255)
            frame.set_alpha(255)

        window.blit(frame, (self.x, self.y))
        window.blit(icon, (icon.get_rect(center=(int(self.x + self.length/2), int(self.y + self.height/2)))))

    def drawDisplayBox(self):
        upgrade_font = pygame.font.Font('Font/ChelseaMarket-Regular.ttf', 20)
        upgrade_title = upgrade_font.render('{}'.format(self.name), True, WHITE)

        cost_font = pygame.font.Font('Font/ChelseaMarket-Regular.ttf', 14)
        cost = cost_font.render('Cost: {}'.format(format_number(self.cost)), True, LIGHT_GREEN)

        description_font = pygame.font.Font('Font/ChelseaMarket-Regular.ttf', 14)
        description = description_font.render('{}s are twice as efficient.'.format(self.upgrade), True, WHITE)

        x_pos = 320
        y_pos = pygame.mouse.get_pos()[1] - 72
        if y_pos < 0:
            y_pos = 0

        window.blit(building_display_background, (x_pos, y_pos))
        window.blit(self.image, (x_pos + 3, y_pos + 3))
        window.blit(upgrade_title, (x_pos + 43, y_pos + 3))

        window.blit(cost, (x_pos + 10, y_pos + 50))

        space_between_lines = 16
        window.blit(description, (x_pos + 10, y_pos + 50 + space_between_lines))

    def upgradeBuilding(self, list_of_buildings):
        if self.upgrade == 'Mouse':
            user.click_multiplier *= 2
        elif self.upgrade == 'Cursor':
            cursor.cps *= 2
        elif self.upgrade == 'Grandma':
            grandma.cps *= 2


class Player:
    def __init__(self):
        self.score = 0
        self.click_multiplier = 1
        self.cps = 0

    def updateTotalCPS(self, list_of_buildings):
        self.cps = 0
        for building in list_of_buildings:
            self.cps += building.cps * building.quantity


window_length = 1000
window_height = 600
window = pygame.display.set_mode((window_length, window_height))

cookie = MainCookie(100, 100)
score_display = ScoreDisplay(100, 0)
user = Player()

'''Buildings'''
store_y = 212
cursor = Building('Cursor', 700, store_y, cursor_img, cursor_icon, base_cost=15, increase_per_purchase=1.15, cps=0.1)
grandma = Building('Cursor', 700, store_y + 64, grandma_img, grandma_icon, base_cost=100, increase_per_purchase=1.15,
                   cps=1)
farm = Building('Cursor', 700, store_y + 64 * 2, farm_img, farm_icon, base_cost=1100, increase_per_purchase=1.15, cps=8)
mine = Building('Cursor', 700, store_y + 64 * 3, mine_img, mine_icon, base_cost=12000, increase_per_purchase=1.15,
                cps=47)
factory = Building('Cursor', 700, store_y + 64 * 4, factory_img, factory_icon, base_cost=130000,
                   increase_per_purchase=1.15, cps=260)
bank = Building('Cursor', 700, store_y + 64 * 5, bank_img, bank_icon, base_cost=1400000, increase_per_purchase=1.15,
                cps=1400)
temple = Building('Cursor', 700, store_y + 64 * 6, temple_img, temple_icon, base_cost=20000000,
                  increase_per_purchase=1.15, cps=7000)
wizard_tower = Building('Cursor', 700, store_y + 64 * 7, wizard_tower_img, wizard_tower_icon, base_cost=300000000,
                        increase_per_purchase=1.15, cps=311000)
list_of_buildings = [cursor, grandma, farm, mine, factory, bank, temple, wizard_tower]

upgrade_x = 700
upgrade_y = 16
list_of_upgrades = []

def format_number(n):
    if n >= 1000000000:
        if (n / 1000000000) % 1 == 0:
            n = '{:.0f} billion'.format(n / 1000000000)
        else:
            n = '{:.2f} billion'.format(n / 1000000000)
    elif n >= 1000000:
        if (n / 1000000) % 1 == 0:
            n = '{:.0f} million'.format(n / 1000000)
        else:
            n = '{:.2f} million'.format(n / 1000000)
    return n


def draw():
    '''Draw background'''
    window.blit(background_img, (0, 0))
    window.blit(wooden_bar, (684, 0))
    window.blit(wooden_background, (700, 0))

    '''Draw Cookie and Score Display'''
    cookie.draw()
    score_display.draw()

    '''Draw buildings'''
    for building in list_of_buildings:
        if user.score >= building.getTotalCost():
            building.draw(solid=True)
        else:
            building.draw(solid=False)

        '''Add cookies made through building'''
        user.score += building.quantity * building.cps * .01  # тут тоже в душе не ебу
        building.created += building.quantity * building.cps * .01

        if building.collidepoint(pygame.mouse.get_pos()):
            building.drawDisplayBox()

    for i in range(0, len(list_of_upgrades)):
        upgrade = list_of_upgrades[i]
        upgrade.x = upgrade_x + (i % 5) * 60
        upgrade.y = upgrade_y + (i // 5) * 60

        if user.score >= upgrade.cost:
            upgrade.draw(solid=True)
        else:
            upgrade.draw(solid=False)

        if upgrade.collidepoint(pygame.mouse.get_pos()):
            upgrade.drawDisplayBox()


    window.blit(buildings_wooden_bar, (700, store_y - 16))
    window.blit(upgrades_wooden_bar, (700, 0))
    pygame.display.update()


main = True
while main:

    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            '''Click Cookie'''
            if cookie.collidepoint(mouse_pos):
                user.score += 1
                cookie.animation_state = 1

            '''Buy Building'''
            for building in list_of_buildings:
                if building.collidepoint(mouse_pos) and user.score >= building.getTotalCost():
                    building.addUpgrade()

                    user.score -= building.getTotalCost()
                    building.quantity += 1
                    user.updateTotalCPS(list_of_buildings)

            for upgrade in list_of_upgrades:
                if upgrade.collidepoint(mouse_pos) and user.score >= upgrade.cost:
                    user.score -= upgrade.cost
                    upgrade.upgradeBuilding(list_of_buildings)
                    list_of_upgrades.remove(upgrade)
                    user.updateTotalCPS(list_of_buildings)

        if event.type == pygame.QUIT:
            main = False

    if 700 < pygame.mouse.get_pos()[0] < 1000:
        if store_y < pygame.mouse.get_pos()[1] < store_y + 50:
            if list_of_buildings[0].y < store_y:
                for building in list_of_buildings:
                    building.y += 4
                    if store_y - 404 <= building.y <= store_y - 400:
                        building.y += 400
        elif 550 < pygame.mouse.get_pos()[1] < 600:
            for building in list_of_buildings:
                building.y -= 4
                if store_y - 4 <= building.y < store_y:
                    building.y -= 400

    draw()

pygame.quit()
