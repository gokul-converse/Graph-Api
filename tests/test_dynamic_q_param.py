from src.graph_client import search_users


# ---------------------------------
# Test
# ---------------------------------

users = search_users(
    name="N",
    top=15,
)

print(f"Found {len(users)} users")

for user in users:
    print(user)