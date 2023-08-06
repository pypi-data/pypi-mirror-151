#! /bin/python3
####################################
# Script to benchmark hecho-events #
####################################

import time
from hecho_events.main import RasaEventBroker
import events_helper
import asyncio

API_KEY="b35a3df8-91c6-4042-b0e0-fb41cea2dd8c"
API_URL="https://dev.hecho.ml/api"


class HechoBrokerBenchmark:
    def __init__(self, n_users: int, n_messages_per_user: int, broker_send_interval: int, broker_max_queue_size: int, enable_debug: bool) -> None:
        self.n_users = n_users
        self.n_messages_per_user = n_messages_per_user
        self.broker = RasaEventBroker(API_KEY, API_URL, enable_debug=enable_debug, send_interval=broker_send_interval, max_queue_size=broker_max_queue_size)
        self.enable_debug=enable_debug

    def run(self):
        print(f"Starting hecho-events benchmark with {self.n_users} users sending {self.n_messages_per_user} messages each.")

        loop = asyncio.get_event_loop()

        self.start_time = time.time()
        loop.run_until_complete(self._run_users())

        # Run pending loop tasks
        pending = asyncio.all_tasks(loop)
        loop.run_until_complete(asyncio.gather(*pending))

        self.end_time = time.time()
        return self

    def debug(self, str):
        if self.enable_debug:
            print(str)

    def report(self):
        total_time = self.end_time - self.start_time
        expected_events = self.n_users * self.n_messages_per_user*2 + self.n_users
        total_events = self.broker.events_count
        send_events = self.broker.send_events_count
        failed_events = total_events - send_events
        throughput = total_events/total_time
        total_requests = self.broker.requests_count

        print("-------------------------------------------------")
        print(f"Users: {self.n_users}")
        print(f"Messages per user: {self.n_messages_per_user}")
        print(f"Benchmark done, took {total_time} seconds")
        print(f"Total time: {total_time * 1000} ms")
        print(f"Expected events: {expected_events}")
        print(f"Total events: {total_events}")
        print(f"Send events: {send_events}")
        print(f"Failed events: {failed_events}")
        print(f"Total Requests: {total_requests}")
        print(f"Throughput [events/second]: {throughput}")
        print("-------------------------------------------------")

    async def _run_users(self):
        for user_id in range(self.n_users):
            await self._simulate_user(user_id)
            self.debug(f"User {user_id} sent {self.n_messages_per_user} messages")
        self.debug('All users done!')
        await self.broker.close()

    async def _simulate_user(self, user_id):
        sender_id = f"bench_{events_helper.get_random_string(26)}"
        self.broker.publish(events_helper.make_start_event(sender_id))
        for i in range(self.n_messages_per_user):
            self.broker.publish(events_helper.make_user_message(f"Mensagem {i} do usuário {user_id}", sender_id))
            self.broker.publish(events_helper.make_bot_message(f"Resposta {i} do bot ao usuário {user_id}", sender_id))



def main():
    ENABLE_DEBUG = False
    HechoBrokerBenchmark(n_users=5, n_messages_per_user=100, broker_max_queue_size=100, broker_send_interval=5, enable_debug=ENABLE_DEBUG).run().report()

    HechoBrokerBenchmark(n_users=5, n_messages_per_user=1000, broker_max_queue_size=100, broker_send_interval=5, enable_debug=ENABLE_DEBUG).run().report()

    HechoBrokerBenchmark(n_users=50, n_messages_per_user=1000, broker_max_queue_size=100, broker_send_interval=5, enable_debug=ENABLE_DEBUG).run().report()



main()
