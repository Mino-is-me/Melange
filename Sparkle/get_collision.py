# SM Comp 콜리전 읽음
# landscape는 읽지 않음
# preset이 custom일때만 콜리전 채널 읽음


import unreal

selected_actors = unreal.EditorLevelLibrary.get_selected_level_actors()

for actor in selected_actors:



    # 랜드스케이프건너 뛰기 > 컴포넌트를 다읽어서 오래걸림. 로그 전쟁임
    if isinstance(actor, unreal.Landscape):
        print("오브젝트 {}는 랜드스케이프입니다. 건너뜁니다.".format(actor.get_actor_label()))
        continue


    components = actor.get_components_by_class(unreal.PrimitiveComponent)
        
    for component in components :
            
        component_name = component.get_name() #마지막에 호출할 컴포넌트 네임

        if isinstance(component, unreal.StaticMeshComponent) : #스태틱 매쉬 컴포넌트만 읽어오기 이거 안하면 빌보드 컴포넌트 등 다 읽어옴


            compcol_preset = component.get_collision_profile_name()
            compcol_enabled = component.get_collision_enabled()
            compcol_object = component.get_collision_object_type()

            compcol_enabled_str = str(compcol_enabled).replace("CollisionEnabled.", "")
            compcol_object_str = str(compcol_object).replace("CollisionChannel.ECC_", "")

        
            print(">>>>>", actor.get_actor_label(), "<<<<<")

            print(component_name, ">> Collision Presets <<" ,compcol_preset) # 콜리전 프리셋 프린트 Default = BlockAll
            print(component_name, ">> Collision Enabled <<" , compcol_enabled_str)
            print(component_name, ">> Object Type <<" ,compcol_object_str)

            print("--------------------------------------------------------------------------------------------")


            # collision preset 이 custom일때만 하위 채널 읽기
            if compcol_preset == 'custom' :
        
                for compcolchannel in unreal.CollisionChannel:

                    #모든 채널 읽기 
                    response_type = component.get_collision_response_to_channel(compcolchannel)
                    print("Channel: {} >>>> {}".format(compcolchannel.get_display_name(), response_type.get_display_name()))


                print("============================================================================================")

