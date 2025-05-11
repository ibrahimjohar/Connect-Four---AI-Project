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
This project involves building an AI-based Connect 4 game with a computer opponent powered by the Minimax algorithm and Alpha-Beta pruning. The original two player rules were retained, but the game was enhanced with a smart AI that evaluates board states and makes optimal moves. Key goals included improving AI decision speed, maintaining smooth gameplay, and testing performance against human players.

---

## **2. Introduction**

### Background:
Connect 4 is a classic two player game where players take turns dropping colored discs into a 7x6 grid, aiming to align four discs in a row either horizontally, vertically, or diagonally. This project was chosen due to its clear game logic and suitability for implementing decision making algorithms. The goal was to enhance the standard game by introducing an AI opponent capable of playing intelligently using a search-based algorithm.

### Objectives of the Project:
- Build an AI opponent using the Minimax algorithm with Alpha-Beta pruning  
- Design and implement a user friendly interface for smooth gameplay  
- Integrate the AI with the UI to enable human vs AI matches  
- Evaluate the AI’s performance against human players  
- Optimize decision making speed and responsiveness

---

## **3. Game Description**

### Original Game Rules:
Connect 4 is a two-player game played on a 7x6 grid. Each player takes turns dropping a colored disc into one of the columns. The disc falls to the lowest available space in the column. The objective is to align four of the player's discs in a row, either horizontally, vertically, or diagonally.

### Innovations and Modifications:
- Introduced an AI opponent powered by the Minimax algorithm with Alpha-Beta pruning to make intelligent, optimal moves.
- Added a single-player mode where a player competes against the AI.
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
  
### Turn-based Mechanics:
- The game alternates turns between the two players.
- On each turn, the player (or AI) selects a column to drop a disc, and the disc falls to the lowest available row in that column.
- The AI makes its move immediately after the human player, using the decision making algorithm to select the best move.
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
- **Emman Ali:** Responsible for AI algorithm development (Minimax, Alpha-Beta Pruning).
- **Amna Khan:** Handled game rule modifications and board design.
- **Ibrahim Johar:** Focused on implementing the user interface and integrating AI with gameplay.
- **Areeba Hasnain:** Conducted performance testing and evaluation of the AI's decisions.

---

## **8. Results and Discussion**

### AI Performance and Multi-Player Setting:
The AI’s performance was evaluated through multiple matches against human players at varying difficulty levels, and the results are summarized below:

- **Win Rate**:
  - **Easy Level**: The AI won **30%** of the matches, playing more passively and allowing human players to win most of the time.
  - **Medium Level**: The AI won **70%** of the matches, making intermediate-level strategic moves and leading to more competitive matches.
  - **Hard Level**: The AI won **90%** of the matches, playing optimally and consistently challenging human players by evaluating multiple future moves to select the best course of action.

- **Decision-Making Time**: The AI made optimal moves with an average decision-making time of **1 second** per move, ensuring smooth gameplay.

- **Effectiveness**: The AI demonstrated its strategic depth, including blocking opponent moves and setting up winning opportunities. The implementation of **Alpha-Beta pruning** allowed the AI to evaluate multiple game states quickly, improving performance without compromising on decision quality.

Overall, the AI's performance was highly satisfactory, providing a challenging and enjoyable experience for players at all levels. The use of the **Minimax algorithm** with **Alpha-Beta pruning** allowed the AI to make intelligent decisions in real-time, adapting its strategy based on the difficulty level.

---

## **9. References**
1. 
2. 
3. 

---

## **10. Video Demo**

