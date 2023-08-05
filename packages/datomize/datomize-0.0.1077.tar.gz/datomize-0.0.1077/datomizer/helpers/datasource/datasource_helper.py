import requests
import tempfile
from pathlib import Path
from typing import Tuple
from datomizer import Datomizer
from datomizer.utils.constants import (MANAGEMENT_POST_ADD_ORIGIN_PRIVATE_DATASOURCE, MANAGEMENT_GET_PUT_PRESIGNED_URL,
                                       MANAGEMENT_POST_ADD_TARGET_PRIVATE_DATASOURCE)
from datomizer.utils.general import ID, URL


def create_origin_private_datasource_put_presigned(datomizer: Datomizer, path: str) -> Tuple[int, str]:
    datasource = datomizer.get_response_json(requests.post, url=MANAGEMENT_POST_ADD_ORIGIN_PRIVATE_DATASOURCE)
    put_presigned_response = datomizer.get_response_json(requests.get,
                                                         url=MANAGEMENT_GET_PUT_PRESIGNED_URL,
                                                         url_params=[datasource[ID], path])
    return datasource[ID], put_presigned_response[URL]


def create_origin_private_datasource_from_path(datomizer: Datomizer, path: Path):
    datasource_id, put_presigned_url = create_origin_private_datasource_put_presigned(datomizer, path.name)
    upload_temp_file(path, put_presigned_url)
    return datasource_id


def create_origin_private_datasource_from_df(datomizer: Datomizer, df, name="temp") -> int:
    if not name.endswith(".csv"):
        name = name + ".csv"

    datasource_id, put_presigned_url = create_origin_private_datasource_put_presigned(datomizer, name)
    upload_dataframe(put_presigned_url, df, name)
    return datasource_id


def create_target_private_datasource(datomizer: Datomizer) -> int:
    datasource = datomizer.get_response_json(requests.post, url=MANAGEMENT_POST_ADD_TARGET_PRIVATE_DATASOURCE)
    return datasource[ID]


def upload_dataframe(presigned_url: str, df, name: str) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        path = f"{temp_dir}/{name}"
        df_type = f"{type(df).__module__}.{type(df).__name__}"
        if df_type == "pandas.core.frame.DataFrame":
            df.to_csv(path, index=False)
        upload_temp_file(path, presigned_url)


def upload_temp_file(path, presigned_url):
    with open(path, 'rb') as temp_file:
        response = requests.put(url=presigned_url, data=temp_file)
        Datomizer.validate_response(response, "Upload to put presigned url")
