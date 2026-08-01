import sys
sys.path.insert(0, ".")
from tools.strategy_tool import add_goal, list_goals

print("--- Before ---")
print(list_goals())

print("--- Call 1 ---")
print(add_goal("Expand to EU market"))

print("--- Call 2 (should say already tracked) ---")
print(add_goal("Expand to EU market"))

print("--- After ---")
print(list_goals())
