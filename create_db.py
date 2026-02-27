import sqlite3

conn = sqlite3.connect('coffee.sqlite')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS coffee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roast_level TEXT NOT NULL,
    ground_or_beans TEXT NOT NULL,
    taste_description TEXT,
    price REAL NOT NULL,
    package_volume INTEGER NOT NULL
)
''')

coffees = [
    ('Colombia Supremo', 'Medium', 'beans', 'Шоколад, орехи, карамель', 850, 250),
    ('Ethiopia Yirgacheffe', 'Light', 'ground', 'Цитрус, жасмин, бергамот', 950, 200),
    ('Brazil Santos', 'Dark', 'beans', 'Горький шоколад, орехи', 750, 500),
    ('Kenya AA', 'Medium', 'beans', 'Ягоды, вино, цитрус', 1100, 250),
    ('Guatemala Antigua', 'Medium-Dark', 'ground', 'Какао, специи, карамель', 890, 300),
    ('Sumatra Mandheling', 'Dark', 'beans', 'Травы, табак, пряности', 980, 250),
    ('Costa Rica Tarrazu', 'Light', 'beans', 'Фрукты, мед, цветы', 1050, 200),
    ('Tanzania Peaberry', 'Medium', 'ground', 'Ягоды, вино, специи', 1150, 250)
]

cursor.executemany('INSERT INTO coffee (name, roast_level, ground_or_beans, taste_description, price, package_volume) VALUES (?, ?, ?, ?, ?, ?)', coffees)
conn.commit()
conn.close()
print("Database created successfully!")
