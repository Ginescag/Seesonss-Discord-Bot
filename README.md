# <p align="center"> <img src="https://github.com/user-attachments/assets/5633c04d-418e-46fe-950e-d0ca165cf443" /> <br> S Bot </p>

I am in love with this project because even if the coding part isnt anything special, it combines 2 completely different worlds that I very much enjoy, FASHION AND PROGRAMMING YAYY! 

Seesonss is a fast-growing clothing brand based in Alicante focused on premium quality garments inspired by Londons subcultures and urban scene and I'm proud to say I form part of the team that works on the brand. I developed this discord bot as a way to manage and better develop the community that is being cultivated around the brand. this might be the barebones of a long-lived project as this bot will be in constant development as new challenges and ideas may arise. 

[Go buy Seesonss](https://seesonss.com)

## Overview
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org)
[![Discord.py](https://img.shields.io/badge/Discord.py-2.0+-blue.svg)](https://discordpy.readthedocs.io/)
[![Shopify API](https://img.shields.io/badge/Shopify_API-2024--10-green.svg)](https://shopify.dev/api)

A Discord bot that integrates with Shopify to provide real-time stock updates and generate discount codes through interactive chat commands. The bot also includes a role-based progression system.



## Features
- 🔄 Real-time stock monitoring
- 🎫 Dynamic discount code generation
- 👥 Role-based progression system
- 🎲 Random discount events in chat
- ⏲️ Cooldown system for discount generation

## Technologies
- Python 3.9+
- Discord.py 2.0+
- Shopify Admin API 2024-10
- dotenv for environment management
- requests for API calls
- asyncio for asynchronous operations

## How It Works

### API Integration
#### Shopify API
The bot makes regular API calls to Shopify's Admin API to:

1. **Inventory Monitoring**:
   - Polls inventory levels every 60 seconds
   - Tracks changes in stock quantities
   - Maintains a record of previous stock levels
   - Uses batch processing for efficiency (100 items per request)

2. **Discount Code Generation**:
   - Creates unique 15-character codes
   - Applies percentage-based discounts
   - Sets usage limits and expiration
   - Manages price rules through API

Example of inventory check:
```python
inventory_url = f"https://{SHOPIFY_SHOP_NAME}.myshopify.com/admin/api/2024-10/inventory_levels.json"
params = {"inventory_item_ids": ",".join(map(str, batch_ids))}
```

#### Discord API 
Uses Discord.py events and commands:

1. **Message Handling**:
   - `on_message` event for chat monitoring
   - Command prefix: `!` for bot commands
   - Channel-specific message processing

2. **Role Management**:
   - `on_member_update` event tracking
   - Automatic role progression
   - Role-based permissions

### Stock Monitoring System
The stock monitoring works through multiple components:

1. **Product Tracking**:
   - Maintains list of active products
   - Tracks individual variants
   - Maps inventory items to products

2. **Change Detection**:
   - Compares current vs previous stock
   - Filters significant changes
   - Batches updates for efficiency

3. **Notification System**:
   - Channel: #flare-raffles
   - Formats: "@everyone Stock update!"
   - Includes product name and quantity

### Discount Generation System
The discount system uses a dynamic probability model:

1. **Probability Management**:
   - Base probability: 1%
   - Increments: 0.3% per message
   - Resets after code generation

2. **Cooldown System**:
   - 60-second global cooldown
   - Per-user tracking
   - Prevents spam/abuse

3. **Discount Tiers**:
```python
DISCOUNT_AMOUNTS = {
    5: 0.4,   # 40% chance
    10: 0.4,  # 40% chance
    15: 0.15, # 15% chance
    20: 0.05  # 5% chance
}
```

### Role Progression System
Hierarchical role structure:

1. **Role Levels**:
```python
ROLE_RANKS = {
    "s'cout": 1,
    "s'oldier": 2, 
    "s'enior": 3,
    "s'iso": 4
}
```

2. **Progression Logic**:
   - Automatic role upgrades
   - Activity-based progression
   - DM notifications on level-up

### Channel Management
Channel-specific functionalities:

1. **Monitored Channels**:
   - #general: Basic interaction
   - #fitpics: Community engagement
   - #flare-raffles: Stock updates

2. **Channel Permissions**:
   - Role-based access control
   - Command restrictions
   - Message monitoring

### Error Handling System
Comprehensive error management:

1. **API Errors**:
   - Rate limit handling
   - Connection retry logic
   - Error logging system

2. **Discord Errors**:
   - Permission checks
   - Command validation
   - Event error handling

3. **Recovery Methods**:
   - Automatic reconnection
   - State preservation
   - Error notifications

## Installation
1. Clone the repository
```bash
git clone https://github.com/yourusername/Seesonss-Discord-Bot.git
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Create and configure the `.env` file with your credentials

4. Run the bot
```bash
python Sbot.py
```

## Commands
- `!ping` - Check if bot is running

## Stock Monitoring
The bot continuously monitors Shopify inventory through the `monitor_stock_changes()` function and sends notifications to specified Discord channels when changes are detected.

### Stock Update Messages
When stock changes are detected, the bot sends a message in this format:
```
@everyone Stock update!
"Product Name": "X" more available
```

## Discount System
Discounts are generated based on user activity and random probability with the following tiers:

| Discount | Probability |
|----------|------------|
| 5%       | 40%        |
| 10%      | 40%        |
| 15%      | 15%        |
| 20%      | 5%         |

The system includes:
- Random probability that increases over time
- Automatic code expiration

### Discount Messages
When a discount code is generated, it appears as:
```
A wild discount code has spawned **CODE** with X% off! Fast, claim it before it disappears!
```

## Role System
The bot includes a progression system with the following roles:
1. s'cout
2. s'oldier
3. s'enior
4. s'iso

Each role represents a different level in the community hierarchy and may grant access to special features or privileges.

## Channel Configuration
The bot actively monitors these channels:
- general
- fitpics


## Error Handling
The bot includes comprehensive error handling for:
- API failures
- Invalid commands
- Permission issues
- Network interruptions

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Support
If you encounter any issues or have questions, please open an issue in the repository.
