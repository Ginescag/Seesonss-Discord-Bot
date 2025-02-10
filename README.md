# Seesonss-Discord-Bot

[Your project context here]

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org)
[![Discord.py](https://img.shields.io/badge/Discord.py-2.0+-blue.svg)](https://discordpy.readthedocs.io/)
[![Shopify API](https://img.shields.io/badge/Shopify_API-2024--10-green.svg)](https://shopify.dev/api)

## Overview
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

## API Integration
### Shopify API
The bot interacts with Shopify's Admin API to:
- Monitor inventory levels
- Generate discount codes
- Track product updates
- Manage price rules

### Discord API 
Uses Discord.py for:
- Message handling
- Role management
- User interactions
- Channel monitoring

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
- `!hola` - Greeting command

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
- 60-second cooldown between discount generations
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
- flare-raffles

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