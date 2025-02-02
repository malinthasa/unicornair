🚩 Problems in the Legacy System (Without Kafka)
The current implementation demonstrates several limitations typical of legacy architectures, especially when compared to a Kafka-powered event-driven system.

1️⃣ Polling Inefficiency vs. Real-Time Streaming
Legacy System (Current):

Uses periodic polling to check the API for flight status updates (every 5 minutes).
This causes unnecessary load on the database and API, even when there's no new data.
Kafka-Based System:

Real-time data streaming with event-driven architecture.
As soon as a flight status changes, an event is published to a Kafka topic.
Consumers (like the notification service) react instantly without constant polling.
Impact:
Polling delays notifications and consumes unnecessary resources. Kafka reduces latency to near real-time.

2️⃣ Tight Coupling vs. Loose Coupling
Legacy System:

The notification service is tightly coupled with the API and database schema.
Any change in the API requires code modifications across multiple services.
Kafka-Based System:

Loose coupling through Kafka topics.
Producers (flight status services) and consumers (notification service, dashboards, etc.) communicate via Kafka without knowing each other's internal logic.
Impact:
Tight coupling makes the system hard to scale and maintain. Kafka improves modularity and flexibility.

3️⃣ Scalability Challenges
Legacy System:

Adding more notification channels (SMS, mobile push, etc.) would require duplicate polling logic.
High traffic leads to API bottlenecks.
Kafka-Based System:

Kafka can handle millions of messages per second.
New consumers (like SMS services) simply subscribe to the topic without affecting existing services.
Impact:
Legacy systems struggle under load. Kafka handles large-scale data distribution effortlessly.

4️⃣ Lack of Fault Tolerance
Legacy System:

If the notification service crashes, it may miss updates that occurred during downtime.
No built-in message retry mechanism.
Kafka-Based System:

Kafka provides message durability and replayability.
Consumers can reprocess events from Kafka if they go down and recover.
Impact:
Legacy systems risk data loss. Kafka ensures reliable message delivery even during failures.

5️⃣ Limited Observability
Legacy System:

Hard to track message flows or debug why a notification wasn’t sent.
Relies on database logs and manual tracking.
Kafka-Based System:

Kafka offers built-in monitoring tools (e.g., Kafka Connect, Kafka Streams).
You can trace every event from producer to consumer.
Impact:
Troubleshooting in legacy systems is complex. Kafka improves visibility and observability.