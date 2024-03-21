import unreal
from Lib import __lib_topaz__ as topaz
import importlib
importlib.reload(topaz)


def set_light_env_tag(selected_actors : list[unreal.Actor] ) -> None:
    for each in selected_actors:

        print(each.__class__)

        if each.__class__ == unreal.Actor: # in case of blueprintActor
            if ( each.get_class().get_name() == 'Ultra_Dynamic_Sky' or 
                 each.get_class().get_name() == 'Ultra_Dynamic_Weather'
              ):
                print('Ultra_Dynamic_Weather / Sky')
            else :
                has_light : list = topaz.get_component_by_class(each. unreal.RectLight)
                if has_light.__len__() > 0 :
                    topaz.set_actor_tag_by_class(each, unreal.RectLight, 'Env_Light')  
                print('Blueprint')

        elif ( each.__class__ == unreal.PointLight or # in case of light
               each.__class__ == unreal.SpotLight or 
               each.__class__ == unreal.RectLight
            ):
            print('Light')

        elif each.__class__ == unreal.CameraActor : # in case of camera 
            print('Camera')

        else :
            print('None')


actors = topaz.get_selected_level_actors()
set_light_env_tag(actors)