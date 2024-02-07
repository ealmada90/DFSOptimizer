from flask import Flask, request, jsonify
from Optimizer import *

app = Flask(__name__)

@app.route('/optimize', methods=['POST'])
def optimize_dfs_lineup():
    data = request.get_json()

    # Extract data from the JSON payload (adjust as needed)
    players = data['players']
    settings = data['settings']

    # ... (use your PuLP optimization code here)
    lineups = optimizerLineups(playerList=players, optimizer_settings=settings)
    
    # Return the result as JSON (adjust as needed)
    result = {'status': 'success', 'lineups': lineups}
    return jsonify(result)

@app.route('/test', methods=['GET'])
def testOptimizer():
    data = request.get_json()

    # Extract data from the JSON payload (adjust as needed)
    players = data['players']
    projected_points = data['projected_points']
    salary = data['salary']
    position_limits = data['position_limits']
    salary_cap = data['salary_cap']

    # ... (use your PuLP optimization code here)
    lineups = optimizerLineups()
    
    # Return the result as JSON (adjust as needed)
    result = {'status': 'success', 'lineups': lineups}
    return jsonify(result)

if __name__ == '__main__':
    
    app.run(debug=True)
