"""Util module."""
# <!-- markdown-link-check-disable -->
import copy
import logging
import os
import re
import typing as t
from pathlib import Path

from flywheel_gear_toolkit import GearToolkitContext
from flywheel_gear_toolkit.utils.qc import add_qc_info
from fw_meta import MetaData
from pydicom.tag import BaseTag

AnyPath = t.Union[str, Path]

log = logging.getLogger(__name__)

# From https://gitlab.com/flywheel-io/product/backend/core-api/-/blob/master/core/models/file_types.py
FILETYPES = {
    "dicom": [".dcm", ".dcm.zip", ".dicom.zip", ".dicom"],
    "nifti": [".nii.gz", ".nii", ".nifti"],
    "ParaVision": [".pv5.zip", ".pv6.zip"],
}
# Adding additional file types
FILETYPES.update({"ptd": [".ptd"]})


def get_startswith_lstrip_dict(dict_: t.Dict, startswith: str) -> t.Dict:
    """Returns dictionary filtered with keys starting with startswith."""
    res = {}
    for k, v in dict_.items():
        if k.startswith(startswith):
            res[k.split(f"{startswith}.")[1]] = v
    return res


def validate_file(filepath: AnyPath) -> t.List[str]:
    """Returns a list of validation errors if any."""
    errors = []
    errors += validate_file_size(filepath)
    return errors


def validate_file_size(filepath: AnyPath) -> t.List[str]:
    """Returns a list of validation errors related to file size."""
    errors = []
    if not os.path.getsize(filepath) > 1:
        errors.append("File is empty: {}".format(filepath))
    return errors


def sanitize_modality(modality: str):
    """Remove invalid characters in modality.

    Args:
        modality (str): Modality string.

    Returns:
        str: Modality with only spaces, alphanumeric and '-'.
    """
    reg = re.compile(r"[^ 0-9a-zA-Z_-]+")
    modality_sanitized = reg.sub("-", modality)
    if modality_sanitized != modality:
        log.info(f"Sanitizing modality {modality} -> {modality_sanitized}")
    return modality_sanitized


def create_metadata(
    context: GearToolkitContext, fe: t.Dict, meta: MetaData, qc: t.Dict, tags: t.List
):
    """Populates .metadata.json.

    Args:
        context (GearToolkitContext): The gear context.
        fe (dict): A dictionary containing the file attributes to update.
        meta (MetaData): A MetaData containing the file "metadata" (parents container info)
        qc (dict): A dictionary containing the qc namespace info.
        tags (list): List of tag for output file.
    """
    file_name = context.get_input("input-file")["location"]["name"]

    # Build qc namespace
    info = add_qc_info(context, context.get_input("input-file"), **qc)

    # file update
    info.update(fe.get("info", {}))  # to preserve existing info key/value
    context.update_file_metadata(file_name, info=info, tags=tags)
    if fe.get("modality"):
        modality = sanitize_modality(fe.get("modality"))
        context.update_file_metadata(file_name, modality=modality)

    # parent containers update
    # TODO revisit that age cannot be passed
    if "session.age" in meta:
        _ = meta.pop("session.age")
    context.update_container_metadata(
        "session", **get_startswith_lstrip_dict(meta, "session")
    )
    context.update_container_metadata(
        "subject", **get_startswith_lstrip_dict(meta, "subject")
    )
    context.update_container_metadata(
        "acquisition", **get_startswith_lstrip_dict(meta, "acquisition")
    )

    # https://flywheelio.atlassian.net/browse/GEAR-868
    # Subject needs to be updated on session in old-core
    # These two lines make this gear compatible with 15.x.x and 14.x.x
    sub = context._metadata.pop("subject")
    context._metadata.get("session").update({"subject": sub})


def remove_empty_values(d: t.Dict, recurse=True) -> t.Dict:
    """Removes empty value in dictionary.

    Args:
        d (dict): A dictionary.
        recurse (bool): If true, recurse nested dictionary.

    Returns:
        dict: A filtered dictionary.
    """
    d_copy = copy.deepcopy(d)
    for k, v in d.items():
        if isinstance(v, dict) and recurse:
            d_copy[k] = remove_empty_values(v, recurse=recurse)
        if isinstance(v, BaseTag):
            continue
        if v == "" or v is None or v == [] or v == {}:
            d_copy.pop(k)
    return d_copy


def decode(val: bytes):
    """Decode decoded val or hex repr if cannot be decoded."""
    try:
        val = val.decode("utf-8")
    except UnicodeDecodeError:
        log.debug(f"Cannot decode bytes {val}.  Replacing with hex")
        val = val.hex()
    return val
