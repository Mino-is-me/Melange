import unreal 

objs : list[object] = unreal.EditorLevelLibrary.get_selected_level_actors()
print(objs)

grid_num : int # UI Binded Value
grid_cnt : int # UI Binded Value
offset = 200

offset_vector = unreal.Vector(x=0.0, y=0.0, z=0.0)

for obj in objs : 
        current_location = obj.get_actor_location()
        new_loc = current_location + offset_vector
        
        if offset_vector.x >= offset * (grid_num - 1) :
            offset_vector = unreal.Vector(x=0.0, y=offset * grid_cnt, z=0.0)
            grid_cnt += 1
        else :
            offset_vector += unreal.Vector(x=offset, y=0.0, z=0.0)

        obj.set_actor_location(new_loc, 0, 1)
        print(obj.get_actor_location())