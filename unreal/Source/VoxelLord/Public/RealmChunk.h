#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "RealmCore.h"
#include "RealmChunk.generated.h"

class UProceduralMeshComponent;
class UMaterialInterface;

UCLASS()
class VOXELLORD_API ARealmChunk : public AActor
{
    GENERATED_BODY()
public:
    ARealmChunk();
    void Rebuild(const realm::World& World, int32 ChunkX, int32 ChunkY, UMaterialInterface* Material);
private:
    UPROPERTY(VisibleAnywhere) TObjectPtr<UProceduralMeshComponent> Mesh;
};
