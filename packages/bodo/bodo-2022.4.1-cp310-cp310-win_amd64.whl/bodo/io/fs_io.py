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
            qqcyy__bbwl = self.fs.open_input_file(path)
        except:
            qqcyy__bbwl = self.fs.open_input_stream(path)
    elif mode == 'wb':
        qqcyy__bbwl = self.fs.open_output_stream(path)
    else:
        raise ValueError(f'unsupported mode for Arrow filesystem: {mode!r}')
    return ArrowFile(self, qqcyy__bbwl, path, mode, block_size, **kwargs)


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
    hhzn__rya = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    bmz__ctcci = False
    wvka__zpqrr = get_proxy_uri_from_env_vars()
    if storage_options:
        bmz__ctcci = storage_options.get('anon', False)
    return S3FileSystem(anonymous=bmz__ctcci, region=region,
        endpoint_override=hhzn__rya, proxy_options=wvka__zpqrr)


def get_s3_subtree_fs(bucket_name, region=None, storage_options=None):
    from pyarrow._fs import SubTreeFileSystem
    from pyarrow._s3fs import S3FileSystem
    hhzn__rya = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    bmz__ctcci = False
    wvka__zpqrr = get_proxy_uri_from_env_vars()
    if storage_options:
        bmz__ctcci = storage_options.get('anon', False)
    fs = S3FileSystem(region=region, endpoint_override=hhzn__rya, anonymous
        =bmz__ctcci, proxy_options=wvka__zpqrr)
    return SubTreeFileSystem(bucket_name, fs)


def get_s3_fs_from_path(path, parallel=False, storage_options=None):
    region = get_s3_bucket_region_njit(path, parallel=parallel)
    if region == '':
        region = None
    return get_s3_fs(region, storage_options)


def get_hdfs_fs(path):
    from pyarrow.fs import HadoopFileSystem as HdFS
    qyp__tcew = urlparse(path)
    if qyp__tcew.scheme in ('abfs', 'abfss'):
        kdajg__dqltf = path
        if qyp__tcew.port is None:
            ywa__lwoo = 0
        else:
            ywa__lwoo = qyp__tcew.port
        gsdh__laod = None
    else:
        kdajg__dqltf = qyp__tcew.hostname
        ywa__lwoo = qyp__tcew.port
        gsdh__laod = qyp__tcew.username
    try:
        fs = HdFS(host=kdajg__dqltf, port=ywa__lwoo, user=gsdh__laod)
    except Exception as omjp__mxtb:
        raise BodoError('Hadoop file system cannot be created: {}'.format(
            omjp__mxtb))
    return fs


def gcs_is_directory(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    try:
        teie__ubiw = fs.isdir(path)
    except gcsfs.utils.HttpError as omjp__mxtb:
        raise BodoError(
            f'{omjp__mxtb}. Make sure your google cloud credentials are set!')
    return teie__ubiw


def gcs_list_dir_fnames(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    return [gsp__jtdpt.split('/')[-1] for gsp__jtdpt in fs.ls(path)]


def s3_is_directory(fs, path):
    from pyarrow import fs as pa_fs
    try:
        qyp__tcew = urlparse(path)
        xwv__seea = (qyp__tcew.netloc + qyp__tcew.path).rstrip('/')
        cet__awot = fs.get_file_info(xwv__seea)
        if cet__awot.type in (pa_fs.FileType.NotFound, pa_fs.FileType.Unknown):
            raise FileNotFoundError('{} is a non-existing or unreachable file'
                .format(path))
        if not cet__awot.size and cet__awot.type == pa_fs.FileType.Directory:
            return True
        return False
    except (FileNotFoundError, OSError) as omjp__mxtb:
        raise
    except BodoError as bvg__zudka:
        raise
    except Exception as omjp__mxtb:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(omjp__mxtb).__name__}: {str(omjp__mxtb)}
{bodo_error_msg}"""
            )


def s3_list_dir_fnames(fs, path):
    from pyarrow import fs as pa_fs
    fvyot__aspmy = None
    try:
        if s3_is_directory(fs, path):
            qyp__tcew = urlparse(path)
            xwv__seea = (qyp__tcew.netloc + qyp__tcew.path).rstrip('/')
            qogod__tpa = pa_fs.FileSelector(xwv__seea, recursive=False)
            rigzo__rdslo = fs.get_file_info(qogod__tpa)
            if rigzo__rdslo and rigzo__rdslo[0].path in [xwv__seea,
                f'{xwv__seea}/'] and int(rigzo__rdslo[0].size or 0) == 0:
                rigzo__rdslo = rigzo__rdslo[1:]
            fvyot__aspmy = [tvp__jvu.base_name for tvp__jvu in rigzo__rdslo]
    except BodoError as bvg__zudka:
        raise
    except Exception as omjp__mxtb:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(omjp__mxtb).__name__}: {str(omjp__mxtb)}
{bodo_error_msg}"""
            )
    return fvyot__aspmy


def hdfs_is_directory(path):
    from pyarrow.fs import FileType, HadoopFileSystem
    check_java_installation(path)
    qyp__tcew = urlparse(path)
    qznl__nzwx = qyp__tcew.path
    try:
        ylw__kgayf = HadoopFileSystem.from_uri(path)
    except Exception as omjp__mxtb:
        raise BodoError(' Hadoop file system cannot be created: {}'.format(
            omjp__mxtb))
    oinz__fdo = ylw__kgayf.get_file_info([qznl__nzwx])
    if oinz__fdo[0].type in (FileType.NotFound, FileType.Unknown):
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if not oinz__fdo[0].size and oinz__fdo[0].type == FileType.Directory:
        return ylw__kgayf, True
    return ylw__kgayf, False


def hdfs_list_dir_fnames(path):
    from pyarrow.fs import FileSelector
    fvyot__aspmy = None
    ylw__kgayf, teie__ubiw = hdfs_is_directory(path)
    if teie__ubiw:
        qyp__tcew = urlparse(path)
        qznl__nzwx = qyp__tcew.path
        qogod__tpa = FileSelector(qznl__nzwx, recursive=True)
        try:
            rigzo__rdslo = ylw__kgayf.get_file_info(qogod__tpa)
        except Exception as omjp__mxtb:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(qznl__nzwx, omjp__mxtb))
        fvyot__aspmy = [tvp__jvu.base_name for tvp__jvu in rigzo__rdslo]
    return ylw__kgayf, fvyot__aspmy


def abfs_is_directory(path):
    ylw__kgayf = get_hdfs_fs(path)
    try:
        oinz__fdo = ylw__kgayf.info(path)
    except OSError as bvg__zudka:
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if oinz__fdo['size'] == 0 and oinz__fdo['kind'].lower() == 'directory':
        return ylw__kgayf, True
    return ylw__kgayf, False


def abfs_list_dir_fnames(path):
    fvyot__aspmy = None
    ylw__kgayf, teie__ubiw = abfs_is_directory(path)
    if teie__ubiw:
        qyp__tcew = urlparse(path)
        qznl__nzwx = qyp__tcew.path
        try:
            ngtd__qdcg = ylw__kgayf.ls(qznl__nzwx)
        except Exception as omjp__mxtb:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(qznl__nzwx, omjp__mxtb))
        fvyot__aspmy = [fname[fname.rindex('/') + 1:] for fname in ngtd__qdcg]
    return ylw__kgayf, fvyot__aspmy


def directory_of_files_common_filter(fname):
    return not (fname.endswith('.crc') or fname.endswith('_$folder$') or
        fname.startswith('.') or fname.startswith('_') and fname !=
        '_delta_log')


def find_file_name_or_handler(path, ftype, storage_options=None):
    from urllib.parse import urlparse
    hdsv__utao = urlparse(path)
    fname = path
    fs = None
    itzzf__dkbk = 'read_json' if ftype == 'json' else 'read_csv'
    wehf__kkeq = (
        f'pd.{itzzf__dkbk}(): there is no {ftype} file in directory: {fname}')
    qkyc__xmso = directory_of_files_common_filter
    if hdsv__utao.scheme == 's3':
        zgaik__dtf = True
        fs = get_s3_fs_from_path(path, storage_options=storage_options)
        oxwb__jdve = s3_list_dir_fnames(fs, path)
        xwv__seea = (hdsv__utao.netloc + hdsv__utao.path).rstrip('/')
        fname = xwv__seea
        if oxwb__jdve:
            oxwb__jdve = [(xwv__seea + '/' + gsp__jtdpt) for gsp__jtdpt in
                sorted(filter(qkyc__xmso, oxwb__jdve))]
            gwiv__jmo = [gsp__jtdpt for gsp__jtdpt in oxwb__jdve if int(fs.
                get_file_info(gsp__jtdpt).size or 0) > 0]
            if len(gwiv__jmo) == 0:
                raise BodoError(wehf__kkeq)
            fname = gwiv__jmo[0]
        spsb__grr = int(fs.get_file_info(fname).size or 0)
        fs = ArrowFSWrapper(fs)
        dyi__omb = fs._open(fname)
    elif hdsv__utao.scheme == 'hdfs':
        zgaik__dtf = True
        fs, oxwb__jdve = hdfs_list_dir_fnames(path)
        spsb__grr = fs.get_file_info([hdsv__utao.path])[0].size
        if oxwb__jdve:
            path = path.rstrip('/')
            oxwb__jdve = [(path + '/' + gsp__jtdpt) for gsp__jtdpt in
                sorted(filter(qkyc__xmso, oxwb__jdve))]
            gwiv__jmo = [gsp__jtdpt for gsp__jtdpt in oxwb__jdve if fs.
                get_file_info([urlparse(gsp__jtdpt).path])[0].size > 0]
            if len(gwiv__jmo) == 0:
                raise BodoError(wehf__kkeq)
            fname = gwiv__jmo[0]
            fname = urlparse(fname).path
            spsb__grr = fs.get_file_info([fname])[0].size
        dyi__omb = fs.open_input_file(fname)
    elif hdsv__utao.scheme in ('abfs', 'abfss'):
        zgaik__dtf = True
        fs, oxwb__jdve = abfs_list_dir_fnames(path)
        spsb__grr = fs.info(fname)['size']
        if oxwb__jdve:
            path = path.rstrip('/')
            oxwb__jdve = [(path + '/' + gsp__jtdpt) for gsp__jtdpt in
                sorted(filter(qkyc__xmso, oxwb__jdve))]
            gwiv__jmo = [gsp__jtdpt for gsp__jtdpt in oxwb__jdve if fs.info
                (gsp__jtdpt)['size'] > 0]
            if len(gwiv__jmo) == 0:
                raise BodoError(wehf__kkeq)
            fname = gwiv__jmo[0]
            spsb__grr = fs.info(fname)['size']
            fname = urlparse(fname).path
        dyi__omb = fs.open(fname, 'rb')
    else:
        if hdsv__utao.scheme != '':
            raise BodoError(
                f'Unrecognized scheme {hdsv__utao.scheme}. Please refer to https://docs.bodo.ai/latest/source/file_io.html'
                )
        zgaik__dtf = False
        if os.path.isdir(path):
            ngtd__qdcg = filter(qkyc__xmso, glob.glob(os.path.join(os.path.
                abspath(path), '*')))
            gwiv__jmo = [gsp__jtdpt for gsp__jtdpt in sorted(ngtd__qdcg) if
                os.path.getsize(gsp__jtdpt) > 0]
            if len(gwiv__jmo) == 0:
                raise BodoError(wehf__kkeq)
            fname = gwiv__jmo[0]
        spsb__grr = os.path.getsize(fname)
        dyi__omb = fname
    return zgaik__dtf, dyi__omb, spsb__grr, fs


def get_s3_bucket_region(s3_filepath, parallel):
    try:
        from pyarrow import fs as pa_fs
    except:
        raise BodoError('Reading from s3 requires pyarrow currently.')
    from mpi4py import MPI
    lkkwa__wywam = MPI.COMM_WORLD
    bucket_loc = None
    if parallel and bodo.get_rank() == 0 or not parallel:
        try:
            hvuyk__xwsv, gig__zrtd = pa_fs.S3FileSystem.from_uri(s3_filepath)
            bucket_loc = hvuyk__xwsv.region
        except Exception as omjp__mxtb:
            if os.environ.get('AWS_DEFAULT_REGION', '') == '':
                warnings.warn(BodoWarning(
                    f"""Unable to get S3 Bucket Region.
{omjp__mxtb}.
Value not defined in the AWS_DEFAULT_REGION environment variable either. Region defaults to us-east-1 currently."""
                    ))
            bucket_loc = ''
    if parallel:
        bucket_loc = lkkwa__wywam.bcast(bucket_loc)
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
        lzw__ugxjx = get_s3_bucket_region_njit(path_or_buf, parallel=
            is_parallel)
        nrpdv__euog, ina__nbe = unicode_to_utf8_and_len(D)
        eguw__mdxvj = 0
        if is_parallel:
            eguw__mdxvj = bodo.libs.distributed_api.dist_exscan(ina__nbe,
                np.int32(Reduce_Type.Sum.value))
        _csv_write(unicode_to_utf8(path_or_buf), nrpdv__euog, eguw__mdxvj,
            ina__nbe, is_parallel, unicode_to_utf8(lzw__ugxjx))
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
    upd__equq = get_overload_constant_dict(storage_options)
    jxig__rwhp = 'def impl(storage_options):\n'
    jxig__rwhp += (
        "  with numba.objmode(storage_options_py='storage_options_dict_type'):\n"
        )
    jxig__rwhp += f'    storage_options_py = {str(upd__equq)}\n'
    jxig__rwhp += '  return storage_options_py\n'
    txtd__npow = {}
    exec(jxig__rwhp, globals(), txtd__npow)
    return txtd__npow['impl']
