"""derived module to host source for derived metadata."""

import typing as t


def compute_scan_coverage(z_array: t.List[float]):
    """Computes ScanCoverage and Min/Max of Slice location.

    Args:
        collection (DICOMCollection): A DICOMCollection instance.

    Returns:
        float: Scan Coverage.
        float: Max location of slice.
        float: Min location of slice.
    """
    max_slice_location = max(z_array)
    min_slice_location = min(z_array)
    scan_coverage = abs(max_slice_location - min_slice_location)
    return scan_coverage, max_slice_location, min_slice_location
