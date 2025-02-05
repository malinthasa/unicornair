#!/bin/bash

echo "🚨 WARNING: This will remove ALL Docker containers, images, volumes, and networks!"
read -p "Are you sure you want to proceed? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
  echo "❌ Aborted."
  exit 1
fi

echo "🛑 Stopping all running containers..."
docker stop $(docker ps -aq) 2>/dev/null

echo "🗑️ Removing all containers..."
docker rm -f $(docker ps -aq) 2>/dev/null

echo "🗑️ Removing all images..."
docker rmi -f $(docker images -aq) 2>/dev/null

echo "🗑️ Removing all volumes..."
docker volume rm $(docker volume ls -q) 2>/dev/null

echo "🗑️ Removing all networks (except default)..."
docker network rm $(docker network ls -q) 2>/dev/null

echo "🧹 Pruning dangling images..."
docker image prune -f

echo "🧹 Pruning dangling volumes..."
docker volume prune -f

echo "🧹 Cleaning up Docker build cache..."
docker builder prune -af

echo "✅ Docker cleanup complete!"

echo "🔍 Verifying cleanup..."
docker ps -a
docker images
docker volume ls
docker network ls
