#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "RealmCore.h"
#include "RealmWorld.generated.h"

class ARealmChunk;
class ARealmCharacter;
class UMaterialInterface;

UCLASS()
class VOXELLORD_API ARealmWorld : public AActor
{
    GENERATED_BODY()
public:
    ARealmWorld();
    virtual void BeginPlay() override;
    virtual void Tick(float DeltaSeconds) override;
    bool Mine(realm::Cell Cell);
    bool Place(realm::Cell Cell, realm::Item Item);
    bool Craft(realm::Recipe Recipe);
    bool SaveRealm(ARealmCharacter* Player);
    bool LoadRealm(ARealmCharacter* Player);
    FVector SpawnLocation() const;
    const realm::Inventory& Inventory() const { return Stockpile; }
    const realm::Clock& Calendar() const { return Time; }
    int32 BlockAt(realm::Cell Cell) const;
    FString Status = TEXT("Welcome to your realm. Mine timber, craft planks, build a shelter.");
private:
    void RebuildAll();
    void RebuildAffected(realm::Cell Cell);
    void RebuildChunk(FIntPoint Key);
    realm::World Data;
    realm::Inventory Stockpile;
    realm::Clock Time;
    UPROPERTY() TMap<FIntPoint,TObjectPtr<ARealmChunk>> Chunks;
    UPROPERTY() TObjectPtr<UMaterialInterface> VoxelMaterial;
};
