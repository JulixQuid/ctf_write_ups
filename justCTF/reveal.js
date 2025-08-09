const seedrandom = require('seedrandom');
const crypto = require('crypto');

// Initial values
const SERVER_SEED = "0b50c1a9415f0da111d83bb30bdbedc1c4ea2524332097e10cfc3b6920a620f6";
const SERVER_SEED_HASH = ""; // Add your expected hash here if needed                       =
const INITIAL_CLIENT_SEED = "1111111111111111111111111111111111111111111111111111111111111111";

// Verify server seed hash (if hash is provided)
if (SERVER_SEED_HASH && crypto.createHash("sha256").update(SERVER_SEED).digest("hex") !== SERVER_SEED_HASH) {
    console.log("Server seed hash doesn't match provided server seed");
    process.exit(1);
}

const rollCounts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0};

for (let i = 0; i < 1000; i++) {
    // Generate a new client seed for each iteration while maintaining 64 hex chars
    const CLIENT_SEED = crypto.createHash('sha256')
        .update(INITIAL_CLIENT_SEED + i.toString())
        .digest('hex'); // Always 64 hex characters

    const roll = (seedrandom(JSON.stringify({
        serverSeed: SERVER_SEED,
        clientSeed: CLIENT_SEED,
        nonce: i
    })).int32() >>> 0) % 6 + 1;
    
    rollCounts[roll]++;
}

// Print results
console.log("\nRoll Counts (1000 rolls with dynamic client seed):");
for (let face = 1; face <= 6; face++) {
    console.log(`  ${face}: ${rollCounts[face]} times (${(rollCounts[face]/10).toFixed(1)}%)`);
}

// Calculate standard deviation to check fairness
const mean = 1000 / 6;
let variance = 0;
for (let face = 1; face <= 6; face++) {
    variance += Math.pow(rollCounts[face] - mean, 2);
}
const stdDev = Math.sqrt(variance / 6);
console.log(`\nStandard deviation: ${stdDev.toFixed(2)} (lower = more uniform)`);