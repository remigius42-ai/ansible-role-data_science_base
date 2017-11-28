def scrub_output_and_execution_count(model, **kwargs):
    """Scrub output and execution count before saving notebooks.

    Scrubbing may be disabled for an entrire notebook by setting
    the notebook metadata
    {
      'pre_save_hook_config': {
        'is_output_preserved': true
      }
    }
    """
    # check if scrubbing is overridden
    try:
        notebook_metadata = model['content']['metadata']
        if notebook_metadata['pre_save_hook_config']['is_output_preserved']:
            return
    except KeyError:
        pass
    # only run on notebooks
    if model['type'] != 'notebook':
        return
    # only run on nbformat v4
    if model['content']['nbformat'] != 4:
        return

    for cell in model['content']['cells']:
        if cell['cell_type'] != 'code':
            continue
        cell['outputs'] = []
        cell['execution_count'] = None


def jupyter_pre_save_hook(model, **kwargs):
    scrub_output_and_execution_count(model, **kwargs)
