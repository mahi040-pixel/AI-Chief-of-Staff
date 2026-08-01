import asyncio
from dotenv import load_dotenv
from agents import Runner

from my_agents.planner import planner_agent
from memory.memory import save_memory

from tools.meeting_tool import prepare_meeting

load_dotenv()


async def main():

    while True:

        user = input("\nYou : ")

        if user.lower() == "exit":

            print("\nGoodbye!")
            break

        # ---------- Meeting Preparation ----------

        if (
            "meeting brief" in user.lower()
            or "prepare meeting" in user.lower()
            or "prepare a meeting" in user.lower()
            or "executive brief" in user.lower()
            or "agenda" in user.lower()
        ):

            output = prepare_meeting(user)

        # ---------- Other Agents ----------

        else:

            result = await Runner.run(
                planner_agent,
                user
            )

            output = result.final_output

        print("\nAssistant:\n")
        print(output)

        approval = input("\nApprove this response? (yes/no): ")

        if approval.lower() == "yes":

            save_memory(
                user,
                output
            )

            print("\n✅ Response approved and saved.")

        else:

            print("\n❌ Response rejected.")


if __name__ == "__main__":
    asyncio.run(main())