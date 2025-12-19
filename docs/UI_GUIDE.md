
# MeshChain UI System Documentation

**Author**: Manus AI
**Date**: Dec 18, 2025

## 1. Introduction

This document provides a comprehensive overview of the user interface (UI) system for MeshChain on Meshtastic devices. The UI is designed to be lightweight, efficient, and user-friendly, providing a complete on-device experience for managing wallets, creating transactions, and monitoring the blockchain network on small 128x64 OLED screens.

### 1.1. Design Principles

The UI system is built on the following principles:

- **Efficiency**: Minimal memory and CPU usage to run on resource-constrained ESP32 devices.
- **Usability**: Intuitive navigation with a 3-button input system.
- **Clarity**: Clear and concise information display on a small screen.
- **Modularity**: A component-based architecture for easy extension and maintenance.

### 1.2. System Architecture

The UI system is composed of several key modules:

- **Display Framework**: Manages the OLED screen and provides drawing primitives.
- **Input System**: Handles button presses and navigation events.
- **Menu System**: Provides a hierarchical menu structure.
- **UI Pages**: Individual screens for different functionalities (wallet, transactions, etc.).

## 2. Display Framework (`ui_display.py`)

The display framework is the foundation of the UI system, responsible for rendering all visual elements on the 128x64 OLED screen. It is designed for minimal memory usage, utilizing a 1 KB buffer for the entire display.

### 2.1. `DisplayBuffer`

The `DisplayBuffer` class manages the bitmap buffer for the screen. It provides low-level drawing primitives and tracks dirty regions to optimize screen updates.

| Method | Description |
|---|---|
| `clear()` | Clears the entire display buffer. |
| `set_pixel(x, y, color)` | Sets a single pixel on the screen. |
| `draw_line(x1, y1, x2, y2, color)` | Draws a line using Bresenham's algorithm. |
| `draw_rect(rect, filled, color)` | Draws a rectangle (filled or outline). |
| `draw_text(text, x, y, size, align)` | Draws text with specified font size and alignment. |

### 2.2. `Display`

The `Display` class is a high-level interface that manages pages and orchestrates screen updates. It ensures that only the necessary parts of the screen are redrawn, saving power and improving performance.

### 2.3. Widgets

The UI is built from a set of reusable widgets:

- **`TextWidget`**: Displays text with various fonts and alignments.
- **`ButtonWidget`**: A clickable button with a text label.
- **`ListWidget`**: A scrollable list of items.
- **`ProgressWidget`**: A progress bar for showing task completion.
- **`StatusBar`**: A status bar at the bottom of the screen for displaying system information.

## 3. Input System (`ui_input.py`)

The input system handles button presses from the 3-button interface common on Meshtastic devices. It provides debouncing, long-press detection, and a navigation model.

### 3.1. `InputHandler`

The `InputHandler` class processes raw button states and generates high-level events such as `PRESSED`, `RELEASED`, and `LONG_PRESSED`. It uses a state machine to manage debouncing and long-press timing.

### 3.2. `NavigationController`

The `NavigationController` manages the flow between different pages in the UI. It uses a stack-based approach to handle page navigation, allowing for easy back-and-forth movement.

### 3.3. `MenuNavigator`

The `MenuNavigator` works with the `MenuSystem` to provide intuitive menu navigation. It maps button presses to menu actions such as `UP`, `DOWN`, and `SELECT`.

## 4. Menu System (`ui_menu.py`)

The menu system provides a hierarchical, tree-based structure for all UI menus. It is designed to be flexible and easily extensible.

### 4.1. `Menu` and `MenuItem`

The `Menu` class represents a single menu screen, containing a list of `MenuItem` objects. Each `MenuItem` can be an action, a link to a submenu, a toggle, or a value display.

### 4.2. `MenuSystem`

The `MenuSystem` class manages the entire menu hierarchy. It handles menu navigation, submenu transitions, and the execution of menu actions.

### 4.3. Main Menu Structure

The main menu is organized as follows:

- **Wallet**: View balance, receive funds, send funds, backup wallet.
- **Transactions**: View recent and historical transactions.
- **Node Status**: Display blockchain, network, and validator information.
- **Settings**: Configure display, network, and security settings.

## 5. Wallet UI (`ui_wallet.py`)

The wallet UI provides all the necessary screens for managing a user's wallet directly on the device.

### 5.1. `WalletDisplayPage`

This page shows a summary of the current wallet, including:

- Wallet name
- Locked/unlocked status
- Current balance
- Truncated wallet address
- Total number of transactions

### 5.2. `ReceiveAddressPage`

This page displays the full wallet address for receiving funds. The address is split into multiple lines to fit on the small screen.

### 5.3. `TransactionHistoryPage`

This page shows a scrollable list of recent transactions, indicating the direction (sent/received) and the amount.

### 5.4. `WalletBackupPage`

This page guides the user through the wallet backup process, displaying the 12-word seed phrase. It includes strong warnings about the importance of keeping the seed phrase secure.

## 6. Transaction UI (`ui_transaction.py`)

The transaction UI provides a step-by-step workflow for creating and signing transactions.

### 6.1. `AmountInputPage`

This page allows the user to enter the transaction amount using the up/down buttons to adjust the value.

### 6.2. `RecipientInputPage`

This page provides an interface for entering the recipient's address. Due to the limited input, this is a simplified character-by-character input.

### 6.3. `TransactionReviewPage`

This page displays a summary of the transaction for final review before signing, including:

- Amount
- Fee
- Total
- Recipient address

### 6.4. `TransactionSigningPage`

This page shows a progress bar while the transaction is being signed, providing visual feedback to the user.

### 6.5. `TransactionStatusPage`

After a transaction is sent, this page displays its status, including the transaction hash and the number of confirmations.

## 7. Node Status UI (`ui_node_status.py`)

The node status UI provides detailed information about the state of the blockchain and the network.

### 7.1. `BlockchainInfoPage`

Displays key blockchain metrics:

- Current block height
- Total number of transactions
- Current difficulty
- Hash of the latest block

### 7.2. `NetworkInfoPage`

Shows network-related information:

- Number of connected peers
- Sync status (synced or syncing)
- Sync progress bar
- Bandwidth usage

### 7.3. `ValidatorListPage` and `ValidatorDetailPage`

These pages display a list of current network validators and detailed information about each one, including their stake, uptime, and reputation.

## 8. Security UI (`ui_security.py`)

The security UI handles all security-related interactions, including PIN entry and warnings.

### 8.1. `PINEntryPage`

Provides a secure interface for entering a 4-6 digit PIN. It displays dots instead of the actual digits to prevent shoulder surfing.

### 8.2. `PINLockoutPage`

If the PIN is entered incorrectly multiple times, this page is displayed, locking the user out for a configurable amount of time to prevent brute-force attacks.

### 8.3. `WarningPage`

Displays important security warnings to the user, such as when they are about to perform a sensitive action.

## 9. Settings UI (`ui_settings.py`)

The settings UI allows the user to configure various aspects of the device and the MeshChain node.

### 9.1. Settings Pages

The settings are organized into several pages:

- **Display Settings**: Brightness, contrast, screen timeout.
- **Network Settings**: LoRa frequency, power, bandwidth.
- **Security Settings**: Enable/disable PIN, change PIN length.
- **Node Settings**: Change node name, role (validator/observer).

### 9.2. `AboutPage`

Displays information about the MeshChain software, including the version number and author.
