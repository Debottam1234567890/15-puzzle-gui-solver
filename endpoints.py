from flask import Flask, render_template_string, request, jsonify
import time
import os

app = Flask(__name__)

# Goal configuration
goal = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 0]
]
goal_positions = {val: (i, j) for i, row in enumerate(goal) for j, val in enumerate(row)}

def manhattan_linear_conflict(puzzle):
    dist = 0
    for i in range(4):
        for j in range(4):
            val = puzzle[i][j]
            if val == 0:
                continue
            goal_i, goal_j = goal_positions[val]
            dist += abs(goal_i - i) + abs(goal_j - j)
            if goal_i == i:
                for k in range(j + 1, 4):
                    other = puzzle[i][k]
                    if other != 0 and goal_positions[other][0] == i and goal_positions[other][1] < goal_j:
                        dist += 2
            if goal_j == j:
                for k in range(i + 1, 4):
                    other = puzzle[k][j]
                    if other != 0 and goal_positions[other][1] == j and goal_positions[other][0] < goal_i:
                        dist += 2
    return dist

def is_goal(p):
    return p == goal

def get_neighbors(board):
    neighbors = []
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                x, y = i, j
                directions = [(-1, 0, 'up'), (1, 0, 'down'), (0, -1, 'left'), (0, 1, 'right')]
                for dx, dy, move in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 4 and 0 <= ny < 4:
                        new_board = [row[:] for row in board]
                        new_board[x][y], new_board[nx][ny] = new_board[nx][ny], new_board[x][y]
                        neighbors.append((new_board, move))
    return neighbors

def ida_star(start):
    threshold = manhattan_linear_conflict(start)
    path = [(start, None)]
    
    def search(path, g, threshold):
        node, _ = path[-1]
        f = g + manhattan_linear_conflict(node)
        if f > threshold:
            return f
        if is_goal(node):
            return "FOUND"
        min_cost = float('inf')
        for neighbor, move in get_neighbors(node):
            if any(prev[0] == neighbor for prev in path):
                continue
            path.append((neighbor, move))
            temp = search(path, g + 1, threshold)
            if temp == "FOUND":
                return "FOUND"
            if temp < min_cost:
                min_cost = temp
            path.pop()
        return min_cost
    
    iterations = 0
    while iterations < 50:  # Limit iterations for web safety
        temp = search(path, 0, threshold)
        if temp == "FOUND":
            return [m for _, m in path[1:]]
        if temp == float('inf'):
            return None
        threshold = temp
        iterations += 1
    return None

HOME_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>15 Puzzle Solver - Home</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .navbar {
            background: rgba(255, 255, 255, 0.95);
            padding: 15px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        .navbar-content {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 20px;
        }
        .navbar-brand {
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
            text-decoration: none;
        }
        .navbar-links {
            display: flex;
            gap: 30px;
        }
        .navbar-links a {
            color: #333;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
        }
        .navbar-links a:hover {
            color: #667eea;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        .hero {
            text-align: center;
            color: white;
            margin-bottom: 60px;
            padding: 40px 0;
        }
        .hero h1 {
            font-size: 3.5em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        .hero p {
            font-size: 1.3em;
            opacity: 0.95;
        }
        .card {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }
        .card h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 2em;
        }
        .card h3 {
            color: #764ba2;
            margin-top: 30px;
            margin-bottom: 15px;
            font-size: 1.5em;
        }
        .card p {
            line-height: 1.8;
            color: #333;
            margin-bottom: 15px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin-top: 30px;
        }
        .stat-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
        }
        .stat-number {
            font-size: 3em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .stat-label {
            font-size: 1.1em;
            opacity: 0.95;
        }
        .info-box {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 25px;
            border-radius: 15px;
            border-left: 5px solid #667eea;
        }
        .info-box h4 {
            color: #667eea;
            margin-bottom: 12px;
            font-size: 1.3em;
        }
        .info-box p {
            font-size: 0.95em;
            color: #555;
            line-height: 1.6;
        }
        .timeline {
            position: relative;
            padding: 20px 0;
        }
        .timeline-item {
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
        }
        .timeline-year {
            font-weight: bold;
            color: #667eea;
            font-size: 1.2em;
            margin-bottom: 8px;
        }
        .cta-button {
            display: inline-block;
            padding: 15px 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 30px;
            font-weight: bold;
            font-size: 1.1em;
            margin-top: 20px;
            transition: transform 0.2s;
        }
        .cta-button:hover {
            transform: scale(1.05);
        }
        .puzzle-visual {
            display: grid;
            grid-template-columns: repeat(4, 80px);
            gap: 5px;
            margin: 30px auto;
            justify-content: center;
        }
        .puzzle-tile {
            width: 80px;
            height: 80px;
            background: #667eea;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5em;
            font-weight: bold;
            border-radius: 8px;
        }
        .puzzle-tile.empty {
            background: #e0e0e0;
        }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="navbar-content">
            <a href="/" class="navbar-brand">🧩 15 Puzzle Solver</a>
            <div class="navbar-links">
                <a href="/">Home</a>
                <a href="/solve">Solve Puzzle</a>
            </div>
        </div>
    </nav>

    <div class="container">
        <div class="hero">
            <h1>🧩 The 15 Puzzle Solver</h1>
            <p>Explore the classic sliding puzzle with AI-powered solutions</p>
        </div>

        <div class="card">
            <h2>What is the 15 Puzzle?</h2>
            <p>The 15 Puzzle is a classic sliding puzzle consisting of a 4×4 grid with 15 numbered tiles and one empty space. The objective is to arrange the tiles in numerical order by sliding them into the empty space, one at a time.</p>
            
            <div class="puzzle-visual">
                <div class="puzzle-tile">1</div>
                <div class="puzzle-tile">2</div>
                <div class="puzzle-tile">3</div>
                <div class="puzzle-tile">4</div>
                <div class="puzzle-tile">5</div>
                <div class="puzzle-tile">6</div>
                <div class="puzzle-tile">7</div>
                <div class="puzzle-tile">8</div>
                <div class="puzzle-tile">9</div>
                <div class="puzzle-tile">10</div>
                <div class="puzzle-tile">11</div>
                <div class="puzzle-tile">12</div>
                <div class="puzzle-tile">13</div>
                <div class="puzzle-tile">14</div>
                <div class="puzzle-tile">15</div>
                <div class="puzzle-tile empty"></div>
            </div>
            
            <a href="/solve" class="cta-button">Solve Your Puzzle Now</a>
        </div>

        <div class="card">
            <h2>📊 By The Numbers</h2>
            <div class="grid">
                <div class="stat-box">
                    <div class="stat-number">150+</div>
                    <div class="stat-label">Years of History</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">20.9 Trillion</div>
                    <div class="stat-label">Possible Configurations</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">50%</div>
                    <div class="stat-label">Are Solvable</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">80</div>
                    <div class="stat-label">Max Moves to Solve</div>
                </div>
            </div>
        </div>

        <div class="card">
            <h2>📜 A Brief History</h2>
            <div class="timeline">
                <div class="timeline-item">
                    <div class="timeline-year">1874</div>
                    <p>The 15 Puzzle was invented by Noyes Palmer Chapman, a postmaster in Canastota, New York. It quickly became a national craze in the United States.</p>
                </div>
                <div class="timeline-item">
                    <div class="timeline-year">1879</div>
                    <p>The puzzle gained worldwide popularity, causing a sensation across Europe and America. Employers complained that workers were neglecting their duties to solve the puzzle.</p>
                </div>
                <div class="timeline-item">
                    <div class="timeline-year">1879</div>
                    <p>American puzzle maker Sam Loyd falsely claimed to have invented the puzzle and offered a $1,000 prize for a solution to an impossible configuration (14 and 15 swapped).</p>
                </div>
                <div class="timeline-item">
                    <div class="timeline-year">1879</div>
                    <p>Mathematician William Woolsey Johnson and MIT professor William Story proved that exactly half of all starting positions are unsolvable, based on mathematical parity.</p>
                </div>
                <div class="timeline-item">
                    <div class="timeline-year">1986</div>
                    <p>Computer scientists proved that any solvable 15 Puzzle can be solved in 80 moves or fewer (God's Number for this puzzle).</p>
                </div>
                <div class="timeline-item">
                    <div class="timeline-year">2000s</div>
                    <p>The 15 Puzzle became a popular subject for AI research, testing various search algorithms including A*, IDA*, and pattern databases.</p>
                </div>
            </div>
        </div>

        <div class="card">
            <h2>🎯 Why People Love It</h2>
            <div class="grid">
                <div class="info-box">
                    <h4>🧠 Mental Exercise</h4>
                    <p>The puzzle provides excellent training for spatial reasoning, planning, and problem-solving skills.</p>
                </div>
                <div class="info-box">
                    <h4>🎮 Simple Yet Deep</h4>
                    <p>Easy to understand but challenging to master, with over 10 trillion solvable configurations.</p>
                </div>
                <div class="info-box">
                    <h4>📱 Timeless Appeal</h4>
                    <p>From wooden toys to smartphone apps, the puzzle has adapted to every generation for 150 years.</p>
                </div>
                <div class="info-box">
                    <h4>🏆 Competitive Challenge</h4>
                    <p>Speedsolvers compete globally, with world records under 10 seconds for solving scrambled puzzles.</p>
                </div>
                <div class="info-box">
                    <h4>🔬 Scientific Value</h4>
                    <p>Used extensively in computer science education to teach search algorithms and heuristics.</p>
                </div>
                <div class="info-box">
                    <h4>😌 Stress Relief</h4>
                    <p>The meditative quality of solving provides relaxation and a sense of accomplishment.</p>
                </div>
            </div>
        </div>

        <div class="card">
            <h2>🤖 About This Solver</h2>
            <p>This solver uses the <strong>IDA* (Iterative Deepening A*)</strong> algorithm with a sophisticated heuristic combining Manhattan Distance and Linear Conflict detection. This approach guarantees optimal solutions while being memory-efficient.</p>
            
            <h3>How It Works</h3>
            <p><strong>Manhattan Distance:</strong> Calculates the minimum number of moves each tile needs to reach its goal position (ignoring other tiles).</p>
            <p><strong>Linear Conflict:</strong> Detects when tiles in the same row or column need to pass each other, adding extra moves to the estimate.</p>
            <p><strong>IDA* Search:</strong> Explores possible move sequences depth-first, pruning paths that exceed the current cost threshold, then incrementally increases the threshold until a solution is found.</p>
            
            <h3>Performance</h3>
            <p>The solver can handle most puzzle configurations within seconds, finding optimal solutions with the fewest possible moves. For extremely difficult puzzles, solving may take longer due to the enormous search space.</p>
            
            <a href="/solve" class="cta-button">Try It Now</a>
        </div>
    </div>
</body>
</html>
'''

SOLVE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>15 Puzzle Solver - Solve</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .navbar {
            background: rgba(255, 255, 255, 0.95);
            padding: 15px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        .navbar-content {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 20px;
        }
        .navbar-brand {
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
            text-decoration: none;
        }
        .navbar-links {
            display: flex;
            gap: 30px;
        }
        .navbar-links a {
            color: #333;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
        }
        .navbar-links a:hover {
            color: #667eea;
        }
        .container {
            max-width: 1000px;
            margin: 40px auto;
            padding: 0 20px;
        }
        .card {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }
        .card h1 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .card h2 {
            color: #764ba2;
            margin-top: 30px;
            margin-bottom: 15px;
            font-size: 1.8em;
        }
        .card p {
            line-height: 1.8;
            color: #555;
            margin-bottom: 15px;
        }
        .input-section {
            margin: 30px 0;
        }
        label {
            display: block;
            color: #333;
            font-weight: 600;
            margin-bottom: 10px;
            font-size: 1.1em;
        }
        textarea {
            width: 100%;
            height: 150px;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            font-size: 1.1em;
            resize: vertical;
            transition: border-color 0.3s;
        }
        textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        .file-input {
            margin-top: 20px;
        }
        input[type="file"] {
            display: none;
        }
        .file-label {
            display: inline-block;
            padding: 12px 30px;
            background: #f5f7fa;
            color: #333;
            border: 2px solid #ddd;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .file-label:hover {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }
        .button-group {
            display: flex;
            gap: 15px;
            margin-top: 25px;
        }
        .btn {
            padding: 15px 40px;
            border: none;
            border-radius: 10px;
            font-size: 1.1em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
        }
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        .btn-secondary {
            background: #f5f7fa;
            color: #333;
            border: 2px solid #ddd;
        }
        .btn-secondary:hover {
            background: #e0e0e0;
        }
        .example-box {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            margin: 20px 0;
        }
        .example-box h4 {
            color: #667eea;
            margin-bottom: 10px;
        }
        .example-box pre {
            font-family: 'Courier New', monospace;
            font-size: 1.1em;
            color: #333;
            line-height: 1.8;
        }
        #result {
            margin-top: 30px;
            padding: 25px;
            background: #f8f9fa;
            border-radius: 10px;
            display: none;
        }
        #result.success {
            background: #d4edda;
            border: 2px solid #28a745;
        }
        #result.error {
            background: #f8d7da;
            border: 2px solid #dc3545;
        }
        #result h3 {
            color: #333;
            margin-bottom: 15px;
        }
        .loader {
            display: none;
            text-align: center;
            margin: 20px 0;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .puzzle-visualization {
            display: grid;
            grid-template-columns: repeat(4, 70px);
            gap: 5px;
            margin: 20px auto;
            justify-content: center;
        }
        .puzzle-tile {
            width: 70px;
            height: 70px;
            background: #667eea;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.3em;
            font-weight: bold;
            border-radius: 8px;
        }
        .puzzle-tile.empty {
            background: #e0e0e0;
        }
        .moves-list {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
        .move-item {
            padding: 10px;
            border-bottom: 1px solid #eee;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .move-item:last-child {
            border-bottom: none;
        }
        .move-number {
            font-weight: bold;
            color: #667eea;
        }
        .move-direction {
            text-transform: capitalize;
            color: #333;
        }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="navbar-content">
            <a href="/" class="navbar-brand">🧩 15 Puzzle Solver</a>
            <div class="navbar-links">
                <a href="/">Home</a>
                <a href="/solve">Solve Puzzle</a>
            </div>
        </div>
    </nav>

    <div class="container">
        <div class="card">
            <h1>🎯 Solve Your 15 Puzzle</h1>
            <p>Enter your puzzle configuration below. You can either type the numbers directly or upload a text file.</p>

            <div class="example-box">
                <h4>📝 Input Format:</h4>
                <pre>12 1 10 2
7 11 4 14
5 0 9 15
8 13 6 3</pre>
                <p style="margin-top: 10px; color: #666;">Use 0 to represent the empty space. Each row should have 4 numbers separated by spaces.</p>
            </div>

            <div class="input-section">
                <label for="puzzleInput">Puzzle Configuration:</label>
                <textarea id="puzzleInput" placeholder="Enter your puzzle configuration here..."></textarea>
                
                <div class="file-input">
                    <input type="file" id="fileInput" accept=".txt">
                    <label for="fileInput" class="file-label">📁 Or Upload a Text File</label>
                    <span id="fileName" style="margin-left: 15px; color: #666;"></span>
                </div>
            </div>

            <div class="button-group">
                <button class="btn btn-primary" onclick="solvePuzzle()">🚀 Solve Puzzle</button>
                <button class="btn btn-secondary" onclick="clearInput()">🗑️ Clear</button>
            </div>

            <div class="loader" id="loader">
                <div class="spinner"></div>
                <p style="margin-top: 15px; color: #667eea; font-weight: bold;">Solving puzzle... This may take a moment.</p>
            </div>

            <div id="result"></div>
        </div>
    </div>

    <script>
        document.getElementById('fileInput').addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                document.getElementById('fileName').textContent = file.name;
                const reader = new FileReader();
                reader.onload = function(e) {
                    document.getElementById('puzzleInput').value = e.target.result;
                };
                reader.readAsText(file);
            }
        });

        function clearInput() {
            document.getElementById('puzzleInput').value = '';
            document.getElementById('fileInput').value = '';
            document.getElementById('fileName').textContent = '';
            document.getElementById('result').style.display = 'none';
        }

        function visualizePuzzle(puzzle) {
            let html = '<div class="puzzle-visualization">';
            for (let i = 0; i < 4; i++) {
                for (let j = 0; j < 4; j++) {
                    const val = puzzle[i][j];
                    if (val === 0) {
                        html += '<div class="puzzle-tile empty"></div>';
                    } else {
                        html += `<div class="puzzle-tile">${val}</div>`;
                    }
                }
            }
            html += '</div>';
            return html;
        }

        async function solvePuzzle() {
            const input = document.getElementById('puzzleInput').value.trim();
            
            if (!input) {
                alert('Please enter a puzzle configuration or upload a file.');
                return;
            }

            document.getElementById('loader').style.display = 'block';
            document.getElementById('result').style.display = 'none';

            try {
                const response = await fetch('/api/solve', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ puzzle: input })
                });

                const data = await response.json();
                
                document.getElementById('loader').style.display = 'none';
                const resultDiv = document.getElementById('result');
                resultDiv.style.display = 'block';

                if (data.success) {
                    resultDiv.className = 'success';
                    let html = `
                        <h3>✅ Solution Found!</h3>
                        <p><strong>Number of moves:</strong> ${data.moves.length}</p>
                        <p><strong>Time taken:</strong> ${data.time.toFixed(2)} seconds</p>
                        <h4 style="margin-top: 20px;">Starting Configuration:</h4>
                        ${visualizePuzzle(data.puzzle)}
                        <div class="moves-list">
                            <h4>Solution Steps:</h4>
                    `;
                    
                    data.moves.forEach((move, index) => {
                        html += `
                            <div class="move-item">
                                <span class="move-number">Move ${index + 1}:</span>
                                <span class="move-direction">${move}</span>
                            </div>
                        `;
                    });
                    
                    html += '</div>';
                    resultDiv.innerHTML = html;
                } else {
                    resultDiv.className = 'error';
                    resultDiv.innerHTML = `
                        <h3>❌ Error</h3>
                        <p>${data.error}</p>
                    `;
                }
            } catch (error) {
                document.getElementById('loader').style.display = 'none';
                const resultDiv = document.getElementById('result');
                resultDiv.style.display = 'block';
                resultDiv.className = 'error';
                resultDiv.innerHTML = `
                    <h3>❌ Error</h3>
                    <p>An error occurred while solving the puzzle. Please try again.</p>
                `;
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HOME_TEMPLATE)

@app.route('/solve')
def solve():
    return render_template_string(SOLVE_TEMPLATE)

@app.route('/api/solve', methods=['POST'])
def api_solve():
    try:
        data = request.get_json()
        puzzle_text = data.get('puzzle', '')
        
        # Parse the puzzle input
        lines = [line.strip() for line in puzzle_text.strip().split('\n') if line.strip()]
        
        if len(lines) != 4:
            return jsonify({
                'success': False,
                'error': 'Puzzle must have exactly 4 rows.'
            })
        
        puzzle = []
        for line in lines:
            row = list(map(int, line.split()))
            if len(row) != 4:
                return jsonify({
                    'success': False,
                    'error': 'Each row must have exactly 4 numbers.'
                })
            puzzle.append(row)
        
        # Validate puzzle (check if all numbers 0-15 are present)
        flat = [num for row in puzzle for num in row]
        if sorted(flat) != list(range(16)):
            return jsonify({
                'success': False,
                'error': 'Puzzle must contain all numbers from 0 to 15 exactly once.'
            })
        
        # Check if puzzle is solvable
        inversions = 0
        flat_no_zero = [x for x in flat if x != 0]
        for i in range(len(flat_no_zero)):
            for j in range(i + 1, len(flat_no_zero)):
                if flat_no_zero[i] > flat_no_zero[j]:
                    inversions += 1
        
        # Find row of empty space (from bottom)
        empty_row = 0
        for i in range(4):
            if 0 in puzzle[i]:
                empty_row = 4 - i
                break
        
        # Puzzle is solvable if:
        # - Grid width is odd and inversions is even
        # - Grid width is even and (inversions + empty_row) is odd
        is_solvable = (inversions + empty_row) % 2 == 1
        
        if not is_solvable:
            return jsonify({
                'success': False,
                'error': 'This puzzle configuration is not solvable. Exactly half of all possible 15-puzzle configurations are unsolvable.'
            })
        
        # Solve the puzzle
        start_time = time.time()
        solution = ida_star(puzzle)
        end_time = time.time()
        
        if solution is None:
            return jsonify({
                'success': False,
                'error': 'No solution found within reasonable time. The puzzle may be too complex.'
            })
        
        return jsonify({
            'success': True,
            'moves': solution,
            'puzzle': puzzle,
            'time': end_time - start_time
        })
        
    except ValueError:
        return jsonify({
            'success': False,
            'error': 'Invalid input format. Please enter numbers only.'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        })

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
