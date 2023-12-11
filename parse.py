import click
import os.path
import json
import DownloadManager as dm


@click.group()
def cli():
    pass

def remove_unspecified(input_dict):
    return {key: value for key, value in input_dict.items() if value is not None}

@cli.command()
@click.option('--path_for_downloads')
@click.option('--folder_name')
@click.option('--noFolder')
def set_up(path_for_downloads, folder_name, noFolder):
    dm.set_up(remove_unspecified({
        "path_for_downloads": path_for_downloads,
        "folder_name": folder_name,
        "noFolder": noFolder
    }))

@cli.command()
@click.option('--name', required=True, type=str)
@click.option('--polygon', default=None, type=str)
@click.option('--dem', default=None, type=list)
@click.option('--begin', required=True, type=str)
def new_area(name, polygon, dem, begin):
    print("called")
    if not ((polygon==None) ^ (dem==None)):
        raise click.UsageError("Either --polygon or --dem must be specified.")
    dm.new_area(name=name, polygon=polygon, dem=dem, begin=begin)

@cli.command()
@click.argument('area', type=str)
def get_area(name):
    dm.get_area(name)

@cli.command()
@click.argument('areaname', type=str, required=True)
@click.option('--name', required=True, type=str)
@click.option('--polygon', default=None, type=str)
@click.option('--dem', default=None, type=list)
@click.option('--begin', required=True, type=int)
@click.option('--options', type=str)
def modify_area(areaname, name, polygon, dem, begin, options):
    if polygon!=None and dem!=None:
        raise click.UsageError("Only one of --polygon and --dem may be specified.")
    dm.modify_area(areaname, remove_unspecified({
        "name": name,
        "polygon": polygon,
        "dem": dem,
        "begin": begin
    }))

@cli.command()
@click.argument('name', required=True)
def remove_area(name):
    dm.remove_area(name)

@cli.command()
def show_destination():
    print(dm.get_destination())

@cli.command()
@click.argument('new_destination', type=str, required=True)
@click.option('--name', type=str)
def modify_destination(new_destination, name):
    if os.path.exists(new_destination):
        if name != None:
            dm.modify_destination(parent_directory=new_destination, folder_name=name)
        else:
            dm.modify_destination(parent_directory=new_destination)
    else:
        print("Invalid path provided, nothing done. (path must already exist prior to use)")

@cli.command()
def show_areas():
    print(json.dumps(dm.get_areas(), indent=4))


if __name__ == '__main__':
    cli()