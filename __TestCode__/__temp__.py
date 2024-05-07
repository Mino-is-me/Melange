import unreal
import importlib
from Lib import __lib_topaz__ as topaz
from Lib import __lib_stelle__ as stelle

importlib.reload(topaz)


csv_to_read = 'D:\CINEVStudio\CINEVStudio\Content\Python\CSV\StaticMeshList.csv'

asset_paths = stelle.read_csv_to_list(csv_to_read)
asset = unreal.load_asset(asset_paths[0])

print(asset)

for asset in asset_paths :
    
    actor : unreal.StaticMeshActor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.StaticMeshActor,
        unreal.Vector(0,0,0),
        unreal.Rotator(0,0,0)
    )
    asset = unreal.load_asset(asset)
    
    if asset.__class__ == unreal.StaticMesh :
        nanite_settings : unreal.MeshNaniteSettings     = asset.get_editor_property('nanite_settings')
        print(nanite_settings.keep_percent_triangles)
    
    actor.static_mesh_component.set_static_mesh(asset)