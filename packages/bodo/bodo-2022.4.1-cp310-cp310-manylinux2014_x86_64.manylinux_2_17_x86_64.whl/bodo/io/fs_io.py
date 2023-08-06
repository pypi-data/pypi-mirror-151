"""
S3 & Hadoop file system supports, and file system dependent calls
"""
import glob
import os
import warnings
from urllib.parse import urlparse
import llvmlite.binding as ll
import numba
import numpy as np
from fsspec.implementations.arrow import ArrowFile, ArrowFSWrapper, wrap_exceptions
from numba.core import types
from numba.extending import NativeValue, models, overload, register_model, unbox
import bodo
from bodo.io import csv_cpp
from bodo.libs.distributed_api import Reduce_Type
from bodo.libs.str_ext import unicode_to_utf8, unicode_to_utf8_and_len
from bodo.utils.typing import BodoError, BodoWarning, get_overload_constant_dict
from bodo.utils.utils import check_java_installation


def fsspec_arrowfswrapper__open(self, path, mode='rb', block_size=None, **
    kwargs):
    if mode == 'rb':
        try:
            qdcu__enqx = self.fs.open_input_file(path)
        except:
            qdcu__enqx = self.fs.open_input_stream(path)
    elif mode == 'wb':
        qdcu__enqx = self.fs.open_output_stream(path)
    else:
        raise ValueError(f'unsupported mode for Arrow filesystem: {mode!r}')
    return ArrowFile(self, qdcu__enqx, path, mode, block_size, **kwargs)


ArrowFSWrapper._open = wrap_exceptions(fsspec_arrowfswrapper__open)
_csv_write = types.ExternalFunction('csv_write', types.void(types.voidptr,
    types.voidptr, types.int64, types.int64, types.bool_, types.voidptr))
ll.add_symbol('csv_write', csv_cpp.csv_write)
bodo_error_msg = """
    Some possible causes:
        (1) Incorrect path: Specified file/directory doesn't exist or is unreachable.
        (2) Missing credentials: You haven't provided S3 credentials, neither through 
            environment variables, nor through a local AWS setup 
            that makes the credentials available at ~/.aws/credentials.
        (3) Incorrect credentials: Your S3 credentials are incorrect or do not have
            the correct permissions.
        (4) Wrong bucket region is used. Set AWS_DEFAULT_REGION variable with correct bucket region.
    """


def get_proxy_uri_from_env_vars():
    return os.environ.get('http_proxy', None) or os.environ.get('https_proxy',
        None) or os.environ.get('HTTP_PROXY', None) or os.environ.get(
        'HTTPS_PROXY', None)


def get_s3_fs(region=None, storage_options=None):
    from pyarrow.fs import S3FileSystem
    zwpkb__hgxlb = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    fgfgz__url = False
    seqsj__untb = get_proxy_uri_from_env_vars()
    if storage_options:
        fgfgz__url = storage_options.get('anon', False)
    return S3FileSystem(anonymous=fgfgz__url, region=region,
        endpoint_override=zwpkb__hgxlb, proxy_options=seqsj__untb)


def get_s3_subtree_fs(bucket_name, region=None, storage_options=None):
    from pyarrow._fs import SubTreeFileSystem
    from pyarrow._s3fs import S3FileSystem
    zwpkb__hgxlb = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    fgfgz__url = False
    seqsj__untb = get_proxy_uri_from_env_vars()
    if storage_options:
        fgfgz__url = storage_options.get('anon', False)
    fs = S3FileSystem(region=region, endpoint_override=zwpkb__hgxlb,
        anonymous=fgfgz__url, proxy_options=seqsj__untb)
    return SubTreeFileSystem(bucket_name, fs)


def get_s3_fs_from_path(path, parallel=False, storage_options=None):
    region = get_s3_bucket_region_njit(path, parallel=parallel)
    if region == '':
        region = None
    return get_s3_fs(region, storage_options)


def get_hdfs_fs(path):
    from pyarrow.fs import HadoopFileSystem as HdFS
    get__jkh = urlparse(path)
    if get__jkh.scheme in ('abfs', 'abfss'):
        vcdn__rkgiz = path
        if get__jkh.port is None:
            dorpn__hhtxa = 0
        else:
            dorpn__hhtxa = get__jkh.port
        ieomo__vdboh = None
    else:
        vcdn__rkgiz = get__jkh.hostname
        dorpn__hhtxa = get__jkh.port
        ieomo__vdboh = get__jkh.username
    try:
        fs = HdFS(host=vcdn__rkgiz, port=dorpn__hhtxa, user=ieomo__vdboh)
    except Exception as xvf__lhu:
        raise BodoError('Hadoop file system cannot be created: {}'.format(
            xvf__lhu))
    return fs


def gcs_is_directory(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    try:
        zlx__zmvyh = fs.isdir(path)
    except gcsfs.utils.HttpError as xvf__lhu:
        raise BodoError(
            f'{xvf__lhu}. Make sure your google cloud credentials are set!')
    return zlx__zmvyh


def gcs_list_dir_fnames(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    return [lzkcs__apc.split('/')[-1] for lzkcs__apc in fs.ls(path)]


def s3_is_directory(fs, path):
    from pyarrow import fs as pa_fs
    try:
        get__jkh = urlparse(path)
        udyvm__bveao = (get__jkh.netloc + get__jkh.path).rstrip('/')
        hpyvq__fido = fs.get_file_info(udyvm__bveao)
        if hpyvq__fido.type in (pa_fs.FileType.NotFound, pa_fs.FileType.Unknown
            ):
            raise FileNotFoundError('{} is a non-existing or unreachable file'
                .format(path))
        if (not hpyvq__fido.size and hpyvq__fido.type == pa_fs.FileType.
            Directory):
            return True
        return False
    except (FileNotFoundError, OSError) as xvf__lhu:
        raise
    except BodoError as yvxel__vdg:
        raise
    except Exception as xvf__lhu:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(xvf__lhu).__name__}: {str(xvf__lhu)}
{bodo_error_msg}"""
            )


def s3_list_dir_fnames(fs, path):
    from pyarrow import fs as pa_fs
    pdbe__kmliy = None
    try:
        if s3_is_directory(fs, path):
            get__jkh = urlparse(path)
            udyvm__bveao = (get__jkh.netloc + get__jkh.path).rstrip('/')
            nya__igsfe = pa_fs.FileSelector(udyvm__bveao, recursive=False)
            rymh__tohti = fs.get_file_info(nya__igsfe)
            if rymh__tohti and rymh__tohti[0].path in [udyvm__bveao,
                f'{udyvm__bveao}/'] and int(rymh__tohti[0].size or 0) == 0:
                rymh__tohti = rymh__tohti[1:]
            pdbe__kmliy = [vunt__cobfb.base_name for vunt__cobfb in rymh__tohti
                ]
    except BodoError as yvxel__vdg:
        raise
    except Exception as xvf__lhu:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(xvf__lhu).__name__}: {str(xvf__lhu)}
{bodo_error_msg}"""
            )
    return pdbe__kmliy


def hdfs_is_directory(path):
    from pyarrow.fs import FileType, HadoopFileSystem
    check_java_installation(path)
    get__jkh = urlparse(path)
    adpk__hni = get__jkh.path
    try:
        zpy__ppp = HadoopFileSystem.from_uri(path)
    except Exception as xvf__lhu:
        raise BodoError(' Hadoop file system cannot be created: {}'.format(
            xvf__lhu))
    nvws__zmvq = zpy__ppp.get_file_info([adpk__hni])
    if nvws__zmvq[0].type in (FileType.NotFound, FileType.Unknown):
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if not nvws__zmvq[0].size and nvws__zmvq[0].type == FileType.Directory:
        return zpy__ppp, True
    return zpy__ppp, False


def hdfs_list_dir_fnames(path):
    from pyarrow.fs import FileSelector
    pdbe__kmliy = None
    zpy__ppp, zlx__zmvyh = hdfs_is_directory(path)
    if zlx__zmvyh:
        get__jkh = urlparse(path)
        adpk__hni = get__jkh.path
        nya__igsfe = FileSelector(adpk__hni, recursive=True)
        try:
            rymh__tohti = zpy__ppp.get_file_info(nya__igsfe)
        except Exception as xvf__lhu:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(adpk__hni, xvf__lhu))
        pdbe__kmliy = [vunt__cobfb.base_name for vunt__cobfb in rymh__tohti]
    return zpy__ppp, pdbe__kmliy


def abfs_is_directory(path):
    zpy__ppp = get_hdfs_fs(path)
    try:
        nvws__zmvq = zpy__ppp.info(path)
    except OSError as yvxel__vdg:
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if nvws__zmvq['size'] == 0 and nvws__zmvq['kind'].lower() == 'directory':
        return zpy__ppp, True
    return zpy__ppp, False


def abfs_list_dir_fnames(path):
    pdbe__kmliy = None
    zpy__ppp, zlx__zmvyh = abfs_is_directory(path)
    if zlx__zmvyh:
        get__jkh = urlparse(path)
        adpk__hni = get__jkh.path
        try:
            ckhak__dymxp = zpy__ppp.ls(adpk__hni)
        except Exception as xvf__lhu:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(adpk__hni, xvf__lhu))
        pdbe__kmliy = [fname[fname.rindex('/') + 1:] for fname in ckhak__dymxp]
    return zpy__ppp, pdbe__kmliy


def directory_of_files_common_filter(fname):
    return not (fname.endswith('.crc') or fname.endswith('_$folder$') or
        fname.startswith('.') or fname.startswith('_') and fname !=
        '_delta_log')


def find_file_name_or_handler(path, ftype, storage_options=None):
    from urllib.parse import urlparse
    hbjib__krt = urlparse(path)
    fname = path
    fs = None
    xxtu__kkkx = 'read_json' if ftype == 'json' else 'read_csv'
    jybb__hhqbx = (
        f'pd.{xxtu__kkkx}(): there is no {ftype} file in directory: {fname}')
    elg__iexds = directory_of_files_common_filter
    if hbjib__krt.scheme == 's3':
        vwelh__lnk = True
        fs = get_s3_fs_from_path(path, storage_options=storage_options)
        zvz__gxdy = s3_list_dir_fnames(fs, path)
        udyvm__bveao = (hbjib__krt.netloc + hbjib__krt.path).rstrip('/')
        fname = udyvm__bveao
        if zvz__gxdy:
            zvz__gxdy = [(udyvm__bveao + '/' + lzkcs__apc) for lzkcs__apc in
                sorted(filter(elg__iexds, zvz__gxdy))]
            odd__erpuw = [lzkcs__apc for lzkcs__apc in zvz__gxdy if int(fs.
                get_file_info(lzkcs__apc).size or 0) > 0]
            if len(odd__erpuw) == 0:
                raise BodoError(jybb__hhqbx)
            fname = odd__erpuw[0]
        cgm__qlj = int(fs.get_file_info(fname).size or 0)
        fs = ArrowFSWrapper(fs)
        fhccy__dpeq = fs._open(fname)
    elif hbjib__krt.scheme == 'hdfs':
        vwelh__lnk = True
        fs, zvz__gxdy = hdfs_list_dir_fnames(path)
        cgm__qlj = fs.get_file_info([hbjib__krt.path])[0].size
        if zvz__gxdy:
            path = path.rstrip('/')
            zvz__gxdy = [(path + '/' + lzkcs__apc) for lzkcs__apc in sorted
                (filter(elg__iexds, zvz__gxdy))]
            odd__erpuw = [lzkcs__apc for lzkcs__apc in zvz__gxdy if fs.
                get_file_info([urlparse(lzkcs__apc).path])[0].size > 0]
            if len(odd__erpuw) == 0:
                raise BodoError(jybb__hhqbx)
            fname = odd__erpuw[0]
            fname = urlparse(fname).path
            cgm__qlj = fs.get_file_info([fname])[0].size
        fhccy__dpeq = fs.open_input_file(fname)
    elif hbjib__krt.scheme in ('abfs', 'abfss'):
        vwelh__lnk = True
        fs, zvz__gxdy = abfs_list_dir_fnames(path)
        cgm__qlj = fs.info(fname)['size']
        if zvz__gxdy:
            path = path.rstrip('/')
            zvz__gxdy = [(path + '/' + lzkcs__apc) for lzkcs__apc in sorted
                (filter(elg__iexds, zvz__gxdy))]
            odd__erpuw = [lzkcs__apc for lzkcs__apc in zvz__gxdy if fs.info
                (lzkcs__apc)['size'] > 0]
            if len(odd__erpuw) == 0:
                raise BodoError(jybb__hhqbx)
            fname = odd__erpuw[0]
            cgm__qlj = fs.info(fname)['size']
            fname = urlparse(fname).path
        fhccy__dpeq = fs.open(fname, 'rb')
    else:
        if hbjib__krt.scheme != '':
            raise BodoError(
                f'Unrecognized scheme {hbjib__krt.scheme}. Please refer to https://docs.bodo.ai/latest/source/file_io.html'
                )
        vwelh__lnk = False
        if os.path.isdir(path):
            ckhak__dymxp = filter(elg__iexds, glob.glob(os.path.join(os.
                path.abspath(path), '*')))
            odd__erpuw = [lzkcs__apc for lzkcs__apc in sorted(ckhak__dymxp) if
                os.path.getsize(lzkcs__apc) > 0]
            if len(odd__erpuw) == 0:
                raise BodoError(jybb__hhqbx)
            fname = odd__erpuw[0]
        cgm__qlj = os.path.getsize(fname)
        fhccy__dpeq = fname
    return vwelh__lnk, fhccy__dpeq, cgm__qlj, fs


def get_s3_bucket_region(s3_filepath, parallel):
    try:
        from pyarrow import fs as pa_fs
    except:
        raise BodoError('Reading from s3 requires pyarrow currently.')
    from mpi4py import MPI
    sdygf__zym = MPI.COMM_WORLD
    bucket_loc = None
    if parallel and bodo.get_rank() == 0 or not parallel:
        try:
            web__ugi, aec__berz = pa_fs.S3FileSystem.from_uri(s3_filepath)
            bucket_loc = web__ugi.region
        except Exception as xvf__lhu:
            if os.environ.get('AWS_DEFAULT_REGION', '') == '':
                warnings.warn(BodoWarning(
                    f"""Unable to get S3 Bucket Region.
{xvf__lhu}.
Value not defined in the AWS_DEFAULT_REGION environment variable either. Region defaults to us-east-1 currently."""
                    ))
            bucket_loc = ''
    if parallel:
        bucket_loc = sdygf__zym.bcast(bucket_loc)
    return bucket_loc


@numba.njit()
def get_s3_bucket_region_njit(s3_filepath, parallel):
    with numba.objmode(bucket_loc='unicode_type'):
        bucket_loc = ''
        if isinstance(s3_filepath, list):
            s3_filepath = s3_filepath[0]
        if s3_filepath.startswith('s3://'):
            bucket_loc = get_s3_bucket_region(s3_filepath, parallel)
    return bucket_loc


def csv_write(path_or_buf, D, is_parallel=False):
    return None


@overload(csv_write, no_unliteral=True)
def csv_write_overload(path_or_buf, D, is_parallel=False):

    def impl(path_or_buf, D, is_parallel=False):
        vijk__gnf = get_s3_bucket_region_njit(path_or_buf, parallel=is_parallel
            )
        arh__vpur, bgrfg__xjez = unicode_to_utf8_and_len(D)
        lwxbs__tzz = 0
        if is_parallel:
            lwxbs__tzz = bodo.libs.distributed_api.dist_exscan(bgrfg__xjez,
                np.int32(Reduce_Type.Sum.value))
        _csv_write(unicode_to_utf8(path_or_buf), arh__vpur, lwxbs__tzz,
            bgrfg__xjez, is_parallel, unicode_to_utf8(vijk__gnf))
        bodo.utils.utils.check_and_propagate_cpp_exception()
    return impl


class StorageOptionsDictType(types.Opaque):

    def __init__(self):
        super(StorageOptionsDictType, self).__init__(name=
            'StorageOptionsDictType')


storage_options_dict_type = StorageOptionsDictType()
types.storage_options_dict_type = storage_options_dict_type
register_model(StorageOptionsDictType)(models.OpaqueModel)


@unbox(StorageOptionsDictType)
def unbox_storage_options_dict_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


def get_storage_options_pyobject(storage_options):
    pass


@overload(get_storage_options_pyobject, no_unliteral=True)
def overload_get_storage_options_pyobject(storage_options):
    fdm__zas = get_overload_constant_dict(storage_options)
    aaqv__jyqve = 'def impl(storage_options):\n'
    aaqv__jyqve += (
        "  with numba.objmode(storage_options_py='storage_options_dict_type'):\n"
        )
    aaqv__jyqve += f'    storage_options_py = {str(fdm__zas)}\n'
    aaqv__jyqve += '  return storage_options_py\n'
    gwpg__nhbsv = {}
    exec(aaqv__jyqve, globals(), gwpg__nhbsv)
    return gwpg__nhbsv['impl']
