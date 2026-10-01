import math
import os
import random
import struct
import wave

import pygame

from .target import Target


WHITE = (255, 255, 255)
RED = (220, 60, 60)
GREEN = (70, 200, 100)
YELLOW = (240, 200, 60)
DARK_GRAY = (35, 35, 40)
BLUE = (70, 140, 220)


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.margin = 60
        self.hud_height = 60

        self.round_seconds = 30
        self.time_left_frames = self.round_seconds * 60

        self.hits = 0
        self.misses = 0
        self.score = 0

        self.font = pygame.font.SysFont("Arial", 26)
        self.large_font = pygame.font.SysFont("Arial", 42, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 22)

        self.game_over = False
        self.difficulty_select = False
        self.running = True

        self.difficulty = "Medium"

        self.difficulty_settings = {
            "Easy": {
                "base_radius": 48,
                "min_radius": 18,
                "lifespan_frames": 120,
            },
            "Medium": {
                "base_radius": 40,
                "min_radius": 12,
                "lifespan_frames": 90,
            },
            "Hard": {
                "base_radius": 34,
                "min_radius": 9,
                "lifespan_frames": 60,
            },
        }

        self._setup_sounds()
        self.target = self._spawn_target()

    # ---------------------------------------------------------
    # SOUND SETUP
    # ---------------------------------------------------------

    def _setup_sounds(self):
        self.hit_sound = None
        self.miss_sound = None
        self.timeout_sound = None
        self.game_over_sound = None

        try:
            pygame.mixer.init()

            sound_folder = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "sounds",
            )

            os.makedirs(sound_folder, exist_ok=True)

            hit_path = os.path.join(sound_folder, "hit.wav")
            miss_path = os.path.join(sound_folder, "miss.wav")
            timeout_path = os.path.join(sound_folder, "timeout.wav")
            game_over_path = os.path.join(sound_folder, "game_over.wav")

            self._create_tone(hit_path, 700, 0.10)
            self._create_tone(miss_path, 250, 0.12)
            self._create_tone(timeout_path, 180, 0.15)
            self._create_tone(game_over_path, 120, 0.35)

            self.hit_sound = pygame.mixer.Sound(hit_path)
            self.miss_sound = pygame.mixer.Sound(miss_path)
            self.timeout_sound = pygame.mixer.Sound(timeout_path)
            self.game_over_sound = pygame.mixer.Sound(game_over_path)

        except pygame.error:
            # If sound cannot be initialized, the game still works.
            pass

    def _create_tone(self, filename, frequency, duration):
        sample_rate = 44100
        number_of_samples = int(sample_rate * duration)
        amplitude = 12000

        with wave.open(filename, "w") as sound_file:
            sound_file.setnchannels(1)
            sound_file.setsampwidth(2)
            sound_file.setframerate(sample_rate)

            frames = bytearray()

            for i in range(number_of_samples):
                value = int(
                    amplitude
                    * math.sin(
                        2 * math.pi * frequency * i / sample_rate
                    )
                )

                frames.extend(struct.pack("<h", value))

            sound_file.writeframes(frames)

    def _play_sound(self, sound):
        if sound is not None:
            try:
                sound.play()
            except pygame.error:
                pass

    # ---------------------------------------------------------
    # TARGET / ROUND
    # ---------------------------------------------------------

    def _spawn_target(self):
        settings = self.difficulty_settings[self.difficulty]

        x = random.randint(
            self.margin,
            self.width - self.margin,
        )

        y = random.randint(
            self.margin + self.hud_height,
            self.height - self.margin,
        )

        return Target(
            x,
            y,
            base_radius=settings["base_radius"],
            min_radius=settings["min_radius"],
            lifespan_frames=settings["lifespan_frames"],
        )

    def _reset_round(self, difficulty=None):
        if difficulty is not None:
            self.difficulty = difficulty

        self.hits = 0
        self.misses = 0
        self.score = 0

        self.time_left_frames = self.round_seconds * 60

        self.game_over = False
        self.difficulty_select = False

        self.target = self._spawn_target()

    # ---------------------------------------------------------
    # EVENT HANDLING
    # ---------------------------------------------------------

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            return

        # Game Over screen
        if self.game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.difficulty_select = True
                    self.game_over = False

                elif event.key == pygame.K_ESCAPE:
                    self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.difficulty_select = True
                self.game_over = False

            return

        # Difficulty selection screen
        if self.difficulty_select:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self._reset_round("Easy")

                elif event.key == pygame.K_2:
                    self._reset_round("Medium")

                elif event.key == pygame.K_3:
                    self._reset_round("Hard")

                elif event.key == pygame.K_ESCAPE:
                    self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if 70 <= x <= 210 and 300 <= y <= 360:
                    self._reset_round("Easy")

                elif 280 <= x <= 420 and 300 <= y <= 360:
                    self._reset_round("Medium")

                elif 490 <= x <= 630 and 300 <= y <= 360:
                    self._reset_round("Hard")

            return

        # Normal gameplay
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_click(event.pos)

    def _handle_click(self, pos):
        if self.game_over or self.difficulty_select:
            return

        if self.target.contains_point(pos[0], pos[1]):
            self.hits += 1
            self.score += 1

            self._play_sound(self.hit_sound)

            self.target = self._spawn_target()

        else:
            self.misses += 1

            self._play_sound(self.miss_sound)

    def handle_input(self):
        pass

    # ---------------------------------------------------------
    # GAME UPDATE
    # ---------------------------------------------------------

    def update(self):
        if self.game_over or self.difficulty_select:
            return

        self.time_left_frames -= 1

        if self.time_left_frames <= 0:
            self.time_left_frames = 0

            # Target that remains when the timer ends counts as a miss.
            self.misses += 1

            self._play_sound(self.timeout_sound)
            self._play_sound(self.game_over_sound)

            self.game_over = True
            return

        self.target.update()

        if self.target.expired():
            self.misses += 1

            self._play_sound(self.timeout_sound)

            self.target = self._spawn_target()

    # ---------------------------------------------------------
    # ACCURACY
    # ---------------------------------------------------------

    def accuracy(self):
        total = self.hits + self.misses

        if total == 0:
            return 0.0

        return round(
            100 * self.hits / total,
            1,
        )

    # ---------------------------------------------------------
    # RENDERING
    # ---------------------------------------------------------

    def _render_gameplay(self, screen):
        # Draw target using its current visual radius.
        radius = int(self.target.visual_radius())

        pygame.draw.circle(
            screen,
            RED,
            (self.target.x, self.target.y),
            radius,
        )

        # Draw a smaller inner circle for visual appearance.
        inner_radius = max(2, radius // 3)

        pygame.draw.circle(
            screen,
            WHITE,
            (self.target.x, self.target.y),
            inner_radius,
        )

        seconds_left = max(
            0,
            self.time_left_frames // 60,
        )

        hud_text = (
            f"Score: {self.score}    "
            f"Accuracy: {self.accuracy()}%    "
            f"Time: {seconds_left}s"
        )

        hud = self.font.render(
            hud_text,
            True,
            WHITE,
        )

        screen.blit(
            hud,
            (20, 18),
        )

    def _render_game_over(self, screen):
        title = self.large_font.render(
            "GAME OVER",
            True,
            WHITE,
        )

        title_rect = title.get_rect(
            center=(self.width // 2, 100),
        )

        screen.blit(
            title,
            title_rect,
        )

        score_text = self.font.render(
            f"Final Score: {self.score}",
            True,
            GREEN,
        )

        score_rect = score_text.get_rect(
            center=(self.width // 2, 180),
        )

        screen.blit(
            score_text,
            score_rect,
        )

        accuracy_text = self.font.render(
            f"Accuracy: {self.accuracy()}%",
            True,
            YELLOW,
        )

        accuracy_rect = accuracy_text.get_rect(
            center=(self.width // 2, 225),
        )

        screen.blit(
            accuracy_text,
            accuracy_rect,
        )

        difficulty_text = self.small_font.render(
            f"Difficulty: {self.difficulty}",
            True,
            WHITE,
        )

        difficulty_rect = difficulty_text.get_rect(
            center=(self.width // 2, 265),
        )

        screen.blit(
            difficulty_text,
            difficulty_rect,
        )

        replay_text = self.font.render(
            "Press ENTER or click to play again",
            True,
            BLUE,
        )

        replay_rect = replay_text.get_rect(
            center=(self.width // 2, 330),
        )

        screen.blit(
            replay_text,
            replay_rect,
        )

        exit_text = self.small_font.render(
            "Press ESC to exit",
            True,
            WHITE,
	)

        exit_rect = exit_text.get_rect(

            center=(self.width // 2, 390),
        )


        screen.blit(

            exit_text,

            exit_rect,

        )


    def _render_difficulty_select(self, screen):
        title = self.large_font.render(

            "SELECT DIFFICULTY",
            True,

            WHITE,

        )


        title_rect = title.get_rect(

            center=(self.width // 2, 100),
        )


        screen.blit(

            title,
            title_rect,

        )


        difficulties = [
            ("1 - EASY", 70, GREEN),

            ("2 - MEDIUM", 280, YELLOW),

            ("3 - HARD", 490, RED),
        ]


        for label, x, color in difficulties:
            button = pygame.Rect(
                x,

                300,

                140,

                60,
            )

            pygame.draw.rect(
                screen,
                color,
                button,
                border_radius=8,
            )

            text = self.font.render(

                label,
                True,
                DARK_GRAY,
            )

            text_rect = text.get_rect(
                center=button.center,
            )

            screen.blit(
                text,
                text_rect,
            )

        instruction = self.font.render(
            "Choose 1, 2, or 3    |    ESC to exit",
            True,
            WHITE,
        )

        instruction_rect = instruction.get_rect(
            center=(self.width // 2, 420),
        )

        screen.blit(
            instruction,
            instruction_rect,
        )

    def render(self, screen):
        screen.fill(DARK_GRAY)

        if self.game_over:
            self._render_game_over(screen)
            return

        if self.difficulty_select:
            self._render_difficulty_select(screen)
            return

        self._render_gameplay(screen)
