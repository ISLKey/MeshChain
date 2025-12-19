# MeshChain Tokenomics Design

## Executive Summary

MeshChain introduces **MESH tokens** as the native currency of the LoRa-based blockchain network. The tokenomics model is designed to ensure fair distribution, prevent wealth concentration, maintain price stability, and create sustainable incentives for network participation.

---

## Part 1: Coin Supply & Initial Distribution

### 1.1 Total Supply

**Maximum Supply: 21,000,000 MESH**

This fixed cap mirrors Bitcoin's approach, creating scarcity and predictable economics. The choice of 21 million is intentional—it's a well-understood number in crypto that signals long-term value preservation.

**Rationale**:
- Fixed supply prevents unlimited inflation
- Creates scarcity value over time
- Predictable for long-term planning
- Aligns with proven Bitcoin model
- Suitable for LoRa network scale (not billions of devices initially)

### 1.2 Supply Schedule

**Phase 1-5 (Weeks 1-20): Genesis Allocation**
- Total: 2,100,000 MESH (10% of total supply)
- Community: 840,000 MESH (4%)
- Developers: 420,000 MESH (2%)
- Foundation: 420,000 MESH (2%)
- Reserve: 420,000 MESH (2%)

**Phase 2+ (Ongoing): Block Rewards**
- Initial block reward: 50 MESH per block
- Halving schedule: Every 210,000 blocks (~4 years)
- 4 halvings total over 16 years
- Final supply reached: Year 16

**Halving Schedule**:

| Phase | Years | Block Reward | Blocks | Total Issued |
|-------|-------|--------------|--------|--------------|
| 1 | 0-4 | 50 MESH | 210,000 | 10,500,000 |
| 2 | 4-8 | 25 MESH | 210,000 | 15,750,000 |
| 3 | 8-12 | 12.5 MESH | 210,000 | 18,375,000 |
| 4 | 12-16 | 6.25 MESH | 210,000 | 19,687,500 |
| 5 | 16+ | 3.125 MESH | Infinite | 20,843,750 |

**Note**: After 16 years, block rewards continue at 3.125 MESH indefinitely, approaching but never exceeding 21 million.

### 1.3 Genesis Distribution (Initial 2.1 Million MESH)

**Community Allocation: 840,000 MESH (4%)**
- **Early Adopters**: 420,000 MESH
  - Distributed to first 1,000 nodes that join network
  - 420 MESH per node (encourages early participation)
  - Vesting: 50% immediately, 50% over 6 months
  
- **Community Grants**: 210,000 MESH
  - Educational initiatives
  - Community development
  - Ecosystem projects
  
- **Airdrop**: 210,000 MESH
  - Distributed to Meshtastic community members
  - Snapshot-based (fair to existing community)
  - 1 MESH per active Meshtastic node at snapshot time

**Developer Allocation: 420,000 MESH (2%)**
- **Core Team**: 210,000 MESH
  - Vesting: 4-year schedule (25% per year)
  - Ensures long-term commitment
  
- **Ecosystem Developers**: 210,000 MESH
  - Grants for Phase 2-5 implementation
  - Bounties for bug fixes and features
  - Community developer rewards

**Foundation Allocation: 420,000 MESH (2%)**
- **Network Operations**: 210,000 MESH
  - Infrastructure costs
  - Development tools
  - Community support
  
- **Treasury**: 210,000 MESH
  - Long-term sustainability
  - Emergency reserves
  - Future initiatives

**Reserve Allocation: 420,000 MESH (2%)**
- Held for future strategic needs
- Governance votes required for use
- Prevents dilution from unexpected needs

### 1.4 Circulating Supply Timeline

**Year 1**: ~5.25M MESH circulating
- Genesis allocation: 2.1M
- Block rewards (52 weeks): 2.6M
- Remaining locked/vesting: 13.75M

**Year 4**: ~10.5M MESH circulating
- All genesis allocation fully vested
- Block rewards: 10.5M total
- Remaining: 10.5M

**Year 8**: ~15.75M MESH circulating
- Halving occurs
- Reward rate drops to 25 MESH/block

**Year 16**: ~19.69M MESH circulating
- Final halving occurs
- Reward rate drops to 6.25 MESH/block
- Approaching maximum supply

---

## Part 2: Anti-Centralization & Fairness Mechanisms

### 2.1 The Problem: "Rich Get Richer"

In traditional Proof-of-Stake systems, validators with more coins have:
- Higher probability of being selected
- More rewards earned
- Ability to accumulate more coins
- Increasing power over network

This creates wealth concentration and centralization.

### 2.2 Solution: Proximity-Based Fairness

**MeshChain uses Delegated Proof-of-Proximity (DPoP)** instead of pure stake-based selection:

**Validator Selection Formula**:
```
Selection Probability = (Hop Distance Weight × Stake Weight) / Total Weight

Where:
- Hop Distance Weight: Inverse of hop distance (closer = higher weight)
- Stake Weight: Stake amount (prevents zero-stake attacks)
- Total Weight: Sum of all validator weights
```

**Key Features**:
1. **Geographic Fairness**: Nodes closer to proposer have higher chance
2. **Stake Requirement**: Minimum 100 MESH to validate (prevents spam)
3. **No Maximum Stake**: More coins = higher chance, but not guaranteed
4. **Proximity Advantage**: Network topology matters as much as wealth

**Example**:
- Node A: 1,000 MESH, 2 hops away → Weight = (1/2) × 1,000 = 500
- Node B: 10,000 MESH, 5 hops away → Weight = (1/5) × 10,000 = 2,000
- Node C: 100 MESH, 1 hop away → Weight = (1/1) × 100 = 100
- Node A has 25% selection probability despite having less stake than B

### 2.3 Gini Coefficient Stabilization

**Target Gini Coefficient: 0.35** (moderate inequality)

This means:
- Not perfectly equal (0.0) - rewards effort and participation
- Not highly concentrated (0.9+) - prevents oligarchy
- Sustainable long-term distribution

**Monitoring & Adjustment**:
- Gini coefficient calculated every epoch (1 week)
- If Gini > 0.40: Increase proximity weight (favor distributed nodes)
- If Gini < 0.30: Increase stake weight (reward validators)
- Smooth transitions prevent sudden changes

### 2.4 Slashing & Penalties

**Misbehavior Penalties**:
- **Missed Validation**: -5% of stake (temporary)
- **Invalid Block**: -10% of stake (temporary)
- **Double Signing**: -25% of stake (permanent)
- **Network Attack**: -50% of stake (permanent)

**Slashing Recovery**:
- Temporary slashes recovered after 30 days of good behavior
- Permanent slashes cannot be recovered
- Encourages honest participation

### 2.5 Minimum Stake Requirements

**Validator Stake Tiers**:

| Tier | Minimum MESH | Selection Probability | Reward Multiplier |
|------|--------------|----------------------|-------------------|
| Basic | 100 | 1x | 1.0x |
| Standard | 500 | 1.5x | 1.1x |
| Premium | 1,000 | 2.0x | 1.2x |
| Elite | 5,000 | 2.5x | 1.3x |

**Rationale**:
- Prevents zero-stake attacks
- Incentivizes long-term commitment
- Doesn't prevent small nodes from participating
- Higher stakes get modest bonuses (not exponential)

### 2.6 Anti-Whale Mechanisms

**Maximum Validator Stake: 50,000 MESH**

- Prevents any single node from dominating
- Encourages distribution of coins
- Nodes with >50,000 MESH must split or delegate
- Enforced at protocol level

**Delegation System**:
- Nodes can delegate stake to other nodes
- Delegated stake counts toward validator's weight
- Delegation fee: 5% of rewards (goes to delegator)
- Prevents concentration while allowing participation

**Example**:
- Alice has 100,000 MESH
- Can't validate with all 100,000 (max 50,000)
- Delegates 50,000 to Bob (receives 5% of Bob's rewards)
- Validates with 50,000 herself
- Network benefits from distribution

---

## Part 3: Price Stability & Growth Mechanisms

### 3.1 Utility-Driven Value

**MESH tokens are essential for network operation**:

**Transaction Fees**:
- Base fee: 0.001 MESH per transaction
- Fee market: Increases during congestion
- Burned: All transaction fees are burned (deflationary)

**Network Operations**:
- Validator stake: Required to validate blocks
- Governance voting: Required to vote on protocol changes
- Channel access: May require MESH for premium channels

**Utility Creates Demand**:
- Every transaction removes MESH from circulation
- Every validator locks MESH in stake
- Every governance vote requires MESH
- Growing network = growing demand

### 3.2 Deflationary Mechanism: Fee Burning

**Transaction Fee Burning**:
- 100% of transaction fees burned (removed from circulation)
- Reduces total supply over time
- Creates scarcity value
- Counteracts inflation from block rewards

**Fee Burn Example**:
- Year 1: 5,000 transactions/day × 0.001 MESH = 5 MESH/day burned
- Year 5: 50,000 transactions/day × 0.001 MESH = 50 MESH/day burned
- Year 10: 500,000 transactions/day × 0.001 MESH = 500 MESH/day burned
- Over 10 years: ~1.8M MESH burned (8.6% of supply)

### 3.3 Supply & Demand Balance

**Supply Growth** (Inflation):
- Year 1: +2.6M MESH from block rewards
- Year 2: +2.6M MESH from block rewards
- Year 5: +1.3M MESH from block rewards (after halving)
- Decreasing over time

**Demand Growth** (Usage):
- Transaction fees (burned)
- Validator staking (locked)
- Governance participation (locked)
- Ecosystem growth

**Price Dynamics**:
- If demand grows faster than supply: Price increases ↑
- If supply grows faster than demand: Price decreases ↓
- Equilibrium creates stability

### 3.4 Price Growth Drivers

**1. Network Growth**:
- More nodes = more transactions
- More transactions = more fee burning
- More fee burning = less supply
- Less supply + same demand = higher price

**2. Adoption Waves**:
- Early adopters (Year 1-2): Speculative growth
- Utility phase (Year 3-5): Usage-based growth
- Maturity phase (Year 6+): Stable growth

**3. Halving Events**:
- Every 4 years, block rewards halve
- Supply growth rate decreases
- Creates scarcity events
- Historically drives price appreciation

**4. Ecosystem Development**:
- More use cases = more demand
- Phase 2-5 features unlock new uses
- Community projects create utility
- Expanding addressable market

### 3.5 Price Stability Safeguards

**Preventing Stagnation**:
- Continuous network growth required
- New features unlock new use cases
- Community development encouraged
- Ecosystem incentivized

**Preventing Hyperinflation**:
- Fixed maximum supply (21M)
- Halving schedule (predictable)
- Fee burning (deflationary)
- Slashing (removes bad coins)

**Preventing Speculation Bubbles**:
- Utility-based value (not pure speculation)
- Network fundamentals matter
- Long-term incentives aligned
- Gradual supply release

---

## Part 4: Token Economics Summary

### 4.1 Key Metrics

| Metric | Value |
|--------|-------|
| **Total Supply** | 21,000,000 MESH |
| **Genesis Allocation** | 2,100,000 MESH (10%) |
| **Block Reward (Year 1)** | 50 MESH/block |
| **Halving Interval** | 210,000 blocks (~4 years) |
| **Target Gini Coefficient** | 0.35 |
| **Minimum Validator Stake** | 100 MESH |
| **Maximum Validator Stake** | 50,000 MESH |
| **Base Transaction Fee** | 0.001 MESH |
| **Delegation Fee** | 5% of rewards |
| **Slashing Penalty (Double Sign)** | 25% of stake |

### 4.2 Distribution Philosophy

**Fair Distribution**:
- Early adopters rewarded (420 MESH per node)
- Community gets 4% (840,000 MESH)
- Developers get 2% (420,000 MESH)
- Foundation gets 2% (420,000 MESH)
- Reserve gets 2% (420,000 MESH)

**Earned Distribution**:
- Block rewards for validation
- Transaction fees for network security
- Governance rewards for participation
- No free coins after genesis

**Sustainable Distribution**:
- Halving schedule prevents runaway inflation
- Fee burning creates deflation
- Stake requirements lock coins
- Long-term incentives aligned

### 4.3 Fairness Guarantees

| Mechanism | Purpose | Implementation |
|-----------|---------|-----------------|
| **DPoP Consensus** | Geographic fairness | Proximity-weighted selection |
| **Gini Stabilization** | Wealth distribution | Adaptive validator selection |
| **Stake Limits** | Prevent whales | Max 50,000 MESH per validator |
| **Delegation System** | Inclusive participation | 5% delegation fee |
| **Slashing Penalties** | Honest behavior | Up to 50% stake loss |
| **Minimum Stake** | Spam prevention | 100 MESH required |

### 4.4 Price Growth Drivers

| Driver | Mechanism | Timeline |
|--------|-----------|----------|
| **Network Growth** | More nodes → more fees → more burning | Continuous |
| **Halving Events** | Supply reduction every 4 years | Years 4, 8, 12, 16 |
| **Ecosystem Development** | New use cases → new demand | Phases 2-5 |
| **Adoption Waves** | Speculative → Utility → Stable | Years 1-10+ |
| **Fee Burning** | Deflationary pressure | Continuous |

---

## Part 5: Implementation Roadmap

### Phase 1 (Weeks 1-4): Genesis
- [ ] Deploy tokenomics smart contract
- [ ] Distribute genesis allocation
- [ ] Set up block reward system
- [ ] Initialize validator stake requirements

### Phase 2 (Weeks 5-8): Consensus
- [ ] Implement DPoP validator selection
- [ ] Deploy Gini stabilization algorithm
- [ ] Set up slashing penalties
- [ ] Enable fee burning

### Phase 3 (Weeks 9-12): Network
- [ ] Integrate with Meshtastic
- [ ] Deploy delegation system
- [ ] Enable governance voting
- [ ] Monitor Gini coefficient

### Phase 4 (Weeks 13-16): Optimization
- [ ] Fine-tune parameters based on data
- [ ] Adjust halving schedule if needed
- [ ] Optimize fee structure
- [ ] Improve validator selection

### Phase 5 (Weeks 17-20): Tools
- [ ] Build wallet with staking UI
- [ ] Create block explorer
- [ ] Deploy governance interface
- [ ] Release CLI tools

---

## Part 6: FAQ & Rationale

### Q: Why 21 million MESH?
**A**: This number is proven (Bitcoin uses it), creates scarcity, and is appropriate for LoRa network scale. It's large enough to allow microtransactions but small enough to create value.

### Q: Why halving every 4 years?
**A**: Bitcoin's 4-year halving creates predictable scarcity events that historically drive adoption. It's a proven model that the community understands.

### Q: Why burn transaction fees?
**A**: Burning creates deflationary pressure that counteracts block reward inflation. It aligns incentives—more network usage = more value for remaining coins.

### Q: Why Gini coefficient 0.35?
**A**: This balances fairness with incentives. It's not perfectly equal (which removes incentive to validate) but not concentrated (which creates oligarchy).

### Q: Why 50,000 MESH maximum stake?
**A**: This prevents any single node from dominating. With 21M total supply, 50,000 represents 0.24% of supply—enough to be meaningful but not dominant.

### Q: Why proximity-based selection?
**A**: LoRa networks are geographic. Proximity-based selection aligns incentives with network topology, ensuring distributed validation and preventing geographic centralization.

### Q: How do we ensure price goes up?
**A**: Through network growth (more demand), fee burning (less supply), and halving events (reduced inflation). Price appreciation requires the network to be useful and growing.

### Q: What prevents rogue nodes from mining lots of coins?
**A**: Multiple mechanisms: (1) Minimum stake requirement, (2) Proximity-based selection, (3) Slashing penalties, (4) Maximum stake limits, (5) Gini stabilization.

---

## Conclusion

MeshChain's tokenomics model is designed to create a **fair, sustainable, and valuable** cryptocurrency for the LoRa mesh network. By combining proximity-based consensus, wealth distribution safeguards, and deflationary mechanisms, MESH tokens create genuine utility while preventing centralization and wealth concentration.

The model rewards early adopters, incentivizes honest participation, and creates natural price appreciation through network growth and scarcity.

---

**Version**: 1.0  
**Date**: December 2024  
**Status**: Ready for Implementation
