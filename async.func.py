import asyncio
from time import sleep

def hello():
	print("World")
	sleep(10)

async def async_long_running_task(duration):
	print(f"Async task started, will 'sleep' for {duration} seconds...")
	hello()
	await asyncio.sleep(duration)
	print("Async task finished normally.")
	return "Async Success"

async def main():
	print("--- Testing normal async completion ---")
	try:
		# Wait for async_long_running_task(2) for up to 5 seconds
		result_normal = await asyncio.wait_for(async_long_running_task(2), timeout=3.0)
		print(f"Result (normal): {result_normal}\n")
	except asyncio.TimeoutError:
		print("Caught asyncio.TimeoutError (normal case) - this shouldn't happen.\n")

	print("--- Testing async timeout ---")
	try:
		# Wait for async_long_running_task(8) for up to 5 seconds
		result_timeout = await asyncio.wait_for(async_long_running_task(8), timeout=3.0)
		print(f"Result (timeout): {result_timeout}") # This line won't be reached
	except asyncio.TimeoutError:
		print("Caught asyncio.TimeoutError successfully!")

# --- Example Usage ---
if __name__ == "__main__":
	# Run the main async function
	asyncio.run(main())