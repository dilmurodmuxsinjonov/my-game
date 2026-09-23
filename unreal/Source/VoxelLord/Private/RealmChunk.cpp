#include "RealmChunk.h"
#include "ProceduralMeshComponent.h"
#include "Materials/MaterialInterface.h"

namespace {
FLinearColor BlockColor(realm::Block Block)
{
    using B = realm::Block;
    switch (Block) {
        case B::Grass: return FLinearColor(0.19f,0.34f,0.08f);
        case B::Dirt: return FLinearColor(0.28f,0.14f,0.07f);
        case B::Stone: return FLinearColor(0.34f,0.36f,0.39f);
        case B::Wood: return FLinearColor(0.22f,0.10f,0.035f);
        case B::Leaves: return FLinearColor(0.10f,0.26f,0.055f);
        case B::IronOre: return FLinearColor(0.39f,0.22f,0.12f);
        case B::Coal: return FLinearColor(0.07f,0.07f,0.075f);
        case B::Planks: return FLinearColor(0.52f,0.30f,0.11f);
        default: return FLinearColor(0.12f,0.13f,0.15f);
    }
}
}

ARealmChunk::ARealmChunk()
{
    PrimaryActorTick.bCanEverTick = false;
    Mesh = CreateDefaultSubobject<UProceduralMeshComponent>(TEXT("VoxelMesh"));
    SetRootComponent(Mesh);
    // Synchronous collision is intentional for the first correctness slice.
    // Async cooking needs stale-job cancellation and an edit/collision gate.
    Mesh->bUseAsyncCooking = false;
    Mesh->bUseComplexAsSimpleCollision = true;
    Mesh->SetCollisionProfileName(TEXT("BlockAll"));
}

void ARealmChunk::Rebuild(const realm::World& World, int32 ChunkX, int32 ChunkY, UMaterialInterface* Material)
{
    const auto Faces = World.MeshChunk(ChunkX,ChunkY);
    TArray<FVector> Vertices, Normals;
    TArray<int32> Triangles;
    TArray<FVector2D> UVs;
    TArray<FLinearColor> Colors;
    TArray<FProcMeshTangent> Tangents;
    Vertices.Reserve(static_cast<int32>(Faces.size()*4));
    Triangles.Reserve(static_cast<int32>(Faces.size()*6));
    static const FVector Directions[] = {{1,0,0},{-1,0,0},{0,1,0},{0,-1,0},{0,0,1},{0,0,-1}};
    static const FVector Corners[6][4] = {
        {{1,0,0},{1,1,0},{1,1,1},{1,0,1}},
        {{0,1,0},{0,0,0},{0,0,1},{0,1,1}},
        {{1,1,0},{0,1,0},{0,1,1},{1,1,1}},
        {{0,0,0},{1,0,0},{1,0,1},{0,0,1}},
        {{0,0,1},{1,0,1},{1,1,1},{0,1,1}},
        {{0,1,0},{1,1,0},{1,0,0},{0,0,0}}
    };
    static const FVector2D FaceUVs[] = {{0,0},{1,0},{1,1},{0,1}};
    for (const auto& Face : Faces) {
        const int32 Start = Vertices.Num();
        const FVector Origin(Face.cell.x-ChunkX*realm::ChunkSide,Face.cell.y-ChunkY*realm::ChunkSide,Face.cell.z);
        const FVector Tangent = (Corners[Face.direction][1]-Corners[Face.direction][0]).GetSafeNormal();
        for (int32 I=0;I<4;++I) {
            Vertices.Add((Origin+Corners[Face.direction][I])*100.0);
            Normals.Add(Directions[Face.direction]); UVs.Add(FaceUVs[I]);
            Colors.Add(BlockColor(Face.block)); Tangents.Add(FProcMeshTangent(Tangent,false));
        }
        Triangles.Append({Start,Start+1,Start+2,Start,Start+2,Start+3});
    }
    Mesh->ClearAllMeshSections();
    if (!Vertices.IsEmpty()) Mesh->CreateMeshSection_LinearColor(0,Vertices,Triangles,Normals,UVs,Colors,Tangents,true);
    if (Material) Mesh->SetMaterial(0,Material);
}
