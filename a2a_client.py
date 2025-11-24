import logging

from typing import Any
from uuid import uuid4
import time
import httpx

from a2a.client import A2ACardResolver, ClientFactory, ClientConfig,A2AClient
from a2a.types import (
    AgentCard,
    MessageSendParams,
    SendMessageRequest,
    SendStreamingMessageRequest,
    Message
)

async def run_conversation(message: str, assistantID: str) -> Any:
    """Run a complete conversation with the agent."""
    # Create a single httpx client that stays open for the entire conversation
    timeout = httpx.Timeout(300.0, connect=10.0)  # 300s total, 10s connect
    async with httpx.AsyncClient(timeout=timeout) as httpx_client:
        # Get agent card
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url="http://localhost:3000",
            agent_card_path="/api/.well-known/agent-card.json?assistant_id=agentic-rag-assistant-v1",
        )
        agent_card = await resolver.get_agent_card()
        # print(f"Public Agent Card: {agent_card}")

        agent_card.url = f"http://localhost:3000/api/a2a/{assistantID}/agentic-rag-assistant-v1/message"
        
        # Initialize client with the same httpx_client
        client = ClientFactory(config=ClientConfig(httpx_client=httpx_client,streaming=True)).create(agent_card)
        # request = SendMessageRequest(
        #     id=str(uuid4()),
        #     jsonrpc= "2.0",
        #     method= "message/send",
        #     params=MessageSendParams(
        #         message=Message(
        #             message_id="msg_" + str(uuid4()),
        #             context_id="ctx_" + str(uuid4()),
        #             task_id="task_" + str(uuid4()),               
        #             parts=[
        #                 {
        #                     "kind": "text",
        #                     "text": message
        #                 }
        #             ],
        #             role="user",
        #         )
        #     )
        # )
        # streamrequest = SendStreamingMessageRequest(
        #     id=str(uuid4()),
        #     jsonrpc= "2.0",
        #     method= "message/stream",
        #     params=MessageSendParams(
        #         message=Message(
        #             message_id="msg_" + str(uuid4()),
        #             context_id="ctx_" + str(uuid4()),
        #             task_id="task_" + str(uuid4()),               
        #             parts=[
        #                 {
        #                     "kind": "text",
        #                     "text": message
        #                 }
        #             ],
        #             role="user",
        #         )
        #     )
        # )
        
        responses = []
        async for response in client.send_message(Message(
            message_id=str(uuid4()),
            parts=[
                {
                    "kind": "text",
                    "text": message
                }
            ],
            role="user",
        )):
            
            responses.append(response)
        
        return responses

async def run_stream_conversation(message: str, assistantID: str) -> Any:
    """Run a complete conversation with the agent."""
    # Create a single httpx client that stays open for the entire conversation
    timeout = httpx.Timeout(300.0, connect=10.0)  # 300s total, 10s connect
    async with httpx.AsyncClient(timeout=timeout) as httpx_client:
        # Get agent card
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url="http://localhost:3000",
            agent_card_path="/api/.well-known/agent-card.json?assistant_id=agentic-rag-assistant-v1",
        )
        agent_card = await resolver.get_agent_card()

        agent_card.url = f"http://localhost:3000/api/a2a/{assistantID}/agentic-rag-assistant-v1/message"
        
        # Initialize client with the same httpx_client
        client = A2AClient(httpx_client=httpx_client,agent_card=agent_card)
        send_message_payload = {
            'message': {
                'role': 'user',
                'parts': [
                    {'kind': 'text', 'text': message}
                ],
                'message_id': uuid4().hex,
            },
        }
        streaming_request = SendStreamingMessageRequest(id=str(uuid4()),params=MessageSendParams(**send_message_payload))
        
        stream_response = client.send_message_streaming(streaming_request)
                 
        async for chunk in stream_response:
            print(chunk.model_dump(mode='json', exclude_none=True))

        return ""

if __name__ == '__main__':
    import asyncio

    # Financial/Inventory analyst bot
    response = asyncio.run(run_conversation("Which products low on stock?","1be68003-a0fb-4c57-938f-964e8af82a28")) 
    bot_message = response[0][0].artifacts[0].parts[0].root.text
    print(f"===========================================")
    print(f"Response from Financial/Inventory Analyst Bot: {bot_message}")

    # Supplier bot
    response1 = asyncio.run(run_conversation(bot_message,"f42a2f37-3e86-46a0-93d9-bb75cdd74d33")) 
    bot_message1 = response1[0][0].artifacts[0].parts[0].root.text
    print(f"===========================================")
    print(f"Response from Supplier Bot: {bot_message1}")

    # Streaming example
    # response = asyncio.run(run_stream_conversation("Which products low on stock?","1be68003-a0fb-4c57-938f-964e8af82a28"))
