from telethon import TelegramClient
import csv
import os
from dotenv import load_dotenv
import asyncio

# Load environment variables once
load_dotenv('.env')
api_id = os.getenv('29256575')
api_hash = os.getenv('0d56f14d00f288928f28a53baa3e1298')
phone = os.getenv('251911834030')

# Function to scrape data from a single channel
async def scrape_channel(client, channel_username, writer, media_dir):
    entity = await client.get_entity(channel_username)
    channel_title = entity.title  # Extract the channel's title
    async for message in client.iter_messages(entity, limit=10000):
        media_path = None
        if message.media and hasattr(message.media, 'photo'):
            # Create a unique filename for the photo
            filename = f"{channel_username}_{message.id}.jpg"
            media_path = os.path.join(media_dir, filename)
            # Download the media to the specified directory if it's a photo
            await client.download_media(message.media, media_path)
        
        # Write the channel title along with other data
        writer.writerow([channel_title, channel_username, message.id, message.message, message.date, media_path])

async def main():
    # Initialize the client once
    async with TelegramClient('my_scraping_session', '29256575', '0d56f14d00f288928f28a53baa3e1298') as client:
        # Create a directory for media files
        media_dir = 'photos'
        os.makedirs(media_dir, exist_ok=True)

        # Open the CSV file and prepare the writer
        with open('data\EAHCI.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path'])  # Include channel title in the header
            
            # List of channels to scrape
            channels = [
                '@EAHCI',  # Existing channel
                # You can add more channels here
            ]
            
            # Iterate over channels and scrape data into the single CSV file
            for channel in channels:
                await scrape_channel(client, channel, writer, media_dir)
                print(f"Scraped data from {channel}")

# Function to run the main coroutine
def run():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

if __name__ == "__main__":
    run()