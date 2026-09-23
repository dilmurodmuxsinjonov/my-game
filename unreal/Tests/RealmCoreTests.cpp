#include "RealmCore.h"
#include <cmath>
#include <iostream>
#include <limits>
#include <string>
#include <functional>

namespace {
int failed = 0;
int checks = 0;
void Check(bool condition, const char* expression, int line) {
    ++checks;
    if (!condition) { ++failed; std::cerr << "FAIL line " << line << ": " << expression << '\n'; }
}
#define CHECK(expression) Check((expression), #expression, __LINE__)
void Rehash(std::vector<std::uint8_t>& bytes) {
    std::uint32_t hash = 2166136261u;
    for (std::size_t i=0;i<bytes.size()-4;++i) { hash ^= bytes[i]; hash *= 16777619u; }
    for (unsigned i=0;i<4;++i) bytes[bytes.size()-4+i] = static_cast<std::uint8_t>(hash >> (i*8));
}
}

int main() {
    using namespace realm;
    CHECK(FloorDivide(-1,16) == -1);
    CHECK(FloorDivide(-16,16) == -1);
    CHECK(FloorDivide(-17,16) == -2);
    CHECK(FloorDivide(16,16) == 1);
    CHECK(LocalCoordinate(-17) == 15);
    CHECK(LocalIndex(15,15,63) == 16383);
    for (int x=-1024;x<1024;++x) {
        CHECK(FloorDivide(x,16)*16+LocalCoordinate(x)==x);
        CHECK(LocalCoordinate(x)>=0 && LocalCoordinate(x)<16);
    }

    Inventory inv;
    CHECK(!inv.Add(Item::Stone,-1));
    CHECK(!inv.Remove(Item::Stone,-1));
    CHECK(!inv.Add(Item::Count,1));
    CHECK(!inv.Add(Item::Stone,std::numeric_limits<int>::max()));
    CHECK(inv.Add(Item::Log,3));
    CHECK(inv.Craft(Recipe::Planks));
    CHECK(inv.Count(Item::Log)==2 && inv.Count(Item::Plank)==4);
    CHECK(inv.Add(Item::IronOre,2));
    const auto before = inv.Counts();
    CHECK(!inv.Craft(Recipe::IronIngot));
    CHECK(inv.Counts()==before); // coal missing: iron must not be consumed.
    CHECK(inv.Add(Item::Coal,1));
    CHECK(inv.Craft(Recipe::IronIngot));
    CHECK(inv.Count(Item::IronOre)==0 && inv.Count(Item::Coal)==0 && inv.Count(Item::IronIngot)==1);
    CHECK(inv.Add(Item::Plank,MaxStack-4));
    const auto full = inv.Counts();
    CHECK(!inv.Craft(Recipe::Planks));
    CHECK(inv.Counts()==full);
    auto invalid = full; invalid[0] = -1;
    CHECK(!inv.Restore(invalid) && inv.Counts()==full);

    World a(1337,32), b(1337,32), c(1377,32);
    bool different = false;
    for (int y=-16;y<16;++y) for (int x=-16;x<16;++x) for (int z=0;z<64;++z) {
        CHECK(a.Get({x,y,z})==b.Get({x,y,z}));
        if (a.Get({x,y,z})!=c.Get({x,y,z})) different = true;
        const Cell recovered = a.CellAt(a.Index({x,y,z}));
        CHECK(recovered.x==x && recovered.y==y && recovered.z==z);
    }
    CHECK(different);
    CHECK(!a.Set({0,0,0},Block::Air));
    CHECK(!a.Set({0,0,64},Block::Stone));
    CHECK(!a.Set({16,0,10},Block::Stone));
    CHECK(!a.Set({0,0,40},Block::Count));
    CHECK(!a.Set({0,0,40},Block::Bedrock));
    CHECK(a.Set({-1,0,40},Block::Stone));
    CHECK(a.Set({0,0,40},Block::Stone));
    int faceCount = 0;
    for (int cx : {-1,0}) for (const auto& face : a.MeshChunk(cx,0)) {
        if (face.cell.z==40) ++faceCount;
        CHECK(!(face.cell.x==-1 && face.cell.y==0 && face.cell.z==40 && face.direction==0));
        CHECK(!(face.cell.x==0 && face.cell.y==0 && face.cell.z==40 && face.direction==1));
    }
    CHECK(faceCount==10); // two cubes across a chunk boundary share a hidden face.
    Inventory stock;
    CHECK(stock.Add(Item::Stone,MaxStack));
    CHECK(!a.Mine({0,0,40},stock));
    CHECK(a.Get({0,0,40})==Block::Stone);
    CHECK(stock.Remove(Item::Stone,1));
    CHECK(a.Mine({0,0,40},stock));
    CHECK(stock.Count(Item::Stone)==MaxStack);
    CHECK(a.Get({0,0,40})==Block::Air);
    CHECK(a.Place({0,0,40},Item::Stone,stock));
    CHECK(stock.Count(Item::Stone)==MaxStack-1);
    CHECK(!a.Place({0,0,40},Item::Stone,stock));
    CHECK(stock.Count(Item::Stone)==MaxStack-1);
    CHECK(!a.Place({0,0,41},Item::IronIngot,stock));
    CHECK(a.Set({0,0,40},Block::Air));
    CHECK(a.Set({-1,0,40},Block::Air));
    CHECK(a.Edits().empty()); // reverting to seed removes redundant deltas.

    CHECK(a.Set({-2,3,42},Block::Planks));
    CHECK(a.Set({4,5,4},Block::Air));
    auto edits = a.Edits();
    CHECK(b.RestoreEdits(edits));
    CHECK(b.Get({-2,3,42})==Block::Planks && b.Get({4,5,4})==Block::Air);
    auto duplicate = edits; duplicate.push_back(edits[0]);
    CHECK(!b.RestoreEdits(duplicate));
    CHECK(b.Edits().size()==edits.size());
    CHECK(!b.RestoreEdits({{std::numeric_limits<std::uint32_t>::max(),Block::Stone}}));
    CHECK(!b.RestoreEdits({{0,Block::Air}}));

    Clock clock;
    CHECK(clock.Day()==1 && clock.Hour()==6);
    clock.Advance(1440);
    CHECK(clock.Day()==2 && clock.Hour()==6);
    clock.Advance(-5); clock.Advance(std::numeric_limits<double>::quiet_NaN());
    CHECK(clock.Day()==2 && clock.Hour()==6);
    CHECK(clock.Restore(7*1440));
    CHECK(clock.Day()==8 && clock.Season()==1);
    CHECK(!clock.Restore(std::numeric_limits<double>::infinity()));

    Snapshot original;
    original.width=32; original.seed=a.Seed(); original.edits=edits; original.inventory=stock;
    original.player={-450,780,3200,90,-25}; original.minutes=clock.Minutes();
    const auto encoded=Encode(original);
    CHECK(!encoded.empty());
    Snapshot loaded;
    CHECK(Decode(encoded,loaded));
    CHECK(loaded.width==32 && loaded.player.x==-450 && loaded.player.pitch==-25);
    CHECK(loaded.inventory.Counts()==stock.Counts());
    CHECK(loaded.minutes==original.minutes && loaded.edits.size()==edits.size());
    World restored(loaded.seed,loaded.width);
    CHECK(restored.RestoreEdits(loaded.edits));
    CHECK(restored.Get({-2,3,42})==Block::Planks);
    const auto immutable = Encode(loaded);
    for (std::size_t size=0;size<encoded.size();++size) {
        const std::vector<std::uint8_t> truncated(encoded.begin(),encoded.begin()+size);
        CHECK(!Decode(truncated,loaded));
        CHECK(Encode(loaded)==immutable);
    }
    for (std::size_t byte=0;byte<encoded.size();++byte) {
        auto corrupt=encoded; corrupt[byte]^=0x80;
        CHECK(!Decode(corrupt,loaded));
        CHECK(Encode(loaded)==immutable);
    }
    auto future=encoded; future[4]=2; Rehash(future);
    CHECK(!Decode(future,loaded));
    auto hugeCount=encoded;
    for (int i=84;i<88;++i) hugeCount[i]=255;
    Rehash(hugeCount); CHECK(!Decode(hugeCount,loaded));
    auto unknownBlock=encoded; unknownBlock[92]=255; unknownBlock[93]=255;
    Rehash(unknownBlock); CHECK(!Decode(unknownBlock,loaded));
    auto trailing=encoded; trailing.push_back(0); Rehash(trailing);
    CHECK(!Decode(trailing,loaded));
    Snapshot bad=original; bad.player.x=std::numeric_limits<float>::quiet_NaN();
    CHECK(Encode(bad).empty());
    bad=original; bad.edits.push_back(bad.edits.front());
    CHECK(Encode(bad).empty());
    std::cout << "RealmCore: " << checks << " checks, " << failed << " failures\n";
    return failed==0 ? 0 : 1;
}
