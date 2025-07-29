import unreal

def render_sequencer():
    """
    Renders the currently open level sequence using Unreal Engine's Movie Render Pipeline.
    """
    # Get the current level sequence
    sequencer = unreal.LevelSequenceEditorBlueprintLibrary.get_current_level_sequence()
    if not sequencer:
        unreal.log_error("No level sequence selected. Please open a sequence in the Sequencer editor.")
        return
    
    sequencer_name = sequencer.get_name()
    unreal.log(f"Setting up render job for sequence: {sequencer_name}")
    
    try:
        # Get the movie pipeline queue subsystem
        pipeline_subsystem = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem)
        
        # Create a new job for the current sequence
        job = pipeline_subsystem.add_job_to_queue(sequencer)
        
        # Create a new configuration
        config = unreal.MoviePipelineMasterConfig()
        job.set_configuration(config)
        
        # Configure output settings
        output_setting = config.find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting)
        output_setting.output_directory = unreal.DirectoryPath("/Game/Movies")
        output_setting.file_name_format = "{sequence_name}/{frame_number}"
        output_setting.output_resolution = unreal.IntPoint(1920, 1080)
        
        # Configure image settings
        image_setting = config.find_or_add_setting_by_class(unreal.MoviePipelineDeferredPassBase)
        if hasattr(image_setting, "output_format"):
            image_setting.output_format = unreal.EImageFormat.PNG
        
        # Set up anti-aliasing
        aa_setting = config.find_or_add_setting_by_class(unreal.MoviePipelineAntiAliasingSetting)
        aa_setting.spatial_sample_count = 4
        aa_setting.temporal_sample_count = 8
        
        # Execute the queue with a local executor
        unreal.log(f"Starting render for sequence: {sequencer_name}")
        executor = unreal.MoviePipelineExecutorLocal()
        pipeline_subsystem.render_queue_with_executor_instance(executor)
        
    except Exception as e:
        unreal.log_error(f"Error setting up render: {str(e)}")

# Execute the function
if __name__ == "__main__":
    render_sequencer()