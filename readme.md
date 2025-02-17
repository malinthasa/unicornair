UnicornAir schedules flights with different airports (at the moment, there is a script to generate the list for the given day)

Each airport that has a schedules flight today sends a report about the status of the flights until the end of day

https://youtu.be/GqAcTrqKcrY?si=DAVCmvbBgVbm3sDe


Docker Clean

1. Stop all containers - `docker rm -f $(docker ps -aq)`
2. Remove all containers - `docker rm -f $(docker ps -aq)`
3. Remove all images - `docker rmi -f $(docker images -aq)`
4. Remove all volumes - `docker volume rm $(docker volume ls -q)`
5. Remove all networks - `docker network rm $(docker network ls -q)`
6. Clean dangling images - `docker image prune -f`
7. Clear build cache - `docker builder prune -af`
8. Remove all volumes - `docker volume prune -f`

Single command - `docker system prune -a --volumes -f`

1. Take all Schedules