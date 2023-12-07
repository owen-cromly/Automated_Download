import click
import DownloadManager as dm

def xor_options(ctx, param, value):
    other_option = ctx.params.get('other_option')
    if bool(value) == bool(other_option):
        raise click.UsageError("Exactly one of --option1 or --option2 must be specified.")
    return value

@click.command()
@click.option('--name', required=True, help="the name of the area")
@click.option('--polygon', is_flag=True, default=None, callback=xor_options, expose_value=False, help="WKT polygon with quotes: e.g. \"POLYGON(lat1 long1, lat1 long2, lat3 long3, lat4 long4)\"")
@click.option('--bounds', type=list, default=None, is_flag=True, callback=xor_options, expose_value=False, help="list geographical bounds with brackets: e.g. [lat_min, lat_max, long_min, long_max]")
@click.option('--begin', required=True)
def new_area(name, polygon, bounds, begin):
    dm.new_area(name=name, polygon=polygon, dem=bounds, begin=begin)