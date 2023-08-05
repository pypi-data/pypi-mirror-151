"""
The HEA Server storage Microservice provides ...
"""

from heaserver.service import response
from heaserver.service.runner import init_cmd_line, routes, start, web
from heaserver.service.db import awsservicelib, mongo
from heaserver.service.wstl import builder_factory, action

MONGODB_STORAGE_COLLECTION = 'storage'


@routes.get('/volumes/{volume_id}/storage')
@routes.get('/volumes/{volume_id}/storage/')
@action('heaserver-storage-storage-get-open-choices', rel='hea-opener-choices',
        path='/volumes/{volume_id}/storage/{id}/opener')
async def get_all_storage(request: web.Request) -> web.Response:
    """
    Gets all the storage of the volume id.
    :param request: the HTTP request.
    :return: all storage list.
    ---
    summary: get all storage for a hea-volume associate with account.
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the user's AWS volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
    responses:
      '200':
        description: Expected response to a valid request.
        content:
            application/json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.collection+json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.wstl+json:
                schema:
                    type: array
                    items:
                        type: object
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.get_all_storages(request)


@routes.get('/ping')
async def ping(request: web.Request) -> web.Response:
    """
    For testing whether the service is up.

    :param request: the HTTP request.
    :return: Always returns status code 200.
    """
    return response.status_ok(None)


@routes.get('/volumes/{volume_id}/buckets/byname/{bucket_name}/storage')
async def get_bucket_storage(request: web.Request) -> web.Response:
    """
    Gets all storage within the specified bucket name.
    :param request: the HTTP request.
    :return: a list of requested storage within the bucket or Not Found.
    ---
    summary: Gets all storage within bucket paginated.
    parameters:
        - name: bucket_name
          in: path
          required: true
          description: The name of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A bucket name
              value: hci-foundation
        - name: volume_id
          in: path
          required: true
          description: The id of the user's AWS volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
    responses:
      '200':
        description: Expected response to a valid request.
        content:
            application/json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.collection+json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.wstl+json:
                schema:
                    type: array
                    items:
                        type: object
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.get_all_storages(request=request)


def main() -> None:
    config = init_cmd_line(description='a service for managing storage and their data within the cloud',
                           default_port=8080)
    start(db=mongo.Mongo, wstl_builder_factory=builder_factory(__package__), config=config)
