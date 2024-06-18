# 레벨의 SM Actor에 Material element bool 파라미터 하드픽스

import unreal

selected_assets = unreal.EditorLevelLibrary.get_selected_level_actors()



for actor in selected_assets :

    actor_class = actor.get_class()


    # 파라미터 이름 및 수치
    parameter_name = "EnableUDW"
    control_bool_val = True


    # SM Actor 대응
    if isinstance(actor, unreal.StaticMeshActor) :

        get_smComp = actor.static_mesh_component

        for get_mi in get_smComp.get_materials() :

            changeval = unreal.MaterialEditingLibrary.set_material_instance_static_switch_parameter_value(get_mi, parameter_name, control_bool_val)
            unreal.MaterialEditingLibrary.update_material_instance(get_mi)

        
            print( actor.get_name(), ">" , get_mi.get_name() , ">>" , parameter_name , ">>>" , control_bool_val )
    

    

    # BP대응
    elif isinstance(actor_class, unreal.BlueprintGeneratedClass) :

        actor_components = actor.get_components_by_class(unreal.ActorComponent)

        for Comp in actor_components :
            if isinstance(Comp, unreal.StaticMeshComponent) : 
                for get_mi in Comp.get_materials() :

                    changeval = unreal.MaterialEditingLibrary.set_material_instance_static_switch_parameter_value(get_mi, parameter_name, control_bool_val)
                    unreal.MaterialEditingLibrary.update_material_instance(get_mi)

                    print( actor.get_name(), ">" , get_mi.get_name() , ">>" , parameter_name , ">>>" , control_bool_val )




    else :
        pass

 




    

