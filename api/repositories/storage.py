import posixpath
from io import BytesIO

from google.auth.credentials import AnonymousCredentials
from google.cloud.storage import Client


class StockSeriesRepository(Client):
    """Storage repository to handle general data from GCS."""

    def __init__(
        self, bucket: str, blob_prefix: str, folder: str = "stocks"
    ) -> None:
        client_credentials = AnonymousCredentials()
        super().__init__(credentials=client_credentials)
        self._bucket = self.bucket(bucket)
        self._folder = folder
        self._blob_prefix = blob_prefix

    def download_as_buffer(self, blob_name: str) -> BytesIO:
        """Download specified blob as bytes."""
        blob_path = posixpath.join(self._blob_prefix, blob_name)
        blob = self._bucket.blob(blob_path)

        buffered_data = BytesIO()
        blob.download_to_file(buffered_data)
        buffered_data.seek(0)

        return buffered_data
