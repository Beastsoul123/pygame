import pygame
import sys
import random
import math
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Defender")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 120, 255)
YELLOW = (255, 255, 0)
PURPLE = (180, 0, 255)
ORANGE = (255, 165, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
DARK_BLUE = (0, 40, 85)
LIGHT_BLUE = (100, 180, 255)

MENU = 0
PLAYING = 1
GAME_OVER = 2
LEVEL_COMPLETE = 3
STORY = 4

game_state = MENU
current_level = 1
max_levels = 3
score = 0
player_health = 100

clock = pygame.time.Clock()

title_font = pygame.font.SysFont("arial", 48, bold=True)
normal_font = pygame.font.SysFont("arial", 24)
small_font = pygame.font.SysFont("arial", 18)

def create_player_ship():
    surf = pygame.Surface((50, 50), pygame.SRCALPHA)
    
    pygame.draw.polygon(surf, BLUE, [(25, 0), (0, 50), (50, 50)])
    pygame.draw.ellipse(surf, LIGHT_BLUE, (15, 15, 20, 20))
    pygame.draw.polygon(surf, DARK_BLUE, [(10, 30), (0, 40), (10, 50)])
    pygame.draw.polygon(surf, DARK_BLUE, [(40, 30), (50, 40), (40, 50)])
    
    pygame.draw.ellipse(surf, YELLOW, (20, 45, 10, 10))
    return surf

def create_enemy_ship(type):
    surf = pygame.Surface((40, 40), pygame.SRCALPHA)
    if type == 1:  
        pygame.draw.polygon(surf, RED, [(20, 0), (0, 40), (40, 40)])
        pygame.draw.circle(surf, ORANGE, (20, 25), 10)
        pygame.draw.polygon(surf, RED, [(15, 40), (20, 50), (25, 40)])
    elif type == 2:  
        pygame.draw.rect(surf, ORANGE, (10, 5, 20, 30))
        pygame.draw.polygon(surf, ORANGE, [(10, 5), (10, 35), (0, 20)])
        pygame.draw.polygon(surf, ORANGE, [(30, 5), (30, 35), (40, 20)])
        pygame.draw.circle(surf, YELLOW, (20, 35), 5)
    else:  
        pygame.draw.circle(surf, PURPLE, (20, 20), 20)
        pygame.draw.circle(surf, (150, 0, 255), (20, 20), 12)
        pygame.draw.rect(surf, PURPLE, (15, 0, 10, 10))
        pygame.draw.rect(surf, PURPLE, (15, 30, 10, 10))
        pygame.draw.rect(surf, PURPLE, (0, 15, 10, 10))
        pygame.draw.rect(surf, PURPLE, (30, 15, 10, 10))
    return surf
player_ship_img = create_player_ship()
enemy_ship_imgs = [create_enemy_ship(1), create_enemy_ship(2), create_enemy_ship(3)]

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.radius = 25
        self.speed = 5
        self.color = BLUE
        self.health = 100
        self.max_health = 100
        self.shoot_cooldown = 0
        self.shoot_delay = 15
        self.angle = 0
        self.engine_particles = []
        self.engine_timer = 0

    def move(self, keys):
        moving = False
        if keys[pygame.K_a] and self.x - self.radius > 0:
            self.x -= self.speed
            moving = True
        if keys[pygame.K_d] and self.x + self.radius < WIDTH:
            self.x += self.speed
            moving = True
        if keys[pygame.K_w] and self.y - self.radius > 0:
            self.y -= self.speed
            moving = True
        if keys[pygame.K_s] and self.y + self.radius < HEIGHT:
            self.y += self.speed
            moving = True
        
        if moving and self.engine_timer <= 0:
            self.engine_particles.append({
                'x': self.x,
                'y': self.y + 25,
                'size': random.randint(3, 8),
                'life': 20
            })
            self.engine_timer = 3
        else:
            self.engine_timer -= 1

    def draw(self, screen):
        for particle in self.engine_particles[:]:
            pygame.draw.circle(screen, YELLOW, (int(particle['x']), int(particle['y'])), particle['size'])
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.engine_particles.remove(particle)
                
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.angle = math.degrees(math.atan2(mouse_y - self.y, mouse_x - self.x)) + 90
        
        rotated_ship = pygame.transform.rotate(player_ship_img, -self.angle)
        ship_rect = rotated_ship.get_rect(center=(self.x, self.y))
        screen.blit(rotated_ship, ship_rect)

    def update(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def shoot(self, bullets):
        if self.shoot_cooldown == 0:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            angle = math.atan2(mouse_y - self.y, mouse_x - self.x)
            bullets.append(Bullet(self.x, self.y, angle))
            self.shoot_cooldown = self.shoot_delay
            return True
        return False

class Enemy:
    def __init__(self, x, y, enemy_type=1):
        self.x = x
        self.y = y
        self.type = enemy_type
        self.angle = 0
        
        if enemy_type == 1:  
            self.radius = 20
            self.color = RED
            self.speed = 2
            self.health = 20
            self.damage = 10
        elif enemy_type == 2:  
            self.radius = 15
            self.color = ORANGE
            self.speed = 3.5
            self.health = 15
            self.damage = 5
        else:  
            self.radius = 25
            self.color = PURPLE
            self.speed = 1.5
            self.health = 40
            self.damage = 15

    def move(self, player_x, player_y):
        self.angle = math.atan2(player_y - self.y, player_x - self.x)
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

    def draw(self, screen):
        rotated_ship = pygame.transform.rotate(enemy_ship_imgs[self.type - 1], -math.degrees(self.angle) + 90)
        ship_rect = rotated_ship.get_rect(center=(self.x, self.y))
        screen.blit(rotated_ship, ship_rect)

    def check_collision(self, player):
        distance = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
        return distance < (self.radius + player.radius)

class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.radius = 5
        self.speed = 10
        self.angle = angle
        self.color = YELLOW
        self.damage = 25
        self.trail = []

    def move(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        
        # Add to trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > 5:
            self.trail.pop(0)

    def draw(self, screen):
        # Draw trail
        for i, (trail_x, trail_y) in enumerate(self.trail):
            alpha = int(255 * (i / len(self.trail)))
            pygame.draw.circle(screen, (255, 255, 0, alpha), (int(trail_x), int(trail_y)), self.radius - 2)
        
        # Draw bullet
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def is_off_screen(self):
        return (self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT)

    def check_collision(self, enemy):
        distance = math.sqrt((self.x - enemy.x)**2 + (self.y - enemy.y)**2)
        return distance < (self.radius + enemy.radius)

class Button:
    def __init__(self, x, y, width, height, text, color=GREEN, hover_color=BLUE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.original_y = y
        self.bob_offset = 0
        self.bob_direction = 1
        self.bob_speed = 0.5

    def update(self):
        self.bob_offset += self.bob_direction * self.bob_speed
        if abs(self.bob_offset) > 5:
            self.bob_direction *= -1
            
        self.rect.y = self.original_y + self.bob_offset

    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        
        shadow_rect = self.rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        pygame.draw.rect(screen, (30, 30, 30), shadow_rect, border_radius=10)
        
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, 3, border_radius=10)
        
        text_surface = normal_font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def check_click(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

player = Player()
bullets = []
enemies = []
enemy_spawn_timer = 0
level_complete_timer = 0

start_button = Button(WIDTH//2 - 100, HEIGHT//2, 200, 50, "Start Game")
quit_button = Button(WIDTH//2 - 100, HEIGHT//2 + 70, 200, 50, "Quit", RED)
restart_button = Button(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50, "Restart")
next_level_button = Button(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50, "Next Level")
menu_button = Button(WIDTH//2 - 100, HEIGHT//2 + 120, 200, 50, "Main Menu", GRAY)
continue_button = Button(WIDTH//2 - 100, HEIGHT//2 + 190, 200, 50, "Continue", PURPLE)

story_messages = [
    "Year 2150: Earth is under attack by alien forces.",
    "You are a space defender tasked with protecting humanity.",
    "Your mission: defeat the alien waves and protect the planet.",
    "Good luck, defender. The fate of humanity is in your hands."
]

menu_stars = []
for _ in range(100):
    menu_stars.append({
        'x': random.randint(0, WIDTH),
        'y': random.randint(0, HEIGHT),
        'speed': random.uniform(0.1, 0.5),
        'size': random.randint(1, 3)
    })

menu_ships = []
for _ in range(5):
    menu_ships.append({
        'x': random.randint(0, WIDTH),
        'y': random.randint(0, HEIGHT),
        'speed': random.uniform(1, 3),
        'type': random.randint(0, 2),
        'angle': random.uniform(0, 2 * math.pi)
    })

def spawn_enemies(level):
    global enemies, enemy_spawn_timer
    
    if enemy_spawn_timer <= 0 and len(enemies) < 5 + level * 2:
        enemy_type = 1  # Basic enemy by default
       
        if level >= 2 and random.random() < 0.3:
            enemy_type = 2  # Fast enemy
        if level >= 3 and random.random() < 0.2:
            enemy_type = 3  # Strong enemy
            
        side = random.randint(0, 3)
        if side == 0:  # Top
            x = random.randint(0, WIDTH)
            y = -20
        elif side == 1:  # Right
            x = WIDTH + 20
            y = random.randint(0, HEIGHT)
        elif side == 2:  # Bottom
            x = random.randint(0, WIDTH)
            y = HEIGHT + 20
        else:  # Left
            x = -20
            y = random.randint(0, HEIGHT)
            
        enemies.append(Enemy(x, y, enemy_type))
        enemy_spawn_timer = 60 - level * 10  # Spawn faster as levels increase
    else:
        enemy_spawn_timer -= 1

def check_level_complete():
    global game_state, level_complete_timer, current_level
    if len(enemies) == 0 and enemy_spawn_timer <= 0 and current_level * 10 <= score:
        game_state = LEVEL_COMPLETE
        level_complete_timer = 180  # 3 seconds at 60 FPS

def draw_health_bar(screen, x, y, width, height, value, max_value):
    ratio = value / max_value
    pygame.draw.rect(screen, DARK_GRAY, (x - 2, y - 2, width + 4, height + 4))
    pygame.draw.rect(screen, RED, (x, y, width, height))
    pygame.draw.rect(screen, GREEN, (x, y, width * ratio, height))
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, width + 4, height + 4), 2)

def draw_game_ui():
    draw_health_bar(screen, 20, 20, 200, 20, player.health, player.max_health)
    score_text = normal_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH - score_text.get_width() - 20, 20))
    
    # Draw level
    level_text = normal_font.render(f"Level: {current_level}", True, WHITE)
    screen.blit(level_text, (WIDTH - level_text.get_width() - 20, 60))
    enemies_text = normal_font.render(f"Enemies: {len(enemies)}", True, WHITE)
    screen.blit(enemies_text, (WIDTH - enemies_text.get_width() - 20, 100))
    objective_text = small_font.render(f"Defeat {current_level * 10} enemies to advance", True, YELLOW)
    screen.blit(objective_text, (WIDTH - objective_text.get_width() - 20, 140))

def update_menu_animation():
    for star in menu_stars:
        star['y'] += star['speed']
        if star['y'] > HEIGHT:
            star['y'] = 0
            star['x'] = random.randint(0, WIDTH)
    for ship in menu_ships:
        ship['x'] += math.cos(ship['angle']) * ship['speed']
        ship['y'] += math.sin(ship['angle']) * ship['speed']
        
        # Bounce off edges
        if ship['x'] < 0 or ship['x'] > WIDTH:
            ship['angle'] = math.pi - ship['angle']
        if ship['y'] < 0 or ship['y'] > HEIGHT:
            ship['angle'] = -ship['angle']
            
        # Keep in bounds
        ship['x'] = max(0, min(WIDTH, ship['x']))
        ship['y'] = max(0, min(HEIGHT, ship['y']))

def draw_menu():
    screen.fill(BLACK)
    for star in menu_stars:
        pygame.draw.circle(screen, WHITE, (int(star['x']), int(star['y'])), star['size'])
    for ship in menu_ships:
        rotated_ship = pygame.transform.rotate(enemy_ship_imgs[ship['type']], -math.degrees(ship['angle']) + 90)
        ship_rect = rotated_ship.get_rect(center=(ship['x'], ship['y']))
        screen.blit(rotated_ship, ship_rect)
    
    # Draw title with gradient
    title_text = title_font.render("SPACE DEFENDER", True, BLUE)
    title_shadow = title_font.render("SPACE DEFENDER", True, LIGHT_BLUE)
    screen.blit(title_shadow, (WIDTH//2 - title_text.get_width()//2 + 2, HEIGHT//4 + 2))
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//4))
    
    # Draw subtitle
    subtitle_text = normal_font.render("A Top-Down Shooter Game", True, WHITE)
    screen.blit(subtitle_text, (WIDTH//2 - subtitle_text.get_width()//2, HEIGHT//4 + 60))
    
    # Draw buttons
    start_button.draw(screen)
    quit_button.draw(screen)
    
    # Draw controls with pulsing effect
    pulse = (math.sin(pygame.time.get_ticks() * 0.002) + 1) * 0.5
    pulse_color = (int(100 + 155 * pulse), int(100 + 155 * pulse), int(100 + 155 * pulse))
    
    controls_text = [
        "Controls:",
        "WASD - Move",
        "Mouse - Aim",
        "Left Click - Shoot",
        "Survive and complete all levels!"
    ]
    
    for i, text in enumerate(controls_text):
        control = small_font.render(text, True, pulse_color)
        screen.blit(control, (WIDTH//2 - control.get_width()//2, HEIGHT//2 + 150 + i*25))

def draw_game_over():
    screen.fill(BLACK)
    
    # Draw game over text
    game_over_text = title_font.render("GAME OVER", True, RED)
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//4))
    
    # Draw score
    score_text = normal_font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//4 + 80))
    
    # Draw buttons
    restart_button.draw(screen)
    menu_button.draw(screen)

def draw_level_complete():
    screen.fill(BLACK)
    
    # Draw level complete text
    complete_text = title_font.render(f"LEVEL {current_level} COMPLETE", True, GREEN)
    screen.blit(complete_text, (WIDTH//2 - complete_text.get_width()//2, HEIGHT//4))
    
    # Draw score
    score_text = normal_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//4 + 80))
    
    if current_level < max_levels:
        next_level_button.draw(screen)
    else:
        win_text = title_font.render("YOU WIN!", True, YELLOW)
        screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2))
    
    menu_button.draw(screen)

def draw_story():
    screen.fill(BLACK)
    
    # Draw story title
    title_text = title_font.render("THE STORY", True, PURPLE)
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//6))
    
    # Draw story messages with typewriter effect
    for i, message in enumerate(story_messages):
        # Simple typewriter effect
        chars_to_show = min(len(message), (pygame.time.get_ticks() // 100) - i * 10)
        if chars_to_show > 0:
            text = normal_font.render(message[:chars_to_show], True, WHITE)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//3 + i*50))
    
    # Draw continue button
    continue_button.draw(screen)

def reset_game():
    global player, bullets, enemies, enemy_spawn_timer, score, player_health, current_level
    player = Player()
    bullets = []
    enemies = []
    enemy_spawn_timer = 0
    score = 0
    player_health = 100
    current_level = 1

# Main game loop
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if game_state == MENU:
            start_button.check_hover(mouse_pos)
            quit_button.check_hover(mouse_pos)
            
            if start_button.check_click(mouse_pos, event):
                game_state = STORY
            
            if quit_button.check_click(mouse_pos, event):
                running = False
                
        elif game_state == PLAYING:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                player.shoot(bullets)
                
        elif game_state == GAME_OVER:
            restart_button.check_hover(mouse_pos)
            menu_button.check_hover(mouse_pos)
            
            if restart_button.check_click(mouse_pos, event):
                reset_game()
                game_state = PLAYING
                
            if menu_button.check_click(mouse_pos, event):
                game_state = MENU
                
        elif game_state == LEVEL_COMPLETE:
            next_level_button.check_hover(mouse_pos)
            menu_button.check_hover(mouse_pos)
            
            if next_level_button.check_click(mouse_pos, event) and current_level < max_levels:
                current_level += 1
                enemies = []
                enemy_spawn_timer = 0
                game_state = PLAYING
                
            if menu_button.check_click(mouse_pos, event):
                game_state = MENU
                
        elif game_state == STORY:
            continue_button.check_hover(mouse_pos)
            
            if continue_button.check_click(mouse_pos, event):
                reset_game()
                game_state = PLAYING
    
    # Update animations
    if game_state == MENU:
        update_menu_animation()
        start_button.update()
        quit_button.update()
    
    # Game logic based on state
    if game_state == PLAYING:
        keys = pygame.key.get_pressed()
        player.move(keys)
        player.update()
        
        # Spawn enemies
        spawn_enemies(current_level)
        for bullet in bullets[:]:
            bullet.move()
            if bullet.is_off_screen():
                bullets.remove(bullet)
            else:
                for enemy in enemies[:]:
                    if bullet.check_collision(enemy):
                        enemy.health -= bullet.damage
                        if enemy.health <= 0:
                            enemies.remove(enemy)
                            score += 10
                        if bullet in bullets:
                            bullets.remove(bullet)
                        break
        
        # Update enemies
        for enemy in enemies:
            enemy.move(player.x, player.y)
            if enemy.check_collision(player):
                player.health -= enemy.damage
                enemies.remove(enemy)
                if player.health <= 0:
                    game_state = GAME_OVER
        
        # Check if level is complete
        check_level_complete()
    
    # Drawing
    screen.fill(BLACK)
    
    if game_state == MENU:
        draw_menu()
    elif game_state == PLAYING:
        # Draw background stars
        for _ in range(100):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            pygame.draw.circle(screen, WHITE, (x, y), 1)
        for bullet in bullets:
            bullet.draw(screen)
        
        for enemy in enemies:
            enemy.draw(screen)
        
        player.draw(screen)
        draw_game_ui()
    elif game_state == GAME_OVER:
        draw_game_over()
    elif game_state == LEVEL_COMPLETE:
        draw_level_complete()
        level_complete_timer -= 1
        if level_complete_timer <= 0 and current_level >= max_levels:
            game_state = MENU
    elif game_state == STORY:
        draw_story()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()