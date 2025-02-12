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

Deploying Kafka with KRaft with Docker: https://dev.to/deeshath/apache-kafka-kraft-mode-setup-5nj
Change Data Capture with Debezuim: https://medium.com/geekculture/listen-to-database-changes-with-apache-kafka-35440a3344f0

Facker to Fake data

1. The airline has 300 flights - Create 300 flights and store in the DB
2. The airline flyes to many destinations in europe and all around the world. It flies to 200 destinations domectic and global
3. Write a scheduling algorithm. Write a code to find the flying time between destination. consider the factors
4. Fly airplanes with full capacity