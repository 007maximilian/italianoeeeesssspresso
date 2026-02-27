#!/bin/bash
echo "Building executable..."

# Установка зависимостей
pip install -r requirements.txt

# Сборка exe
pyinstaller coffee_app.spec

# Копируем в папку release
mkdir -p release
cp -r dist/CoffeeManager/* release/
cp data/coffee.sqlite release/data/
cp -r UI release/

echo "Executable built successfully in release/ folder!"
