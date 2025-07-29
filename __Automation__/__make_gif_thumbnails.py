import unreal

anim_seqs = unreal.EditorUtilityLibrary.get_selected_assets()
level_sequence: unreal.LevelSequence = unreal.LevelSequenceEditorBlueprintLibrary.get_current_level_sequence()

def get_anim_section():
    for binding in level_sequence.get_bindings():
        for track in binding.get_tracks():
            if isinstance(track, unreal.MovieSceneSkeletalAnimationTrack):
                skeletal_animation_sections = track.get_sections()
    print(skeletal_animation_sections[0].params.animation)
    return skeletal_animation_sections[0]

anim_iter = iter(anim_seqs)
on_finished_callback = None  # 글로벌로 유지

def render_next_anim():
    global on_finished_callback
    try:
        anim_seq = next(anim_iter)
    except StopIteration:
        print('----All renders finished----')
        return

    section = get_anim_section()
    section.params.animation = anim_seq

    directory_path = 'E:/temp/' + anim_seq.get_name()
    sequencer_asset_path = '/Game/RnD/Common/EnvChecker/SQ_ENVCHECk.SQ_ENVCHECk'
    capture_settings = unreal.AutomatedLevelSequenceCapture()
    capture_settings.level_sequence_asset = unreal.SoftObjectPath(sequencer_asset_path)
    capture_settings.set_image_capture_protocol_type(unreal.load_class(None, "/Script/MovieSceneCapture.ImageSequenceProtocol_PNG"))
    capture_settings.settings.resolution.res_x = 256
    capture_settings.settings.resolution.res_y = 256
    capture_settings.settings.output_directory = unreal.DirectoryPath(directory_path)
    capture_settings.settings.use_custom_frame_rate = True
    capture_settings.settings.custom_frame_rate = unreal.FrameRate(12,1)
    capture_settings.warm_up_frame_count = 3.0
    capture_settings.delay_before_warm_up = 1.0
    capture_settings.delay_before_shot_warm_up = 1.0

    on_finished_callback = unreal.OnRenderMovieStopped()
    on_finished_callback.bind_callable(on_render_movie_finished)

    print(f"Rendering {anim_seq.get_name()} to movie...")
    unreal.SequencerTools.render_movie(capture_settings, on_finished_callback)

def on_render_movie_finished(success):
    print("Movie has finished rendering. Python can now invoke another movie render if needed. Success: " + str(success))
    render_next_anim()

# 첫 렌더 시작
render_next_anim()