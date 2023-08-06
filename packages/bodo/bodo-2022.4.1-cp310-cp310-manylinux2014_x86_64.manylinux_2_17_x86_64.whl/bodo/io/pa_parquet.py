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
    except Exception as wtnzo__swy:
        raise ImportError(
            "Bodo Error: please pip install the 'deltalake' package to read parquet from delta lake"
            )
    ntrwy__turh = None
    cfv__kmzr = delta_lake_path.rstrip('/')
    rbhrf__ktopl = 'AWS_DEFAULT_REGION' in os.environ
    vux__hoksb = os.environ.get('AWS_DEFAULT_REGION', '')
    xqw__kxadw = False
    if delta_lake_path.startswith('s3://'):
        npv__buxwy = get_s3_bucket_region_njit(delta_lake_path, parallel=False)
        if npv__buxwy != '':
            os.environ['AWS_DEFAULT_REGION'] = npv__buxwy
            xqw__kxadw = True
    pxx__yxztu = DeltaTable(delta_lake_path)
    ntrwy__turh = pxx__yxztu.files()
    ntrwy__turh = [(cfv__kmzr + '/' + ihnru__khwpu) for ihnru__khwpu in
        sorted(ntrwy__turh)]
    if xqw__kxadw:
        if rbhrf__ktopl:
            os.environ['AWS_DEFAULT_REGION'] = vux__hoksb
        else:
            del os.environ['AWS_DEFAULT_REGION']
    return ntrwy__turh


def _make_manifest(path_or_paths, fs, pathsep='/', metadata_nthreads=1,
    open_file_func=None):
    partitions = None
    cry__tsx = None
    uxn__fie = None
    if isinstance(path_or_paths, list) and len(path_or_paths) == 1:
        path_or_paths = path_or_paths[0]
    if pq._is_path_like(path_or_paths) and fs.isdir(path_or_paths):
        manifest = ParquetManifest(path_or_paths, filesystem=fs,
            open_file_func=open_file_func, pathsep=getattr(fs, 'pathsep',
            '/'), metadata_nthreads=metadata_nthreads)
        cry__tsx = manifest.common_metadata_path
        uxn__fie = manifest.metadata_path
        pieces = manifest.pieces
        partitions = manifest.partitions
    else:
        if not isinstance(path_or_paths, list):
            path_or_paths = [path_or_paths]
        if len(path_or_paths) == 0:
            raise ValueError('Must pass at least one file path')
        pieces = []
        qejc__bxt = urlparse(path_or_paths[0]).scheme
        for cfv__kmzr in path_or_paths:
            if not qejc__bxt and not fs.isfile(cfv__kmzr):
                raise OSError(
                    f'Passed non-file path: {cfv__kmzr}, but only files or glob strings (no directories) are supported when passing a list'
                    )
            piece = pq.ParquetDatasetPiece._create(cfv__kmzr,
                open_file_func=open_file_func)
            pieces.append(piece)
    return pieces, partitions, cry__tsx, uxn__fie


pq._make_manifest = _make_manifest


def get_dataset_schema(dataset):
    if dataset.metadata is None and dataset.schema is None:
        if dataset.common_metadata is not None:
            dataset.schema = dataset.common_metadata.schema
        else:
            dataset.schema = dataset.pieces[0].get_metadata().schema
    elif dataset.schema is None:
        dataset.schema = dataset.metadata.schema
    wpjxc__nah = dataset.schema.to_arrow_schema()
    if dataset.partitions is not None:
        for glq__ngr in dataset.partitions.partition_names:
            if wpjxc__nah.get_field_index(glq__ngr) != -1:
                jliy__hbc = wpjxc__nah.get_field_index(glq__ngr)
                wpjxc__nah = wpjxc__nah.remove(jliy__hbc)
    return wpjxc__nah


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
        except Exception as wtnzo__swy:
            self.exc = wtnzo__swy
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
        uulq__aft = VisitLevelThread(self)
        uulq__aft.start()
        uulq__aft.join()
        for mrurm__vsb in self.partition_vals.keys():
            self.partition_vals[mrurm__vsb] = sorted(self.partition_vals[
                mrurm__vsb])
        for pkhao__qptp in self.partitions.levels:
            pkhao__qptp.keys = sorted(pkhao__qptp.keys)
        for ilh__eirw in self.pieces:
            if ilh__eirw.partition_keys is not None:
                ilh__eirw.partition_keys = [(kroat__dffdp, self.
                    partition_vals[kroat__dffdp].index(hqwv__acn)) for 
                    kroat__dffdp, hqwv__acn in ilh__eirw.partition_keys]
        self.pieces.sort(key=lambda piece: piece.path)
        if self.common_metadata_path is None:
            self.common_metadata_path = self.metadata_path
        self._thread_pool.shutdown()

    async def _visit_level(self, qxh__acvjq, base_path, bwi__pbb):
        fs = self.filesystem
        qvdy__zqkwq, bxi__vtqw, cquph__tye = await self.loop.run_in_executor(
            self._thread_pool, lambda fs, base_bath: next(fs.walk(base_path
            )), fs, base_path)
        if qxh__acvjq == 0 and '_delta_log' in bxi__vtqw:
            self.delta_lake_filter = set(get_parquet_filesnames_from_deltalake
                (base_path))
        frin__opm = []
        for cfv__kmzr in cquph__tye:
            if cfv__kmzr == '':
                continue
            bxr__uutyl = self.pathsep.join((base_path, cfv__kmzr))
            if cfv__kmzr.endswith('_common_metadata'):
                self.common_metadata_path = bxr__uutyl
            elif cfv__kmzr.endswith('_metadata'):
                self.metadata_path = bxr__uutyl
            elif self._should_silently_exclude(cfv__kmzr):
                continue
            elif self.delta_lake_filter and bxr__uutyl not in self.delta_lake_filter:
                continue
            else:
                frin__opm.append(bxr__uutyl)
        cogs__vrkk = [self.pathsep.join((base_path, wdjel__iai)) for
            wdjel__iai in bxi__vtqw if not pq._is_private_directory(wdjel__iai)
            ]
        frin__opm.sort()
        cogs__vrkk.sort()
        if len(frin__opm) > 0 and len(cogs__vrkk) > 0:
            raise ValueError('Found files in an intermediate directory: {}'
                .format(base_path))
        elif len(cogs__vrkk) > 0:
            await self._visit_directories(qxh__acvjq, cogs__vrkk, bwi__pbb)
        else:
            self._push_pieces(frin__opm, bwi__pbb)

    async def _visit_directories(self, qxh__acvjq, bxi__vtqw, bwi__pbb):
        bale__wavf = []
        for cfv__kmzr in bxi__vtqw:
            qum__yxdxd, labgl__jyn = pq._path_split(cfv__kmzr, self.pathsep)
            kroat__dffdp, wrqak__irs = pq._parse_hive_partition(labgl__jyn)
            jzvx__hsba = self.partitions.get_index(qxh__acvjq, kroat__dffdp,
                wrqak__irs)
            self.partition_vals[kroat__dffdp].add(wrqak__irs)
            exflk__rfm = bwi__pbb + [(kroat__dffdp, wrqak__irs)]
            bale__wavf.append(self._visit_level(qxh__acvjq + 1, cfv__kmzr,
                exflk__rfm))
        await asyncio.wait(bale__wavf)


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
