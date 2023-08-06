import asyncio
import os
import threading
from collections import defaultdict
from concurrent import futures
from urllib.parse import urlparse
import pyarrow.parquet as pq
from bodo.io.fs_io import get_s3_bucket_region_njit


def get_parquet_filesnames_from_deltalake(delta_lake_path):
    try:
        from deltalake import DeltaTable
    except Exception as korf__qetak:
        raise ImportError(
            "Bodo Error: please pip install the 'deltalake' package to read parquet from delta lake"
            )
    ylc__vqd = None
    ykkip__eiaah = delta_lake_path.rstrip('/')
    bvh__vjtw = 'AWS_DEFAULT_REGION' in os.environ
    wfz__rqx = os.environ.get('AWS_DEFAULT_REGION', '')
    jlo__bng = False
    if delta_lake_path.startswith('s3://'):
        hpzx__rpoqh = get_s3_bucket_region_njit(delta_lake_path, parallel=False
            )
        if hpzx__rpoqh != '':
            os.environ['AWS_DEFAULT_REGION'] = hpzx__rpoqh
            jlo__bng = True
    fxwcb__atb = DeltaTable(delta_lake_path)
    ylc__vqd = fxwcb__atb.files()
    ylc__vqd = [(ykkip__eiaah + '/' + ruccq__zylr) for ruccq__zylr in
        sorted(ylc__vqd)]
    if jlo__bng:
        if bvh__vjtw:
            os.environ['AWS_DEFAULT_REGION'] = wfz__rqx
        else:
            del os.environ['AWS_DEFAULT_REGION']
    return ylc__vqd


def _make_manifest(path_or_paths, fs, pathsep='/', metadata_nthreads=1,
    open_file_func=None):
    partitions = None
    lot__nmmfc = None
    qtos__rppy = None
    if isinstance(path_or_paths, list) and len(path_or_paths) == 1:
        path_or_paths = path_or_paths[0]
    if pq._is_path_like(path_or_paths) and fs.isdir(path_or_paths):
        manifest = ParquetManifest(path_or_paths, filesystem=fs,
            open_file_func=open_file_func, pathsep=getattr(fs, 'pathsep',
            '/'), metadata_nthreads=metadata_nthreads)
        lot__nmmfc = manifest.common_metadata_path
        qtos__rppy = manifest.metadata_path
        pieces = manifest.pieces
        partitions = manifest.partitions
    else:
        if not isinstance(path_or_paths, list):
            path_or_paths = [path_or_paths]
        if len(path_or_paths) == 0:
            raise ValueError('Must pass at least one file path')
        pieces = []
        geew__ihru = urlparse(path_or_paths[0]).scheme
        for ykkip__eiaah in path_or_paths:
            if not geew__ihru and not fs.isfile(ykkip__eiaah):
                raise OSError(
                    f'Passed non-file path: {ykkip__eiaah}, but only files or glob strings (no directories) are supported when passing a list'
                    )
            piece = pq.ParquetDatasetPiece._create(ykkip__eiaah,
                open_file_func=open_file_func)
            pieces.append(piece)
    return pieces, partitions, lot__nmmfc, qtos__rppy


pq._make_manifest = _make_manifest


def get_dataset_schema(dataset):
    if dataset.metadata is None and dataset.schema is None:
        if dataset.common_metadata is not None:
            dataset.schema = dataset.common_metadata.schema
        else:
            dataset.schema = dataset.pieces[0].get_metadata().schema
    elif dataset.schema is None:
        dataset.schema = dataset.metadata.schema
    ezcmg__guq = dataset.schema.to_arrow_schema()
    if dataset.partitions is not None:
        for jic__hfkr in dataset.partitions.partition_names:
            if ezcmg__guq.get_field_index(jic__hfkr) != -1:
                tryot__ytv = ezcmg__guq.get_field_index(jic__hfkr)
                ezcmg__guq = ezcmg__guq.remove(tryot__ytv)
    return ezcmg__guq


class VisitLevelThread(threading.Thread):

    def __init__(self, manifest):
        threading.Thread.__init__(self)
        self.manifest = manifest
        self.exc = None

    def run(self):
        try:
            manifest = self.manifest
            manifest.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(manifest.loop)
            manifest.loop.run_until_complete(manifest._visit_level(0,
                manifest.dirpath, []))
        except Exception as korf__qetak:
            self.exc = korf__qetak
        finally:
            if hasattr(manifest, 'loop') and not manifest.loop.is_closed():
                manifest.loop.close()

    def join(self):
        super(VisitLevelThread, self).join()
        if self.exc:
            raise self.exc


class ParquetManifest:

    def __init__(self, dirpath, open_file_func=None, filesystem=None,
        pathsep='/', partition_scheme='hive', metadata_nthreads=1):
        filesystem, dirpath = pq._get_filesystem_and_path(filesystem, dirpath)
        self.filesystem = filesystem
        self.open_file_func = open_file_func
        self.pathsep = pathsep
        self.dirpath = pq._stringify_path(dirpath)
        self.partition_scheme = partition_scheme
        self.partitions = pq.ParquetPartitions()
        self.pieces = []
        self._metadata_nthreads = metadata_nthreads
        self._thread_pool = futures.ThreadPoolExecutor(max_workers=
            metadata_nthreads)
        self.common_metadata_path = None
        self.metadata_path = None
        self.delta_lake_filter = set()
        self.partition_vals = defaultdict(set)
        ttq__bzq = VisitLevelThread(self)
        ttq__bzq.start()
        ttq__bzq.join()
        for rfeeu__fodvc in self.partition_vals.keys():
            self.partition_vals[rfeeu__fodvc] = sorted(self.partition_vals[
                rfeeu__fodvc])
        for aakd__umfa in self.partitions.levels:
            aakd__umfa.keys = sorted(aakd__umfa.keys)
        for ccrou__inlk in self.pieces:
            if ccrou__inlk.partition_keys is not None:
                ccrou__inlk.partition_keys = [(dbsu__dkc, self.
                    partition_vals[dbsu__dkc].index(nyrxv__dko)) for 
                    dbsu__dkc, nyrxv__dko in ccrou__inlk.partition_keys]
        self.pieces.sort(key=lambda piece: piece.path)
        if self.common_metadata_path is None:
            self.common_metadata_path = self.metadata_path
        self._thread_pool.shutdown()

    async def _visit_level(self, xacq__pnoas, base_path, mkfie__xnnak):
        fs = self.filesystem
        zpqj__miqa, ypgkt__evr, rjiv__bohk = await self.loop.run_in_executor(
            self._thread_pool, lambda fs, base_bath: next(fs.walk(base_path
            )), fs, base_path)
        if xacq__pnoas == 0 and '_delta_log' in ypgkt__evr:
            self.delta_lake_filter = set(get_parquet_filesnames_from_deltalake
                (base_path))
        qmrt__jzakl = []
        for ykkip__eiaah in rjiv__bohk:
            if ykkip__eiaah == '':
                continue
            oyo__fodck = self.pathsep.join((base_path, ykkip__eiaah))
            if ykkip__eiaah.endswith('_common_metadata'):
                self.common_metadata_path = oyo__fodck
            elif ykkip__eiaah.endswith('_metadata'):
                self.metadata_path = oyo__fodck
            elif self._should_silently_exclude(ykkip__eiaah):
                continue
            elif self.delta_lake_filter and oyo__fodck not in self.delta_lake_filter:
                continue
            else:
                qmrt__jzakl.append(oyo__fodck)
        qizq__fpgr = [self.pathsep.join((base_path, taioy__shci)) for
            taioy__shci in ypgkt__evr if not pq._is_private_directory(
            taioy__shci)]
        qmrt__jzakl.sort()
        qizq__fpgr.sort()
        if len(qmrt__jzakl) > 0 and len(qizq__fpgr) > 0:
            raise ValueError('Found files in an intermediate directory: {}'
                .format(base_path))
        elif len(qizq__fpgr) > 0:
            await self._visit_directories(xacq__pnoas, qizq__fpgr, mkfie__xnnak
                )
        else:
            self._push_pieces(qmrt__jzakl, mkfie__xnnak)

    async def _visit_directories(self, xacq__pnoas, ypgkt__evr, mkfie__xnnak):
        brzyf__lgqmj = []
        for ykkip__eiaah in ypgkt__evr:
            bsk__zqe, fwsb__brp = pq._path_split(ykkip__eiaah, self.pathsep)
            dbsu__dkc, ofc__qqex = pq._parse_hive_partition(fwsb__brp)
            uhsqm__ygwt = self.partitions.get_index(xacq__pnoas, dbsu__dkc,
                ofc__qqex)
            self.partition_vals[dbsu__dkc].add(ofc__qqex)
            fvaq__tukt = mkfie__xnnak + [(dbsu__dkc, ofc__qqex)]
            brzyf__lgqmj.append(self._visit_level(xacq__pnoas + 1,
                ykkip__eiaah, fvaq__tukt))
        await asyncio.wait(brzyf__lgqmj)


ParquetManifest._should_silently_exclude = (pq.ParquetManifest.
    _should_silently_exclude)
ParquetManifest._parse_partition = pq.ParquetManifest._parse_partition
ParquetManifest._push_pieces = pq.ParquetManifest._push_pieces
pq.ParquetManifest = ParquetManifest


def pieces(self):
    return self._pieces


pq.ParquetDataset.pieces = property(pieces)


def partitions(self):
    return self._partitions


pq.ParquetDataset.partitions = property(partitions)
