# Gesture-Controlled Pong Game

This repository contains a Gesture-Based Pong Game developed using Python, Pygame, and MediaPipe. The game allows players to control the paddle in a Pong-like game using hand movements detected by a webcam, providing an immersive hands-free gaming experience.

## Features

- **Gesture-Based Control**: Move the paddle by waving your hand in front of the webcam.
- **Ball Movement and Collision**: Ball bounces off the walls and paddle, with score tracking.
- **Game Over Screen**: When lives are lost, a "Game Over" message is displayed with options to restart or quit the game.
- **Audio Feedback**: Voice notifications for game states like "Start Game", "Restarting Game", and "Game Over".
- **Difficulty Levels**: The ball speed increases as you score points.

## Technologies Used

- **Pygame**: For game development and rendering.
- **OpenCV**: For accessing the webcam and capturing real-time images.
- **MediaPipe**: For hand detection and gesture recognition.
- **Pyttsx3**: For generating audio feedback (text-to-speech).

## How to Run the Game

### Prerequisites

Ensure you have the following libraries installed:

```bash
pip install pygame opencv-python mediapipe pyttsx3 numpy
```
## Authors
- Nagulapally Bhargavi
