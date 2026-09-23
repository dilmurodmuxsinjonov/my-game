using UnrealBuildTool;
using System.IO;
public class VoxelLord : ModuleRules
{
    public VoxelLord(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
        CppStandard = CppStandardVersion.Cpp20;
        PublicIncludePaths.Add(Path.Combine(ModuleDirectory, "Core"));
        PublicDependencyModuleNames.AddRange(new[] { "Core", "CoreUObject", "Engine", "InputCore", "ProceduralMeshComponent" });
    }
}
