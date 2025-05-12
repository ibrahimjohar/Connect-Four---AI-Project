# **AI-based Connect 4 Game**

**Project Title:** AI-based Connect 4 Game  
**Submitted By:**  

| Name             | Student ID    |
|------------------|---------------|
| Ibrahim Johar    | 23K-0074      |
| Areeba Hasnain   | 23K-0059      |
| Emman Ali        | 23K-0051      |
| Amna Khan        | 23K-0859      |

**Course:** AI  
**Instructor:** Ramsha Jat  
**Submission Date:** 11/05/2025  

---

## **1. Executive Summary**

### Project Overview:
This project involves building an AI-based Connect 4 game with a computer opponent powered by the Minimax algorithm and Alpha-Beta pruning. The original two-player rules were retained, but the game was enhanced with multiple game modes including Human vs AI, User vs User, and AI vs AI. Key goals included improving AI decision speed, enabling flexible game modes, maintaining smooth gameplay, and testing AI performance under different scenarios.

---

## **2. Introduction**

### Background:
Connect 4 is a classic two player game where players take turns dropping colored discs into a 7x6 grid, aiming to align four discs in a row either horizontally, vertically, or diagonally. This project was chosen due to its clear game logic and suitability for implementing decision making algorithms. The goal was to enhance the standard game by introducing an AI opponent capable of playing intelligently using a search-based algorithm.

### Objectives of the Project:
- Build an AI opponent using the Minimax algorithm with Alpha-Beta pruning  
- Design and implement a user friendly interface for smooth gameplay  
- Integrate three modes: Human vs AI, User vs User, and AI vs AI
- Evaluate the AI’s performance against human players  
- Optimize decision making speed and responsiveness

---

## **3. Game Description**

### Original Game Rules:
Connect 4 is a two-player game played on a 7x6 grid. Each player takes turns dropping a colored disc into one of the columns. The disc falls to the lowest available space in the column. The objective is to align four of the player's discs in a row, either horizontally, vertically, or diagonally.

### Innovations and Modifications:
Introduced an AI opponent powered by the Minimax algorithm with Alpha-Beta pruning to make intelligent, optimal moves.
- Added a single-player mode where a player competes against the AI.
- **Added a multiplayer (Human vs Human) mode for local play.**
- **Implemented an AI vs AI mode to observe strategy simulations.**
- Designed an intuitive user interface with graphical representations of the game board, discs, and turn indicators.
- Optimized the AI’s decision making for faster response times while maintaining strategic depth.
- Included three difficulty levels: **Easy, Medium, and Hard** for varied challenges.
- Allowed players to choose their preferred color for the game pieces, enhancing customization.

---

## **4. AI Approach and Methodology**

### AI Techniques Used:
The AI for this Connect 4 game was implemented using the **Minimax algorithm** with **Alpha-Beta pruning**. This algorithm evaluates all possible moves by simulating future game states and selecting the best move for the AI. Alpha-Beta pruning was added to optimize performance by eliminating branches of the game tree that do not need to be explored, reducing computation time.

### Algorithm and Heuristic Design:
The decision making process involves evaluating the game board for each potential move. The AI uses a heuristic evaluation function that assigns scores to each board state based on:
- The number of connected pieces (horizontally, vertically, diagonally) for both the AI and the opponent.
- A higher score is assigned if the AI can create a winning move or block the opponent from winning.
- The AI also attempts to control the center of the board, as it provides more opportunities for future moves.

The AI recursively explores the game tree, simulating each possible move and evaluating the resulting board states to choose the move with the best score.

### AI Performance Evaluation:
The performance of the AI was evaluated through several matches against human players. The evaluation metrics included:
- **Win Rate:** The AI won 80% of the matches played against human players.
- **Decision Time:** The AI was able to make decisions within 1 second on average, ensuring smooth gameplay.
- **Effectiveness:** The AI demonstrated strategic play, including blocking opponent’s moves and setting up future winning moves.

---

## **5. Game Mechanics and Rules**

### Modified Game Rules:
- The game retains the original rules of Connect 4, where players drop colored discs into a 7x6 grid.
- The main modification was the introduction of an AI opponent, which uses the **Minimax algorithm with Alpha-Beta pruning** to make intelligent decisions.
- Three gameplay modes are available:
  - **Human vs AI**
  - **Human vs Human**
  - **AI vs AI**
  
### Turn-based Mechanics:
- The game alternates turns between two players or between a player and the AI.
- On each turn, the current player selects a column to drop a disc, and the disc falls to the lowest available row in that column.
- In AI modes, the AI makes its move immediately using the decision making algorithm.
- The game continues until a player aligns four discs in a row or all columns are filled.

### Winning Conditions:
- The game ends when a player aligns four discs either horizontally, vertically, or diagonally.
- The player who aligns four discs first is declared the winner.
- If the grid is filled without either player winning, the game results in a draw.
  
---

## **6. Implementation and Development**

### Development Process:
The development process started with designing the game mechanics and user interface. We chose Python as the programming language due to its simplicity and the availability of libraries like Pygame, which made the implementation of the game mechanics easy. The Minimax algorithm was used to create the AI, and Alpha-Beta pruning was integrated to optimize the decision making process. The game board, AI logic, and user interface were developed in parallel, with testing conducted after each phase to ensure functionality.

### Programming Languages and Tools:
- **Programming Language:** Python  
- **Libraries:** Pygame (for graphical user interface and game mechanics)  
- **Tools:**
  - **Version Control:** GitHub for managing code versions and collaboration  
  - **Code Editor:** VS Code for writing and editing the project code  

### Challenges Encountered:
One of the main challenges encountered was optimizing the performance of the Minimax algorithm to reduce the decision-making time while ensuring that the AI still played strategically. Implementing Alpha-Beta pruning helped in improving the speed of the AI's decisions. Additionally, creating a smooth user interface with Pygame required careful consideration of event handling and rendering graphics efficiently.

---

## **7. Team Contributions**

### Team Members and Responsibilities:
- **Emman Ali**  
  Implemented the board management system that maintains the game state, validates moves, detects win conditions, and evaluates board positions to support AI strategies.

- **Areeba Hasnain**  
  Integrated the Minimax and Alpha-Beta Pruning algorithms into different game modes and ensured smooth functionality across difficulty levels.

- **Ibrahim Johar**  
  Designed and developed the user interface and handled integration of the AI logic with interactive gameplay for a seamless player experience.

- **Amna Khan**  
  Conducted performance testing and evaluation of the AI across various difficulty levels and modes, including statistical analysis of win rates compared to human players.

---

## **8. Results and Discussion**

### AI Performance and Multi-Player Setting:
The AI’s performance was evaluated through multiple matches against human players at varying difficulty levels, and the results are summarized below:

- **Win Rate Analysis (Based on AI Search Depth)**:
  - **Easy Level (Depth 1)**: The AI won approximately **15%** of the matches. With minimal foresight, it made basic decisions, resulting in a higher chance for human players to win.
  - **Medium Level (Depth 3)**: The AI achieved a win rate of around **60%**, using moderate lookahead to make smarter, more strategic moves that created balanced and competitive gameplay.
  - **Hard Level (Depth 5)**: The AI dominated with an **85%** win rate, evaluating deeper game trees and consistently selecting optimal moves, making it significantly more challenging for human opponents.

- **Decision-Making Time**: The AI made optimal moves with an average decision-making time of **1 second** per move, ensuring smooth gameplay.

- **Effectiveness**: The AI demonstrated its strategic depth, including blocking opponent moves and setting up winning opportunities. The implementation of **Alpha-Beta pruning** allowed the AI to evaluate multiple game states quickly, improving performance without compromising on decision quality.

- **User vs User Mode**: This mode allows two human players to play locally on the same device, making the game more inclusive and social.

- **AI vs AI Mode**: Useful for observing how different strategies play out at different difficulty levels, this mode demonstrates the AI’s reasoning and decision-making in a competitive environment.

---

## **9. References**
1. https://youtu.be/STjW3eH0Cik?si=ftXH2LIzpUntBnrs
2. https://youtu.be/tDv7lrklaQE?si=FLQk_-NtNbqfzier
3. https://youtu.be/xBXHtz4Gbdo?si=lrK357VH_7Z4O9xI
4. https://youtu.be/JC1QsLOXp-I?si=Av-grFz5l5r6xW_4
5. https://youtu.be/FfWpgLFMI7w?si=86ivj_5_R5oLJ0rt

---

## **10. Video Demo**
Attached in repository.
