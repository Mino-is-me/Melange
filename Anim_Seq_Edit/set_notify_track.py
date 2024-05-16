import unreal, importlib
from Lib import __lib_topaz__ as topaz
from Lib import __lib_stelle__ as stelle
importlib.reload(topaz)
importlib.reload(stelle)

animList : str = 'D:/Parsing/list.csv'

anims : list[str] = stelle.read_csv_to_list(animList)

desired_notify_track_list : list[str] = ['IK_L', 'IK_R', 'Foot_L', 'Foot_R', 'Hand_L', 'Hand_R', 'Spine', 'Head', 'Root'] 
# Notify Track List
## 빌리한테 리스트 받아서 바꿔야함 


anim_sequences : list[unreal.AnimSequence] = []

for anim in anims :
    anim_sequences.append(unreal.load_asset(anim))
# Get the animation sequence

for anim_sequence in anim_sequences :
    
    tracks = unreal.AnimationLibrary.get_animation_notify_track_names(anim_sequence)
    print('이미 있는 트랙 리스트 : ')
    print(tracks)
    
    need_to_add_notify_track_list = [i for i in desired_notify_track_list if i not in tracks]
    print('추가해야 할 트랙 리스트 : ')
    print(need_to_add_notify_track_list)
    
    for i in need_to_add_notify_track_list :
        unreal.AnimationLibrary.add_animation_notify_track(anim_sequence, i)
        
    print(anim_sequence.get_path_name() + '의 Notify Track이 추가되었습니다.   ' + '추가된 Notify Track : ' + ( ', '.join(need_to_add_notify_track_list)))
