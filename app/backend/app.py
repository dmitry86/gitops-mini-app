import os
from flask import Flask, request, jsonify
import psycopg2
import psycopg2.extras

app = Flask(__name__)

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://football:football@postgres:5432/football"
)

def get_db():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            id SERIAL PRIMARY KEY,
            match_date DATE NOT NULL,
            opponent VARCHAR(100) NOT NULL,
            our_score INTEGER NOT NULL,
            opponent_score INTEGER NOT NULL,
            player_goals INTEGER NOT NULL DEFAULT 0,
            player_assists INTEGER NOT NULL DEFAULT 0,
            notes TEXT DEFAULT ''
        )
    """)

    conn.commit()
    cur.close()
    conn.close()

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/api/matches", methods=["GET"])
def matches():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT *
        FROM matches
        ORDER BY match_date DESC, id DESC
    """)

    data = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(data)

@app.route("/api/matches", methods=["POST"])
def add_match():
    data = request.get_json()

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        INSERT INTO matches (
            match_date,
            opponent,
            our_score,
            opponent_score,
            player_goals,
            player_assists,
            notes
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        RETURNING *
    """, (
        data["match_date"],
        data["opponent"],
        data["our_score"],
        data["opponent_score"],
        data.get("player_goals", 0),
        data.get("player_assists", 0),
        data.get("notes", "")
    ))

    match = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return jsonify(match), 201

@app.route("/api/stats")
def stats():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT
            COUNT(*) AS matches,
            COUNT(*) FILTER (WHERE our_score > opponent_score) AS wins,
            COUNT(*) FILTER (WHERE our_score = opponent_score) AS draws,
            COUNT(*) FILTER (WHERE our_score < opponent_score) AS losses,
            COALESCE(SUM(our_score), 0) AS goals_for,
            COALESCE(SUM(opponent_score), 0) AS goals_against,
            COALESCE(SUM(player_goals), 0) AS player_goals,
            COALESCE(SUM(player_assists), 0) AS player_assists
        FROM matches
    """)

    result = cur.fetchone()

    cur.close()
    conn.close()

    return jsonify(result)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8000)
