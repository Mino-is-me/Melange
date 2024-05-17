import unreal, importlib
from Lib import __lib_topaz__ as topaz
from Lib import __lib_stelle__ as stelle
importlib.reload(topaz)
importlib.reload(stelle)

animList : str = 'D:/Parsing/list.csv'

anims : list[str] = stelle.read_csv_to_list(animList)

anims = [i in for i in anims '/Game/Customizing/Motion_Final/' + i] ## 경로추가 

desired_notify_track_list : list[str] = ['IK_Pelvis', 'IK_Hand_R', 'Attach_Hand_R', 'IK_Hand_L', 'Attach_Hand_L'] 
desired_curve_track_list : list[str] = ['IKCurve_Pelvis', 'IKCurve_Hand_R', 'IKCurve_Hand_L']
# Notify and Curve Track List


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
    
    
    curve_tracks = unreal.AnimationLibrary.get_animation_curve_names(anim_sequence, unreal.RawCurveTrackTypes.RCT_FLOAT)
    print('이미 있는 커브 리스트 :')
    print(curve_tracks)
    
    need_to_add_curve_track_list = [i for i in desired_curve_track_list if i not in curve_tracks]
    print('추가해야 할 커브 리스트 : ')
    print(need_to_add_curve_track_list)
    
    
    for i in need_to_add_notify_track_list :
        unreal.AnimationLibrary.add_animation_notify_track(anim_sequence, i)
        
    for i in need_to_add_curve_track_list :
        unreal.AnimationLibrary.add_curve(anim_sequence, i, unreal.RawCurveTrackTypes.RCT_FLOAT)
        
    print(anim_sequence.get_path_name() + '의 Notify Track이 추가되었습니다.   ' + '추가된 Notify Track : ' + ( ', '.join(need_to_add_notify_track_list)))
    print(anim_sequence.get_path_name() + '의 Curve Track이 추가되었습니다.   ' + '추가된 Curve Track : ' + ( ', '.join(need_to_add_curve_track_list)))
