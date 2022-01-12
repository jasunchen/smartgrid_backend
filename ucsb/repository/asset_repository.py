from ucsb.models import user_asset, user
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ucsb.repository.asset_data_repository import delete_asset_data_helper
from ucsb.repository.helpers import *

@api_view(['POST'])
def add_asset(request):

    params = ["email", "name", "description"]
    
    #Check for Required Fields
    for p in params:
        if request.data.get(p, None) == None:
            return Response(
                {"message": "Missing Required Parameters: {}".format(p)}, 
                status = 400)

    #Check for Invalid Parameters
    if verify(request.data, params): 
        return Response(
            {"message": "Request has invalid parameter not in {}".format(params)}, 
            status = 400)

    email = request.data.get('email')
    tmp_user = user(user_email=email)
    name = request.data.get('name')
    desc = request.data.get('description')
    asset = user_asset(user=tmp_user, asset_name=name, description=desc)
    asset.save()
    return Response({"detail":"Asset created successfully"})

@api_view(['POST'])
def update_asset(request):

    params = ["id", "name", "description"]
    
    #Check for Required Fields
    for p in params:
        if request.data.get(p, None) == None:
            return Response(
                {"message": "Missing Required Parameters: {}".format(p)}, 
                status = 400)

    #Check for Invalid Parameters
    if verify(request.data, params): 
        return Response(
            {"message": "Request has invalid parameter not in {}".format(params)}, 
            status = 400)

    id = request.data.get('id')
    name = request.data.get('name')
    desc = request.data.get('description')
    try:
        asset = user_asset.objects.get(id=id)
    except:
        return Response({"detail":"Asset does not exist"}, status=400)
    asset.asset_name = name
    asset.description = desc
    asset.save()
    
    return Response({"detail":"Asset updated successfully"})

@api_view(['DELETE'])
def delete_asset(request):

    params = ["id"]
    
    #Check for Required Fields
    for p in params:
        if request.data.get(p, None) == None:
            return Response(
                {"message": "Missing Required Parameters: {}".format(p)}, 
                status = 400)

    #Check for Invalid Parameters
    if verify(request.data, params): 
        return Response(
            {"message": "Request has invalid parameter not in {}".format(params)}, 
            status = 400)

    id = request.data.get('id')
    try:
        asset = user_asset.objects.get(id=id)
    except:
        return Response({"detail":"Asset does not exist"}, status=400)
    delete_asset_data_helper(id)
    user_asset.objects.filter(id=id).delete()
    return Response({"detail": "Asset deleted successfully"})

@api_view(['GET'])
def get_all_assets(request):

    params = ["email"]
    
    #Check for Required Fields
    for p in params:
        if request.query_params.get(p, None) == None:
            return Response(
                {"message": "Missing Required Parameters: {}".format(p)}, 
                status = 400)

    #Check for Invalid Parameters
    if verify(request.query_params, params): 
        return Response(
            {"message": "Request has invalid parameter not in {}".format(params)}, 
            status = 400)

    email = request.query_params.get('email')
    tmp_user = user.objects.get(user_email=email)
    assets = user_asset.objects.filter(user=tmp_user, is_generation=0).values('id', 'asset_name', 'description')
    generations = user_asset.objects.filter(user=tmp_user, is_generation=1).values('id', 'asset_name', 'description', 'declination', 'azimuth', 'modules_power')
    result = {"assets": assets, "generations": generations}
    return Response(result)
