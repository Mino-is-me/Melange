import unreal, importlib
from Lib import __lib_topaz__ as topaz
from Lib import __lib_stelle__ as stelle
importlib.reload(topaz)
importlib.reload(stelle)

animList : str = 'D:/Parsing/list.csv'

anims : list[str] = stelle.read_csv_to_list(animList)

desired_notify_track_list : list[str] = ['IK_L', 'IK_R', 'Foot_L', 'Foot_R', 'Hand_L', 'Hand_R', 'Spine', 'Head', 'Root']


anim_sequences : list[unreal.AnimSequence] = []

for anim in anims :
    anim_sequences.append(unreal.load_asset(anim))
# Get the animation sequence

for anim_sequence in anim_sequences :
    
    for i in desired_notify_track_list :
        
        unreal.AnimationLibrary.add_animation_notify_track(anim_sequence, i)
        

print('Done')