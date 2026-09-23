#include "RealmCore.h"
#include <algorithm>
#include <cmath>
#include <cstring>
#include <limits>
#include <set>

namespace realm {
namespace {
bool ValidItem(Item item) { return static_cast<std::size_t>(item) < ItemCount; }
bool ValidWidth(int width) { return width >= 16 && width <= MaxWorldWidth && width % 32 == 0; }
std::uint32_t Hash(std::uint32_t x) {
    x ^= x >> 16; x *= 0x7feb352du; x ^= x >> 15; x *= 0x846ca68bu; return x ^ (x >> 16);
}
std::uint32_t Sample(int x, int y, std::uint32_t seed) {
    return Hash(static_cast<std::uint32_t>(x) * 0x9e3779b9u ^ static_cast<std::uint32_t>(y) * 0x85ebca6bu ^ seed);
}
bool ValidPose(const Pose& p, int width) {
    const float bound = static_cast<float>(width * 100);
    return std::isfinite(p.x) && std::isfinite(p.y) && std::isfinite(p.z) &&
        std::isfinite(p.yaw) && std::isfinite(p.pitch) && std::abs(p.x) <= bound &&
        std::abs(p.y) <= bound && p.z >= -1000 && p.z <= 10000 && std::abs(p.yaw) <= 360 && std::abs(p.pitch) <= 90;
}
bool ValidEdits(const std::vector<Edit>& edits, int width) {
    const auto volume = static_cast<std::uint32_t>(width * width * WorldHeight);
    if (edits.size() > volume) return false;
    std::set<std::uint32_t> seen;
    for (const auto& edit : edits) {
        if (edit.index >= volume || edit.index < static_cast<std::uint32_t>(width * width) ||
            !ValidBlock(edit.block) || edit.block == Block::Bedrock || !seen.insert(edit.index).second) return false;
    }
    return true;
}
std::uint32_t Checksum(const std::vector<std::uint8_t>& bytes, std::size_t count) {
    std::uint32_t hash = 2166136261u;
    for (std::size_t i = 0; i < count; ++i) { hash ^= bytes[i]; hash *= 16777619u; }
    return hash;
}
void Put(std::vector<std::uint8_t>& bytes, std::uint64_t value, unsigned count) {
    for (unsigned i = 0; i < count; ++i) bytes.push_back(static_cast<std::uint8_t>(value >> (i * 8)));
}
std::uint64_t Get(const std::vector<std::uint8_t>& bytes, std::size_t& at, unsigned count) {
    std::uint64_t result = 0;
    for (unsigned i = 0; i < count; ++i) result |= static_cast<std::uint64_t>(bytes[at++]) << (i * 8);
    return result;
}
void PutFloat(std::vector<std::uint8_t>& bytes, float value) {
    std::uint32_t bits; std::memcpy(&bits, &value, sizeof bits); Put(bytes, bits, 4);
}
float GetFloat(const std::vector<std::uint8_t>& bytes, std::size_t& at) {
    const auto bits = static_cast<std::uint32_t>(Get(bytes, at, 4));
    float value; std::memcpy(&value, &bits, sizeof value); return value;
}
}

int FloorDivide(int value, int divisor) {
    if (divisor <= 0) return 0;
    const int quotient = value / divisor;
    return quotient - (value % divisor < 0 ? 1 : 0);
}
int LocalCoordinate(int value) { return value - FloorDivide(value, ChunkSide) * ChunkSide; }
std::uint32_t LocalIndex(int x, int y, int z) { return static_cast<std::uint32_t>(x + ChunkSide * (y + ChunkSide * z)); }
bool ValidBlock(Block block) { return static_cast<unsigned>(block) < static_cast<unsigned>(Block::Count); }
bool Solid(Block block) { return ValidBlock(block) && block != Block::Air; }
const char* ItemName(Item item) {
    static constexpr const char* names[] = {"Dirt", "Stone", "Logs", "Planks", "Iron ore", "Iron ingots", "Coal", "Wheat", "Bread"};
    return ValidItem(item) ? names[static_cast<std::size_t>(item)] : "Unknown";
}
Block PlaceableBlock(Item item) {
    switch (item) {
        case Item::Dirt: return Block::Dirt;
        case Item::Stone: return Block::Stone;
        case Item::Log: return Block::Wood;
        case Item::Plank: return Block::Planks;
        default: return Block::Air;
    }
}
bool DropForBlock(Block block, Item& item) {
    switch (block) {
        case Block::Grass: case Block::Dirt: item = Item::Dirt; return true;
        case Block::Stone: item = Item::Stone; return true;
        case Block::Wood: item = Item::Log; return true;
        case Block::Leaves: return false;
        case Block::IronOre: item = Item::IronOre; return true;
        case Block::Coal: item = Item::Coal; return true;
        case Block::Planks: item = Item::Plank; return true;
        default: return false;
    }
}
int Inventory::Count(Item item) const { return ValidItem(item) ? counts_[static_cast<std::size_t>(item)] : 0; }
bool Inventory::Add(Item item, int amount) {
    if (!ValidItem(item) || amount <= 0 || amount > MaxStack - Count(item)) return false;
    counts_[static_cast<std::size_t>(item)] += amount; return true;
}
bool Inventory::Remove(Item item, int amount) {
    if (!ValidItem(item) || amount <= 0 || amount > Count(item)) return false;
    counts_[static_cast<std::size_t>(item)] -= amount; return true;
}
bool Inventory::Craft(Recipe recipe) {
    Inventory candidate = *this;
    bool result = false;
    switch (recipe) {
        case Recipe::Planks: result = candidate.Remove(Item::Log, 1) && candidate.Add(Item::Plank, 4); break;
        case Recipe::IronIngot: result = candidate.Remove(Item::IronOre, 2) && candidate.Remove(Item::Coal, 1) && candidate.Add(Item::IronIngot, 1); break;
        case Recipe::Bread: result = candidate.Remove(Item::Wheat, 2) && candidate.Add(Item::Bread, 1); break;
    }
    if (result) *this = candidate;
    return result;
}
bool Inventory::Restore(const std::array<std::int32_t, ItemCount>& counts) {
    for (int count : counts) if (count < 0 || count > MaxStack) return false;
    counts_ = counts; return true;
}

World::World(std::uint32_t seed, int width) { Reset(seed, width); }
int World::TerrainHeight(int x, int y) const {
    const int gx = FloorDivide(x, 16), gy = FloorDivide(y, 16);
    const int tx = x - gx * 16, ty = y - gy * 16;
    const auto height = [this](int a, int b) { return 9 + static_cast<int>(Sample(a, b, seed_) % 13); };
    const int a = height(gx, gy) * (16 - tx) + height(gx + 1, gy) * tx;
    const int b = height(gx, gy + 1) * (16 - tx) + height(gx + 1, gy + 1) * tx;
    return (a * (16 - ty) + b * ty) / 256;
}
void World::Reset(std::uint32_t seed, int width) {
    seed_ = seed; width_ = ValidWidth(width) ? width : 64;
    blocks_.assign(static_cast<std::size_t>(width_ * width_ * WorldHeight), Block::Air);
    edits_.clear();
    for (int y = Min(); y < Max(); ++y) for (int x = Min(); x < Max(); ++x) {
        const int height = TerrainHeight(x, y);
        for (int z = 0; z <= height; ++z) {
            Block block = z == 0 ? Block::Bedrock : (z == height ? Block::Grass : (z >= height - 2 ? Block::Dirt : Block::Stone));
            if (block == Block::Stone) {
                const auto ore = Sample(x, y, seed_ ^ static_cast<std::uint32_t>(z * 7919)) % 100;
                if (ore < 4) block = Block::IronOre;
                else if (ore < 9) block = Block::Coal;
            }
            blocks_[Index({x, y, z})] = block;
        }
    }
    // Deterministic trees away from the central first-play area.
    for (int y = Min() + 3; y < Max() - 3; y += 7) for (int x = Min() + 3; x < Max() - 3; x += 7) {
        if ((std::abs(x) < 5 && std::abs(y) < 5) || Sample(x, y, seed_ + 101) % 3 != 0) continue;
        const int base = TerrainHeight(x, y) + 1;
        for (int z = base; z < base + 4; ++z) blocks_[Index({x, y, z})] = Block::Wood;
        for (int dz = 2; dz < 6; ++dz) for (int dy = -2; dy <= 2; ++dy) for (int dx = -2; dx <= 2; ++dx) {
            const Cell cell{x + dx, y + dy, base + dz};
            if (std::abs(dx) + std::abs(dy) + (dz == 5 ? 1 : 0) > 3 || !Contains(cell)) continue;
            if (Get(cell) == Block::Air) blocks_[Index(cell)] = Block::Leaves;
        }
    }
    original_ = blocks_;
}
bool World::Contains(Cell c) const { return c.x >= Min() && c.x < Max() && c.y >= Min() && c.y < Max() && c.z >= 0 && c.z < WorldHeight; }
std::uint32_t World::Index(Cell c) const { return static_cast<std::uint32_t>((c.x - Min()) + width_ * ((c.y - Min()) + width_ * c.z)); }
Cell World::CellAt(std::uint32_t i) const {
    return {static_cast<int>(i % width_) + Min(), static_cast<int>((i / width_) % width_) + Min(), static_cast<int>(i / (width_ * width_))};
}
Block World::Get(Cell c) const { return Contains(c) ? blocks_[Index(c)] : Block::Air; }
bool World::Set(Cell c, Block block) {
    if (!Contains(c) || c.z == 0 || !ValidBlock(block) || block == Block::Bedrock) return false;
    const auto index = Index(c);
    if (blocks_[index] == block) return false;
    blocks_[index] = block;
    if (block == original_[index]) edits_.erase(index); else edits_[index] = block;
    return true;
}
int World::Surface(int x, int y) const {
    for (int z = WorldHeight - 1; z >= 0; --z) if (Solid(Get({x, y, z}))) return z;
    return -1;
}
bool World::Mine(Cell c, Inventory& inventory) {
    if (!Contains(c) || c.z == 0) return false;
    const auto block = Get(c);
    if (block == Block::Air) return false;
    Inventory candidate = inventory;
    Item drop = Item::Dirt;
    if (DropForBlock(block, drop) && !candidate.Add(drop, 1)) return false;
    if (!Set(c, Block::Air)) return false;
    inventory = candidate; return true;
}
bool World::Place(Cell c, Item item, Inventory& inventory) {
    const auto block = PlaceableBlock(item);
    if (!Contains(c) || c.z == 0 || block == Block::Air || Get(c) != Block::Air) return false;
    Inventory candidate = inventory;
    if (!candidate.Remove(item, 1) || !Set(c, block)) return false;
    inventory = candidate; return true;
}
std::vector<Face> World::MeshChunk(int chunkX, int chunkY) const {
    static constexpr Cell normals[] = {{1,0,0},{-1,0,0},{0,1,0},{0,-1,0},{0,0,1},{0,0,-1}};
    std::vector<Face> faces;
    for (int z = 0; z < WorldHeight; ++z) for (int y = chunkY * ChunkSide; y < (chunkY + 1) * ChunkSide; ++y)
        for (int x = chunkX * ChunkSide; x < (chunkX + 1) * ChunkSide; ++x) {
            const Cell cell{x,y,z}; const auto block = Get(cell);
            if (!Solid(block)) continue;
            for (std::uint8_t direction = 0; direction < 6; ++direction) {
                const auto n = normals[direction];
                if (z == 0 && direction == 5) continue;
                if (!Solid(Get({x+n.x,y+n.y,z+n.z}))) faces.push_back({cell,direction,block});
            }
        }
    return faces;
}
std::vector<Edit> World::Edits() const {
    std::vector<Edit> result; result.reserve(edits_.size());
    for (const auto& pair : edits_) result.push_back({pair.first,pair.second});
    return result;
}
bool World::RestoreEdits(const std::vector<Edit>& edits) {
    if (!ValidEdits(edits, width_)) return false;
    auto candidate = original_;
    std::map<std::uint32_t,Block> candidateEdits;
    for (const auto& edit : edits) {
        candidate[edit.index] = edit.block;
        if (original_[edit.index] != edit.block) candidateEdits[edit.index] = edit.block;
    }
    blocks_.swap(candidate); edits_.swap(candidateEdits); return true;
}
void Clock::Advance(double seconds) {
    if (std::isfinite(seconds) && seconds > 0 && seconds <= 3600) minutes_ = std::min(525600000.0, minutes_ + seconds);
}
bool Clock::Restore(double minutes) {
    if (!std::isfinite(minutes) || minutes < 0 || minutes > 525600000.0) return false;
    minutes_ = minutes; return true;
}
int Clock::Day() const { return static_cast<int>(minutes_ / 1440.0) + 1; }
int Clock::Hour() const { return (static_cast<int>(minutes_) / 60) % 24; }
int Clock::Minute() const { return static_cast<int>(minutes_) % 60; }
int Clock::Season() const { return ((Day() - 1) / 7) % 4; }

std::vector<std::uint8_t> Encode(const Snapshot& s) {
    Clock check;
    if (!ValidWidth(s.width) || !ValidPose(s.player,s.width) || !check.Restore(s.minutes) || !ValidEdits(s.edits,s.width)) return {};
    std::vector<std::uint8_t> bytes{'V','L','P','T'};
    Put(bytes,1,4); Put(bytes,GeneratorVersion,4); Put(bytes,s.seed,4); Put(bytes,static_cast<std::uint32_t>(s.width),4);
    for (float value : {s.player.x,s.player.y,s.player.z,s.player.yaw,s.player.pitch}) PutFloat(bytes,value);
    std::uint64_t clockBits; std::memcpy(&clockBits,&s.minutes,sizeof clockBits); Put(bytes,clockBits,8);
    for (auto count : s.inventory.Counts()) Put(bytes,static_cast<std::uint32_t>(count),4);
    Put(bytes,s.edits.size(),4);
    for (const auto& edit : s.edits) { Put(bytes,edit.index,4); Put(bytes,static_cast<std::uint16_t>(edit.block),2); }
    Put(bytes,Checksum(bytes,bytes.size()),4);
    return bytes;
}
bool Decode(const std::vector<std::uint8_t>& bytes, Snapshot& snapshot) {
    constexpr std::size_t fixedSize = 4+4+4+4+4+20+8+ItemCount*4+4+4;
    constexpr std::size_t maxBytes = fixedSize + MaxWorldWidth*MaxWorldWidth*WorldHeight*6;
    if (bytes.size() < fixedSize || bytes.size() > maxBytes || bytes[0]!='V' || bytes[1]!='L' || bytes[2]!='P' || bytes[3]!='T') return false;
    std::size_t tail = bytes.size()-4;
    if (Get(bytes,tail,4) != Checksum(bytes,bytes.size()-4)) return false;
    std::size_t at = 4;
    if (Get(bytes,at,4) != 1 || Get(bytes,at,4) != GeneratorVersion) return false;
    Snapshot candidate;
    candidate.seed = static_cast<std::uint32_t>(Get(bytes,at,4));
    const auto width = Get(bytes,at,4);
    if (width > MaxWorldWidth || !ValidWidth(static_cast<int>(width))) return false;
    candidate.width = static_cast<int>(width);
    candidate.player = {GetFloat(bytes,at),GetFloat(bytes,at),GetFloat(bytes,at),GetFloat(bytes,at),GetFloat(bytes,at)};
    if (!ValidPose(candidate.player,candidate.width)) return false;
    const auto clockBits = Get(bytes,at,8); std::memcpy(&candidate.minutes,&clockBits,sizeof clockBits);
    Clock check; if (!check.Restore(candidate.minutes)) return false;
    std::array<std::int32_t,ItemCount> counts{};
    for (auto& count : counts) { const auto raw = Get(bytes,at,4); if (raw > MaxStack) return false; count = static_cast<std::int32_t>(raw); }
    if (!candidate.inventory.Restore(counts)) return false;
    const auto editCount = Get(bytes,at,4);
    if (editCount > static_cast<std::uint64_t>(candidate.width*candidate.width*WorldHeight) || bytes.size() != fixedSize + editCount*6) return false;
    candidate.edits.reserve(static_cast<std::size_t>(editCount));
    for (std::uint64_t i=0;i<editCount;++i) {
        const auto index = static_cast<std::uint32_t>(Get(bytes,at,4));
        const auto block = static_cast<Block>(Get(bytes,at,2)); candidate.edits.push_back({index,block});
    }
    if (!ValidEdits(candidate.edits,candidate.width)) return false;
    snapshot = std::move(candidate); return true;
}
} // namespace realm
