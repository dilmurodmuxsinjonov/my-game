#include "RealmWorld.h"
#include "RealmChunk.h"
#include "RealmCharacter.h"
#include "Engine/World.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/Controller.h"
#include "Materials/MaterialInterface.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "HAL/FileManager.h"

ARealmWorld::ARealmWorld()
{
    PrimaryActorTick.bCanEverTick = true;
}

void ARealmWorld::BeginPlay()
{
    Super::BeginPlay();
    VoxelMaterial = LoadObject<UMaterialInterface>(nullptr,TEXT("/Game/Materials/M_Voxel.M_Voxel"));
    if (!VoxelMaterial) UE_LOG(LogTemp, Warning, TEXT("Run Tools/Unreal.ps1 Bootstrap to create the voxel material/map."));
    Stockpile.Add(realm::Item::Log,8);
    Stockpile.Add(realm::Item::Stone,16);
    Stockpile.Add(realm::Item::Wheat,6);
    RebuildAll();
}

void ARealmWorld::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);
    Time.Advance(DeltaSeconds);
}

int32 ARealmWorld::BlockAt(realm::Cell Cell) const { return static_cast<int32>(Data.Get(Cell)); }
FVector ARealmWorld::SpawnLocation() const { return FVector(50,50,(Data.Surface(0,0)+1)*100.0+110.0); }

void ARealmWorld::RebuildAll()
{
    for (auto& Pair : Chunks) if (IsValid(Pair.Value)) Pair.Value->Destroy();
    Chunks.Empty();
    const int32 Start = realm::FloorDivide(Data.Min(),realm::ChunkSide);
    const int32 End = realm::FloorDivide(Data.Max()-1,realm::ChunkSide);
    for (int32 Y=Start;Y<=End;++Y) for (int32 X=Start;X<=End;++X) {
        const FVector Origin(X*realm::ChunkSide*100.0,Y*realm::ChunkSide*100.0,0);
        auto* Chunk = GetWorld()->SpawnActor<ARealmChunk>(ARealmChunk::StaticClass(),Origin,FRotator::ZeroRotator);
        if (Chunk) { Chunks.Add(FIntPoint(X,Y),Chunk); Chunk->Rebuild(Data,X,Y,VoxelMaterial); }
    }
}

void ARealmWorld::RebuildChunk(FIntPoint Key)
{
    if (auto* Found = Chunks.Find(Key); Found && IsValid(*Found)) (*Found)->Rebuild(Data,Key.X,Key.Y,VoxelMaterial);
}

void ARealmWorld::RebuildAffected(realm::Cell Cell)
{
    const FIntPoint Key(realm::FloorDivide(Cell.x,realm::ChunkSide),realm::FloorDivide(Cell.y,realm::ChunkSide));
    RebuildChunk(Key);
    const int32 X=realm::LocalCoordinate(Cell.x), Y=realm::LocalCoordinate(Cell.y);
    if (X==0) RebuildChunk(Key+FIntPoint(-1,0));
    if (X==realm::ChunkSide-1) RebuildChunk(Key+FIntPoint(1,0));
    if (Y==0) RebuildChunk(Key+FIntPoint(0,-1));
    if (Y==realm::ChunkSide-1) RebuildChunk(Key+FIntPoint(0,1));
}

bool ARealmWorld::Mine(realm::Cell Cell)
{
    if (!Data.Mine(Cell,Stockpile)) { Status=TEXT("Cannot mine: protected ground, empty target or full stockpile."); return false; }
    RebuildAffected(Cell); Status=TEXT("Resource gathered."); return true;
}
bool ARealmWorld::Place(realm::Cell Cell, realm::Item Item)
{
    if (!Data.Place(Cell,Item,Stockpile)) { Status=TEXT("Cannot build: occupied cell, world boundary or missing material."); return false; }
    RebuildAffected(Cell); Status=TEXT("Block placed."); return true;
}
bool ARealmWorld::Craft(realm::Recipe Recipe)
{
    const bool Result=Stockpile.Craft(Recipe);
    Status=Result ? TEXT("Crafted and stored in the shared stockpile.") : TEXT("Craft failed: missing ingredients or output stack is full.");
    return Result;
}

bool ARealmWorld::SaveRealm(ARealmCharacter* Player)
{
    if (!Player) return false;
    realm::Snapshot Snapshot;
    Snapshot.seed=Data.Seed(); Snapshot.width=Data.Width(); Snapshot.minutes=Time.Minutes();
    Snapshot.inventory=Stockpile; Snapshot.edits=Data.Edits();
    const FVector Position=Player->GetActorLocation();
    const FRotator Rotation=Player->GetControlRotation().GetNormalized();
    Snapshot.player={static_cast<float>(Position.X),static_cast<float>(Position.Y),static_cast<float>(Position.Z),static_cast<float>(Rotation.Yaw),static_cast<float>(Rotation.Pitch)};
    const auto Encoded=realm::Encode(Snapshot);
    if (Encoded.empty()) { Status=TEXT("Save rejected: invalid player/world state."); return false; }
    TArray<uint8> Bytes;
    Bytes.Append(Encoded.data(),static_cast<int32>(Encoded.size()));
    const FString Directory=FPaths::Combine(FPaths::ProjectSavedDir(),TEXT("SaveGames"));
    IFileManager::Get().MakeDirectory(*Directory,true);
    const FString Path=FPaths::Combine(Directory,TEXT("quicksave.vlpt"));
    const FString Temporary=Path+TEXT(".tmp"), Backup=Path+TEXT(".bak");
    if (!FFileHelper::SaveArrayToFile(Bytes,*Temporary)) { Status=TEXT("Save failed: cannot write temporary file."); return false; }
    if (IFileManager::Get().FileExists(*Path) && IFileManager::Get().Copy(*Backup,*Path,true,true)!=COPY_OK) {
        Status=TEXT("Save cancelled: previous save could not be backed up."); return false;
    }
    if (!IFileManager::Get().Move(*Path,*Temporary,true,true)) {
        Status=TEXT("Save replacement failed; previous snapshot is retained in .bak."); return false;
    }
    Status=TEXT("Realm saved (prototype format v1)."); return true;
}

bool ARealmWorld::LoadRealm(ARealmCharacter* Player)
{
    if (!Player) return false;
    const FString Path=FPaths::Combine(FPaths::ProjectSavedDir(),TEXT("SaveGames/quicksave.vlpt"));
    const int64 Size=IFileManager::Get().FileSize(*Path);
    if (Size<=0 || Size>32*1024*1024) { Status=TEXT("No valid quicksave found."); return false; }
    TArray<uint8> Bytes;
    if (!FFileHelper::LoadFileToArray(Bytes,*Path)) { Status=TEXT("Cannot read quicksave."); return false; }
    realm::Snapshot Snapshot;
    const std::vector<std::uint8_t> Encoded(Bytes.GetData(),Bytes.GetData()+Bytes.Num());
    if (!realm::Decode(Encoded,Snapshot)) { Status=TEXT("Save is corrupt or incompatible; current realm was preserved."); return false; }
    realm::World Candidate(Snapshot.seed,Snapshot.width);
    if (!Candidate.RestoreEdits(Snapshot.edits)) { Status=TEXT("Invalid voxel edits; current realm was preserved."); return false; }
    Data=std::move(Candidate); Stockpile=Snapshot.inventory; Time.Restore(Snapshot.minutes);
    RebuildAll();
    Player->SetActorLocation(FVector(Snapshot.player.x,Snapshot.player.y,Snapshot.player.z),false,nullptr,ETeleportType::TeleportPhysics);
    Player->GetCharacterMovement()->StopMovementImmediately();
    if (Player->GetController()) Player->GetController()->SetControlRotation(FRotator(Snapshot.player.pitch,Snapshot.player.yaw,0));
    Status=TEXT("Saved terrain, stockpile, clock and position restored."); return true;
}
