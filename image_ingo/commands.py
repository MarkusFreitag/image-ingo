import click
import re
from .models import ImageList


def validate_offset(ctx, param, value):
    if bool(re.match(r'^(?:\+|\-)\d\d\d\d$', value)):
        return value
    raise click.BadParameter('The offset should look like -0100(-1h) or +0130 (+1h30min).')


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.argument('sourcepath', required=True, type=click.Path(exists=True, file_okay=False, readable=True, resolve_path=True))
@click.argument('destinationpath', required=True, type=click.Path(exists=True, file_okay=False, readable=True, resolve_path=True))
@click.option('--topic', '-t', required=True, help='Specify the topic of source images.')
@click.option('--photographer', '-p', default='', help='Photographer that took the images.')
@click.option('--offset', callback=validate_offset, help='Specify a time offset like -0100(-1h) or +0130 (+1h30min)')
@click.option('--no-preview', is_flag=True, help='Disable the preview for destination files.')
@click.option('--no-progress', is_flag=True, help='Disable the progress bar while copying files.')
def cli(sourcepath, destinationpath, topic, photographer, offset, no_preview, no_progress):
    click.echo('source path: {}'.format(sourcepath))
    click.echo('destination path: {}'.format(destinationpath))
    click.echo('topic: {}'.format(topic))
    click.echo('photographer: {}'.format(photographer))
    for type_ in ['JPG', 'CR2']:
        click.echo('Processing {} files...'.format(type_))
        imglist = ImageList(sourcepath, destinationpath, topic, photographer, type_)
        imglist.load()
        imglist.process(offset=offset)
        if not no_preview:
            click.echo_via_pager(imglist.preview())
        if not click.confirm('Do you want to move the files?'):
            click.echo('Aborted!')
            continue
        imglist.copy_files(no_progress=no_progress)
