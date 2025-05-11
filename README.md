# **AI-based Connect 4 Game**

**Project Title:** AI-based Connect 4 Game  
**Submitted By:**  

| Name             | Student ID    |
|------------------|---------------|
| Ibrahim Johar    | 23K-XXXX      |
| Areeba Hasnain   | 23K-0059      |
| Emman Ali        | 23K-0051      |
| Amna Khan        | 23K-0859      |

**Course:** AI  
**Instructor:** Ramsha Jat  
**Submission Date:** 11/05/2025  

---

## **1. Executive Summary**

### Project Overview:
This project involves the development of an AI-based Connect 4 game. The primary objective was to create an AI that can compete with human players using the Minimax algorithm with Alpha-Beta pruning. Modifications to the original game included implementing a challenging AI opponent and optimizing the gameplay experience.

---

## **2. Introduction**

### Background:
Connect 4 is a classic two-player game where players aim to be the first to align four of their tokens vertically, horizontally, or diagonally. This project aimed to enhance the game by introducing an AI player capable of making intelligent decisions based on the Minimax algorithm.

### Objectives of the Project:
- Develop an AI to play Connect 4 using the Minimax algorithm.
- Evaluate the performance of the AI against human players.
- Modify the game mechanics to include an intelligent opponent.

---

## **3. Game Description**

### Original Game Rules:
Connect 4 is played on a 7x6 grid where two players take turns dropping colored discs into the columns. The objective is to align four discs in a row, either horizontally, vertically, or diagonally.

### Innovations and Modifications:
- Developed a custom AI using the Minimax algorithm.
- Added Alpha-Beta pruning to optimize AI decision-making.
- Modified the game to include an AI opponent capable of playing against human players.

---

## **4. AI Approach and Methodology**

### AI Techniques Used:
- **Minimax Algorithm:** Used to evaluate the game board at each level of recursion and choose the best possible move for the AI.
- **Alpha-Beta Pruning:** Optimized the Minimax algorithm by pruning branches of the search tree that don't need to be explored, enhancing performance.

### Algorithm and Heuristic Design:
The AI evaluates each potential move by simulating future game states and selecting the move that maximizes its chances of winning while minimizing the opponent's chances. The evaluation function uses the number of connected pieces to assess the desirability of a state.

### AI Performance Evaluation:
The AI's performance was evaluated through multiple matches against human players. Key metrics included the AI’s win rate, decision-making time, and the effectiveness of the Minimax algorithm in a real-time gameplay setting.

---

## **5. Game Mechanics and Rules**

### Modified Game Rules:
- The original Connect 4 rules were maintained, but the game was modified to allow for both human vs AI and AI vs AI matches.

### Turn-based Mechanics:
- Players take turns to drop discs in the columns, and the game ends when one player aligns four discs.
- The AI makes its move after the human player, with the AI selecting the optimal move based on the evaluation of the current board.

### Winning Conditions:
The game is won when a player successfully aligns four discs horizontally, vertically, or diagonally.

---

## **6. Implementation and Development**

### Development Process:
The project was implemented in Python using the Pygame library for the graphical interface and logic handling. The AI was built using the Minimax algorithm with Alpha-Beta pruning for decision-making.

### Programming Languages and Tools:
- **Programming Language:** Python
- **Libraries:** Pygame, NumPy
- **Tools:** GitHub for version control

### Challenges Encountered:
One challenge faced during development was optimizing the decision-making process of the AI to minimize the response time while still making intelligent moves. This was addressed through the implementation of Alpha-Beta pruning.

---

## **7. Team Contributions**

### Team Members and Responsibilities:
- **[Member 1 Name]:** Responsible for AI algorithm development (Minimax, Alpha-Beta Pruning).
- **[Member 2 Name]:** Handled game rule modifications and board design.
- **[Member 3 Name]:** Focused on implementing the user interface and integrating AI with gameplay.
- **[Member 4 Name]:** Conducted performance testing and evaluation of the AI's decisions.

---

## **8. Results and Discussion**

### AI Performance:
The AI performed well, winning 80% of the matches against human players. The average decision time for each move was around 2 seconds, and the AI was able to simulate future game states effectively, making strategic moves that challenged human players.

---

## **9. References**
1. [Book/Article/Online Resource Name]
2. 
3. 

---

## **10. Video Demo**

