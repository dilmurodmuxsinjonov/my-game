#pragma once

#include <array>
#include <cstdint>
#include <map>
#include <vector>

// Engine independent rules, compiled by both UnrealBuildTool and the core tests.
namespace realm {
constexpr int ChunkSide = 16;
constexpr int WorldHeight = 64;
constexpr int MaxWorldWidth = 256;
constexpr int MaxStack = 999;
constexpr std::uint32_t GeneratorVersion = 1;

enum class Block : std::uint16_t { Air, Bedrock, Grass, Dirt, Stone, Wood, Leaves, IronOre, Coal, Planks, Count };
enum class Item : std::uint8_t { Dirt, Stone, Log, Plank, IronOre, IronIngot, Coal, Wheat, Bread, Count };
constexpr std::size_t ItemCount = static_cast<std::size_t>(Item::Count);
enum class Recipe { Planks, IronIngot, Bread };
struct Cell { int x = 0, y = 0, z = 0; };
struct Face { Cell cell; std::uint8_t direction; Block block; };
struct Edit { std::uint32_t index; Block block; };
struct Pose { float x = 0, y = 0, z = 2400, yaw = 0, pitch = 0; };

int FloorDivide(int value, int divisor);
int LocalCoordinate(int value);
std::uint32_t LocalIndex(int x, int y, int z);
bool ValidBlock(Block block);
bool Solid(Block block);
const char* ItemName(Item item);
Block PlaceableBlock(Item item);
bool DropForBlock(Block block, Item& item);

class Inventory {
public:
    int Count(Item item) const;
    bool Add(Item item, int amount);
    bool Remove(Item item, int amount);
    bool Craft(Recipe recipe);
    const std::array<std::int32_t, ItemCount>& Counts() const { return counts_; }
    bool Restore(const std::array<std::int32_t, ItemCount>& counts);
private:
    std::array<std::int32_t, ItemCount> counts_{};
};

class World {
public:
    explicit World(std::uint32_t seed = 1337, int width = 64);
    void Reset(std::uint32_t seed, int width);
    int Width() const { return width_; }
    int Min() const { return -width_ / 2; }
    int Max() const { return Min() + width_; }
    std::uint32_t Seed() const { return seed_; }
    bool Contains(Cell cell) const;
    Block Get(Cell cell) const;
    bool Set(Cell cell, Block block);
    int Surface(int x, int y) const;
    bool Mine(Cell cell, Inventory& inventory);
    bool Place(Cell cell, Item item, Inventory& inventory);
    std::vector<Face> MeshChunk(int chunkX, int chunkY) const;
    std::vector<Edit> Edits() const;
    bool RestoreEdits(const std::vector<Edit>& edits);
    std::uint32_t Index(Cell cell) const;
    Cell CellAt(std::uint32_t index) const;
private:
    int width_ = 64;
    std::uint32_t seed_ = 1337;
    std::vector<Block> blocks_;
    std::vector<Block> original_;
    std::map<std::uint32_t, Block> edits_;
    int TerrainHeight(int x, int y) const;
};

class Clock {
public:
    // One real second = one game minute, 24 real minutes per day (GDD 3).
    void Advance(double seconds);
    bool Restore(double minutes);
    double Minutes() const { return minutes_; }
    int Day() const;
    int Hour() const;
    int Minute() const;
    int Season() const;
private:
    double minutes_ = 6.0 * 60.0;
};

struct Snapshot {
    std::uint32_t seed = 1337;
    int width = 64;
    Pose player;
    double minutes = 360.0;
    Inventory inventory;
    std::vector<Edit> edits;
};

// VLPT v1 is a bounded prototype format, not the final compressed VLSA archive.
// Decode is transactional: failures never modify the caller's snapshot.
std::vector<std::uint8_t> Encode(const Snapshot& snapshot);
bool Decode(const std::vector<std::uint8_t>& bytes, Snapshot& snapshot);
} // namespace realm
