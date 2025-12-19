"""
MeshChain UI Integration Example

This example demonstrates how to integrate the UI system with the MeshChain node
to create a complete on-device application for Meshtastic devices.

The example shows:
1. Initializing the UI system
2. Setting up the main menu
3. Handling user input
4. Updating the display
5. Integrating with the blockchain node
"""

import time
from meshchain.ui_display import Display, DisplayBuffer
from meshchain.ui_input import InputManager, ButtonID
from meshchain.ui_menu import MainMenuBuilder
from meshchain.ui_wallet import WalletManager, WalletInfo
from meshchain.ui_transaction import TransactionManager
from meshchain.ui_node_status import NodeStatusManager, BlockchainInfo, NetworkInfo
from meshchain.ui_security import SecurityManager
from meshchain.ui_settings import SettingsManager
from meshchain.micronode import MicroNode, NodeConfig


class MeshChainUIApplication:
    """
    Main application class that integrates the UI with the MeshChain node.
    
    This class orchestrates all UI components and connects them to the blockchain node.
    """
    
    def __init__(self, node_config: NodeConfig):
        """Initialize the UI application."""
        # Initialize the blockchain node
        self.node = MicroNode(node_config)
        
        # Initialize UI components
        self.display = Display()
        self.input_manager = InputManager()
        self.menu_system = MainMenuBuilder.build_main_menu()
        
        # Initialize managers
        self.wallet_manager = WalletManager()
        self.transaction_manager = TransactionManager()
        self.node_status_manager = NodeStatusManager()
        self.security_manager = SecurityManager()
        self.settings_manager = SettingsManager()
        
        # Set up security
        self.security_manager.set_correct_pin("1234")
        self.security_manager.lock_wallet()
        
        # Register callbacks
        self._register_callbacks()
        
        # Application state
        self.is_running = False
        self.current_page = None
    
    def _register_callbacks(self):
        """Register UI callbacks."""
        # Register page change callback
        self.input_manager.nav_controller.on_page_change = self._on_page_change
        
        # Register selection callback
        self.input_manager.nav_controller.on_selection = self._on_selection
        
        # Register back callback
        self.input_manager.nav_controller.on_back = self._on_back
        
        # Register security callbacks
        self.security_manager.on_pin_verified = self._on_pin_verified
        self.security_manager.on_pin_failed = self._on_pin_failed
    
    def initialize(self):
        """Initialize the application."""
        # Start the blockchain node
        self.node.startup()
        
        # Add sample wallet
        wallet = WalletInfo(
            name="Main Wallet",
            address="meshchain1a2b3c4d5e6f7g8h9i0j",
            balance=100.0,
            transactions=5
        )
        self.wallet_manager.add_wallet(wallet)
        
        # Show main menu
        self.input_manager.goto_page("Main")
        self.is_running = True
    
    def shutdown(self):
        """Shutdown the application."""
        self.is_running = False
        self.node.shutdown()
    
    def _on_page_change(self, page_name: str):
        """Handle page changes."""
        print(f"Navigating to page: {page_name}")
        
        # Update menu system
        if page_name in self.menu_system.menus:
            self.menu_system.set_current_menu(page_name)
    
    def _on_selection(self, item: str):
        """Handle menu item selection."""
        print(f"Selected: {item}")
        
        # Handle different menu selections
        if item == "View Balance":
            page = self.wallet_manager.create_wallet_page()
            if page:
                self.display.register_page("Wallet Display", page)
                self.display.show_page("Wallet Display")
        
        elif item == "Receive":
            page = self.wallet_manager.create_receive_page()
            if page:
                self.display.register_page("Receive", page)
                self.display.show_page("Receive")
        
        elif item == "Send":
            # Start transaction creation workflow
            self.transaction_manager.start_transaction()
            # In a real app, would navigate to amount input page
        
        elif item == "Blockchain":
            # Update blockchain info from node
            blockchain_info = BlockchainInfo(
                height=self.node.blockchain.get_height(),
                hash=self.node.blockchain.get_latest_block_hash(),
                timestamp=int(time.time()),
                transactions=self.node.blockchain.get_transaction_count(),
                difficulty=self.node.blockchain.get_difficulty()
            )
            self.node_status_manager.update_blockchain(blockchain_info)
            page = self.node_status_manager.create_blockchain_page()
            if page:
                self.display.register_page("Blockchain", page)
                self.display.show_page("Blockchain")
        
        elif item == "Network":
            # Update network info from node
            network_info = NetworkInfo(
                peers=len(self.node.peer_manager.get_peers()),
                synced=self.node.synchronizer.is_synced(),
                sync_progress=self.node.synchronizer.get_sync_progress(),
                bandwidth_up=0.0,
                bandwidth_down=0.0
            )
            self.node_status_manager.update_network(network_info)
            page = self.node_status_manager.create_network_page()
            if page:
                self.display.register_page("Network", page)
                self.display.show_page("Network")
    
    def _on_back(self):
        """Handle back button."""
        print("Going back")
    
    def _on_pin_verified(self):
        """Handle successful PIN verification."""
        print("PIN verified - wallet unlocked")
    
    def _on_pin_failed(self, attempts: int):
        """Handle failed PIN attempt."""
        remaining = self.security_manager.get_remaining_attempts()
        print(f"PIN failed - {remaining} attempts remaining")
    
    def handle_input(self, button_states: dict):
        """Handle button input."""
        # Update input manager
        events = self.input_manager.update(button_states)
        
        # Update menu navigator
        current_menu = self.menu_system.current_menu
        if current_menu:
            for event in events:
                if event.button == ButtonID.UP:
                    self.menu_system.navigate_up()
                elif event.button == ButtonID.DOWN:
                    self.menu_system.navigate_down()
                elif event.button == ButtonID.SELECT:
                    self.menu_system.select_item()
    
    def update_display(self):
        """Update the display."""
        # Get current menu items
        items = self.menu_system.get_current_items()
        selected_index = self.menu_system.get_selected_index()
        
        # Update menu items in input manager
        item_names = [item.name for item in items]
        self.input_manager.set_menu_items(item_names)
        
        # Render the current page
        if self.display.current_page:
            self.display.update()
        
        # Return dirty regions for display update
        return self.display.buffer.get_dirty_regions()
    
    def run(self):
        """Main application loop."""
        self.initialize()
        
        try:
            while self.is_running:
                # Simulate button input (in real app, would read from GPIO)
                button_states = {
                    ButtonID.UP: False,
                    ButtonID.SELECT: False,
                    ButtonID.DOWN: False
                }
                
                # Handle input
                self.handle_input(button_states)
                
                # Update display
                dirty_regions = self.update_display()
                
                # In a real app, would update the OLED display here
                # oled.display(self.display.get_buffer())
                
                # Update blockchain node
                self.node.event_loop.process_events()
                
                # Small delay to prevent busy waiting
                time.sleep(0.05)
        
        finally:
            self.shutdown()


class SimulatedMeshtasticDevice:
    """
    Simulates a Meshtastic device for testing purposes.
    
    This class provides a mock environment for testing the UI without actual hardware.
    """
    
    def __init__(self):
        """Initialize simulated device."""
        self.button_states = {
            ButtonID.UP: False,
            ButtonID.SELECT: False,
            ButtonID.DOWN: False
        }
        self.display_buffer = DisplayBuffer()
    
    def press_button(self, button: ButtonID):
        """Simulate pressing a button."""
        self.button_states[button] = True
    
    def release_button(self, button: ButtonID):
        """Simulate releasing a button."""
        self.button_states[button] = False
    
    def get_display_buffer(self) -> bytearray:
        """Get the current display buffer."""
        return self.display_buffer.get_buffer()


def example_basic_usage():
    """
    Example: Basic UI usage without blockchain integration.
    
    This example shows how to use the UI components in isolation.
    """
    print("=== Basic UI Usage Example ===\n")
    
    # Create input manager
    input_manager = InputManager()
    
    # Create menu system
    menu_system = MainMenuBuilder.build_main_menu()
    
    # Simulate button presses
    print("Initial menu:", menu_system.current_menu.name)
    print("Selected item:", menu_system.current_menu.get_selected_item().name)
    
    # Navigate down
    input_manager.menu_navigator._on_down()
    print("After DOWN:", menu_system.current_menu.get_selected_item().name)
    
    # Navigate down again
    input_manager.menu_navigator._on_down()
    print("After DOWN:", menu_system.current_menu.get_selected_item().name)
    
    # Navigate up
    input_manager.menu_navigator._on_up()
    print("After UP:", menu_system.current_menu.get_selected_item().name)


def example_wallet_workflow():
    """
    Example: Wallet management workflow.
    
    This example demonstrates the wallet creation and management workflow.
    """
    print("\n=== Wallet Workflow Example ===\n")
    
    # Create wallet manager
    wallet_manager = WalletManager()
    
    # Create wallets
    wallet1 = WalletInfo("Main", "addr1", 100.0, 5)
    wallet2 = WalletInfo("Savings", "addr2", 500.0, 2)
    
    wallet_manager.add_wallet(wallet1)
    wallet_manager.add_wallet(wallet2)
    
    print(f"Wallets: {len(wallet_manager.get_wallets())}")
    print(f"Current: {wallet_manager.get_current_wallet().name}")
    
    # Switch wallet
    wallet_manager.set_current_wallet("Savings")
    print(f"Switched to: {wallet_manager.get_current_wallet().name}")
    
    # Update balance
    wallet_manager.update_balance("Savings", 600.0)
    print(f"New balance: {wallet_manager.get_current_wallet().balance}")


def example_transaction_workflow():
    """
    Example: Transaction creation workflow.
    
    This example demonstrates the transaction creation process.
    """
    print("\n=== Transaction Workflow Example ===\n")
    
    # Create transaction manager
    tx_manager = TransactionManager()
    
    # Start transaction
    tx = tx_manager.start_transaction()
    print(f"Started transaction: {tx}")
    
    # Set recipient and amount
    tx_manager.set_recipient("meshchain1xyz...")
    tx_manager.set_amount(50.0)
    
    # Review transaction
    current_tx = tx_manager.get_current_tx()
    print(f"Recipient: {current_tx.recipient}")
    print(f"Amount: {current_tx.amount}")
    print(f"Fee: {current_tx.fee}")
    print(f"Total: {current_tx.get_total()}")


if __name__ == "__main__":
    # Run examples
    example_basic_usage()
    example_wallet_workflow()
    example_transaction_workflow()
    
    print("\n=== Full Application Example ===\n")
    print("To run the full application with blockchain integration:")
    print("1. Create a NodeConfig with your device settings")
    print("2. Create a MeshChainUIApplication instance")
    print("3. Call app.run() to start the main loop")
    print("\nExample:")
    print("  config = NodeConfig(node_id=1, storage_path='/spiffs/blockchain')")
    print("  app = MeshChainUIApplication(config)")
    print("  app.run()")
