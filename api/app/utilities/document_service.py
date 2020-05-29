"""
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
        http://www.apache.org/licenses/LICENSE-2.0
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
import logging
from datetime import timedelta
from minio import Minio

logger = logging.getLogger(__name__)


class DocumentService():
    """ Load a minio client to handle file requests
    Requires environment variables:
        S3_HOST: hostname for document storage
        S3_BUCKET: storage bucket
        MINIO_ACCESS_KEY: private storage account
        MINIO_SECRET_KEY: private storage secret
    The optional "request" param can be set to the request that requires the minio client.
    This allows generation of full URIs including domain name.
    This is only required for generating private, local links.
    e.g.:
    def get(self, request):
        client = MinioClient(request)
    """

    def __init__(self, host, bucket, access_key, secret_key, use_secure):
        self.host = host
        self.bucket = bucket
        self.access_key = access_key
        self.secret_key = secret_key
        self.use_secure = use_secure

        self.client = Minio(
            self.host,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=self.use_secure
        )

    def get_presigned_put_url(self, object_name):
        """Retrieves the a presigned URL for putting objects into an S3 source"""
        url = self.client.presigned_put_object(self.bucket, object_name, expires=timedelta(days=7))

        return url

    def get_presigned_get_url(self, object_name):
        """Retrieves the presigned URL for GETting objects out of an S3 source"""
        url = self.client.presigned_get_object(self.bucket, object_name, expires=timedelta(days=7))

        return url
