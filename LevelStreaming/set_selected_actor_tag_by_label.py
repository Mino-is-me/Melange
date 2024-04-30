import unreal
from Lib import __lib_topaz__ as topaz


selected_actors: list[unreal.Actor] = topaz.get_selected_level_actors()

for actor in selected_actors:
    if len(selected_actors) > 0:
        actor_class = actor.__class__

        if actor_class == unreal.RectLight or unreal.SpotLight or unreal.PointLight:

            actor_tags = actor.get_editor_property("tags")

            if len(actor_tags) == 0:
                actor_tags = ["ENV_Light"]
                actor.set_editor_property("tags", actor_tags)
