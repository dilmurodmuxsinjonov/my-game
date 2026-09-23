using UnrealBuildTool;
public class VoxelLordEditorTarget : TargetRules
{
    public VoxelLordEditorTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Editor;
        DefaultBuildSettings = BuildSettingsVersion.V5;
        IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
        ExtraModuleNames.Add("VoxelLord");
    }
}
