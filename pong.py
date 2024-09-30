import cv2
import mediapipe as mp
import numpy as np
import pygame
import pyttsx3  # Text-to-speech


# Initialize MediaPipe's Hands model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

# Initialize Pygame and set full-screen mode
pygame.init()
infoObject = pygame.display.Info()
window_width, window_height = infoObject.current_w, infoObject.current_h

# Set game and webcam feed sizes
game_area_width = window_width * 3 // 4
game_area_height = window_height
webcam_feed_width = window_width // 4
webcam_feed_height = window_height // 4

# Set up full-screen window
window = pygame.display.set_mode((window_width, window_height), pygame.FULLSCREEN)
pygame.display.set_caption("Gesture-Based Pong Game")

# Initialize Text-to-Speech (TTS) engine
engine = pyttsx3.init()

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Paddle setup
paddle_width = 150
paddle_height = 20
paddle_x = game_area_width // 2 - paddle_width // 2
paddle_y = game_area_height - paddle_height - 30
paddle_speed = 15

# Ball setup
ball_x = game_area_width // 2
ball_y = game_area_height // 2
ball_radius = 10
ball_dx = 8
ball_dy = -8

# Score, lives, and level
score = 0
lives = 3
level = 1

# Game over flag
game_over = False
font = pygame.font.Font('freesansbold.ttf', 64)
game_over_text = font.render('Game Over', True, (255, 255, 255))

# Button setup for restart/quit options
button_font = pygame.font.Font('freesansbold.ttf', 40)
def create_button(text, font, padding):
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.inflate_ip(padding[0], padding[1])
    return text_surface, text_rect

restart_button_text, restart_button_rect = create_button('Restart', button_font, (40, 20))
quit_button_text, quit_button_rect = create_button('Quit', button_font, (40, 20))

# Center the buttons
restart_button_rect.center = (window_width // 2, window_height // 2 + 80)
quit_button_rect.center = (window_width // 2, window_height // 2 + 160)

# Initialize webcam capture
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Webcam not detected.")
    pygame.quit()
    exit()

# Function to track paddle movement via hand gestures
previous_hand_x = None

def detect_gesture(hand_landmarks):
    global previous_hand_x
    current_hand_x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
    
    if previous_hand_x is None:
        previous_hand_x = current_hand_x
        return 0

    move_x = int((current_hand_x - previous_hand_x) * game_area_width)
    previous_hand_x = current_hand_x
    return move_x

def draw_button(button_text, button_rect, is_hovered):
    # Change color when hovered and add rounded corners
    color = (255, 100, 100) if is_hovered else (255, 0, 0)
    pygame.draw.rect(window, color, button_rect, border_radius=12)
    window.blit(button_text, button_rect)

# Say "Start the game" when the game starts
speak("Start the game")

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouse_pos = pygame.mouse.get_pos()
            if restart_button_rect.collidepoint(mouse_pos):
                # Restart the game
                speak("Restarting the game")
                game_over = False
                score = 0
                lives = 3
                level = 1
                ball_x, ball_y = game_area_width // 2, game_area_height // 2
                ball_dx, ball_dy = 8, -8
            elif quit_button_rect.collidepoint(mouse_pos):
                speak("Quitting the game")
                running = False

    success, frame = cap.read()
    if not success:
        print("Error: Failed to capture image from webcam.")
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_resized = cv2.resize(frame_rgb, (webcam_feed_width, webcam_feed_height))

    if not game_over:
        # Detect hand landmarks
        results = hands.process(frame)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                move_x = detect_gesture(hand_landmarks)
                paddle_x += move_x

        # Keep the paddle within the game area
        paddle_x = max(0, min(paddle_x, game_area_width - paddle_width))

        # Ball movement
        ball_x += ball_dx
        ball_y += ball_dy

        # Ball collision with walls
        if ball_x <= 0 or ball_x >= game_area_width - ball_radius:
            ball_dx = -ball_dx
        if ball_y <= 0:
            ball_dy = -ball_dy

        # Ball collision with paddle
        if paddle_x <= ball_x <= paddle_x + paddle_width and paddle_y <= ball_y + ball_radius <= paddle_y + paddle_height:
            ball_dy = -ball_dy
            score += 1

            # Increase difficulty with levels
            if score % 5 == 0:
                level += 1
                ball_dx += 1 if ball_dx > 0 else -1
                ball_dy += 1 if ball_dy > 0 else -1

        # Ball goes out of bounds (lose a life)
        if ball_y > game_area_height:
            lives -= 1
            ball_x, ball_y = game_area_width // 2, game_area_height // 2
            ball_dx, ball_dy = 8, -8

            if lives == 0 and not game_over:
                game_over = True
                speak(f"your score if {score}")
                speak("Game over")

    # Clear the screen
    window.fill((0, 0, 0))

    if game_over:
        # Display Game Over and buttons
        window.blit(game_over_text, (window_width // 2 - game_over_text.get_width() // 2, window_height // 2 - game_over_text.get_height() // 2))
        draw_button(restart_button_text, restart_button_rect, restart_button_rect.collidepoint(pygame.mouse.get_pos()))
        draw_button(quit_button_text, quit_button_rect, quit_button_rect.collidepoint(pygame.mouse.get_pos()))
        
        # Show the final score on Game Over screen
        final_score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        window.blit(final_score_text, (window_width // 2 - final_score_text.get_width() // 2, window_height // 2 - final_score_text.get_height() // 2 - 100))

    else:
        # Draw paddle
        pygame.draw.rect(window, (255, 255, 255), (paddle_x, paddle_y, paddle_width, paddle_height))

        # Draw ball
        pygame.draw.circle(window, (255, 0, 0), (ball_x, ball_y), ball_radius)

        # Draw the webcam feed in the top-right corner
        webcam_feed = pygame.surfarray.make_surface(np.transpose(frame_resized, (1, 0, 2)))
        window.blit(webcam_feed, (game_area_width, 0))

        # Draw score, lives, and level
        font_small = pygame.font.Font('freesansbold.ttf', 32)
        score_text = font_small.render(f'Score: {score}', True, (255, 255, 255))
        lives_text = font_small.render(f'Lives: {lives}', True, (255, 255, 255))
        level_text = font_small.render(f'Level: {level}', True, (255, 255, 255))
        window.blit(score_text, (10, 10))
        window.blit(lives_text, (10, 50))
        window.blit(level_text, (10, 90))

    # Update the display
    pygame.display.update()
    clock.tick(60)

cap.release()
cv2.destroyAllWindows()
pygame.quit()
