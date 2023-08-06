from typing import Union
from typing import Optional
from typing import List
from typing import Sequence
from typing import TextIO

import os
import io
import tempfile
import pathlib
import gzip

from rdkit.Chem import PandasTools
from rdkit.Chem import rdmolfiles
from rdkit import Chem

import pandas as pd
import fsspec
import fsspec.utils

import datamol as dm

from .types import Mol


def read_csv(
    urlpath: Union[str, os.PathLike, TextIO],
    smiles_column: Optional[str] = None,
    mol_column: str = "mol",
    **kwargs,
) -> pd.DataFrame:
    """Read a CSV file.

    Args:
        urlpath: Path to a file or a file-like object. Path can be remote or local.
        smiles_column: Use this column to build a mol column.
        mol_column: Name to give to the mol column. If not None a mol column will be build.
            Avoid when loading a very large file.
        kwargs: Arguments to pass to `pd.read_csv()`.

    Returns:
        df: a `pandas.DataFrame`
    """

    df: pd.DataFrame = pd.read_csv(urlpath, **kwargs)  # type: ignore

    if smiles_column is not None:
        PandasTools.AddMoleculeColumnToFrame(df, smiles_column, mol_column)

    return df


def read_excel(
    urlpath: Union[str, os.PathLike, TextIO],
    sheet_name: Optional[Union[str, int, list]] = 0,
    smiles_column: Optional[str] = None,
    mol_column: str = "mol",
    **kwargs,
) -> pd.DataFrame:
    """Read an excel file.

    Args:
        urlpath: Path to a file or a file-like object. Path can be remote or local.
        sheet_name: see `pandas.read_excel()` doc.
        mol_column: Name to give to the mol column. If not None a mol column will be build.
            Avoid when loading a very large file.
        mol_column: name to give to the mol column.
        kwargs: Arguments to pass to `pd.read_excel()`.

    Returns:
        df: a `pandas.DataFrame`
    """

    df = pd.read_excel(urlpath, sheet_name=sheet_name, **kwargs)  # type: ignore

    if smiles_column is not None:
        PandasTools.AddMoleculeColumnToFrame(df, smiles_column, mol_column)

    return df


def read_sdf(
    urlpath: Union[str, os.PathLike, TextIO],
    sanitize: bool = True,
    as_df: bool = False,
    smiles_column: Optional[str] = "smiles",
    mol_column: Optional[str] = None,
    include_private: bool = False,
    include_computed: bool = False,
    strict_parsing: bool = True,
    remove_hs: bool = True,
) -> Union[List[Mol], pd.DataFrame]:
    """Read an SDF file.

    Note: This function is meant to be used with dataset that fit _in-memory_.
    For a more advanced usage we suggest you to use directly `Chem.ForwardSDMolSupplier`.

    Args:
        urlpath: Path to a file or a file-like object. Path can be remote or local.
        sanitize: Whether to sanitize the molecules.
        as_df: Whether to return a list mol or a pandas DataFrame.
        smiles_column: Name of the SMILES column. Only relevant if `as_df` is True.
        mol_column: Name of the mol column. Only relevant if `as_df` is True.
        include_private: Include private properties in the columns.  Only relevant if
            `as_df` is True.
        include_computed: Include computed properties in the columns.  Only relevant if
            `as_df` is True.
        strict_parsing: If set to false, the parser is more lax about correctness of the contents.
        remove_hs: Whether to remove the existing hydrogens in the SDF files.
    """

    # File-like object
    if isinstance(urlpath, io.IOBase):
        supplier = rdmolfiles.ForwardSDMolSupplier(
            urlpath,
            sanitize=sanitize,
            strictParsing=strict_parsing,
            removeHs=remove_hs,
        )
        mols = list(supplier)

    # Regular local or remote paths
    else:
        with fsspec.open(urlpath) as f:

            # Handle gzip file if needed
            if str(urlpath).endswith(".gz") or str(urlpath).endswith(".gzip"):
                f = gzip.open(f)  # type: ignore

            supplier = rdmolfiles.ForwardSDMolSupplier(
                f,
                sanitize=sanitize,
                strictParsing=strict_parsing,
                removeHs=remove_hs,
            )
            mols = list(supplier)

    # Discard None values
    mols = [mol for mol in mols if mol is not None]

    # Convert to dataframe
    if as_df:
        return dm.to_df(
            mols,
            smiles_column=smiles_column,
            mol_column=mol_column,
            include_private=include_private,
            include_computed=include_computed,
        )  # type: ignore

    return mols


def to_sdf(
    mols: Union[Mol, Sequence[Mol], pd.DataFrame],
    urlpath: Union[str, os.PathLike, TextIO],
    smiles_column: Optional[str] = "smiles",
    mol_column: Optional[str] = None,
):
    """Write molecules to a file.

    Args:
        mols: a dataframe, a molecule or a list of molecule.
        urlpath: Path to a file or a file-like object. Path can be remote or local.
        smiles_column: Column name to extract the molecule.
        mol_column: Column name to extract the molecule. It takes
            precedence over `smiles_column`.
    """

    if isinstance(mols, pd.DataFrame):
        mols = dm.from_df(mols, smiles_column=smiles_column, mol_column=mol_column)

    elif isinstance(mols, Mol):
        mols = [mols]

    # Filter out None values
    mols = [mol for mol in mols if mol is not None]

    # File-like object
    if isinstance(urlpath, io.IOBase):
        writer = rdmolfiles.SDWriter(urlpath)
        for mol in mols:
            writer.write(mol)
        writer.close()

    # Regular local or remote paths
    else:
        with fsspec.open(urlpath, mode="w") as f:
            writer = rdmolfiles.SDWriter(f)
            for mol in mols:
                writer.write(mol)
            writer.close()


def to_smi(
    mols: Sequence[Mol],
    urlpath: Union[str, os.PathLike, TextIO],
    error_if_empty: bool = False,
):
    """Save a list of molecules in an `.smi` file.

    Args:
        mols: a list of molecules.
        urlpath: Path to a file or a file-like object. Path can be remote or local.
        error_if_empty: whether to raise and error if the input list is empty.
    """

    if len(mols) == 0 and error_if_empty:
        raise ValueError("The list of mols/smiles provided is empty.")

    # Filter out None values
    mols = [mol for mol in mols if mol is not None]

    # File-like object
    if isinstance(urlpath, io.IOBase):
        writer = rdmolfiles.SmilesWriter(urlpath, includeHeader=False, nameHeader="")
        for mol in mols:
            writer.write(mol)
        writer.close()

    # Regular local or remote paths
    else:
        with fsspec.open(urlpath, "w") as f:
            writer = rdmolfiles.SmilesWriter(f, includeHeader=False, nameHeader="")
            for mol in mols:
                writer.write(mol)
            writer.close()


def read_smi(
    urlpath: Union[str, pathlib.Path, io.IOBase, fsspec.core.OpenFile],
) -> Sequence[Mol]:
    """Read a list of smiles from am `.smi` file.

    Args:
        urlpath: Path to a file or a file-like object. Path can be remote or local.
            Note: file-like object are not supported yet.
    """

    active_path = urlpath

    # NOTE(hadim): the temporary local file copy
    # is because `SmilesMolSupplier` does not support
    # using file-like object, only path.

    # Copy to a local temporary path if the path is a remote one.
    if not fsspec.utils.can_be_local(str(urlpath)):
        active_path = pathlib.Path(tempfile.mkstemp()[1])
        dm.utils.fs.copy_file(urlpath, active_path)

    # Read the molecules
    supplier = rdmolfiles.SmilesMolSupplier(str(active_path), titleLine=0)
    mols = [mol for mol in supplier if mol is not None]

    # Delete the local temporary path
    if not fsspec.utils.can_be_local(str(urlpath)):
        pathlib.Path(str(active_path)).unlink()

    return mols
