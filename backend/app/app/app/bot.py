import logging
from telethon import TelegramClient, events, functions, types
from anthropic import AsyncAnthropic
import asyncio
import json
from datetime import datetime

from app.db import AsyncDatabaseSession
from app.models import Goal, Result, User
from app.settings import settings

logger = logging.getLogger(__name__)


class ServiceNegotiatorAgent:
    def __init__(self, anthropic_client, service_description):
        self.anthropic_client = anthropic_client
        self.service_description = service_description
        self.conversation_history = []
        self.negotiation_complete = False

    async def get_response(self, message):
        self.conversation_history.append({"role": "user", "content": message})

        # Create system prompt for AI
        system_prompt = f"""You are a potential customer looking to order a service. 
        
        Service needed:
        {self.service_description}
        
        Your goals:
        1. Explain what service you need
        2. Negotiate for a good price (use the prices mentioned in the service description as guidance)
        3. Confirm the order if you're satisfied with the price and terms
        4. Be polite but firm in negotiations
        
        When you've successfully negotiated and confirmed the order, end your message with "ORDER CONFIRMED"."""

        response = await self.anthropic_client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=1024,
            system=system_prompt,
            messages=self.conversation_history,
        )

        assistant_response = response.content[0].text

        # Add Claude's response to conversation history
        self.conversation_history.append({"role": "assistant", "content": assistant_response})

        # Check if negotiation is complete
        if "ORDER CONFIRMED" in assistant_response:
            self.negotiation_complete = True

        return assistant_response


async def start_goal(goal_id: str, user_id: str):
    async with AsyncDatabaseSession() as db_session:
        goal = await db_session.get(Goal, goal_id)
        user = await db_session.get(User, user_id)

        anthropic_client = AsyncAnthropic(api_key=settings.anthropic_api_key)

        telegram_client = TelegramClient(
            f"/tmp/tg-sessions/{user.phone.replace('+', '')}",
            settings.tg_api_id,
            settings.tg_api_hash,
        )

        await telegram_client.start(phone=user.phone)

        try:
            result = await telegram_client(
                functions.contacts.ImportContactsRequest(
                    contacts=[
                        types.InputPhoneContact(
                            client_id=0,
                            phone=settings.service_provider_phone,
                            first_name="Service",
                            last_name="Provider",
                        )
                    ]
                )
            )

            if result.users:
                logger.info("Contact added successfully")
            else:
                raise Exception("Failed to add contact")
        except Exception as e:
            logger.error(f"Error adding contact: {e}")

        agent = ServiceNegotiatorAgent(anthropic_client, goal.description)

        initial_message = "Hello, I'm interested in your service."
        await telegram_client.send_message(settings.service_provider_phone, initial_message)

        agent.conversation_history.append({"role": "assistant", "content": initial_message})

        goal.conversation_history = json.dumps(agent.conversation_history)

        @telegram_client.on(events.NewMessage(from_users=[settings.service_provider_phone]))
        async def message_handler(event):
            response = await agent.get_response(event.text)

            # Small delay to seem more human-like
            await asyncio.sleep(2)
            await event.respond(response)

            # Check if negotiation is complete
            if agent.negotiation_complete:
                logger.info("Negotiation completed!")

                result = Result(
                    goal_id=goal_id,
                    user_id=user_id,
                    status="success",
                    details=json.dumps(
                        {"conversation_history": agent.conversation_history, "timestamp": datetime.now().isoformat()}
                    ),
                )

                db_session.add(result)

                await asyncio.sleep(5)
                await telegram_client.disconnect()

            goal.conversation_history = json.dumps(agent.conversation_history)
            await db_session.commit()

        await telegram_client.run_until_disconnected()
