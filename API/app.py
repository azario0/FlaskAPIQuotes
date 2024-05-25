from flask import Flask, jsonify
import mysql.connector
import random

app = Flask(__name__)

# MySQL database configuration
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'quotes_db'
}

def get_db_connection():
    """Establish a connection to the MySQL database."""
    connection = mysql.connector.connect(**db_config)
    return connection

@app.route('/random-quote', methods=['GET'])
def get_random_quote():
    """Fetch a random quote from the database."""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Get the total number of quotes
    cursor.execute("SELECT COUNT(*) AS count FROM quotes")
    result = cursor.fetchone()
    count = result['count']
    
    # Fetch a random quote
    random_index = random.randint(0, count - 1)
    cursor.execute("SELECT text, author FROM quotes LIMIT %s, 1", (random_index,))
    quote = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    return jsonify(quote)

if __name__ == '__main__':
    app.run(debug=True)
