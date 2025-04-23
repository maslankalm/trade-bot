# Trade Bot

A multi-exchange cryptocurrency trading bot that executes buy and sell orders based on orderbook analysis. The bot operates on multiple exchanges simultaneously, ensuring optimal execution prices and efficient order placement.

## Disclaimer

This project is provided for educational and entertainment purposes only. While the bot is designed to work properly, it is delivered "as is" without any warranties of any kind, either express or implied. The author is not responsible for any financial losses, damages, or other consequences that may result from using this software.

By using this software, you acknowledge that:
- Cryptocurrency trading involves significant risk
- You are solely responsible for your trading decisions
- You should never trade with money you cannot afford to lose
- You should thoroughly test the bot with small amounts before using it with significant funds
- The author is not liable for any losses incurred while using this software

## Discord Integration

This bot is designed to be controlled through Discord, making it easy to use and monitor. You can set up your own free Discord server to control the bot, allowing you to:

- Send trading commands from anywhere
- Monitor trading activity in real-time
- Receive notifications about orders and errors
- Control multiple exchanges simultaneously

No paid services or complex setups required - just create a free Discord server and invite the bot!

## Discord Bot Setup

To use this bot, you need to create your own Discord bot and invite it to your server:

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" tab and click "Add Bot"
4. Under the "Privileged Gateway Intents" section, enable:
   - MESSAGE CONTENT INTENT
   - SERVER MEMBERS INTENT
5. Copy the bot token and set it as the `DISCORD_TOKEN` environment variable
6. Go to the "OAuth2" tab, select "bot" under scopes, and select the following permissions:
   - Read Messages/View Channels
   - Send Messages
   - Read Message History
   - Manage Messages (for purge functionality)
7. Copy the generated URL and open it in your browser to invite the bot to your server

## Features

- **Multi-Exchange Support**: Operates on multiple exchanges simultaneously:
  - Bybit
  - Gate.io
  - MEXC
  - XT.com

- **Smart Order Execution**:
  - Sells only at or above the highest bid price
  - Buys only at or below the lowest ask price
  - Automatically adjusts to market conditions
  - Handles market orders with price validation

- **Safety Features**:
  - Minimum order size validation (3 USDT)
  - Balance checks before order placement
  - Automatic cancellation of existing orders when needed
  - Precision handling for different trading pairs
  - Rate limiting protection

- **Real-time Monitoring**:
  - Discord integration for status updates
  - Order execution notifications
  - Balance and price monitoring
  - Error reporting

## Discord Channels

The bot uses different Discord channels for various purposes:

- `general`: Application status updates and general information
- `cmd`: Command channel for sending trading instructions
- `bybit`: Bybit exchange specific updates and orders
- `gate`: Gate.io exchange specific updates and orders
- `mexc`: MEXC exchange specific updates and orders
- `xt`: XT.com exchange specific updates and orders

## Environment Variables

The bot requires the following environment variables to be set:

### Discord
```
DISCORD_TOKEN=your_discord_bot_token
```

### Bybit
```
BYBIT_KEY=your_bybit_api_key
BYBIT_SECRET=your_bybit_api_secret
```

### Gate.io
```
GATE_KEY=your_gate_api_key
GATE_SECRET=your_gate_api_secret
```

### MEXC
```
MEXC_KEY=your_mexc_api_key
MEXC_SECRET=your_mexc_api_secret
```

### XT.com
```
XT_KEY=your_xt_api_key
XT_SECRET=your_xt_api_secret
```

## Trading Logic

### Sell Orders
1. Validates the trading pair is supported
2. Checks current orderbook for highest bid price
3. If sell price is "Market", uses highest bid price
4. If specified price is lower than highest bid, adjusts to highest bid
5. Continuously monitors orderbook for opportunities
6. Places sell orders when:
   - Price is at or above target price
   - Sufficient balance is available
   - Order size meets minimum requirements
   - Precision requirements are met

### Buy Orders
1. Validates the trading pair is supported
2. Checks current orderbook for lowest ask price
3. If buy price is "Market", uses lowest ask price
4. If specified price is higher than lowest ask, adjusts to lowest ask
5. Continuously monitors orderbook for opportunities
6. Places buy orders when:
   - Price is at or below target price
   - Sufficient USDT balance is available
   - Order size meets minimum requirements
   - Precision requirements are met

## Supported Trading Pairs

By default, the bot supports:
- ETH/USDT

Additional trading pairs can be added by modifying the `TOKENS` variable in each exchange's worker file:
- `bybit.py`
- `gate.py`
- `mexc.py`
- `xt.py`

Example of adding a new token:
```python
TOKENS = ["ETH", "NEW_TOKEN"]  # Add your token to the list
```

## Safety Measures

1. **Price Protection**:
   - Never sells below highest bid
   - Never buys above lowest ask
   - Automatic price adjustment for market orders

2. **Balance Protection**:
   - Checks available balance before each order
   - Cancels existing orders if needed to free up funds
   - Validates minimum order size (3 USDT)

3. **Precision Handling**:
   - Exchange-specific precision requirements
   - Automatic rounding to valid decimal places
   - Multiplier-based precision for specific pairs

4. **Error Handling**:
   - Automatic retries for failed API calls
   - Rate limit protection
   - Comprehensive error reporting via Discord

## Usage

### Running Locally

1. Set up all required environment variables
2. Create a free Discord server
3. Create your own Discord bot and invite it to your server
4. Configure Discord channels in the bot code
5. Start the bot
6. Send commands through the `cmd` channel:
   - Buy orders: `buy <pair> <price>`
   - Sell orders: `sell <pair> <price>`
   - Stop orders: `stop`

### Running with Docker

1. Build the Docker image:
   ```bash
   docker build -t trade-bot .
   ```

2. Run the container with environment variables:
   ```bash
   docker run -d \
     -e DISCORD_TOKEN=your_discord_bot_token \
     -e BYBIT_KEY=your_bybit_api_key \
     -e BYBIT_SECRET=your_bybit_api_secret \
     -e GATE_KEY=your_gate_api_key \
     -e GATE_SECRET=your_gate_api_secret \
     -e MEXC_KEY=your_mexc_api_key \
     -e MEXC_SECRET=your_mexc_api_secret \
     -e XT_KEY=your_xt_api_key \
     -e XT_SECRET=your_xt_api_secret \
     --name trade-bot \
     trade-bot
   ```

3. View logs:
   ```bash
   docker logs -f trade-bot
   ```

### Running with Docker Compose

1. Edit the `docker-compose.yml` file and replace the placeholder values with your actual credentials:
   ```yaml
   environment:
     - DISCORD_TOKEN=your_discord_bot_token_here
     - BYBIT_KEY=your_bybit_api_key_here
     # ... other credentials
   ```

2. Start the bot:
   ```bash
   docker-compose up -d
   ```

3. View logs:
   ```bash
   docker-compose logs -f
   ```

4. Stop the bot:
   ```bash
   docker-compose down
   ```

The bot will execute these commands on all supported exchanges simultaneously. For example, `buy ETH 2000` will attempt to buy ETH at $2000 on all configured exchanges.

## Security Notes

- API keys should have trading permissions only
- Never share your API keys or secrets
- Regularly rotate API keys
- Monitor Discord channels for any suspicious activity
- Keep the bot's code and dependencies updated