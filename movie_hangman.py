import pygame
import sys
import random
import time
from pygame.locals import *

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1000  # Increased from 800 to 1000 to accommodate longer movie titles
SCREEN_HEIGHT = 700  # Increased from 600 to 700 to provide more vertical space
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Movie Hangman")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)  # Lighter gray for the background
GREEN = (0, 128, 0)  # Darker green for better visibility
BRIGHT_GREEN = (34, 177, 76)  # Alternative green that's more visible
RED = (255, 0, 0)

# Fonts - use default font to avoid fc-list timeout issues on macOS
FONT = pygame.font.Font(None, 32)
SMALL_FONT = pygame.font.Font(None, 24)

# Game variables
movie_list = [
    "THE GODFATHER",
    "PULP FICTION",
    "THE DARK KNIGHT",
    "FORREST GUMP",
    "STAR WARS",
    "JURASSIC PARK",
    "THE MATRIX",
    "TITANIC",
    "AVATAR",
    "INCEPTION",
    "THE SHAWSHANK REDEMPTION",
    "SCHINDLER'S LIST",
    "THE LORD OF THE RINGS",
    "FIGHT CLUB",
    "GOODFELLAS",
    "CASABLANCA",
    "CITIZEN KANE",
    "GONE WITH THE WIND",
    "THE WIZARD OF OZ",
    "RAIDERS OF THE LOST ARK",
    "BACK TO THE FUTURE",
    "GLADIATOR",
    "THE SILENCE OF THE LAMBS",
    "SAVING PRIVATE RYAN",
    "JAWS",
    "ET THE EXTRA TERRESTRIAL",
    "THE LION KING",
    "TOY STORY",
    "FINDING NEMO",
    "UP",
    "FROZEN",
    "INSIDE OUT",
    "THE AVENGERS",
    "IRON MAN",
    "BLACK PANTHER",
    "WONDER WOMAN",
    "THE DARK KNIGHT RISES",
    "BATMAN BEGINS",
    "SUPERMAN",
    "SPIDER MAN",
    "DEADPOOL",
    "LOGAN",
    "THE TERMINATOR",
    "ALIEN",
    "BLADE RUNNER",
    "MAD MAX FURY ROAD",
    "DIE HARD",
    "LETHAL WEAPON",
    "MISSION IMPOSSIBLE",
    "JAMES BOND SKYFALL",
    "CASINO ROYALE",
    "THE BOURNE IDENTITY",
    "JOHN WICK",
    "SPEED",
    "THE MATRIX RELOADED",
    "THE HUNGER GAMES",
    "HARRY POTTER",
    "THE HOBBIT",
    "TWILIGHT",
    "FIFTY SHADES OF GREY",
    "PRETTY WOMAN",
    "NOTTING HILL",
    "WHEN HARRY MET SALLY",
    "SLEEPLESS IN SEATTLE",
    "THE NOTEBOOK",
    "TITANIC",
    "ROMEO AND JULIET",
    "PRIDE AND PREJUDICE",
    "BROKEBACK MOUNTAIN",
    "LA LA LAND",
    "A STAR IS BORN",
    "THE GREATEST SHOWMAN",
    "BOHEMIAN RHAPSODY",
    "ROCKETMAN",
    "STRAIGHT OUTTA COMPTON",
    "WHIPLASH",
    "THE SOCIAL NETWORK",
    "STEVE JOBS",
    "THE IMITATION GAME",
    "A BEAUTIFUL MIND",
    "GOOD WILL HUNTING",
    "THE THEORY OF EVERYTHING",
    "HIDDEN FIGURES",
    "THE MARTIAN",
    "INTERSTELLAR",
    "GRAVITY",
    "APOLLO THIRTEEN",
    "JURASSIC WORLD",
    "GODZILLA",
    "KING KONG",
    "PACIFIC RIM",
    "TRANSFORMERS",
    "INDEPENDENCE DAY",
    "THE DAY AFTER TOMORROW",
    "TWISTER",
    "ARMAGEDDON",
    "DEEP IMPACT",
    "THE SIXTH SENSE",
    "GET OUT",
    "THE EXORCIST",
    "THE SHINING"
]

class MovieHangman:
    def __init__(self):
        self.movie = random.choice(movie_list)
        self.guessed_letters = set()
        self.start_time = time.time()
        self.game_over = False
        self.won = False
        self.win_time = None  # Track when the player wins
        self.time_limit = 120  # 2 minutes in seconds
        self.blink_timer = 0  # For blinking text effect
        
        # Load images
        try:
            self.worried_kangaroo = pygame.image.load("worried_kangaroo.png")
            self.happy_kangaroo = pygame.image.load("happy_kangaroo.png")
            self.sad_kangaroo = pygame.image.load("sad_kangaroo.png")
            self.noose = pygame.image.load("noose.png")
        except pygame.error:
            # Fallback to placeholders if images can't be loaded
            self.worried_kangaroo = self.create_placeholder("Worried Kangaroo", (255, 215, 0), (200, 200))
            self.happy_kangaroo = self.create_placeholder("Happy Kangaroo", (144, 238, 144), (200, 200))
            self.sad_kangaroo = self.create_placeholder("Sad Kangaroo", (255, 160, 122), (200, 200))
            self.noose = self.create_placeholder("Noose", (139, 69, 19), (100, 100))
        
        # Create letter boxes
        self.letter_boxes = []
        self.create_letter_boxes()
    
    def create_placeholder(self, text, color, size):
        # Create a colored rectangle with text as a placeholder for images
        surface = pygame.Surface(size)
        surface.fill(color)
        
        # Add text to identify the image
        text_surface = SMALL_FONT.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=(size[0]//2, size[1]//2))
        surface.blit(text_surface, text_rect)
        
        return surface
    
    def create_letter_boxes(self):
        box_width = 40
        box_height = 40
        spacing = 10
        
        # Calculate starting position to center the boxes
        total_width = 0
        for char in self.movie:
            if char != ' ':
                total_width += box_width + spacing
        
        start_x = (SCREEN_WIDTH - total_width) // 2
        y = 200
        
        x = start_x
        for char in self.movie:
            if char == ' ':
                x += box_width + spacing
            else:
                self.letter_boxes.append({
                    'rect': pygame.Rect(x, y, box_width, box_height),
                    'letter': char,
                    'revealed': False
                })
                x += box_width + spacing
    
    def handle_event(self, event):
        if event.type == KEYDOWN and not self.game_over:
            if event.key >= ord('a') and event.key <= ord('z'):
                letter = chr(event.key).upper()
                self.guessed_letters.add(letter)
                
                # Check if all letters are guessed
                all_revealed = True
                for box in self.letter_boxes:
                    if box['letter'] in self.guessed_letters:
                        box['revealed'] = True
                    if not box['revealed'] and box['letter'] != ' ':
                        all_revealed = False
                
                if all_revealed:
                    self.game_over = True
                    self.won = True
                    self.win_time = time.time()  # Record the time when player wins
    
    def update(self):
        # Check if time is up
        elapsed_time = time.time() - self.start_time
        if elapsed_time >= self.time_limit and not self.game_over:
            self.game_over = True
            self.won = False
            
        # Update blink timer
        self.blink_timer = (self.blink_timer + 1) % 30  # 30 frames for a complete blink cycle (faster)
    
    def draw(self):
        SCREEN.fill(LIGHT_GRAY)  # Changed from WHITE to LIGHT_GRAY for the background
        
        # Draw warning message
        warning_text = SMALL_FONT.render("Guess the Movie name in 2 minutes or the Roo gets it!", True, RED)
        SCREEN.blit(warning_text, (20, 20))
        
        # Draw timer - only update if game is not won
        if not self.won:
            elapsed_time = time.time() - self.start_time
            remaining_time = max(0, self.time_limit - elapsed_time)
        else:
            # If won, keep the time at when they won
            remaining_time = self.time_limit - (self.win_time - self.start_time)
            
        timer_text = SMALL_FONT.render(f"Time: {int(remaining_time)}s", True, BLACK)
        SCREEN.blit(timer_text, (20, 50))
        
        # Draw letter boxes
        for box in self.letter_boxes:
            # Fill box with white background
            pygame.draw.rect(SCREEN, WHITE, box['rect'])
            # Draw black border
            pygame.draw.rect(SCREEN, BLACK, box['rect'], 2)
            if box['revealed'] or self.game_over:
                text = FONT.render(box['letter'], True, BLACK)
                text_rect = text.get_rect(center=box['rect'].center)
                SCREEN.blit(text, text_rect)
        
        # Draw guessed letters
        guessed_text = SMALL_FONT.render(f"Guessed: {', '.join(sorted(self.guessed_letters))}", True, BLACK)
        SCREEN.blit(guessed_text, (20, 80))
        
        # Draw kangaroo and noose based on game state
        if self.game_over:
            if self.won:
                # Show happy kangaroo without noose
                kangaroo_x = (SCREEN_WIDTH - self.happy_kangaroo.get_width()) // 2
                SCREEN.blit(self.happy_kangaroo, (kangaroo_x, 300))
                
                # Create a background rectangle for better text visibility
                result_text = FONT.render("You saved the kangaroo!", True, BRIGHT_GREEN)
                result_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2, 550))
                
                # Draw a semi-transparent background behind the text
                bg_rect = result_rect.copy()
                bg_rect.inflate_ip(20, 10)  # Make the background slightly larger than the text
                bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
                bg_surface.set_alpha(180)  # Semi-transparent
                bg_surface.fill(BLACK)
                SCREEN.blit(bg_surface, bg_rect)
                
                # Draw the text
                SCREEN.blit(result_text, result_rect)
            else:
                # Show sad kangaroo with noose
                kangaroo_x = (SCREEN_WIDTH - self.sad_kangaroo.get_width()) // 2
                SCREEN.blit(self.sad_kangaroo, (kangaroo_x, 300))
                noose_x = kangaroo_x + 50  # Position noose relative to kangaroo
                SCREEN.blit(self.noose, (noose_x, 250))
                
                # Create a background rectangle for better text visibility
                result_text = FONT.render("Oh no! The kangaroo is sad!", True, RED)
                result_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2, 550))
                
                # Draw a semi-transparent background behind the text
                bg_rect = result_rect.copy()
                bg_rect.inflate_ip(20, 10)  # Make the background slightly larger than the text
                bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
                bg_surface.set_alpha(180)  # Semi-transparent
                bg_surface.fill(BLACK)
                SCREEN.blit(bg_surface, bg_rect)
                
                # Draw the text
                SCREEN.blit(result_text, result_rect)
            
            # Show play again message with blinking effect
            # Only show text during the first half of the blink cycle (15 frames visible, 15 frames invisible)
            if self.blink_timer < 15:
                again_text = SMALL_FONT.render("Press R to play again or Q to quit", True, WHITE)
                again_rect = again_text.get_rect(center=(SCREEN_WIDTH // 2, 600))
                
                # Draw a semi-transparent background behind the text
                bg_rect = again_rect.copy()
                bg_rect.inflate_ip(20, 10)  # Make the background slightly larger than the text
                bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
                bg_surface.set_alpha(180)  # Semi-transparent
                bg_surface.fill(BLACK)
                SCREEN.blit(bg_surface, bg_rect)
                
                # Draw the text
                SCREEN.blit(again_text, again_rect)
        else:
            # Show worried kangaroo with noose
            kangaroo_x = (SCREEN_WIDTH - self.worried_kangaroo.get_width()) // 2
            SCREEN.blit(self.worried_kangaroo, (kangaroo_x, 300))
            noose_x = kangaroo_x + 50  # Position noose relative to kangaroo
            SCREEN.blit(self.noose, (noose_x, 250))

def main():
    clock = pygame.time.Clock()
    game = MovieHangman()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    running = False
                elif event.key == K_r and game.game_over:
                    game = MovieHangman()  # Reset the game
                else:
                    game.handle_event(event)
        
        game.update()
        game.draw()
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
