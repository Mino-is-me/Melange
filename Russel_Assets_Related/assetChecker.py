from array import array
import unreal;

# Get the currently selected actors in the editor
selected_actors: array = unreal.EditorLevelLibrary.get_selected_level_actors()
actors_with_world_grid_material = []
actors_without_material = []
actors_without_static_mesh = []
for actor in selected_actors:
    static_mesh_component = actor.get_components_by_class(unreal.StaticMeshComponent)[0]

    if static_mesh_component:
        static_mesh = static_mesh_component.static_mesh
        if static_mesh :
            materials = static_mesh_component.get_materials()

            for material_index, material in enumerate(materials):
                if material == None:
                    actors_without_material.append(actor.get_actor_label())
                    break
                material_name = material.get_name()
                if "worldgridmaterial" in material_name.lower():
                    actors_with_world_grid_material.append(actor.get_actor_label())
                    break
        else : 
            actors_without_static_mesh.append(actor.get_actor_label())

# Print the list of actors with "worldposition" materials
print("******Actors with 'WorldGridMaterial' materials:", len(actors_with_world_grid_material))
print(actors_with_world_grid_material)

print("******Actors without material:", len(actors_without_material))
print(actors_without_material)

print("******Actors without static mesh:", len(actors_without_static_mesh))
print(actors_without_static_mesh)
