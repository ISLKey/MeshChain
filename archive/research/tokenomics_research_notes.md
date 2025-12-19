# MeshChain Tokenomics Research Notes

## Key Findings from Research

### 1. Tokenomics Fundamentals (Coinbase)
- **Token Supply**: Powerful factor influencing price
- **Fixed vs Unlimited Supply**: Bitcoin has fixed max supply, others have unlimited
- **Inflation Rate**: Can remain linear or vary over time
- **Burning Mechanism**: Removes tokens from circulation (deflationary)
- **Market Cap**: Current (circulating supply × price) vs Fully-diluted (max supply × price)
- **Supply Dilution**: When supply increases without demand increase, existing holders are diluted

### 2. Fairness in Proof of Stake (Academic Research)
- **The "Rich Get Richer" Problem**: 
  - Wealthier validators have more coins to stake
  - Higher probability of being selected as validator
  - Earn more rewards, become even richer
  - This is the "compounding effect"

- **Gini Coefficient**: Measure of wealth inequality
  - 0 = perfect equality
  - 1 = perfect inequality (one person has all wealth)
  - Can be used as target for fairness

- **Gini-Stabilized PoS** (Academic Solution):
  - Adaptive mechanism that regulates validator selection
  - Interpolates between weighted and opposite-weighted selection
  - Pushes Gini coefficient toward target value
  - Prevents wealth concentration while maintaining incentives

- **Key Parameters**:
  - Target Gini coefficient (θ)
  - Transition speed (s)
  - Interpolation function for smooth transitions
  - Penalty for corrupted validators (slashing)

### 3. Anti-Whale Mechanisms
- **Daily Contribution Limits**: Cap on how much one entity can contribute
- **Maximum Transfer Limits**: Limit token transfers per transaction
- **Voting Power Caps**: Reduce impact of large wallets on governance
- **Proportional Distribution**: Ensure fair allocation regardless of wallet size

### 4. Price Stability & Growth Mechanisms
- **Stablecoins**: Peg to fiat currency or commodities (not suitable for MeshChain)
- **Deflationary Tokens**: 
  - Token burning reduces supply over time
  - Decreasing supply + stable/increasing demand = price appreciation
  - Creates scarcity value
  - Examples: Avalanche (AVAX), Ethereum (gas burning)

- **Utility-Driven Value**:
  - Strong utility creates sustainable demand
  - Without utility, no sustainable demand
  - Utility is condition for token success
  - Must be essential to network operation

- **Halving Schedules**:
  - Bitcoin: Halves every 4 years
  - Creates predictable supply reduction
  - Programmed emissions
  - Creates scarcity events

## MeshChain Specific Considerations

### For LoRa/Meshtastic Network:
1. **Bandwidth Constraints**: Must account for low bandwidth
2. **Decentralization**: Prevent geographic/hardware concentration
3. **Fairness**: Ensure equal opportunity for all nodes
4. **Utility**: Token must be essential to network operation
5. **Sustainability**: System must be stable over long term

### Design Principles:
1. **Fair Distribution**: Not based purely on wealth
2. **Earned Rewards**: Nodes earn coins through validation
3. **Scarcity**: Limited supply creates value
4. **Utility**: Coins used for network fees, governance
5. **Stability**: Mechanisms to prevent wealth concentration
