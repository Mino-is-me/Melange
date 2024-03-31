import unreal 

__all__ = ['movie_queue_render']

def movie_queue_render(u_level_file : str, u_level_seq_file : str, u_preset_file : str):
    subsystem = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem)
    queue = subsystem.get_queue()
    executor = unreal.MoviePipelinePIEExecutor()
    
    # config render job with movie pipeline config
    job = queue.allocate_new_job(unreal.MoviePipelineExecutorJob)
    job.job_name = 'test'
    job.map = unreal.SoftObjectPath(u_level_file)
    job.sequence = unreal.SoftObjectPath(u_level_seq_file)
    preset = unreal.EditorAssetLibrary.find_asset_data(u_preset_file).get_asset()
    job.set_configuration(preset)
    
    subsystem.render_queue_with_executor_instance(executor)